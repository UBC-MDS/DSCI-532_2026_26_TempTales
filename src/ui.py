# imports
from shiny import ui
from shinywidgets import output_widget
from .utils import country_choices, min_year, max_year

# ==========================================
# 0. Footer Configuration (manual update on release)
# ==========================================
FOOTER_LAST_UPDATED = "2026-02-28"
REPO_URL = "https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales"
AUTHORS_LIST = ["Emily Jin", "Ian Gault", "Purity Jangaya", "Yusheng Li"]

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
    ui.output_data_frame("seasonal_temp_ui"),
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
map_plot_card = ui.card(
    ui.card_header("World Heatmap"),
    ui.div(
        output_widget("map_plot"),
        style="height:100%; width:100%;"
    ),
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
# 6. Footer (authors, repo link, last updated; fixed at bottom)
# ==========================================
author_spans = []
for i, name in enumerate(AUTHORS_LIST):
    author_spans.append(ui.span(name, class_="me-2"))
    if i < len(AUTHORS_LIST) - 1:
        author_spans.append(ui.span("·", class_="mx-2 text-muted"))

app_footer = ui.tags.footer(
    ui.div(
        ui.span(*author_spans, class_="d-inline-flex align-items-center me-2"),
        ui.span("·", class_="mx-2 text-muted d-none d-sm-inline"),
        ui.a(
            "Repository", 
            href=REPO_URL, 
            target="_blank", 
            rel="noopener noreferrer", 
            class_="text-decoration-none me-2"
        ),
        ui.span("·", class_="mx-2 text-muted d-none d-sm-inline"),
        ui.span(f"Last updated: {FOOTER_LAST_UPDATED}", class_="text-muted small"),
        class_="d-flex align-items-center justify-content-center flex-wrap gap-1 gap-sm-2 py-2 px-3"
    ),
    class_="border-top bg-light",
    style="position: fixed; bottom: 0; left: 0; right: 0; z-index: 1000; font-size: 0.875rem;"
)

# ==========================================
# 7. Final App UI Assembly
# ==========================================
main_content = ui.div(
    ui.output_ui("title_placeholder"),
    ui.layout_columns(
        left_column,
        right_area,
        col_widths=[3, 9]
    ),
    style="padding-bottom: 50px;"  # prevent content from hiding under fixed footer
)

app_ui = ui.page_sidebar(
    app_sidebar,
    ui.div(
        main_content,
        app_footer
    )
)
