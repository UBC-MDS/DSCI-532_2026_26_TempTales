# imports
from shiny import ui
from shinywidgets import output_widget
from .utils import country_choices, min_year, max_year
from .chat import qc

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
    open="closed",
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

# Right column: row ratio 7:3 (charts : table), heatmap:line 1:1
map_plot_card = ui.card(
    ui.card_header(ui.output_ui("map_card_header")),
    ui.div(
        output_widget("map_plot"),
        style="height:100%; width:100%; min-height: 0;"
    ),
    style="height: 100%; display: flex; flex-direction: column; min-height: 0;",
    class_="h-100",
    full_screen=True
)

temp_plot_card = ui.card(
    ui.card_header("Temperature Over Time"),
    ui.div(
        output_widget("temp_plot"),
        style="height:100%; width:100%; min-height: 0; flex: 1;"
    ),
    style="height: 100%; display: flex; flex-direction: column; min-height: 0;",
    class_="h-100",
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
    ui.div(
        ui.output_data_frame("data_table"),
        class_="data-table-compact"
    ),
    style="min-height: 0; flex: 1;",
    class_="mb-3"
)

# Top section (70%): heatmap 4 + line 6, bottom-aligned; Bottom section (30%): table
charts_row = ui.layout_columns(
    map_plot_card,
    temp_plot_card,
    col_widths=[6, 6],
    row_heights="1fr",
    fill=True,
)

right_area = ui.div(
    ui.div(
        charts_row,
        style="flex: 7; min-height: 0; display: flex; flex-direction: column;"
    ),
    ui.div(
        table_card,
        style="flex: 3; min-height: 0; display: flex; flex-direction: column; overflow: hidden;"
    ),
    style="display: flex; flex-direction: column; min-height: 55vh;"
)


# ==========================================
# 7. AI Tab
# ==========================================

# Query chat card (LEFT COLUMN)
querychat_card = ui.card(
    ui.card_header("Ask the Data (AI Assistant)"), 
    ui.markdown("""
    **TempTales Climate Explorer 🌍**

    Ask questions to explore historical temperature trends across countries.

    *Dataset:* Monthly average temperatures for the **top 100 most populous countries (1860–2013)**.

    **Example queries**
    - Compare temperatures in Canada and Japan between 1950 and 2000  
    - Show Canada and United States from 1945 to 1997
    - Show the temperatures in Canada, United States, Japan, Taiwan in 1930, 1956, 1997, 2000
    - Show the monthly temperature difference for Canada between 1930 and 1980  
    - Compare temperature changes of Canada between 1900 and 2000  

    *Tip:* You can include multiple countries and years in your question.
    """),
    # qc.ui(),
    ui.div(
        qc.ui(),
        style="min-height:300px;"
    ),
    class_="mb-3"     
)

# AI Dataframe card (MIDDLE COLUMN)
ai_data_frame_card = ui.card(
    ui.card_header(
        ui.div(
            "Data Frame",
            ui.download_button("download_ai_table_csv", "Export CSV", class_="btn-sm"),
            class_="d-flex justify-content-between align-items-center w-100",
        )
    ),
    ui.output_data_frame("ai_data_frame"),
    class_="mb-3 h-100",
)

# AI Figures (RIGHT COLUMN)

## a) AI Time Series with Centred Data
ai_centred_series_card = ui.card(
    ui.card_header("Time Series of Centred Temperature Data by Country"),
    ui.div(
        output_widget("ai_centred_ts_plot"),
        style="height:100%; width:100%; min-height:0; flex: 1;",
    ),
    style="height: 100%; display: flex; flex-direction: column; min-height: 0;",
    class_="h-100 mb-3",
)

## b) AI Temperature Changes Across Months
ai_monthly_change_card = ui.card(
    ui.card_header("Difference in Monthly Temperatures Between Reference and Target Years"),
    ui.div(
        output_widget("ai_monthly_change_plot"),
        style="height:100%; width:100%; min-height:0; flex: 1;",
    ),
    style="height: 100%; display: flex; flex-direction: column; min-height: 0;",
    class_="h-100",
)

## Combine figures
ai_right_column = ui.div(
    ui.div(
        ai_centred_series_card,
        style="flex: 1; min-height: 0; display: flex; flex-direction:column;"
    ),
    ui.div(
        ai_monthly_change_card,
        style="flex: 1; min-height: 0; display: flex; flex-direction:column;"
    ),
    style="display: flex; flex-direction:column; min-height: 65vh"
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
# 7. Main Content (Dashboard tab)
# ==========================================
main_content = ui.div(
    ui.layout_columns(
        left_column,
        right_area,
        col_widths=[3, 9]
    )
)

# ==========================================
# AI Assistant tab: 3:9 layout, chatbox left, right empty
# ==========================================
ai_assistant_content = ui.layout_columns(
    querychat_card,
    ai_data_frame_card,
    ai_right_column,
    col_widths=[3, 4, 5]

)

# ==========================================
# 8. Data table compact styling (smaller font and padding)
# ==========================================
data_table_css = ui.tags.style("""
    .data-table-compact { overflow-y: auto; }
    .data-table-compact .shiny-data-frame-output,
    .data-table-compact [class*="data-frame"],
    .data-table-compact table { font-size: 0.7rem !important; }
    .data-table-compact th,
    .data-table-compact td { padding: 0.15rem 0.35rem !important; }
""")

# ==========================================
# 9. Final App UI Assembly (page_navbar with tabs)
# Footer in page_navbar so it appears on both Dashboard and AI Assistant
# ==========================================
app_ui = ui.TagList(
    data_table_css,
    ui.page_navbar(
        ui.nav_panel("Dashboard", main_content, value="dashboard"),
        ui.nav_panel("AI Assistant", ai_assistant_content, value="ai_assistant"),
        title=ui.output_ui("title_placeholder"),
        id="main_nav",
        sidebar=app_sidebar,
        footer=app_footer,
        fillable=True,
        padding=[10, 10, 60, 10],
    )
)
