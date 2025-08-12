import os
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
from core.usgs.utils import load_latest_date, format_usgs_url
from io import StringIO

def ensure_directory_exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
def append_new_data(country, bounds, data_dir="data/usgs"):
    csv_path = os.path.join(data_dir,f"{country}_earthquake.csv")
    ensure_directory_exists(csv_path)
    
    now_utc = datetime.now(timezone.utc)
    last_date = load_latest_date(csv_path)
    
    if last_date:
        # Start from next day
        start_date = (last_date + timedelta(days=1)).date()
    else:
        #First run: start from yesterday
        start_date = (now_utc - timedelta(days=1)).date()
    
    # End at yesterday 23:59:59 UTC
    end_date = (now_utc- timedelta(days=1)).date()
    
    if start_date > end_date:
        print(f"[{country}] upto date, No new data to download")
        return
    
    url = format_usgs_url(start_date, end_date, bounds)
    print(f"[{country}] Downloading data from {start_date} to {end_date}")
    response = requests.get(url)
    
    if response.status_code != 200 or not response.text.strip():
        print(f"[{country}] No data returned for range.")
        return
    
    new_df = pd.read_csv(StringIO(response.text))
    
    if os.path.exists(csv_path):
        old_df = pd.read_csv(csv_path)
        
        # Drop all NA columns from both df before concatenation
        new_df = new_df.dropna(axis=1, how="all")
        old_df = old_df.dropna(axis=1, how="all")
        
        combined = pd.concat([new_df,old_df], ignore_index=True)
        combined.drop_duplicates(subset="id",inplace=True)
        
        if len(combined) > len(old_df):
            combined.to_csv(csv_path, index=False)
            print(f"{country}_earthquake.csv updated with {len(combined) - len(old_df)} new entries.")
        else:
            print(f"[{country}] No new earthquake entries to add.")
        
    else:
        combined = new_df.dropna(axis=1,how="all")
        combined.to_csv(csv_path, index=False)
        print(f"{country}_earthquake.csv created with {len(combined)} entries.")
