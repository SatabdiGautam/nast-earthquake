import requests
import datetime
import time
import os

# Geographic bounding box
NEPAL_BOUNDS = {
    "minlatitude":26.3,
    "maxlatitude":30.5,
    "minlongitude":80.0,
    "maxlongitude":88.2
}

# Configurations
RETRY_LIMIT = 3
REQUEST_DELAY_SECONDS = 1
MIN_MAGNITUDE = 4
OUTPUT_DIR="nepal_earthquake_data"
ERROR_LOG_FILE = "error_log.txt"

# For consistent filenames for USGS data
def generate_output_filename(start_date, end_date, output_dir=OUTPUT_DIR):
    filename = f"nepal_earthquake_{start_date}_to_{end_date}_mag{MIN_MAGNITUDE}.json"
    return os.path.join(output_dir,filename)

# Check if data already exists    
def already_downloaded(start_date, end_date, output_dir=OUTPUT_DIR):
    file_path = generate_output_filename(start_date,end_date,output_dir)
    return os.path.exists(file_path)

def fetch_data_with_retry(url, retries=RETRY_LIMIT):
    for attempt in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                print(f"HTTP ERROR {response.status_code}")
                
        except Exception as e:
            print(f"Error: {e}")
            
        print(f"Retry {attempt + 1 }/{retries}")
        time.sleep(2)
        
    return None

# Fetch Nepals Earthquake data from USGS and save in json file
def fetch_nepal_earthquake_data(start_date, end_date, output_dir="nepal_earthquake_data", log_file="error_log.txt"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    start_str = start_date.isoformat()
    end_str = end_date.isoformat()
    
    url= (
        "https://earthquake.usgs.gov/fdsnws/event/1/query"
        f"?format=geojson&starttime={start_str}&endtime={end_str}"
        f"&minlatitude={NEPAL_BOUNDS['minlatitude']}"
        f"&maxlatitude={NEPAL_BOUNDS['maxlatitude']}"
        f"&minlongitude={NEPAL_BOUNDS['minlongitude']}"
        f"&maxlongitude={NEPAL_BOUNDS['maxlongitude']}"
        f"&minmagnitude={MIN_MAGNITUDE}"
    )
    
    print(f"fetching earthquake data from {start_str} to {end_str}")
    
    data_text = fetch_data_with_retry(url)
    
    if data_text is None:
        with open(log_file,"a") as log:
            log.write(f"Failed to fetch data for {start_str} to {end_str}\n")
        return
    
    output_path = generate_output_filename(start_date,end_date,output_dir)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(data_text)   
    
    print(f"Saved data to {output_path}")
    time.sleep(REQUEST_DELAY_SECONDS)    
    
def get_last_friday(reference_date=None):
    if reference_date is None:
        reference_date = datetime.date.today()
        
    if reference_date.weekday() == 4:
        reference_date -= datetime.timedelta(days=1)
        
    days_since_friday = (reference_date.weekday() - 4)%7
    return reference_date - datetime.timedelta(days=days_since_friday)

def download_earthquake_data(weeks = 2):
    last_friday = get_last_friday()
    
    # Download data for last 4 full weeks (Saturday to Friday)
    for i in range(52):
        end_date = last_friday - datetime.timedelta(weeks = i)
        start_date = end_date - datetime.timedelta(days=6)
        
        if not already_downloaded(start_date, end_date, output_dir=OUTPUT_DIR):
            fetch_nepal_earthquake_data(start_date,end_date,output_dir=OUTPUT_DIR)
        else:
            print(f"Data Exists from {start_date} to {end_date}")
    
   
if __name__ == "__main__":
    download_earthquake_data()
    