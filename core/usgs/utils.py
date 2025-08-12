import os
import pandas as pd
from datetime import datetime, timedelta, timezone

def load_latest_date(csv_path):
    if not os.path.exists(csv_path):
        return None
    try:
        df = pd.read_csv(csv_path,parse_dates=["time"])
        if df.empty:
            return None
        latest = df["time"].max()
        return latest.replace(tzinfo = timezone.utc)
    except Exception as e :
        print(f"Error reading {csv_path}: {e}")
        return None

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
def format_usgs_url(start_date,end_date, bounds):
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query.csv?"
    return(
        f"{base_url}starttime={start_date.isoformat()}T00:00:00"
        f"&endtime={end_date.isoformat()}T23:59:59"
        f"&minlatitude={bounds['minlatitude']}"
        f"&maxlatitude={bounds['maxlatitude']}"
        f"&minlongitude={bounds['minlongitude']}"
        f"&maxlongitude={bounds['maxlongitude']}"
        f"&minmagnitude=4"
        f"&orderby=time"
    )
    

    
    
