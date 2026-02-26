# imports
from shiny import ui
from shinywidgets import output_widget
from utils import country_choices, min_year, max_year

# ==========================================
# 1. Define Inputs (Global Filters)
# ==========================================
country_selector = ui.input_select(
    "country",
    "Select Country",
    choices=country_choices,
    selected="Canada"
)

year_slider = ui.input_slider(
    "year",
    "Select Year:",
    min=min_year,
    max=max_year,
    value=1950,
    sep="",
    width="100%",
    animate=ui.AnimationOptions(interval=2000, loop=False)
)

map_projection_selector = ui.input_select(
    "map_projection",
    None,
    choices=[
        "equirectangular",
        "natural earth",
        "orthographic",
        "robinson",
        "mercator"
    ],
    selected="robinson",
    width="100%"
)

# ==========================================
# 2. Define Left Column Cards
# ==========================================
country_card = ui.card(
    ui.card_header("Location"),
    country_selector
)

data_count_card = ui.card(
    ui.card_header("Data Points"),
    ui.output_ui("data_count_ui"),
    class_="mb-3"
)

event_card = ui.card(
    ui.card_header("Historical Event"),
    ui.output_ui("event_ui"),
    class_="bg-light"
)

seasonal_temp_card = ui.card(
    ui.card_header("Seasonal Temperature"),
    ui.output_ui("seasonal_temp_ui"),
    class_="mb-3"
)

# Group left column components
left_column = ui.div(
    country_card,
    data_count_card,
    event_card,
    seasonal_temp_card
)

# ==========================================
# 3. Define Right Column Cards
# ==========================================
year_card = ui.card(
    year_slider,
    class_="mb-3 p-2"
)

temp_plot_card = ui.card(
    ui.card_header("Temperature Over Time"),
    output_widget("temp_plot"),
    height="200px",
    class_="mb-3"
)

# Wrapper for map projection selector to align it to the right
map_selector_container = ui.div(
    map_projection_selector,
    class_="d-flex justify-content-end",
    style="width: 150px; margin-left: auto;"
)

map_plot_card = ui.card(
    ui.card_header("World Heatmap"),
    map_selector_container,
    output_widget("map_plot"),
    height="500px"
)

# Group right column components
right_column = ui.div(
    year_card,
    temp_plot_card,
    map_plot_card
)

# ==========================================
# 4. Final App UI Assembly
# ==========================================
app_ui = ui.page_fillable(
    ui.layout_columns(
        left_column,
        right_column,
        col_widths=[3, 9]
    )
)
