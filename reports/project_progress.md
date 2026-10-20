# Project progress

## Completed and verified

- GitHub repository: https://github.com/prabinsubedii/flight-delay-cascade
- January 2025 BTS Reporting Carrier On-Time Performance archive and extracted CSV are present under `data/raw/` (ignored by Git).
- `.venv` is present, ignored by Git, and uses Python 3.11.1 with pandas 3.0.6.
- Added `scripts/initial_data_check.py` as a reusable, read-only summary check.
- Added `scripts/prepare_january_sample.py` to standardize codes, parse dates and numeric fields, keep every row, and create explicit status flags. Its output is ignored by Git and remains local.
- Added `scripts/download_january_weather.py` to retrieve January airport observations for the 329 airport codes in the BTS sample. The archive returned observations for 292 codes and is kept under ignored `data/raw/weather/`.
- Added `scripts/train_january_baselines.py` and trained a flight-only XGBoost model and a version with origin-airport weather. The experiment predicts arrival-delay minutes at a 30-minute-before-scheduled-departure cutoff and uses a chronological training, early-stopping, and final-test split. Full method and results are in [the baseline report](january_baseline.md).
- Added `scripts/exploratory_data_check.py` and completed a first exploratory summary of delay values, airports, carriers, repeated tail/date groups, and candidate same-aircraft connections.
- Added a preliminary literature update with published examples of flight-delay GNNs, same-aircraft sequence features, and six- and 24-hour prediction horizons. This is not a systematic review and does not establish a new contribution.
- Verified 539,747 records from January 1 to 31, 14 reporting airlines, 329 origin/destination airports, 2,530 missing or blank tail numbers, 16,312 cancellations, 1,166 diversions, and 17,478 missing arrival delays.
- Verified that the missing arrival-delay records exactly equal cancelled-or-diverted records: 16,312 cancellation only, 1,166 diversion only, none in both or neither.
- Found 5,612 distinct reported tail numbers. Among operated records with a tail number, 127,981 of 142,174 tail/date groups contained multiple records. A first screen produced 449,447 same-tail, same-date, endpoint-compatible candidate pairs with a 0 to 720 minute scheduled clock gap; 62,285 previous-flight records had multiple possible successors. This supports further screening, but does not validate an operational rotation.
- On the January 25–31 holdout, the training-median benchmark had 18.00-minute MAE. The flight-only XGBoost had 24.47-minute MAE; adding origin weather had 24.25-minute MAE. Both models had worse RMSE than the median benchmark. This is a first one-month result, not a validated final model.
- The owner is in the third semester. The first XGBoost comparison is now complete. The current target is to develop network and graph model comparisons by December 31, 2026, finish the main model work in January 2027, then use the remaining time for web design, deployment, testing, and documentation. Project completion is expected around March/April 2027. This schedule is for adviser discussion.

## Decisions and open questions

- Keep the starting comparison: single-flight XGBoost, XGBoost with network/aircraft-rotation features, then a GNN. Discuss substantive changes first.
- For the first prototype, predict arrival delay in minutes 30 minutes before scheduled departure. This target and cutoff are a working choice, not yet confirmed with the adviser.
- Archived origin weather observations were included using the latest report at least 30 minutes before the cutoff and no more than three hours old. Archived valid time does not prove report publication time; destination forecasts are not included.
- Research questions remain: downstream prediction quality; feasible prediction horizons (including investigating the proposal's 6- and 24-hour examples); relative value of weather, congestion, route history, and rotations; generalization across airports, seasons, and disruption periods.
- GNN flight-delay work already exists according to the project owner's supplied context. Update and verify the literature before claiming novelty. Incomplete aircraft connections and information available at prediction time remain possible angles only; neither is a selected contribution.
- The attached proposal's claims that no published GNN study combines this network with cascade prediction, or that no study has deployed a passenger tool, are unverified and should not be repeated as fact.
- The proposal's live prediction and passenger connection-risk goals depend on later data-feasibility checks. Aircraft assignments in historical BTS records do not prove advance availability; prediction must use only information available at the chosen prediction time.
- January 2025 is only an initial development sample. Chronological evaluation and broader data are needed before generalization claims.
- The main model work is targeted for completion in January 2027. After that, the remaining work is expected to be finishing tasks, web design, testing, documentation, and presentation materials. Overall completion and the final presentation are expected around March/April 2027; the semester is expected to end around May 15.
- The first baseline is complete. Review its target and cutoff with the adviser, then test defensible network features and develop an initial graph comparison by December 31, 2026. Finish the main model evaluation in January 2027.

## Next steps

1. Continue exploratory checks and the literature review. Improve the aircraft-link screen by checking local dates, actual timings, and ambiguous successors.
2. Review the prototype's target, cutoff, weather source, and chronological evaluation with the adviser.
3. Validate aircraft-link features before using them, then compare the single-flight model with network features and an initial GNN by December 31, 2026. Finish the main model evaluation in January 2027.
4. After the main work is done, focus on web design, deployment, testing, documentation, and presentation materials. Target completion is March/April 2027.
5. Investigate weather/congestion data feasibility later. Defer live predictions and passenger connection-risk features until the data and research are ready.
