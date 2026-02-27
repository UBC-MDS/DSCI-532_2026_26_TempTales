# imports
from pathlib import Path
import pandas as pd

# Path Configurations
app_dir = Path(__file__).parent
data_path = app_dir / ".." / "data" / "processed"

# Load unified processed data
df_processed = pd.read_pickle(data_path / "df_processed.pkl")

# Pre-aggregate yearly: avg_temp, avg_uncertainty, data_count, temp_lower, temp_upper
df_yearly = df_processed.groupby(["year", "country"], as_index=False).agg(
    avg_temp=("AvgTemp", "mean"),
    avg_uncertainty=("AvgUncertain", "mean"),
    data_count=("AvgTemp", "count")
)
df_yearly["temp_lower"] = df_yearly["avg_temp"] - df_yearly["avg_uncertainty"]
df_yearly["temp_upper"] = df_yearly["avg_temp"] + df_yearly["avg_uncertainty"]
df_yearly = df_yearly.rename(columns={"country": "Country"})

# Pre-aggregate seasonal: mean temperature per year, country, season
df_seasonal = df_processed.groupby(
    ["year", "country", "season"], as_index=False
)["AvgTemp"].mean()
df_seasonal = df_seasonal.rename(columns={"country": "Country", "AvgTemp": "AverageTemperature"})

# Global UI Configurations
country_choices = sorted(df_yearly["Country"].unique().tolist())
min_year = int(df_yearly["year"].min())
max_year = int(df_yearly["year"].max())
