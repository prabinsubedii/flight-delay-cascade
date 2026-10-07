# Predicting Cascading Flight Delays

Master's project by Prabin Subedi.

## About this project

A delay on one flight can affect other flights later in the day, especially when the same plane is used for multiple trips. I want to study how these delays spread and whether using connections between flights helps make better predictions.

I will first build an XGBoost baseline, then compare it with a Graph Neural Network. I also want to build a web demo where someone can check delay predictions and possible risks to their connecting flight.

## Research questions

- Can a GNN predict downstream flight delays better than a traditional model, including one that uses information from connected flights?
- How far in advance can we make useful predictions? How does performance change at different prediction times?
- Which information helps the most: aircraft rotations, weather, airport congestion, or historical route performance?
- Does the model work well across different airports and seasons, including days with major disruptions?

I will refine these questions as I review more papers and work with the data.

## Current progress

The January 2025 BTS sample is downloaded and locally available. A reusable check confirms the initial record counts and shows that missing arrival-delay values correspond exactly to cancelled or diverted records. The check and detailed findings are documented in [reports/initial_data_check.md](reports/initial_data_check.md). No models have been trained.

I am in my third semester. The current target is to do the data exploration, literature update, and model development before the next semester, which is expected to run from about January 20 to May 15, 2027. That semester is expected to focus on the web interface and deployment, testing, documentation, and the final presentation. I expect to complete the project around March or April 2027, near the presentation period; this schedule still needs discussion with my adviser.

## Data

I am starting with the Bureau of Transportation Statistics Reporting Carrier On-Time Performance dataset.

I also plan to look into weather and airport congestion data, depending on access and how useful they are for the predictions.

Large datasets will stay outside GitHub. I will document how to download and prepare them so the work can be reproduced.

## Next steps

- By November 2026, explore the data and check whether aircraft rotations can be reconstructed reliably; update the literature review.
- By January 19, 2027, aim to develop and evaluate the XGBoost baseline, network-feature comparison, and GNN, using chronological validation and only information available at each prediction time. Model training has not started and will follow review of the next step.
- From about January 20 to May 15, 2027, focus on the web interface and deployment, testing, documentation, and the final presentation. Target project completion is March or April 2027.
- Investigate live data and passenger connection-risk feasibility before adding them to the demo.

## Things to work out

I still need to update the literature review and narrow down the specific contribution of this project. GNN-based flight-delay prediction already exists, so novelty claims in the original proposal need verification and revision.

The historical BTS aircraft assignment does not prove that the assignment was known at an earlier prediction time. I also need to check which information would be available at each prediction horizon. Live predictions and passenger connection risk need further investigation. January 2025 alone cannot support claims about seasonal generalization.

See [reports/project_progress.md](reports/project_progress.md) for verified progress, open decisions, and next steps. Re-run the initial check with `.\.venv\Scripts\python.exe scripts/initial_data_check.py` from the repository root.
