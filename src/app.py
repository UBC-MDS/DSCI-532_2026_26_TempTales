# imports
# import numpy as np
from pathlib import Path
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shinywidgets import output_widget, render_plotly
import plotly.graph_objects as go
import pandas as pd

# Path Configurations
app_dir = Path(__file__).parent
data_path = app_dir / ".." / "data" / "processed"

# Data Loading
df_yearly = pd.read_pickle(data_path / "df_yearly.pkl")
df_seasonal = pd.read_pickle(data_path / "df_seasonal.pkl")

country_choices = sorted(df_yearly["Country"].unique().tolist())
min_year = int(df_yearly["year"].min())
max_year = int(df_yearly["year"].max())

# UI Layout
app_ui = ui.page_fillable(
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
                    value=1950,
                    sep="",
                    width="100%",
                    # Set animate=True to enable animation
                    animate=True
                ),
                class_="mb-3 p-2"
            ),
            # 2. Temperature Plot
            ui.card(
                ui.card_header("Temperature Over Time"),
                output_widget("temp_plot"),
                height="200px",
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

# Server Logic


def server(input: Inputs, output: Outputs, session: Session):
    # Reactive Filters
    @reactive.Calc
    def filtered_yearly_data():
        """Aggregated yearly data for the selected country"""
        return df_yearly[df_yearly["Country"] == input.country()]

    @reactive.Calc
    def filtered_global_data():
        """Global data for the selected year"""
        return df_yearly[df_yearly["year"] == input.year()]

    # Data Count UI
    @render.ui
    def data_count_ui():
        """Render the data count UI element"""
        data = filtered_yearly_data()
        curr_year_data = data[data["year"] == input.year()]

        if not curr_year_data.empty:
            temp = curr_year_data.iloc[0]["avg_temp"]
            uncertainty = curr_year_data.iloc[0]["avg_uncertainty"]
            count = curr_year_data.iloc[0]["data_coount"]
            
            display_text = f"{temp:.1f} ± {uncertainty:.1f} °C"
            sub_text = f"Based on {count} observations for {input.year()}"
        else:
            display_text = "No Data"
            sub_text = f"No records for {input.year()}"

        return ui.div(
            ui.h2(display_text, class_="text-primary"),
            ui.p(sub_text, class_="text-muted mb-0")
        )

    # Historical Event UI
    @render.ui
    def event_ui():
        """Render historical context based on year range"""
        year = input.year()
        # Event Place holder
        events = [
            (1860, 1900, "Post-Industrial Revolution"),
            (1914, 1918, "World War I"),
            (1939, 1945, "World War II"),
            (1987, 1989, "Montreal Protocol Signed"),
            (1997, 2012, "Kyoto Protocol Era"),
        ]

        text = "Historical Data View"
        for start, end, desc in events:
            if start <= year <= end:
                text = f"{desc} ({start}-{end})"
                break

        return ui.p(f"{year}: {text}", class_="fw-bold")

    # Seasonal Temperature UI
    @render.ui
    def seasonal_temp_ui():
        """Render the seasonal temperature UI element"""
        mask = (df_seasonal["Country"] == input.country()) & (
            df_seasonal["year"] == input.year())
        curr_data = df_seasonal[mask]

        if curr_data.empty:
            return ui.p("Seasonal data not available.")

        rows = []
        for season in ["Spring", "Summer", "Fall", "Winter"]:
            row = curr_data[curr_data["season"] == season]
            if not row.empty:
                val = row.iloc[0]["AverageTemperature"]
                val_str = f"{val:.1f}°C"
            else:
                val_str = "N/A"

            rows.append(ui.div(
                ui.span(season, class_="fw-bold"),
                ui.span(val_str, class_="float-end"),
                class_="border-bottom py-1"
            ))

        return ui.div(*rows)

    # Temperature Plot
    @render_plotly
    def temp_plot():
        """Render the main trend line with uncertainty bands"""
        data = filtered_yearly_data()
        if data.empty:
            return go.Figure()

        fig = go.Figure()

        # Uncertainty Band (Transparent Upper + Filled Lower)
        fig.add_trace(go.Scatter(
            x=data["year"], y=data["temp_upper"],
            mode='lines', line=dict(width=0),
            showlegend=False, hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=data["year"], y=data["temp_lower"],
            mode='lines', line=dict(width=0),
            fill='tonexty', fillcolor='rgba(68, 68, 68, 0.2)',
            name='Uncertainty', hoverinfo='skip'
        ))

        # Mean Temperature Line
        fig.add_trace(go.Scatter(
            x=data["year"], y=data["avg_temp"],
            mode='lines', name='Avg Temp',
            line=dict(color='firebrick', width=2)
        ))

        # Current Year Marker
        curr = data[data["year"] == input.year()]
        if not curr.empty:
            fig.add_trace(go.Scatter(
                x=curr["year"], y=curr["avg_temp"],
                mode='markers', marker=dict(
                    color='black', size=6, opacity=0.8
                ),
                showlegend=False
            ))

        fig.update_layout(
            title=f"Temperature History: {input.country()}",
            xaxis_title="Year", yaxis_title="Temperature (°C)",
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode="x unified",
            legend=dict(
                orientation="v", 
                y=1,
                x=1.02,
                yanchor="top", 
                xanchor="left"
            )
        )
        return fig

    # World Heatmap
    @render_plotly
    def map_plot():
        """Render the global choropleth map for the selected year"""
        data = filtered_global_data()

        fig = go.Figure(data=go.Choropleth(
            locations=data['Country'],
            locationmode='country names',
            z=data['avg_temp'],
            #text=data['Country'],
            colorscale='RdBu_r',
            zmin=-20, zmax=30,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_title="Temp (°C)"
        ))

        fig.update_layout(
            geo=dict(
                showframe=False, 
                showcoastlines=True,
                projection_type='robinson',
                showland=True, landcolor="lightgray"
            ),
            margin=dict(l=0, r=0, t=0, b=0),
        )
        return fig


app = App(app_ui, server)
