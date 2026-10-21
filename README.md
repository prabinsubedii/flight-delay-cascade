# Flight Delay Cascade

I started with January 2025 U.S. flight records and airport weather. I cleaned the data, looked for basic patterns, and trained two first-pass models to estimate arrival delay.

## First result

I trained on January 1–18, used January 19–24 to set the model, and checked it on January 25–31. The prediction is made 30 minutes before scheduled departure.

| Model | Average error |
| --- | ---: |
| Predict the training median | 18.00 minutes |
| XGBoost with flight details | 24.46 minutes |
| XGBoost with flight details and origin weather | 24.25 minutes |

The simple median was better. Adding weather barely changed the model result, so there is more work to do.

## A few flights from the test week

These flights were in the final test week. Flight numbers identify the records; the model did not use them as inputs. Predictions are in minutes of arrival delay.

| Date, flight | Route | Flight details | With weather | Actual |
| --- | --- | ---: | ---: | ---: |
| Jan 28, WN 2758 | OAK–LAS | 3 min | -3 min | -7 min |
| Jan 25, AA 642 | CLT–EYW | 9 min | 7 min | 55 min |
| Jan 31, OO 6398 | ACT–DFW | 12 min | 10 min | 75 min |
| Jan 28, AA 2420 | IAH–DFW | 4 min | 24 min | 3,282 min |

These examples show how the model handled individual flights; they are not a substitute for the full-week scores. The very long delays were difficult to predict.
Negative actual delays mean the flight arrived early.

## What I did

- Cleaned the January BTS file and checked delay patterns and possible aircraft links.
- Added archived departure-airport weather observations from [Iowa Environmental Mesonet](https://mesonet.agron.iastate.edu/).
- Compared two XGBoost models with a simple median benchmark.

Next I’m checking whether aircraft rotations can be identified reliably, then I’ll compare network and graph models by the end of December. I plan to finish the main model work in January 2027, with the web interface, testing, and documentation afterward.

## Run it

Run these from the project folder:

```powershell
python -m pip install -r requirements.txt
python scripts/prepare_january_sample.py
python scripts/download_january_weather.py
python scripts/train_january_baselines.py
```

The notebook with my first data checks is in `notebooks/`.
