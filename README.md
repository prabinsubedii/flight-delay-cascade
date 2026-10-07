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

I have prepared the project proposal, outlined the research questions, and created this repository to organize the work.

The project is now at the data collection stage. My first task is to download an initial sample of BTS flight data and check whether it has the information needed to connect flights using aircraft tail numbers.

## Data

I am starting with the Bureau of Transportation Statistics Reporting Carrier On-Time Performance dataset.

I also plan to look into weather and airport congestion data, depending on access and how useful they are for the predictions.

Large datasets will stay outside GitHub. I will document how to download and prepare them so the work can be reproduced.

## Next steps

- Download and inspect the first flight dataset.
- Check missing values and explore delay patterns.
- Connect flights operated by the same aircraft.
- Build an XGBoost baseline.
- Add information from previous flights and airport conditions.
- Build the flight graph and train a GNN.
- Compare the models on later time periods and different conditions.
- Build the web demo and complete the report.

## Things to work out

I still need to update the literature review and narrow down the specific contribution of this project.

I also need to check which information would be available at the time of prediction. The first version will use historical data. Live predictions and passenger connection risk will need further investigation.
