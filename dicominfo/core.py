"""Core DICOM file I/O and metadata extraction."""

# ruff: noqa: T201

from __future__ import annotations

from dicominfo.utils import load_dicom_files


def validate_files(files: list[str]) -> None:
    """Validate that DICOM files can be read without printing."""
    load_dicom_files(files)


def print_stats(files: list[str]) -> None:
    """Print DICOM information for the files."""
    dcms = load_dicom_files(files)

    for f, dcm in zip(files, dcms, strict=True):
        banner = "*" * 5 + f" {f} " + "*" * 5
        print(banner, dcm, sep="\n")
