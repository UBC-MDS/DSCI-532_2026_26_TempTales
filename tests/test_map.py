# Tests for apply_country_highlight() in src/map.py

import pytest
from src.map import apply_country_highlight, build_base_map


# ─────────────────────────────────────────────────────────────────────
# Shared fixture — a small figure with three countries
# ─────────────────────────────────────────────────────────────────────
@pytest.fixture
def sample_countries():
    """Return a small, stable list of country names for testing."""
    return ["Canada", "Germany", "Japan"]


@pytest.fixture
def sample_fig(sample_countries):
    """
    Return a FigureWidget built from three countries.
    build_base_map() sets all z-values to None and all markers to
    default styling — apply_country_highlight() then overrides them.
    """
    return build_base_map(sample_countries)


# ─────────────────────────────────────────────────────────────────────
# 1.  Selected country gets distinct styling
# ─────────────────────────────────────────────────────────────────────

def test_selected_country_has_full_opacity(sample_fig, sample_countries):
    """
    Behaviour: the selected country must have opacity 1.0 (fully visible).
    Matters because: unselected countries are dimmed to 0.6; if the
    selected country is also dimmed, users cannot see which one is active.
    """
    apply_country_highlight(sample_fig, sample_countries, "Canada")

    opacities = list(sample_fig.data[0].marker.opacity)
    # Canada is index 0 in sample_countries
    canada_idx = sample_countries.index("Canada")

    assert opacities[canada_idx] == 1.0, (
        f"Expected Canada opacity=1.0, got {opacities[canada_idx]}"
    )


def test_selected_country_has_wider_border(sample_fig, sample_countries):
    """
    Behaviour: the selected country must have a line width of 1.5.
    Matters because: this is the visual cue that distinguishes the active
    country; if it matched the default 0.5 the selection would be invisible.
    """
    apply_country_highlight(sample_fig, sample_countries, "Germany")

    widths = list(sample_fig.data[0].marker.line.width)
    germany_idx = sample_countries.index("Germany")

    assert widths[germany_idx] == 1.5, (
        f"Expected Germany line width=1.5, got {widths[germany_idx]}"
    )


def test_selected_country_has_white_border(sample_fig, sample_countries):
    """
    Behaviour: the selected country's border must be 'white'.
    Matters because: the white border contrasts against the coloured
    choropleth fill; the previous version used 'black' — this test
    documents the current correct value so a regression is caught.
    """
    apply_country_highlight(sample_fig, sample_countries, "Japan")

    colors = list(sample_fig.data[0].marker.line.color)
    japan_idx = sample_countries.index("Japan")

    assert colors[japan_idx] == "white", (
        f"Expected Japan border='white', got {colors[japan_idx]!r}"
    )


# ─────────────────────────────────────────────────────────────────────
# 2.  Unselected countries get default styling
# ─────────────────────────────────────────────────────────────────────

def test_unselected_countries_have_reduced_opacity(sample_fig, sample_countries):
    """
    Behaviour: countries that are NOT selected must have opacity 0.6.
    Matters because: the dimming effect draws attention to the selected
    country; without it, the map looks the same regardless of selection.
    """
    apply_country_highlight(sample_fig, sample_countries, "Canada")

    opacities = list(sample_fig.data[0].marker.opacity)

    # Germany (index 1) and Japan (index 2) are unselected
    for country in ["Germany", "Japan"]:
        idx = sample_countries.index(country)
        assert opacities[idx] == 0.6, (
            f"Expected {country} opacity=0.6, got {opacities[idx]}"
        )


def test_unselected_countries_have_narrow_border(sample_fig, sample_countries):
    """
    Behaviour: unselected countries must have line width 0.5.
    Matters because: if all countries had width 1.5 the selected-country
    highlight would be invisible — the narrow default is load-bearing.
    """
    apply_country_highlight(sample_fig, sample_countries, "Canada")

    widths = list(sample_fig.data[0].marker.line.width)

    for country in ["Germany", "Japan"]:
        idx = sample_countries.index(country)
        assert widths[idx] == 0.5, (
            f"Expected {country} line width=0.5, got {widths[idx]}"
        )


def test_unselected_countries_have_gray_border(sample_fig, sample_countries):
    """
    Behaviour: unselected countries must have border colour 'gray'.
    Matters because: 'gray' is less prominent than 'white', reinforcing
    the visual hierarchy between selected and unselected countries.
    """
    apply_country_highlight(sample_fig, sample_countries, "Canada")

    colors = list(sample_fig.data[0].marker.line.color)

    for country in ["Germany", "Japan"]:
        idx = sample_countries.index(country)
        assert colors[idx] == "gray", (
            f"Expected {country} border='gray', got {colors[idx]!r}"
        )


# ─────────────────────────────────────────────────────────────────────
# 3.  Length invariants — the figure lists must always match country count
# ─────────────────────────────────────────────────────────────────────

def test_opacity_list_length_matches_country_count(sample_fig, sample_countries):
    """
    Behaviour: the opacity list set on the figure must have exactly
    one value per country — same length as all_countries.
    Matters because: a length mismatch causes Plotly to silently ignore
    or mis-apply styles; some countries would get the wrong colour.
    """
    apply_country_highlight(sample_fig, sample_countries, "Canada")
    assert len(sample_fig.data[0].marker.opacity) == len(sample_countries)


def test_line_width_list_length_matches_country_count(sample_fig, sample_countries):
    """
    Behaviour: the line-width list must have exactly one entry per country.
    Matters because: same Plotly length-mismatch hazard as the opacity list.
    """
    apply_country_highlight(sample_fig, sample_countries, "Canada")
    assert len(sample_fig.data[0].marker.line.width) == len(sample_countries)


# ─────────────────────────────────────────────────────────────────────
# 4.  Edge case — selected_country is None
# ─────────────────────────────────────────────────────────────────────

def test_none_selected_country_does_not_crash(sample_fig, sample_countries):
    """
    Behaviour: passing selected_country=None must not raise an exception.
    Matters because: app.py calls apply_country_highlight with None when
    the year range is invalid and no country should be highlighted;
    a crash here would break the reactive update cycle.
    """
    # Should complete without raising any exception
    apply_country_highlight(sample_fig, sample_countries, None)


def test_none_selected_all_countries_dimmed(sample_fig, sample_countries):
    """
    Behaviour: when selected_country=None, every country should be dimmed
    (opacity 0.6), because no country is active.
    Matters because: a leftover highlight from a previous selection would
    persist on the map even after the user clears the year inputs.
    """
    apply_country_highlight(sample_fig, sample_countries, None)

    opacities = list(sample_fig.data[0].marker.opacity)
    # None matches no country so every country gets the "else" branch → 0.6
    for i, country in enumerate(sample_countries):
        assert opacities[i] == 0.6, (
            f"Expected {country} opacity=0.6 when selection is None, "
            f"got {opacities[i]}"
        )
        