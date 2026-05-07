"""
One-time script: download the public CDISC ADaM Pilot datasets (.xpt)
and convert them to Parquet for use in the book's examples.

Usage:
    uv run python scripts/00_fetch_pilot_data.py

Output:
    data/adam/adsl.parquet
    data/adam/adae.parquet
    data/adam/adlbc.parquet
    data/adam/adtte.parquet

Source: PHUSE/CDISC publicly available ADaM pilot submission data.
"""

from __future__ import annotations

import urllib.request
from pathlib import Path

import polars as pl
import pyreadstat

ADAM_DIR = Path(__file__).parent.parent / "data" / "adam"

# Public CDISC pilot ADaM datasets hosted on the CDISC/PHUSE GitHub.
# These are the same datasets used in the Pinnacle21/FDA example submission.
DATASETS = {
    "adsl": "https://raw.githubusercontent.com/phuse-org/phuse-scripts/master/data/adam/cdisc/adsl.xpt",
    "adae": "https://raw.githubusercontent.com/phuse-org/phuse-scripts/master/data/adam/cdisc/adae.xpt",
    "adlbc": "https://raw.githubusercontent.com/phuse-org/phuse-scripts/master/data/adam/cdisc/adlbc.xpt",
    "adtte": "https://raw.githubusercontent.com/phuse-org/phuse-scripts/master/data/adam/cdisc/adtte.xpt",
}

FALLBACK_DATASETS = {
    "adsl": "https://raw.githubusercontent.com/phuse-org/TestDataFactory/main/Updated/ADaM/adsl.xpt",
    "adae": "https://raw.githubusercontent.com/phuse-org/TestDataFactory/main/Updated/ADaM/adae.xpt",
}


def fetch_and_convert(name: str, url: str, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    xpt_path = dest_dir / f"{name}.xpt"
    parquet_path = dest_dir / f"{name}.parquet"

    if parquet_path.exists():
        print(f"  [skip] {parquet_path.name} already exists")
        return

    print(f"  [fetch] {name}.xpt from {url[:60]}...")
    try:
        urllib.request.urlretrieve(url, xpt_path)
    except Exception as e:
        print(f"  [warn] Failed to fetch {name}: {e}")
        if name in FALLBACK_DATASETS:
            print(f"  [retry] Trying fallback URL...")
            try:
                urllib.request.urlretrieve(FALLBACK_DATASETS[name], xpt_path)
            except Exception as e2:
                print(f"  [error] Fallback also failed: {e2}")
                return
        else:
            return

    df_pd, meta = pyreadstat.read_xport(str(xpt_path))
    df_pl = pl.from_pandas(df_pd)
    df_pl.write_parquet(parquet_path)
    xpt_path.unlink()
    print(f"  [done]  {parquet_path.name}  ({len(df_pl)} rows × {len(df_pl.columns)} cols)")


def main() -> None:
    print(f"Writing parquet files to: {ADAM_DIR}\n")
    for name, url in DATASETS.items():
        fetch_and_convert(name, url, ADAM_DIR)
    print("\nDone. Verify with:")
    print("  python -c \"import polars as pl; print(pl.read_parquet('data/adam/adsl.parquet').head(3))\"")


if __name__ == "__main__":
    main()
