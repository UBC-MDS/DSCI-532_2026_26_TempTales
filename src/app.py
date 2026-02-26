# imports
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shinywidgets import render_plotly, render_widget
import plotly.graph_objects as go

# =====================================
# Import shared data and UI layout
# =====================================
from utils import df_yearly, df_seasonal
from ui import app_ui


def server(input: Inputs, output: Outputs, session: Session):
    # =============================
    # Reactive Filters
    # =============================
    @reactive.Calc
    def filtered_yearly_data():
        """Aggregated yearly data for the selected country"""
        return df_yearly[df_yearly["Country"] == input.country()]

    @reactive.Calc
    def filtered_global_data():
        """Global data for the selected year"""
        return df_yearly[df_yearly["year"] == input.year()]

    # =============================
    # Data Count UI
    # =============================
    @render.ui
    def data_count_ui():
        """Render the data count UI element"""
        data = filtered_yearly_data()
        curr_year_data = data[data["year"] == input.year()]

        if not curr_year_data.empty:
            temp = curr_year_data.iloc[0]["avg_temp"]
            uncertainty = curr_year_data.iloc[0]["avg_uncertainty"]
            count = curr_year_data.iloc[0]["data_count"]

            display_text = f"{temp:.1f} ± {uncertainty:.1f} °C"
            sub_text = f"Based on {count} observations for {input.year()}"
        else:
            display_text = "No Data"
            sub_text = f"No records for {input.year()}"

        return ui.div(
            ui.h2(display_text, class_="text-primary"),
            ui.p(sub_text, class_="text-muted mb-0")
        )

    # =============================
    # Historical Event UI
    # =============================
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

    # =============================
    # Seasonal Temperature UI
    # =============================
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

    # =============================
    # Temperature Plot
    # =============================
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

    # =============================
    # World Heatmap
    # =============================
    all_countries = sorted(df_yearly["Country"].unique())
    empty_z = [None] * len(all_countries)

    initial_map = go.FigureWidget(data=go.Choropleth(
        locations=all_countries,
        locationmode='country names',
        z=empty_z,
        colorscale='RdBu_r',
        zmin=-20, zmax=30,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title="Temp (°C)"
    ))

    initial_map.update_layout(
        geo=dict(
            showframe=False, showcoastlines=True,
            projection_type='robinson',
            showland=True, landcolor="lightgray",
            showocean=True, oceancolor="lightblue"
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )

    @render_widget
    def map_plot():
        """Render the global choropleth map for the selected year"""
        return initial_map

    @reactive.Effect
    def update_map_data():
        current_year = input.year()
        df_curr = df_yearly[df_yearly["year"] == current_year]
        df_curr_indexed = df_curr.set_index("Country")

        df_aligned = df_curr_indexed.reindex(all_countries)

        new_z = df_aligned["avg_temp"].values

        initial_map.data[0].z = new_z

        if input.map_projection() != initial_map.layout.geo.projection.type:
            initial_map.layout.geo.projection.type = input.map_projection()


# =============================
# Initialize the application
# =============================
app = App(app_ui, server)
