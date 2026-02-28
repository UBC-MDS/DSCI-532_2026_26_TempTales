"""
Temperature plot module.
Builds the monthly dual-line comparison chart (Altair).
"""
import altair as alt
import pandas as pd


def build_temp_chart(
    data: pd.DataFrame,
    baseline_year: int,
    target_year: int,
    country: str,
    height: int = 300
) -> alt.Chart:
    """
    Build the monthly dual-line temperature overlay chart.

    Args:
        data: DataFrame with Month, {b}_avg, {t}_avg columns (rounded)
        baseline_year: Reference year
        target_year: Target/comparison year
        country: Country name for subtitle
        height: Chart height in pixels

    Returns:
        Altair Chart (or empty chart if data is empty)
    """
    if data.empty:
        empty_df = pd.DataFrame({"Month": [], "Temperature": [], "Year": []})
        return alt.Chart(empty_df).mark_line().encode(x="Month", y="Temperature")

    b, t = baseline_year, target_year
    base_col = f"{b}_avg"
    target_col = f"{t}_avg"

    chart_data = pd.concat([
        data[["Month", base_col]].rename(
            columns={base_col: "Temperature"}).assign(Year=str(b)),
        data[["Month", target_col]].rename(
            columns={target_col: "Temperature"}).assign(Year=str(t))
    ], ignore_index=True)
    chart_data["month_num"] = list(range(1, 13)) * 2

    tooltip_data = data[["Month", base_col, target_col]].copy()
    tooltip_data = tooltip_data.rename(columns={
        base_col: str(b), target_col: str(t)
    })
    tooltip_data["month_num"] = range(1, 13)

    nearest = alt.selection_point(
        nearest=True, on="pointerover", fields=["month_num"], empty=False
    )
    month_axis = alt.Axis(
        title="Month",
        values=list(range(1, 13)),
        labelExpr="['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][datum.value-1]",
        labelAngle=-45,
        labelPadding=8
    )
    month_scale = alt.Scale(domain=[0.5, 12.5])

    line_chart = (
        alt.Chart(chart_data)
        .mark_line(
            interpolate="monotone",
            strokeWidth=2,
            point=alt.OverlayMarkDef(size=60, filled=True)
        )
        .encode(
            x=alt.X("month_num:Q", axis=month_axis,
                    scale=month_scale, title="Month"),
            y=alt.Y("Temperature:Q", title="Temperature (°C)"),
            color=alt.Color(
                "Year:N",
                scale=alt.Scale(range=["#2C7A7B", "#38B2AC"]),
                legend=alt.Legend(
                    title=None,
                    orient="right",
                    direction="vertical"
                )
            )
        )
    )

    selectors = (
        alt.Chart(tooltip_data)
        .mark_point(opacity=0, size=200)
        .encode(
            x=alt.X("month_num:Q", scale=month_scale),
            y=alt.Y(str(b), type="quantitative"),
            tooltip=[
                alt.Tooltip("Month:N", title="Month"),
                alt.Tooltip(str(b), type="quantitative",
                            format=".2f", title=f"{b}"),
                alt.Tooltip(str(t), type="quantitative",
                            format=".2f", title=f"{t}")
            ]
        )
        .add_params(nearest)
    )

    rules = (
        alt.Chart(tooltip_data)
        .mark_rule(color="gray", strokeWidth=1, strokeDash=[4, 2])
        .encode(x=alt.X("month_num:Q", scale=month_scale))
        .transform_filter(nearest)
    )

    chart = (
        alt.layer(line_chart, selectors, rules)
        .properties(
            title=alt.TitleParams(
                text="Temperature Overlay Comparison",
                subtitle=f"Monthly average temperatures for {country} ({b} vs {t})",
                fontSize=14,
                subtitleFontSize=12
            ),
            height=height
        )
        .configure_axis(grid=True, gridOpacity=0.3)
        .configure_view(strokeWidth=0)
        .configure_legend(orient="right", direction="vertical", padding=4, symbolSize=40)
    )
    return chart
