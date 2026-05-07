"""
One-time script: download datasets from the Python Polars: The Definitive Guide
companion repository for use in general Polars exercises.

Usage:
    uv run python scripts/01_fetch_dg_data.py

Output:
    data/definitive_guide/{name}.{ext}
"""

from __future__ import annotations

import urllib.request
from pathlib import Path

DG_DIR = Path(__file__).parent.parent / "data" / "definitive_guide"

BASE = "https://raw.githubusercontent.com/jeroenjanssens/python-polars-the-definitive-guide/main/data"

FILES = [
    "penguins.csv",
    "starwars.parquet",
    "animals.csv",
    "fruit.csv",
    "transactions.csv",
    "tools.csv",
    "sales.csv",
    "nvda.csv",
    "asml.csv",
    "pokedex.json",
]


def fetch_file(filename: str, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / filename

    if dest.exists():
        print(f"  [skip] {filename} already exists")
        return

    url = f"{BASE}/{filename}"
    print(f"  [fetch] {filename}")
    try:
        urllib.request.urlretrieve(url, dest)
        size = dest.stat().st_size
        print(f"  [done]  {filename}  ({size:,} bytes)")
    except Exception as e:
        print(f"  [warn]  {filename}: {e}")


def main() -> None:
    print(f"Writing to: {DG_DIR}\n")
    for f in FILES:
        fetch_file(f, DG_DIR)
    print("\nDone.")


if __name__ == "__main__":
    main()
