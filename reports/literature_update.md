# Literature update for the next check-in

## Scope

This is a short, targeted update on graph models for flight-delay prediction and aircraft connections. It is not a systematic review, so it cannot establish that a particular contribution is new.

## Relevant studies

- Guo et al. (2020), *SGDAN: A Spatio-Temporal Graph Dual-Attention Neural Network for Quantified Flight Delay Prediction*, predicted each flight's departure delay three hours before departure. Its model used airport-neighbor relationships and a sequence of previous flights that shared the same aircraft. This is a direct example of a flight-level graph model using same-aircraft history. [Article and full text](https://doi.org/10.3390/s20226433)
- Cai et al. (2021), *A Deep Learning Approach for Flight Delay Prediction Through Time-Evolving Graphs*, modeled time-varying relationships in a multi-airport network with graph convolution and temporal components. The graph represents airport-level delay relationships, which differs from a graph whose individual nodes are flights. [IEEE article](https://doi.org/10.1109/TITS.2021.3103502)
- Zheng et al. (2024), *A Graph Multi-Attention Network for Predicting Airport Delays*, studied network-wide airport delay forecasts up to 24 hours ahead using BTS data from 2019 and weather features. It is relevant to the proposal's 24-hour example, though its prediction target is airport-level delay. [Article](https://doi.org/10.1016/j.tre.2023.103375)
- Tang et al. (2026), *Edge-Based GNN for Network Delay Prediction Enhanced by Flight Connectivity*, proposed a network-wide delay model that represents directional flight connectivity and upstream delay information. Its topic overlaps with network links and propagated delay. [Article](https://doi.org/10.3390/aerospace13020161)
- A 2026 study, *Delay Propagation Prediction of Aviation Network Based on Spatial-Temporal Dynamic Interaction*, proposed a spatial-temporal graph model and reported six-hour predictions on datasets from China and the United States. This means a six-hour horizon alone is not a new contribution. [Article](https://doi.org/10.1016/j.cja.2025.103884)

## What this means for this project

The proposal's claim that no published study combines a GNN with flight-delay propagation is too broad. GNNs have been used for flight-delay prediction for years. Published work also uses prior flights on the same aircraft, and more recent work models flight connectivity directly. The six-hour and 24-hour examples have also appeared in prior studies.

This does not mean the project has no useful contribution. A possible direction is to test how much aircraft-link features add to a single-flight XGBoost baseline when every input is restricted to information available at the prediction time. The January BTS check is not enough to establish that contribution or generalize across seasons. This is a candidate for discussion, not a selected novelty claim.

Before choosing a contribution, the literature review should compare the studies' prediction unit, graph construction, data source, forecast horizon, feature availability, validation split, and metrics. The project also needs a reproducible method for checking whether tail-number links represent plausible consecutive flights.
