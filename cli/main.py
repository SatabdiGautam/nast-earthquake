import os
import sys
import time
from datetime import datetime, timezone, timedelta
import pandas as pd
from core.usgs.downloader import append_new_data
from core.usgs.utils import load_country_bounds, get_all_countries
from core.raspberryshake.downloader import download_raspberry_data

LOCK_FILE = "/tmp/earthquake_pipeline.lock"
USGS_DATA_DIR = "data/usgs"
RASPBERRY_DIR = "data/raspberryshake"
RUN_HOUR_UTC = 2  # run daily at 02:00 UTC

pipeline_running = False


def is_already_running():
    return os.path.exists(LOCK_FILE)


def create_lock():
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))


def remove_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)


def run_pipeline():
    global pipeline_running
    if pipeline_running:
        print("Pipeline already running.")
        return

    pipeline_running = True
    create_lock()
    try:
        print(f"Pipeline started at {datetime.now(timezone.utc)}")

        # Step 1: Get all countries from config
        countries = get_all_countries()
        print(f"Found countries in config: {countries}")

        # Step 2: USGS data download for all countries
        for country in countries:
            bounds = load_country_bounds(country)
            csv_path = os.path.join(USGS_DATA_DIR, f"{country}_earthquake.csv")
            append_new_data(country, bounds, data_dir=USGS_DATA_DIR)
            time.sleep(1)  # respect 1 req/sec for USGS

        # Step 3: Raspberry Shake data for every earthquake in CSVs
        for country in countries:
            csv_path = os.path.join(USGS_DATA_DIR, f"{country}_earthquake.csv")
            if not os.path.exists(csv_path):
                print(f"No CSV found for {country}, skipping Raspberry Shake download.")
                continue

            df = pd.read_csv(csv_path)
            for _, quake in df.iterrows():
                download_raspberry_data(
                    country,
                    quake,  # pass quake row
                    RASPBERRY_DIR
                )
                time.sleep(1)  # respect 1 req/sec for Raspberry Shake

        print(f"Pipeline finished at {datetime.now(timezone.utc)}")
    finally:
        pipeline_running = False
        remove_lock()


def daily_scheduler():
    while True:
        now = datetime.now(timezone.utc)
        run_time = now.replace(hour=RUN_HOUR_UTC, minute=0, second=0, microsecond=0)
        if now > run_time:
            run_time += timedelta(days=1)

        sleep_seconds = (run_time - now).total_seconds()
        print(f"Next run scheduled at {run_time} UTC. Sleeping {sleep_seconds/3600:.2f} hours.")
        time.sleep(sleep_seconds)

        if not is_already_running():
            run_pipeline()
        else:
            print("Pipeline skipped — already running.")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1].lower() == "start":
        daily_scheduler()
    elif len(sys.argv) == 2 and sys.argv[1].lower() == "run":
        run_pipeline()
    else:
        print("Usage:")
        print("  python cli_main.py start   # run daily at set time")
        print("  python cli_main.py run     # run immediately")


