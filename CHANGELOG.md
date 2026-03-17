# Changelog

All notable changes to this project will be documented in this file.

## [v0.4.0] (Milestone 4 - 2026-03-17)

Note: helped with copilot since v0.3.0 and appraised

## Overview
This release focuses on performance optimization, enhanced user experience, improved dashboard stability, and comprehensive testing. Major improvements include lazy loading with Ibis + DuckDB, interactive map features, better error handling, refined UI components, and full test coverage.

---

## Added

- **Lazy Loading with Ibis + DuckDB** ([#91](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/91))
  - Implemented lazy loading framework using Ibis expressions and DuckDB
  - Converted data from pickle to parquet format for better performance
  - Optimized reactive calculations to support large datasets without memory bloat

- **Interactive Heatmap with Click-to-Select** ([#88](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/88))
  - World heatmap now displays temperature change (relative difference between baseline and target years) instead of absolute temperature
  - Clicking on a country in the heatmap updates the country selector in the sidebar
  - Dynamic map title showing selected country and year comparison
  - Improved ocean vs. land contrast for better visual clarity

- **Country Selection Enhancement** ([#99](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/99))
  - Migrated from `ui.input_select` to `ui.input_selectize` for improved country dropdown navigation
  - Added real-time type-search functionality for easier country selection

- **Tab-Specific Sidebar Layout** ([#99](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/99))
  - Refactored sidebar to be dedicated to the Dashboard tab
  - Sidebar automatically disappears when navigating to the AI Assistant tab for full-width workspace

- **Comprehensive Test Suite** ([#100](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/100), [#101](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/101), [#102](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/102))
  - Added 48 unit tests across 5 test files covering core dashboard logic
  - Added 6 Playwright UI tests (18 total runs across Chromium, Firefox, WebKit)
  - Total: 67 tests with full coverage of critical paths
  - Documentation on running tests for contributors

---

## Changed

- **Enhanced Error Handling & Layout Stability** ([#94](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/94))
  - Prevented Yearly Average Temperature and Historical Event cards from collapsing on invalid input
  - Updated monthly data table and Temperature Over Time figure to display error messages instead of blank output
  - Changed world heatmap invalid state to a neutral map by clearing choropleth values
  - Added layout stabilization in the dashboard column with controlled spacing

- **Color Magnitude Representation in Tables** ([#88](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/88))
  - Data tables now use diverging color scale (blue for cooling, red for warming) with intensity mapped to magnitude
  - Applied consistent styling across monthly comparison and seasonal temperature tables
  - Improved visual clarity of temperature change indicators

- **Documentation Updates** ([#97](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/97), [#98](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/98))
  - Updated CONTRIBUTING.md with M3 reflection and M4 norms
  - Changed notation on branching framework to branch from `dev` instead of `main`
  - Added release highlight, collaboration notes, and reflection sections to changelog
 
- **Figure and Table Updates** ([#105](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/105))
  - addressing label issues in figure and table from  ([#85](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/issues/85))

---

## Fixed

- **Invalid Year Input Handling** ([#94](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/94))
  - Fixed layout shifting issues when invalid years are entered
  - Improved error messaging for all cards and visualizations
  - Issues: [#84](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/issues/84), [#85](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/issues/85), [#89](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/issues/89)

- **Country Dropdown Navigation** ([#99](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/99))
  - Fixed difficult country dropdown navigation by implementing searchable selectize input
  - Issue: [#87](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/issues/87)

- **Sidebar Visibility on AI Tab** ([#99](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/99))
  - Resolved sidebar appearing on AI Assistant tab where it wasn't functional
  - Issue: [#85](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/issues/85)

- **Data Count Formatting** ([#100](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pull/100))
  - Fixed observation counts displaying as floats (e.g., "42.0") instead of integers (e.g., "42")

---

## Known Issues

- Our historical PR's are missing meaningful comments.

---

## Technical Details

**User Experience**
- Heat map interactions
- Error handling and stable app layout
- Clearer titles and purpose per card

**Performance:**
- Database layer optimized with Ibis + DuckDB lazy loading
- Data now stored in parquet format for improved I/O performance
- Reduced memory footprint for large dataset operations

**Testing:**
- 48 unit tests: data preprocessing, table styling, map rendering, plot generation
- 18 Playwright UI tests across 3 browsers
- 100% critical path coverage

**Dependencies Added:**
- ibis-duckdb for lazy loading and query optimization

---

[View all merged PRs for v0.4.0](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/pulls?state=closed)

---

### Release Highlight: [Interactive Map]

<!-- One short paragraph describing what you built and what it does for the user. -->

- **Option chosen:** D
- **PR:** #88
- **Why this option over the others:** We thought this was the best option for an adavanced feature because it's an intuitive response for our dashboard's purpose. It allows user to intuitively filter the data by selecting countries directly from the visualization. This reduces the number of clicks and is in line with the side bar choices.
- **Feature prioritization issue link:** ([#86](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/issues/86))

### Collaboration

<!-- Summary of workflow or collaboration improvements made since M3. -->

- **CONTRIBUTING.md:** #97
- **M3 retrospective:** Biggest change is adding annotation to the PR appraisal and dividing coding tasks more evenly.
- **M4:** We used PR discussions more effectively, created issues first following by specific PRs completing those tasks, and avoided last minute commits.

### Reflection

Reflection on test is in ([reflections.md](https://github.com/UBC-MDS/DSCI-532_2026_26_TempTales/blob/dev/reflections.md))

#### Dashboard Strengths and Limitations

<!-- Standard (see General Guidelines): what the dashboard does well, current limitations,
     any intentional deviations from DSCI 531 visualization best practices. -->

Our dashboard transforms a relatively simple dataset of country-level average temperature measurements into interactive visualizations that enable users to explore long-term trends and compare countries. The project is data-rich, containing high-resolution measurements from 1850 to 2012, but the main challenge was communicating small but consequential signals, given that the overall global warming across the dataset is only approximately 1.9 °C. We therefore needed to be creative in our visualizations, to make gradual trends perceptible while avoiding misleading scales or cherry-picking of the data.

Because the dataset is large, converting the data to Parquet with DuckDB queries improved performance. Furthermore, it was a strength of the dashbaord to be able to present users with meaningfully patterns and comparisons across countries and time, rather than overwhelming them with raw temperature measurements alone.

One limitation of our dashboard is its deviation from its intended purpose of connecting historical events to temperature changes. In practice, this became less meaningful once we saw how small the absolute change in temperature between years was, and that pinpointing a single year with a single historical event became less impactful than looking at the overall timeframe on an informative scale.

#### Feedback prioritization

<!-- Trade-offs: one sentence on feedback prioritization - full rationale is in #<issue> and ### Changed above. -->

We prioritized feedback that was implementable and aligned with the dashboard’s design goals. Simple improvements such as refining map titles and improving layout consistency led us to reconsider the purpose and cohesion of several dashboard cards. Other feedback, such as incorporating historical context across visualizations, was considered but not implemented to avoid cluttering the temperature plots.

#### Relevance to Lecture Material

<!-- Most useful: which lecture, material, or feedback shaped your work most this milestone,
     and anything you wish had been covered. -->

It was useful to have a wide range of examples of tasks/app/functionality to draw from. Some of the shiny tasks are initially complex, but it was a strength of the course to focus more on flow, implementation, reactivity, and higher-level considerations rather than specific coding syntax. It was useful to see how a dashboard can start and then be gradually improved through the different milestones.

It was welcome that generative AI tools were incorporated into the course; if anything, additional skills on how to integrate these tools into coding workflows, such as with Claude Code, agents, etc., would be valuable, as this seems to be increasingly common in professional environments.

## [v0.3.0] (Milestone 3 - 2026-03-08)

### Added

- Implemented AI assistent tab with Chatbot and 3 output components
   - Queried Data Frame
   - *Time Series of Centred Temperature Data by Country* Plot
   - *Difference in Monthly Temperatures Between Reference and Target Years* Plot

### Changed

- Updated Dashboard: 
   - Re-arranged world heatmap, line plots and data table
   - Changed Heatmap background to white and changed to smaller size
   - Transposed data table (vertical to horizontal) for visual consistency

### Fixed

- N/A

### Known Issues

- N/A

### Reflection

- **Implemented AI Assistent Tab**
- **Revision**
    - updated dashboard tab layout based on Intructor's feedback
- **Followup for M4** 
    - close sidebar for user input/filters when in AI tab
    - optimization for AI tab output (narrow down to smaller dataset)

## [v0.2.0] (Milestone 2 - 2026-02-28)

### Added

- Job stories converted from M1 user stories with status tracking 
- New job stories for features implemented in M2 (e.g country highlighting on world heatmap, compact dashboard title)
- Complete component inventory table linking inputs, reactive calculations, and outputs to job stories
- Reactivity diagram (Mermaid) showing input -> reactive calc -> output flow
- Calculation details for each `@reactive.calc` including dependencies, transformations and outputs

### Changed

- Dashboard title updated to display country, selected years, and "Temp Comparison" in a compact format
- Seasonal temperature comparison logic updated to include changes between selected years.
- M1 spec revised to M2 spec to reflect new layouts, components, and job stories.
- Final layout updated from M1 sketch: added a collapsible sidebar for user inputs/filters, positioned the world heatmap at the top, and overlaid line plots and data table at the bottom (M1 had them in the opposite order).

### Fixed

- N/A

### Known Issues

- Zoom functionality on world heatmap for selected country is pending (planned for M3).
- Some reactive calculations may require performance optimization for larger datasets.

### Reflection

- **Implemented job stories:** #1, #3, #4, #6, #7  
- **Partially implemented / pending M3:** #5 (heatmap zoom)  
- The final layout now closely matches the M2 spec. Compared to the M1 sketch, key updates include:
  - A collapsible sidebar for user inputs/filters.
  - World heatmap positioned at the top with line plots and data table overlayed at the bottom (M1 had them reversed).
  - Left column cards showing data count, seasonal temperatures, and historical events.

## [v0.1.0] (Milestone 1 - 2026-02-14)

- Project set up
- Initial dashboard
