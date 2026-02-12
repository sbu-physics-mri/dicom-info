"""Core DICOM file I/O and metadata extraction."""

# ruff: noqa: T201

from __future__ import annotations

import pydicom
import pydicom.errors

from dicominfo.exceptions import DicomReadError


def validate_files(files: list[str]) -> None:
    """Validate that DICOM files can be read without printing."""
    try:
        for f in files:
            pydicom.dcmread(f)

    except (FileNotFoundError, pydicom.errors.InvalidDicomError) as err:
        msg = f"Files could not be read due to {err}"
        raise DicomReadError(msg) from err


def print_stats(files: list[str]) -> None:
    """Print DICOM information for the files."""
    try:
        dcms = [pydicom.dcmread(f) for f in files]

    except (FileNotFoundError, pydicom.errors.InvalidDicomError) as err:
        msg = f"Files could not be read due to {err}"
        raise DicomReadError(msg) from err

    for f, dcm in zip(files, dcms, strict=True):
        banner = "*" * 5 + f" {f} " + "*" * 5
        print(banner, dcm, sep="\n")
