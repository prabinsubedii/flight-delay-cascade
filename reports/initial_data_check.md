# Initial data check

## Source and local file

The sample is the Bureau of Transportation Statistics (BTS) Reporting Carrier On-Time Performance file for January 2025. The original archive is available at [BTS PREZIP](https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2025_1.zip). The archive and extracted CSV are stored locally under `data/raw/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2025_1/`. Raw data is excluded from Git.

CSV: `data/raw/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2025_1/On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)_2025_1.csv`

## Reproduce

From the repository root, with the project environment available, run:

```powershell
.\.venv\Scripts\python.exe scripts/initial_data_check.py
```

The script reads only the eight needed columns and does not modify the source data.

## Verified findings

| Check | Result |
|---|---:|
| Flight records | 539,747 |
| Date range | 2025-01-01 through 2025-01-31 |
| Reporting airlines | 14 |
| Unique origin/destination airports | 329 |
| Missing or blank tail numbers | 2,530 (0.47%) |
| Cancelled records (`Cancelled = 1`) | 16,312 |
| Diverted records (`Diverted = 1`) | 1,166 |
| Missing `ArrDelay` | 17,478 |

All records with missing `ArrDelay` are in the union of cancelled and diverted records: 16,312 are cancelled, 1,166 are diverted, none are both, and none are in neither category. These are status counts, not an analysis of which flights should be included in a future modeling target.

## Interpretation and limits

Most records have a reported tail number, which makes aircraft-based linking worth investigating. A tail number on a completed historical record does not show that the assignment was available at an earlier prediction time. This check does not establish that consecutive aircraft rotations can be reconstructed reliably, and the single month is not enough to support seasonal or cross-period claims. No model training or full exploratory analysis has been done.
