### 2.1 Updated Job Stories

Review your M1 job stories in light of your deployment setup and any new insights. Update or add stories as needed, and track their status:

| #   | Job Story                       | Status         | Notes                         |
| --- | ------------------------------- | -------------- | ----------------------------- |
| 1   | When I … I want to … so I can … | ✅ Implemented |                               |
| 2   | When I … I want to … so I can … | 🔄 Revised     | Changed from X to Y because … |
| 3   | When I … I want to … so I can … | ⏳ Pending M3  |                               |

### 2.2 Component Inventory

Plan every input, reactive calc, and output your app will have. Use this as a checklist during Phase 3. Minimum **2 components per team member** (6 for a 3-person team, 8 for a 4-person team), with **at least 2 inputs and 2 outputs**:

| ID            | Type          | Shiny widget / renderer | Depends on                   | Job story  |
| ------------- | ------------- | ----------------------- | ---------------------------- | ---------- |
| `input_year`  | Input         | `ui.input_slider()`     | —                            | #1, #2     |
| `filtered_df` | Reactive calc | `@reactive.calc`        | `input_year`, `input_region` | #1, #2, #3 |
| `plot_trend`  | Output        | `@render.plot`          | `filtered_df`                | #1         |
| `tbl_summary` | Output        | `@render.data_frame`    | `filtered_df`                | #2         |

### 2.3 Reactivity Diagram

```mermaid
flowchart TD
  C[Country] --> FB{{Filtered DF of Base Year}}
  C[Country] --> FS{{Filtered DF of Select Year}}
  B[Base Year] --> FB
  S[Select Year] --> FS
  C --> TITLE([title])
  B --> TITLE([title])
  S --> TITLE([title])
  B --> HIST([Historical Events])
  S --> HIST([Historical Events])
  FB --> YB([Base Year Average Temp])
  FS --> YS([Select Year Average Temp])
  FB --> ST([Seasonal Average Temp])
  FS --> ST([Seasonal Average Temp])
  FB --> MLP([Monthly Temp Line Chart])
  FS --> MLP([Monthly Temp Line Chart])
  FB --> WM([World Map Temp Difference])
  FS --> WM([World Map Temp Difference])
  C --> WM([World Map Temp Difference])
```

### 2.4 Calculation Details

For each `@reactive.calc` in your diagram, briefly describe:

- Which inputs it depends on.
- What transformation it performs (e.g., "filters rows to the selected year range and region(s)").
- Which outputs consume it.