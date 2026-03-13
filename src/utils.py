# imports
from pathlib import Path
import pandas as pd
import ibis
from ibis import _

# Path Configurations
app_dir = Path(__file__).parent
data_path = app_dir / ".." / "data" / "processed"

# set up connection ibis w/ DuckDB
# Lazy reference only (data not really loaded yet)
con = ibis.duckdb.connect()
df_processed = con.read_parquet(data_path / "df_processed.parquet")

################### Pre-aggregate yearly w/ ibis expressions
df_yearly = (
    df_processed.group_by(["year", "country"])
    .aggregate(
        avg_temp=_.AvgTemp.mean(),
        avg_uncertainty=_.AvgUncertain.mean(),
        data_count=_.AvgTemp.count()
    )
    .mutate(
        temp_lower=_.avg_temp - _.avg_uncertainty,
        temp_upper=_.avg_temp + _.avg_uncertainty
    )
    .rename({"Country":"country"})
)

################### Pre-aggregate seasonal w/ ibis expressions
df_seasonal = (
    df_processed.group_by(["year", "country", "season"])
    .aggregate(AverageTemperature=_.AvgTemp.mean())
    .rename({"Country": "country", "AverageTemperature": "AvgTemp"})
)


################### Pre-aggregate monthly w/ ibis expressions
df_monthly = (
    df_processed.group_by(["year", "country", "month"])
    .aggregate(AverageTemperature=_.AvgTemp.mean())
    .rename({"Country": "country"})
)

################### Global UI Configurations
################### These needs immediately executed for shiny to set up for UI
country_choices = sorted(df_yearly.select("Country").distinct().execute()["Country"].tolist())
min_year = int(df_yearly.year.min().execute())
max_year = int(df_yearly.year.max().execute())

# # Pre-aggregate yearly: avg_temp, avg_uncertainty, data_count, temp_lower, temp_upper
# df_yearly = df_processed.groupby(["year", "country"], as_index=False).agg(
#     avg_temp=("AvgTemp", "mean"),
#     avg_uncertainty=("AvgUncertain", "mean"),
#     data_count=("AvgTemp", "count")
# )
# df_yearly["temp_lower"] = df_yearly["avg_temp"] - df_yearly["avg_uncertainty"]
# df_yearly["temp_upper"] = df_yearly["avg_temp"] + df_yearly["avg_uncertainty"]
# df_yearly = df_yearly.rename(columns={"country": "Country"})

# # Pre-aggregate seasonal: mean temperature per year, country, season
# df_seasonal = df_processed.groupby(
#     ["year", "country", "season"], as_index=False
# )["AvgTemp"].mean()
# df_seasonal = df_seasonal.rename(columns={"country": "Country", "AvgTemp": "AverageTemperature"})

# # Pre-aggregate monthly: mean temperature per year, country, month (for dual-line comparison)
# df_monthly = df_processed.groupby(
#     ["year", "country", "month"], as_index=False
# )["AvgTemp"].mean()
# df_monthly = df_monthly.rename(columns={"country": "Country"})

# # Global UI Configurations
# country_choices = sorted(df_yearly["Country"].unique().tolist())
# min_year = int(df_yearly["year"].min())
# max_year = int(df_yearly["year"].max())
