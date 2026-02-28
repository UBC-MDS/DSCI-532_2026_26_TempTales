# import numpy as np
import pandas as pd
from pathlib import Path


def get_season(month: int) -> str:
    """Map month to season name."""
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"


def process_and_save_data(
    raw_path: Path = Path("data/raw/GlobalLandTemperaturesByCountry.csv"),
    output_dir: Path = Path("data/processed")
) -> None:
    """
    Reads raw climate data, processes it into a unified monthly dataframe,
    and saves the result as a pickle file for high-performance loading.

    Args:
        raw_path (Path):
            Path to the raw GlobalLandTemperaturesByCountry.csv file.
        output_dir (Path):
            Directory where the processed .pkl file will be saved.

    Output Files:
        - df_processed.pkl: Unified dataframe with columns
          year | month | country | AvgTemp | AvgUncertain | season
    """

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(raw_path, index_col="dt", parse_dates=True)

    df["year"] = df.index.year
    df["month"] = df.index.month

    # Filter for relevant timeframe
    df = df[(df["year"] >= 1860)]

    # Build unified dataframe with standardized column names
    df_processed = df.rename(columns={
        "AverageTemperature": "AvgTemp",
        "AverageTemperatureUncertainty": "AvgUncertain",
        "Country": "country"
    })

    df_processed["season"] = df_processed["month"].apply(get_season)

    # Keep only required columns
    df_processed = df_processed[["year", "month", "country", "AvgTemp", "AvgUncertain", "season"]]

    print("Saving to pickle...")
    # Use pickle for fast I/O and data type preservation
    df_processed.to_pickle(output_dir / "df_processed.pkl")


if __name__ == "__main__":
    # Define paths relative to this script
    current_dir = Path(__file__).parent
    # Assuming standard structure: project/src/data_processor.py
    raw_data_path = current_dir / ".." / "data" / \
        "raw" / "GlobalLandTemperaturesByCountry.csv"
    processed_dir = current_dir / ".." / "data" / "processed"

    process_and_save_data(raw_data_path, processed_dir)