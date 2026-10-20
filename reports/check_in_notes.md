# Check-in notes

## What I have done

- Prepared a local working copy of the January 2025 BTS sample. It keeps all 539,747 rows and adds clear flight-status flags.
- Started exploring delay patterns, missing values, airlines, airports, and repeated aircraft identifiers in the [notebook](../notebooks/january_2025_first_look.ipynb).
- Found possible same-aircraft links, but they are not confirmed flight rotations.
- Trained a first XGBoost comparison with flight details alone and with origin weather. The training-median benchmark did better on the final week. See the [method and results](january_baseline.md).
- Checked the final week's scores by day and without delays over three hours. The simple median still did better, so the result is not only due to a few very large delays.

## What I am working out

- The project sequence is still a single-flight XGBoost baseline, then network/aircraft features, then a GNN.
- The prototype predicts arrival-delay minutes using scheduled flight details and origin weather available at least 30 minutes before scheduled departure. I should confirm this target and cutoff with my professor.
- The weather archive has observation times, but not original publication times. I need to decide whether this is adequate for the project or whether forecast data is needed.
- How to handle ambiguous or overnight aircraft links.

## Proposed next steps

- Review the prototype and its limitations with my professor.
- Validate aircraft-link features before including them.
- Compare with network features and an initial graph model by December 31, 2026, then finish the main model work in January 2027.
- After that, focus on web design, deployment, testing, documentation, and presentation materials. Aim to finish around March or April.
