import pandas as pd
import time
from datetime import timedelta
from pathlib import Path

from core.raspberryshake.utils import (
    load_country_bounds,
    get_stations_in_bounds,
    download_waveform
)


def download_raspberry_data(country: str, csv_path: str, base_output_dir="data/raspberryshake"):
    """
    Download Raspberry Shake data for earthquakes listed in a CSV.
    Reads CSV bottom-to-top, downloads 5 min before to 15 min after each event.
    Saves to data/raspberryshake/<country>/<event_id>/<station>.mseed
    """
    # Load earthquake CSV
    df = pd.read_csv(csv_path, parse_dates=["time"])
    if df.empty:
        print(f"[{country}] No earthquake data found.")
        return

    # Load country bounds
    bounds = load_country_bounds(country)
    stations = get_stations_in_bounds(bounds)

    if not stations:
        print(f"[{country}] No stations found in bounds.")
        return

    print(f"[{country}] Found {len(stations)} stations.")

    # Iterate bottom-to-top (oldest events first)
    for _, row in df.iloc[::-1].iterrows():
        eq_time = row["time"]
        event_id = row.get("id", eq_time.strftime("%Y%m%d%H%M%S"))

        start_time = (eq_time - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S")
        end_time = (eq_time + timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%S")

        for station in stations:
            output_path = Path(base_output_dir) / country / event_id / f"{station}.mseed"

            if output_path.exists():
                continue

            try:
                print(f"[{country}] Downloading {station} for event {event_id}...")
                download_waveform(station, start_time, end_time, output_path)
                time.sleep(1)  # Respect 1 request/sec
            except Exception as e:
                print(f"[{country}] Failed to download {station} for event {event_id}: {e}")
