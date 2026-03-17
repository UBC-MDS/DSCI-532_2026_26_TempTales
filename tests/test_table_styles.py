# Tests for table_styles_wide() and diverging_styles() in src/table_styles.py

import math
import pandas as pd
import pytest
from src.table_styles import diverging_styles, table_styles_wide


# ─────────────────────────────────────────────────────────────────────
# Helper — build a minimal wide-format DataFrame
# ─────────────────────────────────────────────────────────────────────

def make_wide_df(change_values: list) -> pd.DataFrame:
    """
    Build a 3-row × (1 + N column) DataFrame that mirrors what
    monthly_comparison_wide() returns in app.py.

    Row 0 = Baseline (°C)
    Row 1 = Target   (°C)
    Row 2 = Change   (°C)   ← the only row that gets colour styling

    change_values: list of 12 floats for the Change row.
    Baseline and Target rows are filled with dummy 0.0 values —
    table_styles_wide() only reads row 2 so they don't matter.
    """
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    assert len(change_values) == 12, "Need exactly 12 change values (one per month)"

    return pd.DataFrame(
        {
            "Metric": ["Baseline (°C)", "Target (°C)", "Change (°C)"],
            **{months[i]: [0.0, 0.0, change_values[i]] for i in range(12)}
        }
    )


# ─────────────────────────────────────────────────────────────────────
# 1.  table_styles_wide — guard rails (empty / too-few rows)
# ─────────────────────────────────────────────────────────────────────

def test_table_styles_wide_empty_df_returns_empty_list():
    """
    Behaviour: an empty DataFrame must return [] without crashing.
    Matters because: data_table() can call _table_styles_wide with an
    empty DataFrame when no valid year range is selected; a crash here
    would break the entire dashboard tab.
    """
    result = table_styles_wide(pd.DataFrame())
    assert result == []


def test_table_styles_wide_too_few_rows_returns_empty_list():
    """
    Behaviour: a DataFrame with fewer than 3 rows must return [].
    Matters because: row index 2 is hardcoded as the Change row;
    accessing it on a 1- or 2-row DataFrame would raise an IndexError.
    The guard must prevent that.
    """
    # Only one row — no Change row exists
    df = pd.DataFrame({"Metric": ["Baseline"], "Jan": [5.0]})
    result = table_styles_wide(df)
    assert result == []


# ─────────────────────────────────────────────────────────────────────
# 2.  table_styles_wide — colour direction
# ─────────────────────────────────────────────────────────────────────

def test_table_styles_wide_positive_change_has_red_background():
    """
    Behaviour: a positive Change value (warming) must produce a style
    entry whose backgroundColor contains the red channel values (231).
    Matters because: the whole point of the colour coding is that users
    immediately see warming = red.  If red were swapped for blue the
    dashboard would be actively misleading.
    """
    # All months have a positive change of +1.0 °C
    df = make_wide_df([1.0] * 12)
    styles = table_styles_wide(df)

    assert len(styles) > 0, "Expected at least one style entry for positive changes"

    # Every style entry must reference row 2 (the Change row)
    for entry in styles:
        assert entry["rows"] == [2]

    # The background colour for a warm value must contain red components
    # diverging_styles interpolates toward (231, 76, 60) for positives
    first_bg = styles[0]["style"]["backgroundColor"]
    assert "231" in first_bg, (
        f"Expected red channel (231) in background for warming, got: {first_bg}"
    )


def test_table_styles_wide_negative_change_has_blue_background():
    """
    Behaviour: a negative Change value (cooling) must produce a style
    entry whose backgroundColor contains the blue channel values (185).
    Matters because: cooling = blue is the visual convention; wrong
    colours would confuse every user reading the table.
    """
    # All months have a negative change of -1.0 °C
    df = make_wide_df([-1.0] * 12)
    styles = table_styles_wide(df)

    assert len(styles) > 0, "Expected at least one style entry for negative changes"

    # diverging_styles interpolates toward (41, 128, 185) for negatives
    first_bg = styles[0]["style"]["backgroundColor"]
    assert "185" in first_bg, (
        f"Expected blue channel (185) in background for cooling, got: {first_bg}"
    )


def test_table_styles_wide_zero_change_gets_neutral_background():
    """
    Behaviour: a Change value of exactly 0.0 must produce the neutral
    grey background "rgba(248,249,250,0.5)" — not red or blue.
    Matters because: zero means no change; colouring it red or blue
    would incorrectly imply a temperature shift.
    """
    df = make_wide_df([0.0] * 12)
    styles = table_styles_wide(df)

    # Zero values still get a style entry (neutral)
    assert len(styles) > 0

    for entry in styles:
        bg = entry["style"]["backgroundColor"]
        assert bg == "rgba(248,249,250,0.5)", (
            f"Expected neutral grey for zero change, got: {bg}"
        )


def test_table_styles_wide_mixed_changes_correct_count():
    """
    Behaviour: a mix of positive, negative, and zero changes must
    produce exactly one style entry per non-NaN column.
    Matters because: missing entries mean some cells are unstyled,
    breaking the visual completeness of the table.
    """
    # 4 positive, 4 negative, 4 zero — all 12 should get a style entry
    changes = [1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0, 0.0, 0.0, 0.0, 0.0]
    df = make_wide_df(changes)
    styles = table_styles_wide(df)

    # 12 month columns (indices 1–12 in the DataFrame → 12 entries)
    assert len(styles) == 12


# ─────────────────────────────────────────────────────────────────────
# 3.  diverging_styles — the underlying engine
# ─────────────────────────────────────────────────────────────────────

def test_diverging_styles_empty_input_returns_empty_list():
    """
    Behaviour: diverging_styles([]) must return [] without error.
    Matters because: table_styles_wide passes an empty cells list
    when the DataFrame has no usable rows; diverging_styles must
    handle this gracefully.
    """
    assert diverging_styles([]) == []


def test_diverging_styles_style_dict_has_required_keys():
    """
    Behaviour: every style dict produced by diverging_styles must
    contain the keys 'rows', 'cols', and 'style'.
    Matters because: Shiny's render.DataGrid will silently ignore —
    or worse, crash on — style dicts missing expected keys.
    """
    cells = [(2, 1, 1.5)]   # (row_idx, col_idx, value)
    styles = diverging_styles(cells)

    assert len(styles) == 1
    entry = styles[0]

    assert "rows"  in entry, "Style dict missing 'rows' key"
    assert "cols"  in entry, "Style dict missing 'cols' key"
    assert "style" in entry, "Style dict missing 'style' key"


def test_diverging_styles_row_and_col_indices_preserved():
    """
    Behaviour: the row and col indices passed in must appear verbatim
    in the returned style dict.
    Matters because: a wrong index means the colour is applied to the
    wrong cell — the user sees colour in the wrong column or row.
    """
    cells = [(2, 5, 2.0)]   # row 2, col 5
    styles = diverging_styles(cells)

    assert styles[0]["rows"] == [2]
    assert styles[0]["cols"] == [5]


def test_diverging_styles_intensity_scales_with_magnitude():
    """
    Behaviour: a larger absolute change value must produce a more
    saturated (closer to pure red/blue) background than a smaller one.
    Matters because: the diverging scale is supposed to show users at
    a glance which months changed more — flat uniform colour would
    remove that information entirely.

    We test this by checking that the interpolation parameter t is
    larger for the bigger value (indirectly, via the red channel).
    """
    # Small positive change vs large positive change
    styles_small = diverging_styles([(2, 1, 0.1)])
    styles_large = diverging_styles([(2, 1, 5.0)])

    # Extract the red channel integer from "rgba(R,G,B,A)"
    def extract_red(style_entry):
        bg = style_entry[0]["style"]["backgroundColor"]
        # bg looks like "rgba(231,76,60,0.65)" — split on commas
        r_str = bg.split("(")[1].split(",")[0]
        return int(r_str)

    red_small = extract_red(styles_small)
    red_large = extract_red(styles_large)

    # Larger change → higher t → red channel further from 255 (white)
    # i.e. red channel should be lower (more saturated) for larger value
    assert red_large <= red_small, (
        f"Expected larger change to be more saturated (lower red), "
        f"got red_small={red_small}, red_large={red_large}"
    )
    