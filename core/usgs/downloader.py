import os
import time
from datetime import datetime, timezone, timedelta
import pandas as pd
import requests
from io import StringIO
from core.usgs.utils import load_latest_date, format_usgs_url, load_country_bounds, get_all_countries

USGS_DATA_DIR = "data/usgs"

def ensure_directory_exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def append_new_data(country, bounds, data_dir=USGS_DATA_DIR):
    csv_path = os.path.join(data_dir,f"{country}_earthquake.csv")
    ensure_directory_exists(csv_path)

    now_utc = datetime.now(timezone.utc)
    last_date = load_latest_date(csv_path)

    start_date = (last_date + timedelta(days=1)).date() if last_date else datetime(2000,1,1).date()
    end_date = (now_utc - timedelta(days=1)).date()

    if start_date > end_date:
        print(f"[{country}] Up to date.")
        return

    url = format_usgs_url(start_date, end_date, bounds)
    print(f"[{country}] Downloading data from {start_date} to {end_date} ...")
    response = requests.get(url)
    if response.status_code != 200 or not response.text.strip():
        print(f"[{country}] No data returned.")
        return

    new_df = pd.read_csv(StringIO(response.text))
    if os.path.exists(csv_path):
        old_df = pd.read_csv(csv_path)
        new_df = new_df.dropna(axis=1, how="all")
        old_df = old_df.dropna(axis=1, how="all")
        combined = pd.concat([old_df, new_df], ignore_index=True)
        combined.drop_duplicates(subset="id", inplace=True)
        if len(combined) > len(old_df):
            combined.to_csv(csv_path, index=False)
            print(f"{country}: {len(combined)-len(old_df)} new entries added.")
        else:
            print(f"{country}: No new entries.")
    else:
        new_df.dropna(axis=1, how="all").to_csv(csv_path, index=False)
        print(f"{country}_earthquake.csv created with {len(new_df)} entries.")

def run_usgs_pipeline():
    countries = get_all_countries()
    for country in countries:
        bounds = load_country_bounds(country)
        append_new_data(country, bounds)
        time.sleep(1)  # respect 1 req/sec
