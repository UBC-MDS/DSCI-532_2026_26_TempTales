# TempTales: Climate Change Explorer Dashboard

| | |
| :--- | :--- |
| **License** | [![License](https://img.shields.io/github/license/ubc-mds/dsci-532_2026_26_tbd?label=License)](LICENSE) |
| **Python** | [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) |
| **Status** | [![Repo Status](https://img.shields.io/badge/repo%20status-Active-brightgreen)](https://github.com/ubc-mds/dsci-532_2026_26_tbd) |
## Overview

**TempTales** is an interactive dashboard that allows users to explore global and country-level temperature trends over time while connecting these trends to major historical events. Users can select a country, view seasonal and monthly temperature patterns, and see how significant events like industrialization or world wars align with temperature changes. A world heatmap provides a spatial view of temperatures for selected years, making regional patterns immediately clear. This tool consolidates climate data from over two centuries into a user-friendly interface for researchers, students, policy makers, and environmentally conscious individuals.

Deployed Dashboard URLs: 
main branch: https://connect.posit.cloud/purityj/content/019c9116-f7e7-177d-42c7-e2e3b140264c
dev branch: https://019c9879-5ec6-dc91-2d43-ec77c0e6fdac.share.connect.posit.cloud

## Table of Contents
- [TempTales: Climate Change Explorer Dashboard](#temptales-climate-change-explorer-dashboard)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Project Directory Structure](#project-directory-structure)
  - [Installation](#installation)
  - [Usage (Makefile Guide)](#usage-makefile-guide)
    - [Initialization](#initialization)
    - [Running the App](#running-the-app)
    - [Cleaning Data](#cleaning-data)
  - [Developer Setup](#developer-setup)
  - [Contributing](#contributing)
  - [Contributors](#contributors)
  - [Copyright](#copyright)

## Features

- Place Holder

## Project Directory Structure

The core logic of the project is located in the `src/` directory.

```text
├── data/                   # Data storage
│   ├── raw/                # Raw data (downloaded via make db)
│   ├── processed/          # Processed pickle files (generated via make db)
│   └── figures/            # Static analysis figures
├── img/                    # Images used in README (e.g., sketches)
├── notebooks/              # Jupyter Notebooks for EDA and prototyping
├── reports/                # Project proposals and reports
├── src/                    # Source code
│   ├── app.py              # Main entry point for the Shiny App
│   ├── data_loader.py      # Script to download and update the database
│   └── data_processor.py   # Script to clean and transform data
├── environment.yml         # Conda environment configuration
├── Makefile                # Project automation scripts
└── README.md               # Main project documentation

```

## Installation

This project uses `conda` for dependency management. Ensure you have Anaconda or Miniconda installed.

```bash
# Clone the repository
$ git clone https://github.com/UBC-MDS/DSCI-532_2026_26_TBD.git

# Navigate to the project directory
$ cd DSCI-532_2026_26_TBD

# Create the environment using Makefile
$ make install
```

## Usage (Makefile Guide)

This project uses `make` to automate common tasks. Below is a guide to the available commands:

### Initialization

Before running the app for the first time, you must download and process the data:

```bash
$ make db
```

This command runs `src/data_loader.py` to download the data and `src/data_processor.py` to convert it into the required format.

### Running the App

To start the **Shiny** app in development mode:

```bash
$ make run
```

This enables reload mode (auto-restart on file save) and automatically launches the app in your browser.

### Cleaning Data

If you need to reset the data environment (delete all raw and processed data files):

```bash
$ make clean
```

**Note**: This command will prompt for confirmation (`y/N`) to prevent accidental deletion.

## Developer Setup

If you wish to contribute to the project, please follow these steps:

1. Clone the repository to your local machine.
2. Create the conda environment: `make install`.
3. Activate the environment: `conda activate 532_project`.
4. Run the app locally using `make run` to test changes.

## Contributing

Contributors are expected to follow the guidelines outlined in **[CONTRIBUTING.md](./CONTRIBUTING.md)**. Please review this document before submitting issues or pull requests.

## Contributors

Emily Jin, Ian Gault, Purity Jangaya, Yusheng Li

## Copyright

- Copyright © 2026 Emily Jin, Ian Gault, Purity Jangaya, Yusheng Li.
- Free software distributed under the [MIT License](./LICENSE).
