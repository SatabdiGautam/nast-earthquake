import json
import requests
from pathlib import Path
from xml.etree import ElementTree as ET

FDSN_STATION_URL = "https://fdsnws.raspberryshakedata.com/fdsnws/station/1/query"
FDSN_DATA_URL = "https://fdsnws.raspberryshakedata.com/fdsnws/dataselect/1/query"


def load_country_bounds(country_name: str, config_path="config/country_bounds.json") -> dict:
    """
    Load bounding box for a country from config.
    """
    bounds_path = Path(config_path)
    if not bounds_path.exists():
        raise FileNotFoundError(f"{bounds_path} not found.")

    with open(bounds_path, "r") as f:
        country_bounds = json.load(f)

    country_name_lower = country_name.lower()
    if country_name_lower not in country_bounds:
        raise ValueError(f"Country '{country_name}' not found in {config_path}.")

    return country_bounds[country_name_lower]


def get_stations_in_bounds(bounds: dict) -> list:
    """
    Fetch Raspberry Shake stations in the bounding box.
    """
    params = {
        "net": "AM",
        "minlat": bounds["minlatitude"],
        "maxlat": bounds["maxlatitude"],
        "minlon": bounds["minlongitude"],
        "maxlon": bounds["maxlongitude"],
        "level": "station",
        "format": "xml"
    }

    response = requests.get(FDSN_STATION_URL, params=params)
    response.raise_for_status()

    stations = []
    root = ET.fromstring(response.text)
    for network in root.findall(".//{*}Network"):
        for station in network.findall("{*}Station"):
            code = station.attrib.get("code")
            if code:
                stations.append(code)
    return stations


def download_waveform(station_code: str, start_time: str, end_time: str, output_path: Path):
    """
    Download waveform from FDSN dataselect API and save as MiniSEED.
    """
    params = {
        "net": "AM",
        "sta": station_code,
        "starttime": start_time,
        "endtime": end_time
    }

    response = requests.get(FDSN_DATA_URL, params=params, stream=True)
    response.raise_for_status()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return output_path
