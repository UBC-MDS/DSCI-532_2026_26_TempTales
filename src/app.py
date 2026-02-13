# imports
from pathlib import Path
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shinywidgets import output_widget, render_plotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Path Configurations
app_dir = Path(__file__).parent
data_path = app_dir / ".." / "data" / "raw" / "GlobalLandTemperaturesByCountry.csv"

# Data Pre-Processing
df = pd.read_csv(data_path, index_col="dt", parse_dates=True)
df["year"] = df.index.year
df["month"] = df.index.month

# Data Flitering and Aggregation
df = df[(df["year"] >= 1860)]

df_yearly = df.groupby(["year", "Country"], as_index=False).agg(
    avg_temp=("AverageTemperature", "mean"),
    avg_uncertainty=("AverageTemperatureUncertainty", "mean"),
)
# Confidence Interval
df_yearly["temp_lower"] = df_yearly["avg_temp"] - df_yearly["avg_uncertainty"]
df_yearly["temp_upper"] = df_yearly["avg_temp"] + df_yearly["avg_uncertainty"]

# UI Widgets
country_choices = sorted(df_yearly["Country"].unique().tolist())

min_year = int(df_yearly["year"].min())
max_year = int(df_yearly["year"].max())

# UI Layout
app_ui = ui.page_fluid(
    ui.page_opts(
        title="Climate Change Explorer",
        fillable=True
    ),
    
    ui.layout_columns(
        # Left Column: Controls and Info
        ui.div(
            # 1. Country Selector (Inpout Filter)
            ui.card(
                ui.card_header("Location"),
                ui.input_select(
                    "country",
                    "Select Country",
                    choices=country_choices,
                    selected="Canada" if "Canada" in country_choices else country_choices[0]
                )
            ),
            # 2. Data Counter
            ui.card(
                ui.card_header("Data Points"),
                ui.output_ui("data_count_ui"),
                class_="mb-3"
            ),
            # 3. Historical Event Card
            ui.card(
                ui.card_header("Historical Event"),
                ui.output_ui("event_ui"),
                class_="bg-light"
            ),
            # 4. Seansonal Temperature Card
            ui.card(
                ui.card_header("Seasonal Temperature"),
                ui.output_ui("seasonal_temp_ui"),
                class_="mb-3"
            )
        ),
        
        # Right Column: Dashboard and Visualizations
        ui.div(
            # 1. Year Slider
            ui.card(
                ui.input_slider(
                    "year",
                    "Select Year:",
                    min=min_year,
                    max=max_year,
                    value=2000,
                    sep="",
                    width="100%",
                    animate=True
                ),
                class_="mb-3 p-2"
            ),
            # 2. Temperature Plot
            ui.card(
                ui.card_header("Temperature Over Time"),
                output_widget("temp_plot"),
                height="350px",
                class_="mb-3"
            ),
            # 3. World Heatmap
            ui.card(
                ui.card_header("World Heatmap"),
                output_widget("map_plot"),
                height="400px",
            ),
        ),       
        col_widths=[3, 9]
    )
)

