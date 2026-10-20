# January flight-delay baseline

## Setup

I trained two XGBoost regression models to predict arrival delay in minutes for operated flights. One uses scheduled flight details; the other adds weather observed at the origin airport. Both predict 30 minutes before scheduled departure. Weather is the latest IEM airport observation no later than that cutoff, and no more than three hours old.

The flight fields are carrier, origin, destination, scheduled local departure hour and day, scheduled distance, and scheduled elapsed time. The weather fields are temperature, dew point, humidity, wind, visibility, pressure, and cloud information. Actual departure delay, actual arrival delay as an input, tail number, and cancellation/diversion status were not used as predictors. Cancelled and diverted flights are outside this arrival-delay target.

The split is chronological: train on January 1–18, choose the number of trees using January 19–24, and report the final holdout on January 25–31. This keeps the last week out of training and early stopping.

Weather observations came from the [Iowa Environmental Mesonet airport archive](https://mesonet.agron.iastate.edu/request/download.phtml), which provides historical ASOS/METAR observations. The request used its [ASOS data service](https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?help=). Observations were available for 292 of the 329 airport codes in the flight sample. For the final week, 113,183 of 118,487 eligible flights (95.5%) had an origin observation within the three-hour window. The archive contains observed conditions, not the forecast that an operator would have seen. The 30-minute buffer reduces the risk of using a report from after the chosen cutoff, but the archive does not provide its original publication time.

## Results

| Model | Final-week MAE | Final-week RMSE | R² |
| --- | ---: | ---: | ---: |
| Training-set median | 18.00 min | 42.05 min | -0.003 |
| XGBoost, flight details | 24.47 min | 43.38 min | -0.068 |
| XGBoost, flight details plus origin weather | 24.25 min | 43.91 min | -0.094 |

The weather version lowered MAE by about 0.22 minutes compared with the flight-only XGBoost model, but its RMSE was worse. Both XGBoost models performed worse than simply predicting the training-set median. The training period's mean arrival delay was 6.13 minutes; the test period's was -4.65 minutes. These results do not show a useful improvement yet.

I checked the final week by day and looked at the largest delays. Model MAE stayed in a similar range each day: 22.44 to 25.71 minutes without weather and 21.25 to 26.91 with it. There were 699 flights delayed by more than three hours. Removing those flights brings the median benchmark MAE to 15.98 minutes, compared with 22.57 for flight-only XGBoost and 22.37 with weather. So a few extreme cases are not the only reason the models fell behind the benchmark. The most extreme record is a 3,282-minute delay; it needs its own follow-up before deciding how to handle such cases in a later model.

## Limits and next steps

This is a first prototype on one month, not a final project result. January alone cannot show seasonal performance. The weather file is based on historical observations with limited quality control, and archived observation times do not prove exactly when each report became available. Weather at the destination and forecast products were not included. Aircraft rotation and network features are also not in this single-flight baseline; the candidate aircraft links still need validation before they are used.

Next, inspect the unusually large delays and split performance by date and airport. Then review the target and cutoff, try a network-feature comparison using only defensible prior-flight information, and continue toward the planned graph model. Do not claim that weather or aircraft links cause delays from these predictive results.

## Reproduce

From the repository root, prepare the January flight file, download the weather observations, then train both models:

```powershell
.\.venv\Scripts\python.exe scripts/prepare_january_sample.py
.\.venv\Scripts\python.exe scripts/download_january_weather.py
.\.venv\Scripts\python.exe scripts/train_january_baselines.py
```

Metrics, predictions, and saved models are written under `data/processed/january_baseline/`. Raw and processed data, model files, and the virtual environment are ignored by Git.
