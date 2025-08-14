import os
import pandas as pd
from datetime import datetime, timezone
import json

def load_latest_date(csv_path):
    if not os.path.exists(csv_path):
        return None
    try:
        df = pd.read_csv(csv_path, parse_dates=["time"])
        if df.empty:
            return None
        latest = df["time"].max()
        return latest.replace(tzinfo=timezone.utc)
    except Exception as e:
        print(f"Error reading {csv_path}: {e}")
        return None

def format_usgs_url(start_date,end_date,bounds):
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query.csv?"
    return (
        f"{base_url}starttime={start_date.isoformat()}T00:00:00"
        f"&endtime={end_date.isoformat()}T23:59:59"
        f"&minlatitude={bounds['minlatitude']}"
        f"&maxlatitude={bounds['maxlatitude']}"
        f"&minlongitude={bounds['minlongitude']}"
        f"&maxlongitude={bounds['maxlongitude']}"
        f"&minmagnitude=4"
        f"&orderby=time"
    )

def load_country_bounds(country_name, config_path="config/country_bounds.json"):
    with open(config_path,"r") as f:
        country_bounds = json.load(f)
    country_name_lower = country_name.lower()
    if country_name_lower not in country_bounds:
        raise ValueError(f"{country_name} not in config")
    return country_bounds[country_name_lower]

def get_all_countries(config_path="config/country_bounds.json"):
    with open(config_path,"r") as f:
        country_bounds = json.load(f)
    return list(country_bounds.keys())
