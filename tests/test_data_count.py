# Tests for data_count_prep() in src/data_count.py
# HOW TO RUN (from project root):
#   pytest tests/test_data_count.py -v

import pandas as pd
import pytest
from src.data_count import data_count_prep


# ─────────────────────────────────────────────────────────────────────
# Helper — build a minimal DataFrame that looks like filtered_global_data
# ─────────────────────────────────────────────────────────────────────

def make_df(year: int, avg_temp: float, avg_uncertainty: float, data_count: int) -> pd.DataFrame:
    """
    Return a single-row DataFrame that mirrors the schema produced by
    filtered_global_data() in app.py.  Column names must match exactly
    because data_count_prep() accesses them by name.
    """
    return pd.DataFrame({
        "year":            [year],
        "avg_temp":        [avg_temp],
        "avg_uncertainty": [avg_uncertainty],
        "data_count":      [float(data_count)],
    })


# ─────────────────────────────────────────────────────────────────────
# 1.  Happy-path: year exists in the DataFrame
# ─────────────────────────────────────────────────────────────────────

def test_data_count_prep_display_text_format():
    """
    Behaviour: when the requested year is present, display_text must
    follow the pattern  "<temp> ± <uncertainty> °C"  (one decimal place).
    Matters because: the value box uses this string verbatim; wrong
    decimal places or missing "±" would look broken to users.
    """
    df = make_df(year=1950, avg_temp=5.678, avg_uncertainty=0.123, data_count=12)

    display_text, _ = data_count_prep(df, 1950)

    # 5.678 rounds to 5.7, 0.123 rounds to 0.1
    assert display_text == "5.7 ± 0.1 °C"


def test_data_count_prep_sub_text_format():
    """
    Behaviour: when the requested year is present, sub_text must say
    "Based on <N> observations" using the exact data_count value.
    Matters because: the sub-text gives users confidence about data
    quality; if the count is missing they cannot judge reliability.
    """
    df = make_df(year=1950, avg_temp=5.0, avg_uncertainty=0.2, data_count=42)

    _, sub_text = data_count_prep(df, 1950)

    assert sub_text == "Based on 42 observations"


def test_data_count_prep_returns_tuple_of_two_strings():
    """
    Behaviour: data_count_prep() must return a 2-tuple of strings.
    Matters because: app.py unpacks exactly two values from the return;
    a changed return signature would cause an immediate runtime crash.
    """
    df = make_df(year=2000, avg_temp=10.0, avg_uncertainty=0.5, data_count=10)

    result = data_count_prep(df, 2000)

    # Must be a tuple (or at least iterable) with exactly 2 items
    assert len(result) == 2
    display_text, sub_text = result
    assert isinstance(display_text, str)
    assert isinstance(sub_text, str)


def test_data_count_prep_negative_temperature():
    """
    Behaviour: negative temperatures (common in cold countries) must
    format correctly — the minus sign must appear in the output.
    Matters because: Canada and Russia have negative avg temps in many
    years; if negatives were silently dropped the card would mislead users.
    """
    df = make_df(year=1990, avg_temp=-12.345, avg_uncertainty=0.456, data_count=7)

    display_text, _ = data_count_prep(df, 1990)

    # -12.345 → -12.3,  0.456 → 0.5
    assert display_text == "-12.3 ± 0.5 °C"


def test_data_count_prep_rounding_edge_case():
    """
    Behaviour: values that land exactly on a rounding boundary (x.x5)
    must still produce a valid formatted string without crashing.
    Matters because: floating-point data from the real dataset can
    produce these boundary values and Python's round() uses
    banker's rounding — this verifies no exception is raised.
    """
    df = make_df(year=1970, avg_temp=5.05, avg_uncertainty=0.05, data_count=3)

    display_text, sub_text = data_count_prep(df, 1970)

    # Just assert we get strings back — the exact rounding value
    # is Python-version dependent, but no crash is the key requirement.
    assert isinstance(display_text, str)
    assert "°C" in display_text


# ─────────────────────────────────────────────────────────────────────
# 2.  Fallback path: year is NOT in the DataFrame
# ─────────────────────────────────────────────────────────────────────

def test_data_count_prep_missing_year_display_text():
    """
    Behaviour: when the requested year has no records, display_text
    must return the string "No Data" (exact match, case-sensitive).
    Matters because: app.py renders this string directly in the
    value-box; an empty string or None would show a blank card.
    """
    # DataFrame contains 1950, but we ask for 2099 which doesn't exist
    df = make_df(year=1950, avg_temp=5.0, avg_uncertainty=0.2, data_count=12)

    display_text, _ = data_count_prep(df, 2099)

    assert display_text == "No Data"


def test_data_count_prep_missing_year_sub_text():
    """
    Behaviour: when the year is missing, sub_text must include the
    requested year number so the user knows which year had no data.
    Matters because: the dashboard may show two value boxes
    (baseline + target); without the year in the message users
    cannot tell which one is missing data.
    """
    df = make_df(year=1950, avg_temp=5.0, avg_uncertainty=0.2, data_count=12)

    _, sub_text = data_count_prep(df, 2099)

    assert "2099" in sub_text


def test_data_count_prep_empty_dataframe():
    """
    Behaviour: an entirely empty DataFrame must return the "No Data"
    fallback without raising an exception.
    Matters because: filtered_global_data() returns an empty DataFrame
    when no records match the selected country + year range.  If
    data_count_prep crashes here, the whole dashboard card breaks.
    """
    # Build an empty DataFrame with the correct column schema
    empty_df = pd.DataFrame(columns=["year", "avg_temp", "avg_uncertainty", "data_count"])

    display_text, sub_text = data_count_prep(empty_df, 1950)

    assert display_text == "No Data"
    assert "1950" in sub_text


# ─────────────────────────────────────────────────────────────────────
# 3.  Multiple rows — correct year is selected
# ─────────────────────────────────────────────────────────────────────

def test_data_count_prep_correct_row_selected():
    """
    Behaviour: when the DataFrame contains multiple years, only the
    row matching the requested year should be used.
    Matters because: filtered_global_data() returns a range of years;
    if data_count_prep accidentally used the wrong row the value box
    would show the temperature for a different year than selected.
    """
    # Two rows — years 1950 and 2000
    df = pd.DataFrame({
        "year":            [1950, 2000],
        "avg_temp":        [3.1,  8.9],
        "avg_uncertainty": [0.2,  0.3],
        "data_count":      [10.0,   20.0],
    })

    display_text, sub_text = data_count_prep(df, 2000)

    # Must use the 2000 row values, not 1950
    assert display_text == "8.9 ± 0.3 °C"
    assert sub_text == "Based on 20 observations"
