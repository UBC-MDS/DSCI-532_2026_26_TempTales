# imports
import io
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shinywidgets import render_altair, render_plotly, render_widget
import plotly.graph_objects as go
import altair as alt
import pandas as pd

from src.chat import qc

# =====================================
# Import shared data, UI layout, and plot builders
# =====================================
from src.utils import df_yearly, df_seasonal, df_monthly, min_year, max_year
from src.ui import app_ui
from src.plot import build_temp_chart, build_yearly_plot, build_diff_plot
from src.data_count import data_count_prep
from src.map import build_base_map, apply_country_highlight


def _diverging_styles(cells: list[tuple[int, int, float]], alpha: float = 0.65) -> list[dict]:
    """
    Generate DataGrid styles for a diverging color scale (0=neutral, negative=blue, positive=red).
    cells: list of (row_idx, col_idx, value)
    alpha: background opacity (higher = deeper colors)
    """
    if not cells:
        return []

    vals = [v for _, _, v in cells]
    low = min(min(vals), 0)
    high = max(max(vals), 0)
    eps = 1e-9
    if high - low < eps:
        high = low + eps

    WHITE = (255, 255, 255)
    BLUE = (41, 128, 185)
    RED = (231, 76, 60)

    def _interp(t: float, c0: tuple, c1: tuple) -> str:
        r = int(c0[0] + t * (c1[0] - c0[0]))
        g = int(c0[1] + t * (c1[1] - c0[1]))
        b = int(c0[2] + t * (c1[2] - c0[2]))
        return f"rgba({r},{g},{b},{alpha})"

    styles = []
    for row_idx, col_idx, val_num in cells:
        if val_num < 0:
            t = val_num / low if low < -eps else 0
            t = max(0, min(1, t))
            bg = _interp(t, WHITE, BLUE)
        elif val_num > 0:
            t = val_num / high if high > eps else 0
            t = max(0, min(1, t))
            bg = _interp(t, WHITE, RED)
        else:
            bg = "rgba(248,249,250,0.5)"

        styles.append({
            "rows": [row_idx],
            "cols": [col_idx],
            "style": {"color": "#333", "backgroundColor": bg}
        })
    return styles


def server(input: Inputs, output: Outputs, session: Session):

    # =====================================
    # Main Dashboard Tab
    # =====================================

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
        """Monthly avg temperature comparison for baseline vs target year (long format for chart)."""
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

    @reactive.Calc
    def monthly_comparison_wide():
        """Monthly comparison in wide format: 3 rows x 12 columns (for data table)."""
        data = monthly_comparison_data()
        if data.empty:
            return pd.DataFrame()

        b, t, err = selected_range()
        if err:
            return pd.DataFrame()

        base_col = f"{b}_avg"
        target_col = f"{t}_avg"
        month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        baseline_vals = data[base_col].values
        target_vals = data[target_col].values
        change_vals = data["Change"].values

        row_labels = ["Baseline (°C)", "Target (°C)", "Change (°C)"]
        df_wide = pd.DataFrame(
            {
                "Metric": row_labels,
                **{month_labels[i]: [
                    round(baseline_vals[i], 2),
                    round(target_vals[i], 2),
                    round(change_vals[i], 2)
                ] for i in range(12)}
            }
        )
        return df_wide

    # =============================
    # Year Validation UI
    # =============================
    @render.ui
    def year_validation_ui():
        _, _, err = selected_range()
        if err:
            return ui.div(err, class_="text-danger")
        return ui.div("Year range is valid.", class_="text-success")

    # Data Count UI
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

    # Seasonal Temperature UI
    # =============================
    @render.data_frame
    def seasonal_temp_ui():
        """Render a table comparing seasonal temperatures for baseline vs target year."""

        b, t, err = selected_range()
        if err:
            return render.DataGrid(pd.DataFrame({"Message": ["Invalid year selection"]}))

        country = input.country()
        df_b = df_seasonal[(df_seasonal["Country"] == country) & (df_seasonal["year"] == b)]
        df_t = df_seasonal[(df_seasonal["Country"] == country) & (df_seasonal["year"] == t)]

        seasons = ["Spring", "Summer", "Fall", "Winter"]
        rows = []

        for season in seasons:
            val_b = df_b[df_b["season"] == season]["AverageTemperature"]
            val_t = df_t[df_t["season"] == season]["AverageTemperature"]

            temp_b = round(val_b.iloc[0], 1) if not val_b.empty else None
            temp_t = round(val_t.iloc[0], 1) if not val_t.empty else None
            change = None
            if temp_b is not None and temp_t is not None:
                change = round(temp_t - temp_b, 1)

            rows.append({
                "Season": season,
                str(b): temp_b if temp_b is not None else "N/A",
                str(t): temp_t if temp_t is not None else "N/A",
                "Change": change
            })

        df_table = pd.DataFrame(rows)

        # Diverging gradient for Change column (reuse shared logic)
        cells = []
        if "Change" in df_table.columns:
            change_col = df_table.columns.get_loc("Change")
            for i, val in enumerate(df_table["Change"]):
                if not pd.isna(val):
                    try:
                        cells.append((i, change_col, float(val)))
                    except (ValueError, TypeError):
                        pass
        styles = _diverging_styles(cells)
        return render.DataGrid(df_table, selection_mode="none", styles=styles)

    # =============================
    # Title UI
    # =============================
    @render.ui
    def title_placeholder():
        b, t, err = selected_range()
        if err:
            return ui.div("Invalid year selection", class_="text-danger fw-bold")

        country = input.country()

        # Compact horizontal title line (navbar-brand styling)
        title_text = f"TempTales — {country}: {b} vs {t} (Temperature Comparison)"

        return ui.span(
            title_text,
            class_="navbar-brand fw-bold text-dark me-2"
        )

    # =============================
    # Data Table (Monthly Comparison)
    # =============================
    def _table_styles_wide(df: pd.DataFrame):
        """Diverging gradient for Change row (row 2): 0=neutral, negative=blue, positive=red."""
        if df.empty or df.shape[0] < 3:
            return []
        row_idx = 2
        cells = []
        for col_idx in range(1, df.shape[1]):
            try:
                val = df.iloc[row_idx, col_idx]
            except (IndexError, KeyError):
                continue
            if pd.isna(val):
                continue
            try:
                cells.append((row_idx, col_idx, float(val)))
            except (ValueError, TypeError):
                continue
        return _diverging_styles(cells)

    @render.data_frame
    def data_table():
        """Table of monthly comparison in wide format (3 rows x 12 columns)."""
        data = monthly_comparison_wide()
        if data.empty:
            return render.DataGrid(pd.DataFrame(), selection_mode="none")
        return render.DataGrid(data, selection_mode="none", styles=_table_styles_wide, height="auto")

    @render.download(filename=lambda: _csv_download_filename())
    def download_table_csv():
        """Export monthly comparison data (wide format) as CSV."""
        data = monthly_comparison_wide()
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
            return build_temp_chart(pd.DataFrame(), 0, 0, "", height=280)
        return build_temp_chart(
            data, b, t, input.country(), height=280
        )
    # =============================
    # World Heatmap
    # =============================
    
    all_countries = sorted(df_yearly["Country"].unique())
    initial_map = build_base_map(all_countries)

    def _map_click(trace, points, state):
        if points.point_inds:
            idx = points.point_inds[0]
            country = all_countries[idx]
            ui.update_select("country", selected=country, session=session)
            
    initial_map.data[0].on_click(_map_click)
    
    @render.ui
    def map_card_header():
        b, t, err = selected_range()
        if err:
            return ui.span("World Heatmap")
        country = input.country()
        return ui.span(f"World Heatmap — {country}: {b} vs {t}")
    
    @render_widget
    def map_plot():
        """Render the global choropleth map for the selected year"""
        initial_map.update_layout(autosize=True)
        return initial_map

    @reactive.Effect
    def update_map_data():
        b, t, err = selected_range()
        if err:
            return

        selected_country = input.country()

        # --- update temperature values (diff = target - baseline) ---
        df_b = df_yearly[df_yearly["year"] == b][["Country", "avg_temp"]].rename(columns={"avg_temp": "temp_b"})
        df_t = df_yearly[df_yearly["year"] == t][["Country", "avg_temp"]].rename(columns={"avg_temp": "temp_t"})
        merged = df_b.merge(df_t, on="Country", how="outer")
        merged["diff"] = merged["temp_t"] - merged["temp_b"]
        df_aligned = merged.set_index("Country").reindex(all_countries)
        new_z = df_aligned["diff"].values

        initial_map.data[0].z = new_z

        # --- highlight selected country ---
        apply_country_highlight(initial_map, all_countries, selected_country)

        # --- zoom select country ---
        if selected_country:
            initial_map.update_geos(
                projection=dict(type="equirectangular", scale=2.0),
                fitbounds="locations",
            )
        else:
            initial_map.update_geos(
                projection=dict(type="natural earth"),
                fitbounds="locations",
            )

    # =====================================
    # AI Tab
    # =====================================

    # Attach QueryChat server to the app
    qc_vals = qc.server()

    # =====================================
    # Reactive Calcs for DF
    # =====================================

    @reactive.Calc
    def ai_filtered_raw_data():
        df = qc_vals.df()
        print("AI RETURN TYPE:", type(df))
        if df is None:
            return pd.DataFrame()
        if isinstance(df, pd.DataFrame):
            return df
        return pd.DataFrame(df)

    @render.data_frame
    def ai_data_frame():
        df = ai_filtered_raw_data()
        if df.empty:
            return pd.DataFrame({"Message": ["Ask the AI a question to see results"]})
        return df

    @render.download(filename="ai_filtered_data.csv")
    def download_ai_table_csv():
        data = ai_filtered_raw_data()
        if data.empty:
            yield ""
            return
        buf = io.StringIO()
        data.to_csv(buf, index=False)
        yield buf.getvalue()

    # =====================================
    # AI Plots
    # =====================================

    @reactive.Calc
    def ai_yearly_prep():
        df = ai_filtered_raw_data()
        if df.empty:
            return pd.DataFrame(columns=["Country", "year", "AvgTemp", "AvgTemp_centered"])
        df_yearly = df.groupby(["Country", "year"], 
                               as_index=False)["AvgTemp"].mean()
        df_yearly["AvgTemp_centered"] = df_yearly.groupby("Country")["AvgTemp"].transform(lambda x: x - x.mean())

        # deterministic country cap (instead of row cap)
        max_countries = 20
        country_order = sorted(df_yearly["Country"].unique())
        keep_countries = country_order[:max_countries]
        df_yearly = df_yearly[df_yearly["Country"].isin(keep_countries)]

        return df_yearly


    @render_widget
    def ai_centred_ts_plot():
        df = ai_yearly_prep()
        # Always return a valid plot even if empty
        if df.empty:
            return alt.Chart(pd.DataFrame(columns=["year", "AvgTemp_centered", "Country"])).mark_line()
        plot = build_yearly_plot(df)
        return plot

    @reactive.Calc
    def ai_monthly_diff_prep():
        df = ai_filtered_raw_data()

        if df.empty:
            return None  # no user input yet

        max_countries = 20
        country_order = sorted(df["Country"].unique())
        keep_countries = country_order[:max_countries]
        df = df[df["Country"].isin(keep_countries)]

        # Get years in the filtered df
        years = sorted(df["year"].unique())
        if len(years) == 1:
            year1 = years[0]
            year2 = df["year"].max()  # latest year in dataset
        else:
            year1, year2 = years[0], years[-2]  # min & max years

        # Filter for the two years only
        df_filtered = df[df["year"].isin([year1, year2])]

        # Pivot to have one column per year for monthly comparison
        df_pivot = df_filtered.pivot_table(
            index=["Country", "month"],
            columns="year",
            values="AvgTemp"
        ).reset_index()

        # Rename columns for clarity
        df_pivot = df_pivot.rename(columns={year1: "year1_temp", year2: "year2_temp"})

        # Compute difference
        df_pivot["AvgTemp_diff"] = df_pivot["year2_temp"] - df_pivot["year1_temp"]

        # Keep only needed columns
        return df_pivot[["Country", "month", "AvgTemp_diff"]]

    @render_widget
    def ai_monthly_change_plot():
        df = ai_monthly_diff_prep()
        if df is None or df.empty:
            return alt.Chart(pd.DataFrame(columns=["month", "AvgTemp_diff", "Country"])).mark_line()
        
        plot = build_diff_plot(df)
        return plot
    

app = App(app_ui, server)
