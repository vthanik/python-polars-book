"""Tests for clintools.demographics."""

from pathlib import Path

import polars as pl
import pytest

from clintools.demographics import subject_ae_summary
from clintools.exceptions import StudyDataError


def test_subject_ae_summary_returns_dataframe(synthetic_adsl, synthetic_adae):
    adsl_path, _ = synthetic_adsl
    adae_path, _ = synthetic_adae

    result = subject_ae_summary(adsl_path, adae_path)

    assert isinstance(result, pl.DataFrame)


def test_subject_ae_summary_only_safety_population(synthetic_adsl, synthetic_adae):
    adsl_path, adsl_df = synthetic_adsl
    adae_path, _ = synthetic_adae

    result = subject_ae_summary(adsl_path, adae_path)
    expected_n = adsl_df.filter(pl.col("SAFFL").eq("Y"))["USUBJID"].n_unique()

    assert len(result) == expected_n


def test_subject_ae_summary_correct_ae_count(synthetic_adsl, synthetic_adae):
    adsl_path, _ = synthetic_adsl
    adae_path, _ = synthetic_adae

    result = subject_ae_summary(adsl_path, adae_path)

    # Subject 01-001 has 2 AEs
    row = result.filter(pl.col("USUBJID").eq("01-001"))
    assert row["n_aes"].item() == 2


def test_subject_ae_summary_worst_severity(synthetic_adsl, synthetic_adae):
    adsl_path, _ = synthetic_adsl
    adae_path, _ = synthetic_adae

    result = subject_ae_summary(adsl_path, adae_path)

    # Subject 01-001 has MILD and MODERATE → worst should be MODERATE
    row = result.filter(pl.col("USUBJID").eq("01-001"))
    assert row["worst_severity"].item() == "MODERATE"

    # Subject 01-003 has SEVERE → worst should be SEVERE
    row = result.filter(pl.col("USUBJID").eq("01-003"))
    assert row["worst_severity"].item() == "SEVERE"


def test_subject_ae_summary_zero_aes(synthetic_adsl, synthetic_adae):
    adsl_path, _ = synthetic_adsl
    adae_path, _ = synthetic_adae

    result = subject_ae_summary(adsl_path, adae_path)

    # Subject 01-004 has no AEs in adae
    row = result.filter(pl.col("USUBJID").eq("01-004"))
    assert row["n_aes"].item() == 0


def test_subject_ae_summary_raises_on_missing_adsl(synthetic_adae, tmp_path):
    missing = tmp_path / "nonexistent_adsl.parquet"
    adae_path, _ = synthetic_adae

    with pytest.raises(StudyDataError, match="File not found"):
        subject_ae_summary(missing, adae_path)


def test_subject_ae_summary_raises_on_missing_adae(synthetic_adsl, tmp_path):
    adsl_path, _ = synthetic_adsl
    missing = tmp_path / "nonexistent_adae.parquet"

    with pytest.raises(StudyDataError, match="File not found"):
        subject_ae_summary(adsl_path, missing)


def test_subject_ae_summary_output_columns(synthetic_adsl, synthetic_adae):
    adsl_path, _ = synthetic_adsl
    adae_path, _ = synthetic_adae

    result = subject_ae_summary(adsl_path, adae_path)

    assert set(result.columns) == {"USUBJID", "TRT01A", "n_aes", "worst_severity"}
