# imports
from pathlib import Path
import pandas as pd

# Path Configurations
app_dir = Path(__file__).parent
data_path = app_dir / ".." / "data" / "processed"

# Data Loading
df_yearly = pd.read_pickle(data_path / "df_yearly.pkl")
df_seasonal = pd.read_pickle(data_path / "df_seasonal.pkl")

# Global UI Configurations
country_choices = sorted(df_yearly["Country"].unique().tolist())
min_year = int(df_yearly["year"].min())
max_year = int(df_yearly["year"].max())
