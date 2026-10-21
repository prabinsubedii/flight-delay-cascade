"""Create a lightly cleaned January 2025 BTS flight file for analysis.

Keeps all source rows and records missing values as they are. This is a
preparation step, not a model-ready feature table.
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "data"
    / "raw"
    / "On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2025_1"
    / "On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)_2025_1.csv"
)
OUTPUT = ROOT / "data" / "processed" / "january_2025_clean.csv"

COLUMNS = [
    "FlightDate",
    "Reporting_Airline",
    "Flight_Number_Reporting_Airline",
    "Tail_Number",
    "Origin",
    "Dest",
    "CRSDepTime",
    "CRSArrTime",
    "CRSElapsedTime",
    "Distance",
    "DepTime",
    "ArrTime",
    "DepDelay",
    "ArrDelay",
    "Cancelled",
    "Diverted",
]


def clean_code(values: pd.Series) -> pd.Series:
    """Trim whitespace, uppercase codes, and treat blank strings as missing."""
    cleaned = values.astype("string").str.strip().str.upper()
    return cleaned.mask(cleaned.eq(""))


def main() -> None:
    flights = pd.read_csv(
        SOURCE,
        usecols=COLUMNS,
        dtype={"Flight_Number_Reporting_Airline": "string"},
        low_memory=False,
    )
    source_rows = len(flights)

    flights["FlightDate"] = pd.to_datetime(flights["FlightDate"], errors="coerce")
    for column in ["Reporting_Airline", "Tail_Number", "Origin", "Dest"]:
        flights[column] = clean_code(flights[column])

    for column in [
        "CRSDepTime", "CRSArrTime", "CRSElapsedTime", "Distance",
        "DepTime", "ArrTime", "DepDelay", "ArrDelay",
    ]:
        flights[column] = pd.to_numeric(flights[column], errors="coerce")

    flights["Cancelled"] = pd.to_numeric(flights["Cancelled"], errors="coerce")
    flights["Diverted"] = pd.to_numeric(flights["Diverted"], errors="coerce")
    flights["is_cancelled"] = flights["Cancelled"].eq(1)
    flights["is_diverted"] = flights["Diverted"].eq(1)
    flights["operated"] = ~flights["is_cancelled"] & ~flights["is_diverted"]
    flights["arrival_delay_observed"] = flights["ArrDelay"].notna()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    flights.to_csv(OUTPUT, index=False)

    print(f"Source rows retained: {source_rows:,}")
    print(f"Output rows: {len(flights):,}")
    print(f"Dates: {flights['FlightDate'].min():%Y-%m-%d} to {flights['FlightDate'].max():%Y-%m-%d}")
    print(f"Cancelled: {flights['is_cancelled'].sum():,}")
    print(f"Diverted: {flights['is_diverted'].sum():,}")
    print(f"Missing arrival delay: {flights['ArrDelay'].isna().sum():,}")
    print(f"Missing tail number: {flights['Tail_Number'].isna().sum():,}")
    print(f"Saved local working file: {OUTPUT.relative_to(ROOT)}")
    print("No rows were dropped, values imputed, or delay labels created.")


if __name__ == "__main__":
    main()
