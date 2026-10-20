# January sample preparation

I made a local working copy of the January 2025 BTS file for analysis. The script trims and uppercases airline, airport, and tail-number codes, parses date and numeric fields, and adds clear cancelled, diverted, operated, and arrival-delay-observed flags.

All 539,747 source rows are kept. I did not fill missing values, remove unusual delays, or create a prediction label. The output is saved under `data/processed/`, which is ignored by Git.

Run from the repository root:

```powershell
.\.venv\Scripts\python.exe scripts/prepare_january_sample.py
```

Then open [the first-look notebook](../notebooks/january_2025_first_look.ipynb). The cleaned file was also used in the [first baseline experiment](january_baseline.md), with scheduled fields kept separate from observed outcomes.
