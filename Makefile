# Variables
ENV_NAME = 532_project
PYTHON = python
SHELL := /bin/bash

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
CYAN := \033[0;36m
RESET := \033[0m

.PHONY: help install db run

# Help command to list available commands
help:
	@echo -e "$(CYAN)Available commands:$(RESET)"
	@echo -e "  $(YELLOW)make install$(RESET)  - Create/Update the conda environment based on environment.yml"
	@echo -e "  $(YELLOW)make run$(RESET)      - Run the Shiny app in reload mode (development)"
	@echo -e "  $(YELLOW)make db$(RESET)       - Download and process the database"

# Create or update the conda environment
install:
	@echo -e "$(GREEN)Creating/updating conda environment $(ENV_NAME)...$(RESET)"
	@conda env update --file environment.yml --prune

db:
	@echo -e "$(CYAN)Downloading and updating database...$(RESET)"
	@$(PYTHON) src/data_loader.py
	@echo -e "$(CYAN)Processing data into pickle format...$(RESET)"
	@$(PYTHON) src/data_processor.py

# Run the Shiny app
# --reload requires 'watchdog' package and allows auto-restart on file save
run:
	@echo -e "$(GREEN)Running Shiny app in development mode...$(RESET)"
	@shiny run src/app.py --reload --launch-browser