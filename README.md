# Flight Delay Cascade

Master's project by Prabin Subedi.

I am looking at whether delays on one flight can affect later flights using the same aircraft, and whether that information helps predict delays.

## Progress

I have cleaned the January 2025 BTS sample, explored it, and run a first XGBoost comparison with and without origin weather. The simple median prediction did better than either model, so this is still a prototype. The aircraft-link checks are also preliminary. See the [exploratory notebook](notebooks/january_2025_first_look.ipynb) and [baseline results](reports/january_baseline.md).

## Next

Next I plan to review the baseline result, improve the data checks, and compare network and graph models by December 31, 2026. I aim to finish the main model work in January 2027. The target and prediction timing used here are a first choice to discuss with my professor.

After the main work is done in January 2027, I plan to use the remaining time for web design, deployment, testing, documentation, and final presentation materials. I expect to finish around March or April.

## Data

The raw BTS and weather files, processed data, and model files stay on my computer and are not committed to Git.
