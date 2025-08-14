import pandas as pd
import time
from datetime import timedelta
from pathlib import Path
from core.raspberryshake.utils import (
    load_country_bounds,
    get_stations_in_bounds,
    download_waveform
)

def download_raspberry_data(country: str, quake_row: pd.Series, base_output_dir="data/raspberryshake"):
    """
    Download Raspberry Shake data for a single earthquake.
    Saves to data/raspberryshake/<country>/<event_id>/<station>.mseed
    """
    # Event time and ID
    eq_time = pd.to_datetime(quake_row["time"])
    event_id = eq_time.strftime("%Y%m%d_%H%M%S")
    
    # Load country bounds
    bounds = load_country_bounds(country)
    stations = get_stations_in_bounds(bounds)
    
    if not stations:
        print(f"[{country}] No stations found in bounds.")
        return

    # Download window: 5 min before to 15 min after event
    start_time = (eq_time - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S")
    end_time = (eq_time + timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%S")
    
    for station in stations:
        output_path = Path(base_output_dir) / country / event_id / f"{station}.mseed"

        # Skip if already downloaded
        if output_path.exists():
            continue

        try:
            print(f"[{country}] Downloading {station} for event {event_id}...")
            download_waveform(station, start_time, end_time, output_path)
            time.sleep(1)  # respect 1 request/sec
        except Exception as e:
            print(f"[{country}] Failed to download {station} for event {event_id}: {e}")
