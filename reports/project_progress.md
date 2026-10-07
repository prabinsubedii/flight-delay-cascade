# Project progress

## Completed and verified

- GitHub repository: https://github.com/prabinsubedii/flight-delay-cascade
- January 2025 BTS Reporting Carrier On-Time Performance archive and extracted CSV are present under `data/raw/` (ignored by Git).
- `.venv` is present, ignored by Git, and uses Python 3.11.1 with pandas 3.0.6.
- Added `scripts/initial_data_check.py` as a reusable, read-only summary check.
- Verified 539,747 records, January 1–31 dates, 14 reporting airlines, 329 origin/destination airports, 2,530 missing or blank tail numbers, 16,312 cancellations, 1,166 diversions, and 17,478 missing arrival delays.
- Verified that the missing arrival-delay records exactly equal cancelled-or-diverted records: 16,312 cancellation only, 1,166 diversion only, none in both or neither.
- Updated the data-check report and README to reflect verified results. No model has been trained.
- The owner is in the third semester. The next semester is expected to run approximately January 20–May 15, 2027. The target is to complete data exploration, literature review, and model development before then; focus the next semester on deployment/web interface, testing, documentation, and the final presentation; and complete the project around March/April 2027. This is a proposed schedule for adviser discussion.

## Decisions and open questions

- Keep the starting comparison: single-flight XGBoost, XGBoost with network/aircraft-rotation features, then a GNN. Discuss substantive changes first.
- Research questions remain: downstream prediction quality; feasible prediction horizons (including investigating the proposal's 6- and 24-hour examples); relative value of weather, congestion, route history, and rotations; generalization across airports, seasons, and disruption periods.
- GNN flight-delay work already exists according to the project owner's supplied context. Update and verify the literature before claiming novelty. Incomplete aircraft connections and information available at prediction time remain possible angles only; neither is a selected contribution.
- The attached proposal's claims that no published GNN study combines this network with cascade prediction, or that no study has deployed a passenger tool, are unverified and should not be repeated as fact.
- The proposal's live prediction and passenger connection-risk goals depend on later data-feasibility checks. Aircraft assignments in historical BTS records do not prove advance availability; prediction must use only information available at the chosen prediction time.
- January 2025 is only an initial development sample. Chronological evaluation and broader data are needed before generalization claims.
- The exact semester end date is approximate (around May 15, 2027); project completion and the final presentation are expected around March/April 2027.

## Next steps

1. Complete exploratory analysis, including whether actual aircraft rotations can be reconstructed and which records are usable.
2. Review current literature and establish a defensible contribution before narrowing the research focus.
3. Agree on and review the next analysis/modeling step before starting model training.
4. Aim to develop and chronologically evaluate the XGBoost baseline, network-feature comparison, and GNN by January 19, 2027.
5. From about January 20 to May 15, 2027, focus on the web interface and deployment, testing, documentation, and final presentation; target completion around March/April 2027.
6. Later, investigate weather/congestion data feasibility and defer live predictions and passenger connection-risk features until the research and data are ready.
