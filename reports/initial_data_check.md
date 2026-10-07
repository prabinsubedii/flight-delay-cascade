# Initial data check

I downloaded the January 2025 BTS Reporting Carrier On-Time Performance data and ran an initial check using pandas.

| Check | Result |
|---|---:|
| Flight records | 539,747 |
| Date range | January 1–31, 2025 |
| Reporting airlines | 14 |
| Airports | 329 |
| Missing aircraft tail numbers | 2,530 (0.47%) |
| Cancelled flights | 16,312 |
| Diverted flights | 1,166 |
| Missing arrival delay values | 17,478 |

Most records have an aircraft tail number. My next step is to check whether I can use these to connect consecutive flights operated by the same plane.

The number of missing arrival delay values equals the total number of cancelled and diverted flights. I still need to check whether they are the same records before deciding how to handle them.

No models have been trained yet.