"""Subject-level demographic and AE summary functions."""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path

import polars as pl

from clintools.exceptions import StudyDataError

logger = logging.getLogger(__name__)

_SEVERITY_RANK: dict[str, int] = {
    "MILD": 1,
    "MODERATE": 2,
    "SEVERE": 3,
    "LIFE-THREATENING": 4,
    "FATAL": 5,
}
_RANK_SEVERITY: dict[int, str] = {v: k for k, v in _SEVERITY_RANK.items()}


def subject_ae_summary(adsl_path: Path, adae_path: Path) -> pl.DataFrame:
    """Compute subject-level AE summary from ADSL and ADAE.

    Args:
        adsl_path: Path to adsl.parquet. Must contain USUBJID, TRT01A, SAFFL.
        adae_path: Path to adae.parquet. Must contain USUBJID, AESEV.

    Returns:
        One row per safety-population subject with columns:
        USUBJID, TRT01A, n_aes, worst_severity.

    Raises:
        StudyDataError: If a required file does not exist.
    """
    for path in (adsl_path, adae_path):
        if not path.exists():
            raise StudyDataError(f"File not found: {path}")

    for path in (adsl_path, adae_path):
        file_hash = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
        logger.info("Input: %s  sha256=%s", path.name, file_hash)

    result = (
        pl.scan_parquet(adsl_path)
        .filter(pl.col("SAFFL") == "Y")
        .select("USUBJID", "TRT01A")
        .join(
            pl.scan_parquet(adae_path).select("USUBJID", "AESEV"),
            on="USUBJID",
            how="left",
        )
        .with_columns(
            pl.col("AESEV")
            .replace_strict(_SEVERITY_RANK, default=0)
            .cast(pl.Int8)
            .alias("SEV_RANK")
        )
        .group_by("USUBJID", "TRT01A")
        .agg(
            pl.col("AESEV").drop_nulls().len().alias("n_aes"),
            pl.col("SEV_RANK").max().alias("worst_sev_rank"),
        )
        .with_columns(
            pl.col("worst_sev_rank")
            .replace_strict(_RANK_SEVERITY, default=None)
            .alias("worst_severity")
        )
        .drop("worst_sev_rank")
        .sort("USUBJID")
        .collect()
    )

    logger.info("subject_ae_summary: %d subjects in output", len(result))
    return result
