# Variables
ENV_NAME = 532_project
PYTHON = python

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
CYAN := \033[0;36m
RESET := \033[0m

.PHONY: help install run

# Help command to list available commands
help:
	@echo -e "$(CYAN)Available commands:$(RESET)"
	@echo -e "  $(YELLOW)make install$(RESET)  - Create/Update the conda environment based on environment.yml"
	@echo -e "  $(YELLOW)make run$(RESET)      - Run the Shiny app in reload mode (development)"

# Create or update the conda environment
install:
	@echo -e "$(CYAN)Creating/updating conda environment $(ENV_NAME)..."
	conda env update --file environment.yml --prune

# Run the Shiny app
# --reload requires 'watchdog' package and allows auto-restart on file save
run:
	@echo -e "$(CYAN)Running Shiny app in development mode..."
	shiny run src/app.py --reload --launch-browser