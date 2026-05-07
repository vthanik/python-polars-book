# Modern Python for Clinical Programmers

A personal revision book for clinical programmers transitioning from R/SAS to Python.
Built around Polars (not pandas), `uv`, `pathlib`, and the `src/` layout.

## Structure

```
8 chapters across 4 parts:
  Part 1 (Ch 1-2):  Setup & IDE mastery
  Part 2 (Ch 3-5):  Python core — types, functions, classes
  Part 3 (Ch 6):    Library authoring — test, document, publish
  Part 4 (Ch 7-8):  Polars — expressions, lazy evaluation, window functions
```

## Setup

```powershell
# Install uv (once)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install Quarto CLI (once) — from quarto.org

# Install book dependencies
cd C:/Users/vt704670/repos/python_polars_book
uv sync --all-extras

# Fetch data (once)
uv run python scripts/00_fetch_pilot_data.py
uv run python scripts/01_fetch_dg_data.py

# Render the book
quarto render

# Install the clintools package (for Ch 6-8 examples)
uv pip install -e .

# Run tests
uv run pytest

# View API docs
uv run mkdocs serve
```

## Data

- `data/adam/` — synthetic CDISC pilot ADaM datasets (ADSL, ADAE, ADLBC, ADTTE) in parquet format
- `data/definitive_guide/` — general Polars examples from Janssens & Nieuwdorp

## Source books

- *Python for Data Analysis, 3E* — McKinney (chapter structure backbone)
- *Python Polars: The Definitive Guide* — Janssens & Nieuwdorp (Polars chapters, companion notebooks: github.com/jeroenjanssens/python-polars-the-definitive-guide)
