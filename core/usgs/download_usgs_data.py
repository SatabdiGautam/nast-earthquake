import sys
from core.usgs.downloader import run_usgs_pipeline

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1].lower() == "run":
        run_usgs_pipeline()
    else:
        print("Usage:")
        print("  python download_usgs_data.py run   # download USGS data immediately")
