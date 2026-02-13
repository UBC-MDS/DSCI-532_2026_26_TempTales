# Title: data_loader.py
# Author: Ian Gault
# Date: Feb 12, 2026

from pathlib import Path
import shutil
import kagglehub
import pandas as pd


DATASET = "berkeleyearth/climate-change-earth-surface-temperature-data"
CSV_FILES = [
    "GlobalLandTemperaturesByCountry.csv",
    "GlobalLandTemperaturesByMajorCity.csv",
    "GlobalLandTemperaturesByState.csv",
    "GlobalTemperatures.csv",
]

# NOTE: I used ChatGPT5 to get get the function below

def load_climate_data():
    """
    Pull climate data from Kaggle and ensure all CSV files are in data/raw.
    """
    repo_root = Path(__file__).resolve().parent.parent
    raw_dir = repo_root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    missing_files = [name for name in CSV_FILES if not (raw_dir / name).exists()]
    if missing_files:
        cache_dir = Path(kagglehub.dataset_download(DATASET))
        for name in missing_files:
            source_csv = cache_dir / name
            target_csv = raw_dir / name
            shutil.copy2(source_csv, target_csv)

    return print(f'Imported: {CSV_FILES}')


if __name__ == "__main__":
    load_climate_data()
