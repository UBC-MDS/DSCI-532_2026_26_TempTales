# DSCI-532_2026_26_TBD

*TEMPLATE TEXT BELOW*

## Project Purpose

### Use case examples

## Functions

## Get started

To install this package for use:

```bash
pip install -i 
```

To install this package for development:

```bash
git clone 
cd 
pip install -e
```

This project uses Hatch to manage environments, run tests, and build documentation
in a reproducible way via `pyproject.toml`.

To create the default development environment:

```bash
hatch env create
```

## Development environment (conda)

A conda environment is provided for development and testing.

To create the environment:

```bash
conda env create -f environment.yml
```

```bash
conda activate __
```

### Running Tests

To run the full test suite with coverage reporting:

```bash
hatch run test:run
```

### Code Style

The project uses ruff for formatting.

To check formatting

```bash
ruff check .
```

To format files:

```bash
ruff format .
```

## Documentation

### Build documentation locally

To generate the API reference pages using quartodoc:

```bash
quartodoc build --verbose
```

To render and preview the documentation:

```bash
quarto render
```

To preview the documentation locally:

```bash
quarto preview
```

## Continuous Integration

All tests, formatting checks, and documentation builds are automatically run
using GitHub Actions on pull requests and merges to `main`.

## Contributors

Contributors are expected to follow the guidelines outlined in **[CONTRIBUTING.md](./CONTRIBUTING.md)**. Please review this document before submitting issues or pull requests.

## Copyright

- Copyright © 2026 Emily Jin, Ian Gault, Purity Jangaya, Yusheng Li.
- Free software distributed under the [MIT License](./LICENSE).
