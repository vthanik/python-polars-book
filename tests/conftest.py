"""Shared pytest fixtures for clintools tests."""

import polars as pl
import pytest


@pytest.fixture
def synthetic_adsl(tmp_path) -> tuple:
    """Minimal ADSL-shaped parquet for testing."""
    df = pl.DataFrame({
        "USUBJID": [f"01-{i:03d}" for i in range(1, 11)],
        "SAFFL":   ["Y"] * 8 + ["N", "N"],
        "TRT01A":  ["Drug A", "Drug A", "Drug A", "Drug A", "Drug A",
                    "Placebo", "Placebo", "Placebo", "Drug A", "Placebo"],
        "AGE":     [65, 72, 58, 61, 70, 45, 53, 68, 77, 50],
        "SEX":     ["M", "F", "M", "F", "M", "F", "M", "F", "M", "F"],
    })
    path = tmp_path / "adsl.parquet"
    df.write_parquet(path)
    return path, df


@pytest.fixture
def synthetic_adae(tmp_path) -> tuple:
    """Minimal ADAE-shaped parquet for testing."""
    df = pl.DataFrame({
        "USUBJID": ["01-001", "01-001", "01-002", "01-003", "01-006"],
        "AETERM":  ["Nausea", "Rash", "Headache", "Fatigue", "Nausea"],
        "AESEV":   ["MILD", "MODERATE", "MILD", "SEVERE", "MILD"],
        "AEBODSYS":["GI disorders", "Skin", "Nervous system", "General", "GI disorders"],
    })
    path = tmp_path / "adae.parquet"
    df.write_parquet(path)
    return path, df
