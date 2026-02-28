# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.2.0] (Unreleased)

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
