"""Download January 2025 airport ASOS/METAR observations from Iowa State IEM.

Weather files are stored under ignored data/raw/weather/ and are not committed.
"""

from pathlib import Path
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FLIGHTS = ROOT / "data" / "processed" / "january_2025_clean.csv"
OUTPUT = ROOT / "data" / "raw" / "weather" / "iem_asos_january_2025.csv"
ENDPOINT = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
VARIABLES = "tmpf,dwpf,relh,drct,sknt,gust,vsby,mslp,skyc1,skyl1,wxcodes"
BATCH_SIZE = 45


def main() -> None:
    flights = pd.read_csv(FLIGHTS, usecols=["Origin", "Dest"], dtype="string")
    stations = sorted(set(flights["Origin"].dropna()) | set(flights["Dest"].dropna()))
    batches = [stations[i : i + BATCH_SIZE] for i in range(0, len(stations), BATCH_SIZE)]
    frames = []

    for batch_number, batch in enumerate(batches, start=1):
        params = [
            ("data", VARIABLES),
            # A short lead-in supplies observations for the first flights of Jan 1.
            ("sts", "2024-12-31T18:00:00Z"),
            ("ets", "2025-02-01T00:00:00Z"),
            ("tz", "UTC"),
            ("format", "comma"),
            ("latlon", "yes"),
            ("elev", "yes"),
            ("missing", "null"),
            ("report_type", "3"),
            ("report_type", "4"),
        ] + [("station", station) for station in batch]
        request = Request(
            f"{ENDPOINT}?{urlencode(params)}",
            headers={"User-Agent": "flight-delay-cascade-research/1.0"},
        )
        with urlopen(request, timeout=120) as response:
            # IEM includes five #DEBUG lines before the CSV header.
            frames.append(pd.read_csv(response, skiprows=5, low_memory=False))
        print(f"Downloaded batch {batch_number}/{len(batches)} ({len(batch)} requested stations)")
        if batch_number < len(batches):
            time.sleep(1.1)

    weather = pd.concat(frames, ignore_index=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    weather.to_csv(OUTPUT, index=False)
    returned = weather["station"].nunique() if "station" in weather else 0
    print(f"Requested airport codes: {len(stations):,}")
    print(f"Stations returning observations: {returned:,}")
    print(f"Observation rows: {len(weather):,}")
    print(f"Saved local weather file: {OUTPUT.relative_to(ROOT)}")
    print("IEM provides archived observations, not the forecast that was issued before a flight.")


if __name__ == "__main__":
    main()
