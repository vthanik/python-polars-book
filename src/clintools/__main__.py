"""CLI entry point: python -m clintools"""

import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python -m clintools <adsl.parquet> <adae.parquet>")
        sys.exit(1)

    from clintools.demographics import subject_ae_summary

    adsl_path = Path(sys.argv[1])
    adae_path = Path(sys.argv[2])
    result = subject_ae_summary(adsl_path, adae_path)
    print(result)


if __name__ == "__main__":
    main()
