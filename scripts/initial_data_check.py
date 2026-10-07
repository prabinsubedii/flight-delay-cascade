"""Summarize the January 2025 BTS on-time performance sample."""

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


def main() -> None:
    columns = [
        "FlightDate", "Reporting_Airline", "Origin", "Dest", "Tail_Number",
        "Cancelled", "Diverted", "ArrDelay",
    ]
    df = pd.read_csv(DATA_FILE, usecols=columns, low_memory=False)
    missing_arrival = df["ArrDelay"].isna()
    cancelled = df["Cancelled"].eq(1)
    diverted = df["Diverted"].eq(1)
    missing_tail = df["Tail_Number"].isna() | df["Tail_Number"].astype("string").str.strip().eq("")

    print(f"CSV: {DATA_FILE.relative_to(ROOT)}")
    print(f"Rows: {len(df):,}")
    print(f"Dates: {df['FlightDate'].min()} through {df['FlightDate'].max()}")
    print(f"Reporting airlines: {df['Reporting_Airline'].nunique(dropna=True):,}")
    print(f"Unique origin/destination airports: {pd.unique(pd.concat([df['Origin'], df['Dest']])).size:,}")
    print(f"Missing/blank tail numbers: {missing_tail.sum():,} ({missing_tail.mean():.2%})")
    print(f"Cancelled: {cancelled.sum():,}")
    print(f"Diverted: {diverted.sum():,}")
    print(f"Missing arrival delay: {missing_arrival.sum():,}")
    print("Missing arrival-delay overlap:")
    print(f"  also cancelled: {(missing_arrival & cancelled).sum():,}")
    print(f"  also diverted: {(missing_arrival & diverted).sum():,}")
    print(f"  both cancelled and diverted: {(missing_arrival & cancelled & diverted).sum():,}")
    print(f"  neither cancelled nor diverted: {(missing_arrival & ~cancelled & ~diverted).sum():,}")
    print("All category counts below are record counts; cancellations and diversions may overlap.")


if __name__ == "__main__":
    main()
