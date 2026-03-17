# Tests for build_temp_chart() in src/plot.py
# HOW TO RUN (from project root):
#   pytest tests/test_plot.py -v

import altair as alt
import pandas as pd
import pytest
from src.plot import build_temp_chart


# ─────────────────────────────────────────────────────────────────────
# Helper — build a realistic monthly comparison DataFrame
# ─────────────────────────────────────────────────────────────────────

def make_monthly_df(baseline_year: int = 1950, target_year: int = 2000) -> pd.DataFrame:
    """
    Return a 12-row DataFrame that mirrors what monthly_comparison_data()
    produces in app.py.  Columns: Month, {b}_avg, {t}_avg, Change.
    We use simple arithmetic values so tests are easy to reason about.
    """
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    b_col = f"{baseline_year}_avg"
    t_col = f"{target_year}_avg"

    return pd.DataFrame({
        "Month":  months,
        b_col:    [float(i) for i in range(1, 13)],       # 1.0 – 12.0
        t_col:    [float(i) + 0.5 for i in range(1, 13)], # 1.5 – 12.5
        "Change": [0.5] * 12,
    })


# ─────────────────────────────────────────────────────────────────────
# 1.  Empty-data path — must return a valid Altair chart, not crash
# ─────────────────────────────────────────────────────────────────────

def test_build_temp_chart_empty_df_returns_altair_chart():
    """
    Behaviour: passing an empty DataFrame must return an Altair Chart
    object without raising any exception.
    Matters because: app.py calls build_temp_chart with an empty DataFrame
    whenever the year validation fails; a crash here would take down the
    entire dashboard tab.
    """
    result = build_temp_chart(pd.DataFrame(), 0, 0, "", height=280)

    assert isinstance(result, alt.Chart), (
        f"Expected alt.Chart, got {type(result)}"
    )


def test_build_temp_chart_empty_df_does_not_raise():
    """
    Behaviour: the empty-data path must complete cleanly with no exception.
    Matters because: a raised exception in a Shiny render function shows
    an error panel to the user instead of the chart placeholder.
    """
    build_temp_chart(pd.DataFrame(), 0, 0, "Canada", height=280)


def test_build_temp_chart_empty_df_custom_message():
    """
    Behaviour: when data is empty the chart should encode the empty_message
    string so that users see a readable explanation instead of a blank panel.
    Matters because: the default Altair empty chart is just a grey box;
    the custom message tells users *why* there is nothing to show.
    """
    msg = "Invalid year selection."
    result = build_temp_chart(
        pd.DataFrame(), 0, 0, "", height=280, empty_message=msg
    )
    spec = result.to_dict()
    spec_str = str(spec)
    assert msg in spec_str, (
        f"Expected empty_message {msg!r} to appear in chart spec"
    )


# ─────────────────────────────────────────────────────────────────────
# 2.  Valid-data path — chart is returned and contains expected metadata
# ─────────────────────────────────────────────────────────────────────

def test_build_temp_chart_valid_data_returns_altair_object():
    """
    Behaviour: with valid data, build_temp_chart must return an Altair
    object (LayerChart or Chart — both are valid Altair types).
    Matters because: a non-Altair return value would cause render_altair
    in app.py to silently show nothing.
    """
    df = make_monthly_df(1950, 2000)
    result = build_temp_chart(df, 1950, 2000, "Canada", height=280)

    assert hasattr(result, "to_dict"), (
        f"Expected an Altair chart object with to_dict(), got {type(result)}"
    )


def test_build_temp_chart_title_contains_country():
    """
    Behaviour: the chart title spec must contain the country name.
    Matters because: users rely on the chart title to confirm they are
    looking at the right country; a missing or wrong country name is a
    silent data labelling error.
    """
    df = make_monthly_df(1950, 2000)
    result = build_temp_chart(df, 1950, 2000, "Canada", height=280)

    spec_str = str(result.to_dict())
    assert "Canada" in spec_str, (
        "Expected country name 'Canada' to appear in the chart spec"
    )


def test_build_temp_chart_title_contains_both_years():
    """
    Behaviour: the chart subtitle must contain both the baseline and
    target years so users can confirm which years are being compared.
    Matters because: if the year labels are wrong or missing, the chart
    is ambiguous — users cannot tell which line is baseline vs target.
    """
    df = make_monthly_df(1950, 2000)
    result = build_temp_chart(df, 1950, 2000, "Japan", height=280)

    spec_str = str(result.to_dict())
    assert "1950" in spec_str, "Expected baseline year 1950 in chart spec"
    assert "2000" in spec_str, "Expected target year 2000 in chart spec"


def test_build_temp_chart_height_is_respected():
    """
    Behaviour: the height parameter passed in must appear in the chart spec.
    Matters because: the dashboard layout gives the chart card a fixed
    height budget; if the chart ignores the height parameter it will
    overflow its card or be too small.
    """
    df = make_monthly_df(1950, 2000)
    result = build_temp_chart(df, 1950, 2000, "Canada", height=350)

    spec_str = str(result.to_dict())
    assert "350" in spec_str, (
        "Expected height=350 to appear in the Altair chart spec"
    )


# ─────────────────────────────────────────────────────────────────────
# 3.  Edge cases — unusual but valid inputs
# ─────────────────────────────────────────────────────────────────────

def test_build_temp_chart_country_with_spaces():
    """
    Behaviour: a country name containing spaces (e.g. 'United States')
    must not cause any exception or corrupt the chart spec.
    Matters because: many countries in the dataset have multi-word names;
    a string-formatting bug could silently produce wrong column names.
    """
    df = make_monthly_df(1960, 2010)
    result = build_temp_chart(df, 1960, 2010, "United States", height=280)
    assert hasattr(result, "to_dict")


def test_build_temp_chart_single_year_span():
    """
    Behaviour: years that are adjacent (e.g. 1999 vs 2000) must produce
    a valid chart — not a crash or empty output.
    Matters because: the minimum valid year gap is 1; this is the
    tightest real-world comparison a user can make.
    """
    df = make_monthly_df(1999, 2000)
    result = build_temp_chart(df, 1999, 2000, "Canada", height=280)
    assert hasattr(result, "to_dict")


def test_build_temp_chart_negative_temperatures():
    """
    Behaviour: DataFrames with negative temperature values (e.g. Siberia
    in January) must produce a valid chart without crashing.
    Matters because: the y-axis domain is computed dynamically from the
    data; negative values could produce a zero-width domain if the
    padding logic has a bug.
    """
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df = pd.DataFrame({
        "Month":    months,
        "1950_avg": [-20.0 + i for i in range(12)],  # -20 to -9
        "2000_avg": [-19.5 + i for i in range(12)],  # -19.5 to -8.5
        "Change":   [0.5] * 12,
    })

    result = build_temp_chart(df, 1950, 2000, "Russia", height=280)
    assert hasattr(result, "to_dict")
