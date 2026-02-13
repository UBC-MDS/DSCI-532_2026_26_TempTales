# Milestone 1 Proposal

## Section 1: Motivation and Purpose

### Target Audience

**Our role:** Data analyst and environmental consultant.

**Target audience:** Students, researchers, policy makers, and environmentally conscious individuals interested in exploring climate change trends and their relation to major historical events.

### Problem

Climate change is a complex, long-term phenomenon influenced by multiple human and natural factors. For most audiences, it is challenging to navigate large climate datasets and understand how global and country-level temperatures have evolved over time.

Additionally, connecting these temperature trends to historical events—such as industrialization, wars, or global environmental agreements—can be difficult. This makes it hard for users to answer questions such as:

    - How have global and country-level temperatures evolved over the last two centuries?
    - How do significant historical events align with trends in climate data?
    - Which countries have experienced the most warming?

### Solution

Our interactive dashboard will allow users to explore global and country-level temperature trends over time while connecting these trends to major historical events. Features include:

- Time series visualizations of global and country-level temperatures, showing long-term trends and seasonal variations.
- Country selection to compare trends across countries and examine seasonal patterns for a specific year.
- Historical event markers to contextualize periods of accelerated warming and provide insight into potential associations.
- World heatmaps to visualize global and country-level temperatures for selected year(s) and country, making spatial patterns immediately clear.

By consolidating complex climate datasets into a user-friendly, interactive dashboard, our tool enables the audience to quickly explore patterns, compare countries, and understand how historical events coincide with changes in climate, supporting informed conclusions without requiring manual data analysis.

## Section 2: Description of the Data

rubric={reasoning:8}

Describe the dataset you finalized in Step 1.

- **Stats:** Number of rows/columns.
- **Relevance:** How variables potentially link to the problem.

## Section 3: Research Questions & Usage Scenarios

### Persona

Anna is a climate researcher interested in understanding how global warming has evolved across countries over time and how major historical events may have influenced temperature trends. She is comfortable exploring data but wants a visual, interactive tool that allows her to quickly identify trends, compare countries and contextualize these trends with historical events, without manually processing large datasets.

### Usage Scenario

Anna opens the “Climate Change Explorer” dashboard to investigate climate trends for Canada. On the left, she selects Germany from the country dropdown, and sees a data card showing the number of data used. Below it, the historical event card updates automatically as she adjusts the year slider at the top right, showing major events like World War I or II for the selected year.

She then examines the seasonal temperature card to see how temperatures vary across winter, spring, summer, and fall in the selected country and year. Below the year slider, the monthly trendline chart displays the selected country’s temperature pattern throughout the month/year. Finally, Anna observes the world heatmap at the bottom right, which visualizes the country’s temperature in a global context, allowing her to compare regional and global warming patterns.

This workflow lets Anna explore, contextualize, and compare temperature trends interactively, enabling her to investigate correlations between historical events and climate changes efficiently.

### User Stories

**User Story 1**

As a climate researcher, I want to select a country and view its seasonal and monthly temperature trends for a specific year, so that I can analyze climate patterns over time.

**User Story 2**

As a climate researcher, I want to see historical events associated with the selected year, so that I can contextualize unusual trends or anomalies in temperature data.

**User Story 3**

As a climate researcher, I want to visualize a world heatmap showing the selected country’s temperature for the selected year, so that I can compare regional and global temperature patterns.

### Section 4: Exploratory Data Analysis

rubric={reasoning:10}

Demonstrate that your data can actually support your user stories.

- Select **one** of your User Stories/JTBD from Section 3.
- Create a Jupyter notebook in the `notebooks/` folder (e.g., `notebooks/eda_analysis.ipynb`).
  - Create 1-2 static visualizations or summary tables that directly address the user's task.
- In your proposal document (this section), briefly explain what the visualization shows and how comparing these values specifically supports the user's decision-making.
  - _(Include the relevant plots or a link to the notebook in this section)._

### Section 5: App Sketch & Description

rubric={viz:8,reasoning:4}

- **Sketch:** A visual mockup showing layout and components (hand-drawn or software-generated). Save it as `img/sketch.png` and embed it in your proposal markdown file (e.g., `![Sketch](../img/sketch.png)`).
- **Description:** High-level explanation of interface components and interactions (landing page, filters, charts).
