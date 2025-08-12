import json
from core.usgs.downloader import append_new_data

CONFIG_FILE = "config/country_bounds.json"

def main():
    with open(CONFIG_FILE ,"r") as f:
        coutry_bounds = json.load(f)
        
    for country, bounds in coutry_bounds.items():
        append_new_data(country,bounds)

if __name__ == "__main__":
    main()