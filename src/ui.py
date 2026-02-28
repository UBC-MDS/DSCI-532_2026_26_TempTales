# imports
from shiny import ui
from shinywidgets import output_widget
from .utils import country_choices, min_year, max_year

# ==========================================
# 1. Define Inputs
# ==========================================
country_selector = ui.input_select(
    "country",
    "Select Country",
    choices=country_choices,
    selected="Canada"
)

baseline_year_input = ui.input_numeric(
    "baseline_year",
    "Select Reference Year:",
    value=1950,
    min=min_year,
    max=max_year,
    step=1,
    width="100%"
)

target_year_input = ui.input_numeric(
    "target_year",
    "Select Target Year:",
    value=2000,
    min=min_year,
    max=max_year,
    step=1,
    width="100%"
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
# 2. Define Sidebar (Collapsible)
# ==========================================
app_sidebar = ui.sidebar(
    country_selector,
    baseline_year_input,
    target_year_input,
    ui.output_ui("year_validation_ui"),
    title="Filters",
    open="desktop",
    id="app_sidebar",
)

# ==========================================
# 3. Define Title Placeholder (Value Box)
# ==========================================
title_value_box = ui.value_box(
    "TempTales",
    ui.output_ui("title_placeholder"),
    theme="primary"
)

# ==========================================
# 4. Define Left Column Cards
# ==========================================
data_count_card = ui.card(
    ui.card_header("Yearly Average Temperature"),
    ui.output_ui("data_count_ui"),
    class_="mb-3"
)

event_card = ui.card(
    ui.card_header("Historical Event"),
    ui.output_ui("event_ui"),
    class_="bg-light mb-3"
)

seasonal_temp_card = ui.card(
    ui.card_header("Seasonal Temperature"),
    ui.output_ui("seasonal_temp_ui"),
    class_="mb-3"
)

left_column = ui.div(
    data_count_card,
    event_card,
    seasonal_temp_card
)

# ==========================================
# 5. Define Right Area Cards
# ==========================================
map_selector_container = ui.div(
    map_projection_selector,
    class_="d-flex justify-content-end",
    style="width: 150px; margin-left: auto;"
)

map_plot_card = ui.card(
    ui.card_header("World Heatmap"),
    map_selector_container,
    output_widget("map_plot"),
    height="500px",
    full_screen=True
)

temp_plot_card = ui.card(
    ui.card_header("Temperature Over Time"),
    output_widget("temp_plot"),
    height="450px",
    class_="mb-3",
    full_screen=True
)

table_card = ui.card(
    ui.card_header(
        ui.div(
            "Data Table",
            ui.download_button("download_table_csv", "Export CSV", class_="btn-sm"),
            class_="d-flex justify-content-between align-items-center w-100"
        )
    ),
    ui.output_data_frame("data_table"),
    height="300px",
    class_="mb-3"
)

# Right area: Heatmap on top, Line plot + Table side-by-side (8:4)
right_area = ui.div(
    map_plot_card,
    ui.layout_columns(
        temp_plot_card,
        table_card,
        col_widths=[8, 4]
    )
)

# ==========================================
# 6. Final App UI Assembly
# ==========================================
main_content = ui.div(
    title_value_box,
    ui.layout_columns(
        left_column,
        right_area,
        col_widths=[3, 9]
    )
)

app_ui = ui.page_sidebar(
    app_sidebar,
    main_content
)
