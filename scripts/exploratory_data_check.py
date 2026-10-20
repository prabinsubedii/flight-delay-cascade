"""Explore January 2025 BTS flights and screen possible aircraft connections.

This script reports descriptive statistics and possible same-aircraft links.
Those links are not verified aircraft rotations. The script does not train a model.
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = (
    ROOT
    / "data"
    / "raw"
    / "On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2025_1"
    / "On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)_2025_1.csv"
)


def clock_minutes(values: pd.Series) -> pd.Series:
    """Convert BTS HHMM clock values to minutes after midnight."""
    numeric = pd.to_numeric(values, errors="coerce")
    hour = (numeric // 100).astype("Int64")
    minute = (numeric % 100).astype("Int64")
    valid = (hour.between(0, 23) & minute.between(0, 59)) | (hour.eq(24) & minute.eq(0))
    result = hour * 60 + minute
    return result.where(valid).astype("Float64")


def main() -> None:
    columns = [
        "FlightDate",
        "Reporting_Airline",
        "Tail_Number",
        "Origin",
        "Dest",
        "ArrDelay",
        "DepDelay",
        "CRSDepTime",
        "CRSArrTime",
        "Cancelled",
        "Diverted",
    ]
    df = pd.read_csv(DATA_FILE, usecols=columns, low_memory=False)
    df["FlightDate"] = pd.to_datetime(df["FlightDate"], errors="coerce")
    df["Tail_Number"] = df["Tail_Number"].astype("string").str.strip().str.upper()
    df["Tail_Number"] = df["Tail_Number"].mask(df["Tail_Number"].eq(""))
    df["_scheduled_departure_minutes"] = clock_minutes(df["CRSDepTime"])
    df["_scheduled_arrival_minutes"] = clock_minutes(df["CRSArrTime"])

    cancelled = df["Cancelled"].eq(1)
    diverted = df["Diverted"].eq(1)
    missing_arrival = df["ArrDelay"].isna()
    missing_tail = df["Tail_Number"].isna()
    operated_with_tail = df.loc[~cancelled & ~diverted & ~missing_tail]
    tail_date_counts = operated_with_tail.groupby(
        ["Tail_Number", "FlightDate"], dropna=True
    ).size()
    repeated_tail_dates = tail_date_counts[tail_date_counts >= 2]
    repeated_tail_date_records = int(repeated_tail_dates.sum())

    eligible = df.loc[
        ~cancelled
        & ~diverted
        & ~missing_tail
        & df["_scheduled_departure_minutes"].notna()
        & df["_scheduled_arrival_minutes"].notna()
        & df["Origin"].notna()
        & df["Dest"].notna()
        & df["FlightDate"].notna(),
        ["Tail_Number", "FlightDate", "Origin", "Dest", "_scheduled_departure_minutes", "_scheduled_arrival_minutes"],
    ].copy()
    eligible["_flight_id"] = eligible.index
    previous = eligible.rename(
        columns={
            "Dest": "_connection_airport",
            "_scheduled_arrival_minutes": "_arrival_at_connection",
            "_flight_id": "_previous_flight_id",
        }
    )[["Tail_Number", "FlightDate", "_connection_airport", "_arrival_at_connection", "_previous_flight_id"]]
    following = eligible.rename(
        columns={
            "Origin": "_connection_airport",
            "_scheduled_departure_minutes": "_departure_from_connection",
            "_flight_id": "_following_flight_id",
        }
    )[["Tail_Number", "FlightDate", "_connection_airport", "_departure_from_connection", "_following_flight_id"]]
    possible = previous.merge(following, on=["Tail_Number", "FlightDate", "_connection_airport"])
    possible = possible.loc[possible["_previous_flight_id"] != possible["_following_flight_id"]].copy()
    possible["_scheduled_ground_minutes"] = (
        possible["_departure_from_connection"] - possible["_arrival_at_connection"]
    )
    possible = possible.loc[possible["_scheduled_ground_minutes"].between(0, 720)]
    nearest = possible.sort_values("_scheduled_ground_minutes").drop_duplicates(
        "_previous_flight_id", keep="first"
    )

    print(f"CSV: {DATA_FILE.relative_to(ROOT)}")
    print(f"Flight records: {len(df):,}")
    print(f"Dates: {df['FlightDate'].min():%Y-%m-%d} through {df['FlightDate'].max():%Y-%m-%d}")
    print(f"Reporting airlines: {df['Reporting_Airline'].nunique(dropna=True):,}")
    airports = pd.unique(pd.concat([df["Origin"], df["Dest"]], ignore_index=True).dropna())
    print(f"Unique origin/destination airports: {len(airports):,}")

    known_arrivals = df["ArrDelay"].dropna()
    print(f"Records with arrival delay available: {len(known_arrivals):,}")
    print(f"Arrival delay median (minutes): {known_arrivals.median():.1f}")
    print(f"Arrival delay 90th percentile (minutes): {known_arrivals.quantile(0.90):.1f}")
    print(f"Records with arrival delay >= 15 minutes: {(known_arrivals >= 15).sum():,} ({(known_arrivals >= 15).mean():.1%} of records with a value)")
    print(f"Records with departure delay available: {df['DepDelay'].notna().sum():,}")

    print(f"Missing/blank tail numbers: {missing_tail.sum():,} ({missing_tail.mean():.2%})")
    print(f"Unique reported tail numbers: {df['Tail_Number'].nunique(dropna=True):,}")
    print(f"Cancelled: {cancelled.sum():,}")
    print(f"Diverted: {diverted.sum():,}")
    print(f"Missing arrival delay: {missing_arrival.sum():,}")
    print(f"Missing arrival delay and cancelled: {(missing_arrival & cancelled).sum():,}")
    print(f"Missing arrival delay and diverted: {(missing_arrival & diverted).sum():,}")
    print(f"Missing arrival delay, both statuses: {(missing_arrival & cancelled & diverted).sum():,}")
    print(f"Missing arrival delay, neither status: {(missing_arrival & ~cancelled & ~diverted).sum():,}")

    print(f"Operated records with a tail number: {len(operated_with_tail):,}")
    print(f"Unique tail/date groups among operated records with a tail: {len(tail_date_counts):,}")
    print(f"Tail/date groups with 2+ operated records: {len(repeated_tail_dates):,}")
    print(f"Records in those repeated tail/date groups: {repeated_tail_date_records:,}")
    print(f"Maximum operated records for one tail/date: {int(tail_date_counts.max()):,}")
    print("Repeated tail/date groups are a screening signal only, not verified consecutive aircraft rotations.")

    print("Same-aircraft connection screen (candidate links only):")
    print(f"  Same tail, same FlightDate, and previous destination = next origin, with 0-720 scheduled minutes at that airport: {len(possible):,} candidate pairs")
    print(f"  Previous-flight records with at least one candidate: {nearest['_previous_flight_id'].nunique():,}")
    print(f"  Candidate predecessor records with multiple possible successors in this window: {(possible.groupby('_previous_flight_id').size() > 1).sum():,}")
    print(f"  Nearest-candidate ground time median (minutes): {nearest['_scheduled_ground_minutes'].median():.1f}")
    print(f"  Nearest-candidate ground time 90th percentile (minutes): {nearest['_scheduled_ground_minutes'].quantile(0.90):.1f}")
    print(f"  Nearest candidates with at least 30 scheduled ground minutes: {(nearest['_scheduled_ground_minutes'] >= 30).sum():,}")
    print(f"  Nearest candidates with at least 60 scheduled ground minutes: {(nearest['_scheduled_ground_minutes'] >= 60).sum():,}")
    print("  The screen assumes the two records' FlightDate is the same connection date; local-date changes and overnight legs can invalidate or hide pairs.")

    print("Top 10 origin airports by record count:")
    for airport, count in df["Origin"].value_counts().head(10).items():
        print(f"  {airport}: {count:,}")
    print("Top reporting airlines by record count:")
    for airline, count in df["Reporting_Airline"].value_counts().head(10).items():
        print(f"  {airline}: {count:,}")
    print("Arrival-delay summaries exclude records where ArrDelay is missing.")
    print("This one-month check does not establish prediction-time availability or causal delay propagation.")


if __name__ == "__main__":
    main()
