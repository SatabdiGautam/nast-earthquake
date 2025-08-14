import os
import sys
import time
from datetime import datetime, timezone, timedelta
from core.usgs.downloader import run_usgs_pipeline, append_new_data, USGS_DATA_DIR, get_all_countries, load_country_bounds
from core.raspberryshake.downloader import download_raspberry_data
import pandas as pd

LOCK_FILE = "/tmp/earthquake_pipeline.lock"
DAILY_RUN_HOUR_UTC = 11  # daily at 11:00 UTC

def is_already_running():
    return os.path.exists(LOCK_FILE)

def create_lock():
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

def remove_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

def run_pipeline():
    if is_already_running():
        print("Pipeline already running.")
        return

    create_lock()
    try:
        print(f"Pipeline started at {datetime.now(timezone.utc)} UTC")

        # Step 1: USGS download & check for new events
        countries = get_all_countries()
        new_events_dict = {}

        for country in countries:
            bounds = load_country_bounds(country)
            csv_path = os.path.join(USGS_DATA_DIR, f"{country}_earthquake.csv")

            # Save previous count
            old_count = 0
            if os.path.exists(csv_path):
                df_old = pd.read_csv(csv_path)
                old_count = len(df_old)

            append_new_data(country, bounds, data_dir=USGS_DATA_DIR)

            # Check how many new events
            df_new = pd.read_csv(csv_path)
            new_count = len(df_new) - old_count
            if new_count > 0:
                new_events_dict[country] = csv_path
                print(f"[{country}] {new_count} new events detected.")
            else:
                print(f"[{country}] No new events.")

        # Step 2: Only download Raspberry Shake data for countries with new events
        for country, csv_path in new_events_dict.items():
            download_raspberry_data(country, csv_path)

        print(f"Pipeline finished at {datetime.now(timezone.utc)} UTC")

    finally:
        remove_lock()

def daily_scheduler():
    while True:
        now = datetime.now(timezone.utc)
        run_time = now.replace(hour=DAILY_RUN_HOUR_UTC, minute=0, second=0, microsecond=0)
        if now > run_time:
            run_time += timedelta(days=1)

        sleep_seconds = (run_time - now).total_seconds()
        print(f"Next run scheduled at {run_time} UTC. Sleeping {sleep_seconds/3600:.2f} hours.")
        time.sleep(sleep_seconds)

        run_pipeline()

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1].lower() == "run":
        run_pipeline()
    elif len(sys.argv) == 2 and sys.argv[1].lower() == "start":
        daily_scheduler()
    else:
        print("Usage:")
        print("  python main.py run    # run immediately")
        print("  python main.py start  # run daily at 11:00 UTC")
