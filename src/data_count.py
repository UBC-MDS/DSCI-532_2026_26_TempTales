"""
Data count module.
Provide the display text for the average temperature and the number of data used for calculation. 
"""
import pandas as pd


def data_count_prep(df: pd.DataFrame, year: int): 
    year_df = df[df["year"] == year]
    if not year_df.empty: 
        temp = year_df.iloc[0]["avg_temp"]
        uncertainty = year_df.iloc[0]["avg_uncertainty"]
        count = year_df.iloc[0]["data_count"]
        display_text = f"{temp:.1f} ± {uncertainty:.1f} °C"
        sub_text = f"Based on {int(count)} observations"
    else: 
        display_text = "No Data"
        sub_text = f"No records for {year}"
    return display_text, sub_text
