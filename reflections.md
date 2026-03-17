## Test Reflection

### `test_data_preprocessor.py` — `get_season()`
Covers the month-to-season mapping for all 12 months including all four
boundary months (March, June, September, December). If the month ranges
in `get_season()` were edited — for example changing `[12, 1, 2]` to
`[1, 2, 3]` — December would silently be labelled Fall and the seasonal
temperature table would show wrong data with no error raised.

### `test_data_count.py` — `data_count_prep()`
Covers correct temperature string formatting, the "No Data" fallback for
missing years, and correct row selection when multiple years are present.
If the f-string format changed (e.g. removing `±` or changing decimal
places) the value box would display malformed text. If the fallback path
were removed, an empty DataFrame would raise an IndexError and crash the
dashboard card.

### `test_table_styles.py` — `table_styles_wide()`, `diverging_styles()`
Covers colour direction (positive → red, negative → blue, zero → neutral),
guard rails for empty DataFrames, and intensity scaling with magnitude.
If red and blue were swapped the table would be actively misleading —
users would read warming as cooling. If the empty DataFrame guard were
removed, the function would raise an IndexError whenever no valid year
range is selected.

### `test_map.py` — `apply_country_highlight()`
Covers that the selected country gets opacity 1.0, line width 1.5, and
white border, while all others get opacity 0.6, width 0.5, and gray
border. Also covers the `None` selection edge case. If the selected and
unselected styles were swapped the map highlight would be invisible. If
`None` caused a crash, the map would break every time the year inputs
are invalid.

### `test_plot.py` — `build_temp_chart()`
Covers the empty-data path (no crash, returns valid Altair object, custom
message in spec), the valid-data path (country and years in title, height
respected), and edge cases (negative temperatures, spaces in country name).
If the empty-data branch raised an exception, the entire Dashboard tab
would show an error panel whenever the year range is invalid instead of
a placeholder message.

### `test_ui_playwright.py` — Full dashboard UI
Covers end-to-end reactive behaviour across Chromium, Firefox, and WebKit:
year validation errors, success confirmation, navbar title updates, data
table row count, and the out-of-range boundary condition. If the Shiny
reactive `selected_range()` were refactored and the error message text
changed, users would see no feedback for invalid inputs. If the DataGrid
renderer changed its HTML structure, the 3-row assertion would catch it
before users noticed a broken table.
