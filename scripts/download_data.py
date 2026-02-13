from pathlib import Path
import kaggle
import shutil
import zipfile

kaggle.api.authenticate()  # check Kaggle API credentials set up in ~/.kaggle/kaggle.json
print("Authenticated with Kaggle API successfully.")

DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATASET = "berkeleyearth/climate-change-earth-surface-temperature-data"
ZIP_PATH = DATA_DIR / "dataset.zip"

kaggle.api.dataset_download_files(DATASET, path=DATA_DIR, unzip=True)

print("Data downloaded and extracted successfully.")
