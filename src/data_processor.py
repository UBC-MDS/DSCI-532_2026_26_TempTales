# import numpy as np
import pandas as pd
from pathlib import Path


def process_and_save_data(
    raw_path: Path = Path("data/raw/GlobalLandTemperaturesByCountry.csv"),
    output_dir: Path = Path("data/processed")
) -> None:
    """
    Reads raw climate data, processes it into yearly and seasonal aggregations, 
    and saves the results as pickle files for high-performance loading.

    Args:
        raw_path (Path): 
            Path to the raw GlobalLandTemperaturesByCountry.csv file.
        output_dir (Path): 
            Directory where the processed .pkl files will be saved.

    Output Files:
        - df_yearly.pkl: Aggregated yearly data with confidence intervals.
        - df_seasonal.pkl: Aggregated seasonal data.
    """

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(raw_path, index_col="dt", parse_dates=True)

    df["year"] = df.index.year
    df["month"] = df.index.month

    # Filter for relevant timeframe
    df = df[(df["year"] >= 1860)]

    # Yearly Aggregation
    df_yearly = df.groupby(["year", "Country"], as_index=False).agg(
        avg_temp=("AverageTemperature", "mean"),
        avg_uncertainty=("AverageTemperatureUncertainty", "mean"),
        data_coount=("AverageTemperature", "count")
    )

    # Calculate 95% Confidence Interval proxies (Upper/Lower bounds)
    df_yearly["temp_lower"] = df_yearly["avg_temp"] - \
        df_yearly["avg_uncertainty"]
    df_yearly["temp_upper"] = df_yearly["avg_temp"] + \
        df_yearly["avg_uncertainty"]

    # Seasonal Aggregation
    def get_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"

    df_seasonal_source = df.copy()
    df_seasonal_source["season"] = df_seasonal_source["month"].apply(
        get_season)

    df_seasonal = df_seasonal_source.groupby(
        ["year", "Country", "season"], as_index=False
    )["AverageTemperature"].mean()

    print("Saving to pickle...")
    # 4. Save to Disk
    # Use pickle for fast I/O and data type preservation
    df_yearly.to_pickle(output_dir / "df_yearly.pkl")
    df_seasonal.to_pickle(output_dir / "df_seasonal.pkl")


if __name__ == "__main__":
    # Define paths relative to this script
    current_dir = Path(__file__).parent
    # Assuming standard structure: project/src/data_processor.py
    raw_data_path = current_dir / ".." / "data" / \
        "raw" / "GlobalLandTemperaturesByCountry.csv"
    processed_dir = current_dir / ".." / "data" / "processed"

    process_and_save_data(raw_data_path, processed_dir)
