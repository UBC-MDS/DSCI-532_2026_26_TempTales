# Tests for get_season() in src/data_processor.py
#
# WHY THIS FILE EXISTS:
#   get_season() maps month numbers (1–12) to season names.
#   If this mapping breaks (e.g. someone edits the month ranges),
#   the seasonal temperature table in the dashboard will silently
#   show wrong season labels. These tests pin down the exact
#   expected behaviour for every boundary condition.

import pytest
from src.data_processor import get_season

# ──────────────────────────────────────────────────────────────
# 1.  Core season mapping — one representative month per season
# ──────────────────────────────────────────────────────────────

def test_get_season_spring():
    """
    Behaviour: month 4 (April) must return 'Spring'.
    """
    assert get_season(4) == "Spring"


def test_get_season_summer():
    """
    Behaviour: month 7 (July) must return 'Summer'.
    """
    assert get_season(7) == "Summer"


def test_get_season_fall():
    """
    Behaviour: month 10 (October) must return 'Fall'.
    """
    assert get_season(10) == "Fall"


def test_get_season_winter_january():
    """
    Behaviour: month 1 (January) must return 'Winter'.
    """
    assert get_season(1) == "Winter"


def test_get_season_winter_february():
    """
    Behaviour: month 2 (February) must return 'Winter'.
    """
    assert get_season(2) == "Winter"


# ──────────────────────────────────────────────────────────────
# 2.  Boundary months — the most error-prone edge cases
# ──────────────────────────────────────────────────────────────

def test_get_season_boundary_december_is_winter():
    """
    Behaviour: month 12 (December) must return 'Winter', not 'Fall'.
    """
    assert get_season(12) == "Winter"


def test_get_season_boundary_march_is_spring():
    """
    Behaviour: month 3 (March) must return 'Spring', not 'Winter'.
    """
    assert get_season(3) == "Spring"


def test_get_season_boundary_june_is_summer():
    """
    Behaviour: month 6 (June) must return 'Summer', not 'Spring'.
    """
    assert get_season(6) == "Summer"


def test_get_season_boundary_september_is_fall():
    """
    Behaviour: month 9 (September) must return 'Fall', not 'Summer'.
    """
    assert get_season(9) == "Fall"


def test_get_season_boundary_november_is_fall():
    """
    Behaviour: month 11 (November) must return 'Fall', not 'Winter'.
    """
    assert get_season(11) == "Fall"


# ──────────────────────────────────────────────────────────────
# 3.  Return type check
# ──────────────────────────────────────────────────────────────

def test_get_season_returns_string():
    """
    Behaviour: get_season() must always return a plain Python str.
    """
    result = get_season(6)
    assert isinstance(result, str)


# ──────────────────────────────────────────────────────────────
# 4.  Parametrized full sweep — all 12 months at once
# ──────────────────────────────────────────────────────────────

# This parametrize decorator runs the same test function once for
# each (month, expected_season) pair
@pytest.mark.parametrize("month, expected", [
    (1,  "Winter"),
    (2,  "Winter"),
    (3,  "Spring"),
    (4,  "Spring"),
    (5,  "Spring"),
    (6,  "Summer"),
    (7,  "Summer"),
    (8,  "Summer"),
    (9,  "Fall"),
    (10, "Fall"),
    (11, "Fall"),
    (12, "Winter"),
])
def test_get_season_all_months(month, expected):
    """
    Behaviour: every month 1–12 must map to the correct season.
    """
    assert get_season(month) == expected
