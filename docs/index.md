# clintools

`clintools` is the capstone library built progressively through *Modern Python for Clinical Programmers*.

It demonstrates modern Python library authoring: `src/` layout, `pyproject.toml`, pytest, type hints, mkdocstrings, and pharma-grade traceability (input file hashing, structured logging).

## Quick start

```python
from pathlib import Path
from clintools import subject_ae_summary

result = subject_ae_summary(
    adsl_path=Path("data/adam/adsl.parquet"),
    adae_path=Path("data/adam/adae.parquet"),
)
print(result.head(5))
```

## Installation

```bash
uv pip install -e .
```
