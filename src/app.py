# imports
import io
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shinywidgets import render_altair, render_plotly, render_widget
import plotly.graph_objects as go
import pandas as pd

# =====================================
# Import shared data, UI layout, and plot builders
# =====================================
from src.utils import df_yearly, df_seasonal, df_monthly, min_year, max_year
from src.ui import app_ui
from src.plot import build_temp_chart
from src.data_count import data_count_prep


def server(input: Inputs, output: Outputs, session: Session):
    # =============================
    # Reactive Filters
    # =============================
    @reactive.Calc
    def selected_range():
        b = input.baseline_year()
        t = input.target_year()

        if b is None or t is None:
            return None, None, "Enter both years."

        try:
            b, t = int(b), int(t)
        except (TypeError, ValueError):
            return None, None, "Years must be numeric."

        if not (min_year <= b <= max_year):
            return None, None, f"Reference year must be between {min_year} and {max_year}."

        if not (min_year <= t <= max_year):
            return None, None, f"Target year must be between {min_year} and {max_year}."

        if t <= b:
            return None, None, "Target year must be greater than reference year."

        return b, t, None

    @reactive.Calc
    def filtered_yearly_data():
        """Aggregated yearly data for the selected country"""
        return df_yearly[df_yearly["Country"] == input.country()]

    @reactive.Calc
    def filtered_global_data():
        """Global data for the selected year range"""
        b, t, err = selected_range()
        if err:
            return pd.DataFrame()

        data = filtered_yearly_data()
        return data[(data["year"] >= b) & (data["year"] <= t)]

    @reactive.Calc
    def monthly_comparison_data():
        """Monthly avg temperature comparison for baseline vs target year (avg only)."""
        b, t, err = selected_range()
        if err:
            return pd.DataFrame()

        country = input.country()
        df = df_monthly[(df_monthly["Country"] == country) &
                        (df_monthly["year"].isin([b, t]))]
        if df.empty:
            return pd.DataFrame()

        month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        base = df[df["year"] == b][["month", "AvgTemp"]].rename(
            columns={"AvgTemp": f"{b}_avg"})
        target = df[df["year"] == t][["month", "AvgTemp"]].rename(
            columns={"AvgTemp": f"{t}_avg"})
        merged = base.merge(target, on="month")
        merged["Change"] = merged[f"{t}_avg"] - merged[f"{b}_avg"]
        merged["Month"] = merged["month"].map(lambda m: month_labels[m - 1])
        return merged[["Month", f"{b}_avg", f"{t}_avg", "Change"]].round(2)

    # =============================
    # Year Validation UI
    # =============================
    @render.ui
    def year_validation_ui():
        _, _, err = selected_range()
        if err:
            return ui.div(err, class_="text-danger")
        return ui.div("Year range is valid.", class_="text-success")

    # =============================
    # Data Count UI
    # =============================
    @render.ui
    def data_count_ui():
        """Render the data count UI element"""
        data = filtered_global_data()

        b, t, err = selected_range()
        if err:
            return

        baseline_display_text, baseline_sub_text = data_count_prep(data, b)
        target_display_text, target_sub_text = data_count_prep(data, t)

        return ui.div(
            ui.h6(f"Year {b}"),
            ui.h5(baseline_display_text, class_="text-primary"),
            ui.p(baseline_sub_text, class_="text-muted mb-0 small"), 
            ui.h6(f"Year {t}"),
            ui.h5(target_display_text, class_="text-primary"),
            ui.p(target_sub_text, class_="text-muted mb-0 small") 
        )
    
    # =============================
    # Historical Event UI
    # =============================
    @render.ui
    def event_ui():
        """Render historical context based on year range"""

        # Guard against invalid year inputs
        b, t, err = selected_range()
        if err:
            return

        # Event Place holder
        events = [
            (1860, 1900, "Post-Industrial Revolution"),
            (1914, 1918, "World War I"),
            (1939, 1945, "World War II"),
            (1987, 1989, "Montreal Protocol Signed"),
            (1997, 2012, "Kyoto Protocol Era"),
        ]

        text = "Historical Data View"
        list_events = []

        for ev_s, ev_e, desc in events:
            if b <= ev_s <= t or b <= ev_e <= t:
                text = f"{ev_s}-{ev_e}: {desc}"
                list_events.append(ui.tags.li(text))

        if not list_events:
            return ui.p("No major recorded events in selected range.",
                        class_="text-muted small")

        return ui.tags.ul(
            *list_events,
            class_="text-muted small mb-0"
        )

    # =============================
    # Seasonal Temperature UI
    # =============================
    @render.ui
    def seasonal_temp_ui():
        """Render the seasonal temperature UI element"""

        # Guard against invalid year inputs
        b, t, err = selected_range()
        if err:
            return

        mask = (df_seasonal["Country"] == input.country()) & (
            df_seasonal["year"] == t)
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
    # Title Placeholder (Value Box)
    # =============================
    @render.ui
    def title_placeholder():
        # Guard against invalid year inputs
        b, t, err = selected_range()
        if err:
            return ...

        return f"{b} to {t}"

    # =============================
    # Data Table (Monthly Comparison)
    # =============================
    def _table_styles(df: pd.DataFrame):
        """Red (warmer) / blue (cooler) color scheme for Change column."""
        if df.empty or "Change" not in df.columns:
            return []
        change_col = df.columns.get_loc("Change")
        styles = []
        for i, val in enumerate(df["Change"]):
            if pd.isna(val):
                continue
            if val > 0:
                styles.append({
                    "rows": [i],
                    "cols": [change_col],
                    "style": {"color": "#c0392b", "backgroundColor": "rgba(231, 76, 60, 0.15)"}
                })
            elif val < 0:
                styles.append({
                    "rows": [i],
                    "cols": [change_col],
                    "style": {"color": "#2980b9", "backgroundColor": "rgba(52, 152, 219, 0.15)"}
                })
        return styles

    @render.data_frame
    def data_table():
        """Table of monthly avg temperature comparison; supports data_view() for export."""
        data = monthly_comparison_data()
        if data.empty:
            return render.DataGrid(pd.DataFrame(), selection_mode="rows")
        return render.DataGrid(data, selection_mode="rows", styles=_table_styles)

    @render.download(filename=lambda: _csv_download_filename())
    def download_table_csv():
        """Export monthly comparison data as CSV."""
        data = monthly_comparison_data()
        if data.empty:
            yield ""
            return
        buf = io.StringIO()
        data.to_csv(buf, index=False)
        yield buf.getvalue()

    def _csv_download_filename():
        """Generate download filename from current filters."""
        b, t, err = selected_range()
        if err:
            return "temperature_data.csv"
        country = input.country().replace(" ", "_")
        return f"temperature_{country}_{b}_{t}.csv"

    # =============================
    # Temperature Plot (Monthly Dual-Line, Altair)
    # =============================
    @render_altair
    def temp_plot():
        """Render monthly dual-line comparison: baseline vs target year avg temps."""
        data = monthly_comparison_data()
        b, t, err = selected_range()
        if err:
            return build_temp_chart(pd.DataFrame(), 0, 0, "", height=300)
        return build_temp_chart(
            data, b, t, input.country(), height=300
        )

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
        b, t, err = selected_range()
        if err:
            return
        df_curr = df_yearly[df_yearly["year"] == t]
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
