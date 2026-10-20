# Exploratory check of the January 2025 BTS sample

## What I tried

I started by asking a few basic questions about the January file: where are values missing, how are arrival delays distributed, do delays look different by day, airline, or airport, and do repeated tail numbers look promising for checking aircraft links? The notebook records those checks and leaves the outputs visible for discussion: [January 2025 first look](../notebooks/january_2025_first_look.ipynb).

I also kept a small script for rerunning the summary numbers and candidate-link screen. It does not change the raw file, confirm a final flight network, or train a model.

Run it from the repository root with:

```powershell
.\.venv\Scripts\python.exe scripts/exploratory_data_check.py
```

## Findings so far

- The sample has 539,747 records from January 1 through January 31, 2025. It covers 14 reporting airlines and 329 origin and destination airports.
- Arrival delay is available for 522,269 records. Among those records, the median arrival delay is -8 minutes, the 90th percentile is 37 minutes, and 18.8% have an arrival delay of at least 15 minutes. Cancelled and diverted records are not included in these delay summaries because their arrival delays are missing.
- There are 5,612 distinct reported tail numbers. After excluding cancelled and diverted records and records without a tail number, 522,269 records remain.
- Grouping those records by tail number and `FlightDate` gives 142,174 tail/date groups. Of these, 127,981 have at least two records. Those repeated groups contain 508,076 records. The largest group has 13 records.
- A first connection screen found 449,447 possible record pairs with the same tail number and `FlightDate`, a matching destination and next origin, and a scheduled local-clock gap from 0 to 720 minutes at that shared airport. There were 377,790 previous-flight records with at least one such candidate. For 62,285 previous-flight records, more than one possible successor passed the screen. Selecting only the nearest candidate gives a median scheduled gap of 57 minutes; 373,747 candidates have at least 30 minutes and 181,870 have at least 60 minutes.
- The busiest origins by record count are DFW, DEN, ATL, ORD, and CLT. The largest reporting carriers in this sample are WN, DL, AA, OO, and UA.

## What this says about aircraft rotations

The dataset has useful ingredients for an aircraft-link feasibility study: tail numbers, dates, origin and destination airports, and scheduled and actual clock times. Tail numbers repeat often enough to make a closer screen worthwhile.

The connection screen is only a candidate-generation step. It does not identify verified consecutive flights or confirm that those flights used the same aircraft in operational sequence. BTS reports schedule times as local clock times, and its reporting guidance says time-zone differences must be handled when calculating elapsed time ([BTS Technical Directive 39](https://www.bts.gov/explore-topics-and-geography/modes/aviation/number-39-technical-directive-reporting-time)). The screen compares arrival and departure clocks at the shared airport, but assumes the two records' `FlightDate` is also the same local connection date. Overnight arrivals can break that assumption, and same-day pairs may still have another leg between them. The 62,285 records with multiple possible successors also need resolution. A follow-up should account for local arrival dates, test against actual timings, and inspect ambiguous or missing assignments. Historical tail numbers also do not prove the assignment was available at a prediction time.

The result is a partial feasibility finding, not a validated rotation network. January is one month and cannot support seasonal generalization. A separate first single-flight baseline has since been trained; it does not use these candidate links.
