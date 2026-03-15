# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.4.0] (Milestone 4 - 2026-03-17)

### Added

- <!-- New features, components, tests - one line each. Reference PRs where relevant (e.g. #12). -->


### Changed

- <!-- Spec or design deviations, and motivation. -->
- <!-- Feedback items you addressed: "Addressed: <item description> (#<prioritization issue>) via #<PR>" -->

### Fixed

- <!-- Bugs resolved since M3. -->

- **Feedback prioritization issue link:** #...

### Known Issues

- Our historical PR's are missing comments.

### Release Highlight: [Name of your advanced feature]

<!-- One short paragraph describing what you built and what it does for the user. -->

- **Option chosen:** D
- **PR:** #88
- **Why this option over the others:** We thought this was the best option for an adavanced feature because it's an intuitive response for our dashboard's purpose. It allows user to intuitively filter the data by selecting countries directly from the visualization. This reduces the number of clicks and is in line with the side bar choices.
- **Feature prioritization issue link:** #86

### Collaboration

<!-- Summary of workflow or collaboration improvements made since M3. -->

- **CONTRIBUTING.md:** #97
- **M3 retrospective:** Biggest change is adding annotation to the PR appraisal and dividing coding tasks more evenly.
- **M4:** We used PR discussions more effectively, created issues first following by specific PRs completing those tasks, and avoided last minute commits.

### Reflection

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
