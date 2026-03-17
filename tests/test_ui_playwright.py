# tests/test_ui_playwright.py
#
# Playwright UI tests for the TempTales dashboard.
#
# WHY THIS FILE EXISTS:
#   Unit tests verify isolated Python functions. These tests verify that
#   the *running app* behaves correctly in a real browser — inputs trigger
#   the right reactive outputs, validation messages appear, and the data
#   table renders with the correct shape.
#
# HOW PLAYWRIGHT WORKS HERE:
#   1. The shiny_app fixture starts `src/app.py` as a background subprocess
#      on port 8000 before any test runs.
#   2. Playwright opens a real browser invisibly (headless=True), navigates
#      to http://localhost:8000, and simulates user interactions.
#   3. After all tests finish the subprocess is torn down automatically.
#   You do NOT need to open a browser manually — Playwright handles this.
#
# BROWSERS:
#   The `page` fixture is parametrized with all three Playwright browsers.
#   Every test runs 3 times — once each on Chromium, Firefox, and WebKit
#   — giving 18 runs total (6 tests × 3 browsers).
#
# HOW TO RUN (from project root):
#   pytest tests/test_ui_playwright.py -v
#
#   Run on a single browser only (faster during development):
#   pytest tests/test_ui_playwright.py -v -k "chromium"
#
# PREREQUISITE:
#   The app must NOT already be running on port 8000 when you run the
#   tests. The shiny_app fixture starts its own instance — if port 8000
#   is already occupied it will fail with a connection error.

import subprocess
import time

import pytest
from playwright.sync_api import Page, expect


# ─────────────────────────────────────────────────────────────────────
# 1.  App subprocess fixture
#     Starts `src/app.py` once for the whole test session and tears it
#     down afterward. scope="session" means it starts once and is shared
#     across all tests — much faster than restarting per test.
# ─────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def shiny_app():
    """
    Start the Shiny app as a background subprocess and wait until it is
    ready to accept connections before yielding to the tests.

    'yield' is used instead of 'return' so the cleanup code after it
    (proc.terminate()) runs automatically when all tests finish —
    even if a test crashes midway.
    """
    # Start the app exactly as your Makefile does, minus --launch-browser
    proc = subprocess.Popen(
        ["python", "-m", "shiny", "run", "src/app.py", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Give the app time to boot before tests start hitting it.
    # 5 seconds is conservative — increase to 10 if your machine is slow
    # or if you see "ERR_CONNECTION_REFUSED" errors in the first tests.
    time.sleep(5)

    # 'yield' passes the base URL to every test that uses this fixture.
    # Everything after yield runs on teardown (after all tests finish).
    yield "http://localhost:8000"

    # ── Teardown ── kill the app process when the session ends ──
    proc.terminate()
    proc.wait()


# ─────────────────────────────────────────────────────────────────────
# 2.  Browser parametrization
#     This fixture makes every test run once per browser automatically.
#     pytest calls the test once for each value in params=[...],
#     substituting the browser name each time.
# ─────────────────────────────────────────────────────────────────────

@pytest.fixture(params=["chromium", "firefox", "webkit"])
def page(request, shiny_app, playwright):
    """
    Open a fresh browser page for each test on each browser engine.
    scope defaults to "function" — a new page per test — so one test's
    input changes never bleed into the next test.

    `playwright` is a built-in pytest-playwright fixture that provides
    access to the three browser engine objects. We do NOT need to open
    any browser manually — Playwright does it here automatically.
    """
    browser_name = request.param

    # headless=True = browser runs invisibly in the background.
    # Change to headless=False if you want to watch the tests run live
    # in a visible browser window (useful for debugging).
    if browser_name == "chromium":
        browser = playwright.chromium.launch(headless=True)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=True)
    else:
        browser = playwright.webkit.launch(headless=True)

    # new_context() is like a fresh incognito window — no cookies or
    # state carried over from other tests.
    context = browser.new_context()
    page = context.new_page()

    # Navigate to the running app before handing the page to the test.
    # wait_until="networkidle" waits until there are no more network
    # requests in flight — ensures the app is fully loaded.
    page.goto(shiny_app, wait_until="networkidle")

    yield page

    # ── Teardown ── close the page and browser after each individual test ──
    context.close()
    browser.close()


# ─────────────────────────────────────────────────────────────────────
# Helper — fill a numeric input with a new value and trigger Shiny
# ─────────────────────────────────────────────────────────────────────

def fill_year_input(page: Page, input_id: str, value: int):
    """
    Clear a Shiny numeric input and replace it with a new value.

    We use three steps that work reliably across all browsers in
    playwright 0.7.x:
      1. click(click_count=3) — triple-click to select all existing text.
         NOTE: triple_click() does not exist in playwright 0.7.x —
         click(click_count=3) is the correct equivalent.
      2. fill(str(value))     — replaces the selection with the new value.
         fill() is more reliable than type() because it always clears
         the field first before typing.
      3. press("Tab")         — moves focus away, which fires Shiny's
         'change' event so the reactive chain updates.

    Args:
        page:     The Playwright Page object
        input_id: The Shiny input id (e.g. "baseline_year")
        value:    The integer year to enter
    """
    locator = page.locator(f"#{input_id}")

    # Triple-click selects all text already in the input so the next
    # fill() replaces it entirely rather than appending to it.
    # click_count=3 is the playwright 0.7.x API — triple_click() was
    # added in a later version and raises AttributeError here.
    locator.click(click_count=3)

    # fill() atomically clears the field and types the new value.
    # This is safer than keyboard.type() which can leave partial old
    # values if the selection step above didn't work perfectly.
    locator.fill(str(value))

    # Tab away to fire the 'change' event that Shiny listens for.
    # Without this, the reactive does not update and the test would
    # be checking stale UI state.
    locator.press("Tab")


# ─────────────────────────────────────────────────────────────────────
# TEST 1 — Year validation: target ≤ baseline shows error message
# ─────────────────────────────────────────────────────────────────────

def test_target_year_less_than_baseline_shows_error(page: Page):
    """
    Behaviour: entering a target year less than the baseline year must
    display "Target year must be greater than reference year."
    Matters because: this is the primary guard rail preventing nonsensical
    comparisons; without it users get empty charts with no explanation.
    """
    fill_year_input(page, "baseline_year", 2000)
    fill_year_input(page, "target_year", 1990)

    # expect() automatically retries for up to 5 seconds — essential
    # because Shiny reactives take a moment to update the DOM after
    # an input change. No manual sleep() needed.
    error_locator = page.locator("#year_validation_ui")
    expect(error_locator).to_contain_text(
        "Target year must be greater than reference year."
    )


def test_equal_years_shows_error(page: Page):
    """
    Behaviour: entering the same value for baseline and target must also
    trigger the validation error — equal years are not a valid range.
    Matters because: selected_range() uses `t <= b` so equal years must
    be rejected; this test verifies the boundary is correctly inclusive.
    """
    fill_year_input(page, "baseline_year", 1990)
    fill_year_input(page, "target_year", 1990)

    error_locator = page.locator("#year_validation_ui")
    expect(error_locator).to_contain_text(
        "Target year must be greater than reference year."
    )


# ─────────────────────────────────────────────────────────────────────
# TEST 2 — Valid inputs show success message
# ─────────────────────────────────────────────────────────────────────

def test_valid_year_range_shows_success_message(page: Page):
    """
    Behaviour: a valid baseline/target pair must show "Year range is valid."
    Matters because: without this confirmation users have no feedback that
    their selection was accepted and may keep adjusting inputs needlessly.
    """
    # Re-enter defaults explicitly so this test is self-contained and
    # does not depend on whatever a previous test left in the inputs.
    fill_year_input(page, "baseline_year", 1950)
    fill_year_input(page, "target_year", 2000)

    validation_locator = page.locator("#year_validation_ui")
    expect(validation_locator).to_contain_text("Year range is valid.")


# ─────────────────────────────────────────────────────────────────────
# TEST 3 — Navbar title updates to reflect country and years
# ─────────────────────────────────────────────────────────────────────

def test_title_updates_with_country_and_years(page: Page):
    """
    Behaviour: with valid inputs, the navbar title must contain the
    selected country name and both years.
    Matters because: the title is the user's primary confirmation of what
    they are looking at; a stale or wrong title breaks trust in the dashboard.
    """
    fill_year_input(page, "baseline_year", 1950)
    fill_year_input(page, "target_year", 2000)

    # title_placeholder() in app.py renders inside #title_placeholder.
    # Canada is the default selected country on app load.
    title_locator = page.locator("#title_placeholder")
    expect(title_locator).to_contain_text("Canada")
    expect(title_locator).to_contain_text("1950")
    expect(title_locator).to_contain_text("2000")


# ─────────────────────────────────────────────────────────────────────
# TEST 4 — Data table renders with correct shape (3 rows)
# ─────────────────────────────────────────────────────────────────────

def test_data_table_renders_three_rows(page: Page):
    """
    Behaviour: with valid inputs, the monthly comparison table must render
    exactly 3 rows — Baseline, Target, and Change.
    Matters because: a missing Change row means users lose the most
    important row in the table with no error shown.
    """
    fill_year_input(page, "baseline_year", 1950)
    fill_year_input(page, "target_year", 2000)

    # Wait for the table to appear — Shiny renders it asynchronously
    table_locator = page.locator("#data_table table")
    expect(table_locator).to_be_visible()

    # Count <tr> elements in <tbody> only — the header row in <thead>
    # is excluded. Each tbody <tr> is one data row.
    rows = page.locator("#data_table table tbody tr")
    expect(rows).to_have_count(3)


# ─────────────────────────────────────────────────────────────────────
# TEST 5 — Out-of-range year shows boundary validation error
# ─────────────────────────────────────────────────────────────────────

def test_year_below_min_shows_validation_error(page: Page):
    """
    Behaviour: a year below the dataset minimum (1860) must display
    a validation error referencing the valid range.
    Matters because: the dataset only covers 1860–2012; year 1800 has
    no data and would silently produce an empty chart without this guard.
    This is the boundary condition test required by the assignment.
    """
    fill_year_input(page, "baseline_year", 1800)
    fill_year_input(page, "target_year", 2000)

    # selected_range() produces "Reference year must be between {min} and {max}."
    error_locator = page.locator("#year_validation_ui")
    expect(error_locator).to_contain_text("Reference year must be between")
