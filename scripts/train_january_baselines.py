"""Train January 2025 flight-only and flight-plus-weather XGBoost prototypes.

The chronological holdout is January 25-31. Weather uses the latest origin
airport observation at least 30 minutes before scheduled departure. This is an
initial one-month comparison, not the project's final validated model.
"""

from pathlib import Path
import json
import os
from zoneinfo import ZoneInfo

import airportsdata
import numpy as np
import pandas as pd
import xgboost as xgb


ROOT = Path(__file__).resolve().parents[1]
FLIGHTS_FILE = ROOT / "data" / "processed" / "january_2025_clean.csv"
WEATHER_FILE = ROOT / "data" / "raw" / "weather" / "iem_asos_january_2025.csv"
OUTPUT_DIR = ROOT / "data" / "processed" / "january_baseline"
TRAIN_END = pd.Timestamp("2025-01-18 23:59:59")
EARLY_STOP_END = pd.Timestamp("2025-01-24 23:59:59")
WEATHER_LAG = pd.Timedelta(minutes=30)
WEATHER_MAX_AGE = pd.Timedelta(hours=3)

FLIGHT_FEATURES = [
    "Reporting_Airline",
    "Origin",
    "Dest",
    "DepartureHour",
    "DepartureDayOfWeek",
    "Distance",
    "CRSElapsedTime",
]
WEATHER_FEATURES = [
    "tmpf",
    "dwpf",
    "relh",
    "drct",
    "sknt",
    "gust",
    "vsby",
    "mslp",
    "skyl1",
    "skyc1",
    "WeatherAgeMinutes",
    "WeatherMissing",
]
CATEGORICAL_FEATURES = ["Reporting_Airline", "Origin", "Dest", "skyc1"]
WEATHER_NUMERIC = [
    "tmpf", "dwpf", "relh", "drct", "sknt", "gust", "vsby", "mslp", "skyl1"
]


def scheduled_departure_local(row: pd.Series) -> pd.Timestamp:
    """Turn a valid BTS HHMM schedule into a naive local timestamp."""
    value = row["CRSDepTime"]
    if pd.isna(value):
        return pd.NaT
    hhmm = int(value)
    hour, minute = divmod(hhmm, 100)
    if (hour == 24 and minute == 0):
        hour, minute = 0, 0
    elif not (0 <= hour <= 23 and 0 <= minute <= 59):
        return pd.NaT
    return pd.Timestamp(row["FlightDate"]).normalize() + pd.Timedelta(hours=hour, minutes=minute) + (
        pd.Timedelta(days=1) if hhmm == 2400 else pd.Timedelta(0)
    )


def add_departure_utc(flights: pd.DataFrame) -> pd.DataFrame:
    airports = airportsdata.load("IATA")
    timezone_by_iata = {code: item["tz"] for code, item in airports.items() if item.get("tz")}
    flights["OriginTimezone"] = flights["Origin"].map(timezone_by_iata)
    flights["ScheduledDepartureLocal"] = flights.apply(scheduled_departure_local, axis=1)
    flights["ScheduledDepartureUTC"] = pd.Series(
        pd.NaT, index=flights.index, dtype="datetime64[ns, UTC]"
    )

    for timezone, indexes in flights.groupby("OriginTimezone", dropna=True).groups.items():
        local = flights.loc[indexes, "ScheduledDepartureLocal"]
        utc = local.dt.tz_localize(timezone, ambiguous="NaT", nonexistent="NaT").dt.tz_convert("UTC")
        flights.loc[indexes, "ScheduledDepartureUTC"] = utc

    flights["ScheduledDepartureUTC"] = pd.to_datetime(flights["ScheduledDepartureUTC"], utc=True)
    flights["WeatherCutoffUTC"] = flights["ScheduledDepartureUTC"] - WEATHER_LAG
    flights["DepartureHour"] = flights["ScheduledDepartureLocal"].dt.hour
    flights["DepartureDayOfWeek"] = flights["ScheduledDepartureLocal"].dt.dayofweek
    return flights


def attach_origin_weather(flights: pd.DataFrame) -> pd.DataFrame:
    weather = pd.read_csv(WEATHER_FILE, low_memory=False)
    weather["station"] = weather["station"].astype("string").str.strip().str.upper()
    weather["valid"] = pd.to_datetime(weather["valid"], utc=True, errors="coerce").astype(
        "datetime64[ns, UTC]"
    )
    for column in WEATHER_NUMERIC:
        weather[column] = pd.to_numeric(weather[column], errors="coerce")
    weather["skyc1"] = weather["skyc1"].astype("string").str.strip().replace("", pd.NA)
    weather = weather.dropna(subset=["station", "valid"])
    weather = weather.sort_values("valid").drop_duplicates(["station", "valid"], keep="last")
    weather = weather.rename(columns={"station": "Origin", "valid": "WeatherObservedUTC"})
    weather_columns = ["Origin", "WeatherObservedUTC", *WEATHER_NUMERIC, "skyc1"]

    flights["Origin"] = flights["Origin"].astype("string").str.strip().str.upper()
    flights = flights.sort_values("WeatherCutoffUTC")
    merged = pd.merge_asof(
        flights,
        weather[weather_columns].sort_values("WeatherObservedUTC"),
        left_on="WeatherCutoffUTC",
        right_on="WeatherObservedUTC",
        by="Origin",
        direction="backward",
        tolerance=WEATHER_MAX_AGE,
    )
    merged["WeatherAgeMinutes"] = (
        (merged["WeatherCutoffUTC"] - merged["WeatherObservedUTC"]).dt.total_seconds() / 60
    )
    merged["WeatherMissing"] = merged["WeatherObservedUTC"].isna().astype("int8")
    return merged


def metric_row(name: str, actual: np.ndarray, predicted: np.ndarray) -> dict[str, float | int | str]:
    error = predicted - actual
    denominator = float(((actual - actual.mean()) ** 2).sum())
    r2 = 1.0 - float((error**2).sum()) / denominator if denominator else float("nan")
    return {
        "model": name,
        "test_rows": int(len(actual)),
        "mae_minutes": float(np.abs(error).mean()),
        "rmse_minutes": float(np.sqrt(np.mean(error**2))),
        "r2": r2,
    }


def train_model(
    name: str,
    train_x: pd.DataFrame,
    train_y: pd.Series,
    early_stop_x: pd.DataFrame,
    early_stop_y: pd.Series,
    test_x: pd.DataFrame,
) -> tuple[xgb.Booster, np.ndarray]:
    train_x = train_x.copy()
    early_stop_x = early_stop_x.copy()
    test_x = test_x.copy()
    for column in CATEGORICAL_FEATURES:
        if column not in train_x:
            continue
        values = sorted(train_x[column].dropna().astype(str).unique())
        dtype = pd.CategoricalDtype(categories=values)
        train_x[column] = train_x[column].astype("string").astype(dtype)
        early_stop_x[column] = early_stop_x[column].astype("string").astype(dtype)
        test_x[column] = test_x[column].astype("string").astype(dtype)

    training_matrix = xgb.DMatrix(train_x, label=train_y, enable_categorical=True)
    early_stop_matrix = xgb.DMatrix(early_stop_x, label=early_stop_y, enable_categorical=True)
    test_matrix = xgb.DMatrix(test_x, enable_categorical=True)
    model = xgb.train(
        {
            "objective": "reg:squarederror",
            "eval_metric": "mae",
            "tree_method": "hist",
            "eta": 0.05,
            "max_depth": 6,
            "min_child_weight": 20,
            "subsample": 0.8,
            "colsample_bytree": 0.85,
            "lambda": 8.0,
            "nthread": min(8, os.cpu_count() or 2),
            "seed": 42,
        },
        training_matrix,
        num_boost_round=500,
        evals=[(early_stop_matrix, "early_stop")],
        early_stopping_rounds=30,
        verbose_eval=False,
    )
    predictions = model.predict(test_matrix, iteration_range=(0, model.best_iteration + 1))
    model.save_model(OUTPUT_DIR / f"{name}.json")
    scores = model.get_score(importance_type="gain")
    importance = pd.DataFrame(
        {"feature": train_x.columns, "gain": [scores.get(column, 0.0) for column in train_x.columns]}
    ).sort_values("gain", ascending=False)
    importance.to_csv(OUTPUT_DIR / f"{name}_feature_importance.csv", index=False)
    return model, predictions


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    flights = pd.read_csv(FLIGHTS_FILE, low_memory=False)
    flights["FlightDate"] = pd.to_datetime(flights["FlightDate"], errors="coerce")
    flights = add_departure_utc(flights)
    flights = attach_origin_weather(flights)

    target_eligible = flights["operated"] & flights["ArrDelay"].notna()
    missing_model_time = target_eligible & (
        flights["ScheduledDepartureUTC"].isna()
        | flights["ScheduledDepartureLocal"].isna()
    )
    eligible = flights.loc[target_eligible & ~missing_model_time].copy()
    train = eligible.loc[eligible["FlightDate"] <= TRAIN_END].copy()
    early_stop = eligible.loc[
        (eligible["FlightDate"] > TRAIN_END)
        & (eligible["FlightDate"] <= EARLY_STOP_END)
    ].copy()
    test = eligible.loc[eligible["FlightDate"] > EARLY_STOP_END].copy()
    target_train = train["ArrDelay"].astype(float)
    target_early_stop = early_stop["ArrDelay"].astype(float)
    target_test = test["ArrDelay"].astype(float).to_numpy()

    flight_only_features = FLIGHT_FEATURES
    weather_features = FLIGHT_FEATURES + WEATHER_FEATURES
    results = [
        metric_row(
            "training-set median",
            target_test,
            np.full(len(test), target_train.median()),
        )
    ]
    predictions = test[["FlightDate", "Reporting_Airline", "Origin", "Dest", "ArrDelay"]].copy()
    predictions = predictions.rename(columns={"ArrDelay": "actual_arrival_delay_minutes"})

    best_iterations = {}
    for name, features in [
        ("xgb_flight_only", flight_only_features),
        ("xgb_flight_plus_origin_weather", weather_features),
    ]:
        model, prediction = train_model(
            name,
            train[features],
            target_train,
            early_stop[features],
            target_early_stop,
            test[features],
        )
        best_iterations[name] = int(model.best_iteration)
        results.append(metric_row(name, target_test, prediction))
        predictions[f"{name}_prediction_minutes"] = prediction

    metrics = pd.DataFrame(results)
    metrics.to_csv(OUTPUT_DIR / "metrics.csv", index=False)
    predictions.to_csv(OUTPUT_DIR / "test_predictions.csv", index=False)
    summary = {
        "target": "ArrDelay in minutes for operated flights",
        "prediction_cutoff": "30 minutes before scheduled departure",
        "training_period": "2025-01-01 through 2025-01-18",
        "early_stopping_period": "2025-01-19 through 2025-01-24",
        "final_test_period": "2025-01-25 through 2025-01-31",
        "training_rows": int(len(train)),
        "early_stopping_rows": int(len(early_stop)),
        "final_test_rows": int(len(test)),
        "weather_source": "Iowa Environmental Mesonet archived airport observations",
        "test_rows_with_weather": int(test["WeatherObservedUTC"].notna().sum()),
        "test_weather_match_rate": float(test["WeatherObservedUTC"].notna().mean()),
        "weather_max_age_minutes": int(WEATHER_MAX_AGE.total_seconds() / 60),
        "weather_lag_minutes": int(WEATHER_LAG.total_seconds() / 60),
        "excluded_cancelled_diverted_or_missing_target": int((~target_eligible).sum()),
        "excluded_for_missing_timezone_or_schedule": int(missing_model_time.sum()),
        "caution": "One month is an exploratory development sample, not evidence of seasonal generalization.",
    }
    (OUTPUT_DIR / "run_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print(f"Training rows (Jan 1-18): {len(train):,}")
    print(f"Early-stopping rows (Jan 19-24): {len(early_stop):,}")
    print(f"Final test rows (Jan 25-31): {len(test):,}")
    print(f"Test weather available within 3 hours of cutoff: {summary['test_weather_match_rate']:.1%}")
    print(metrics.to_string(index=False, float_format=lambda value: f"{value:.3f}"))
    print(f"Best iterations: {best_iterations}")
    print(f"Saved metrics and models under {OUTPUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
