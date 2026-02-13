"""Utility functions for DICOM file I/O."""

from __future__ import annotations

# Type Checking
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

# Module imports
import pydicom
import pydicom.errors

from dicominfo.exceptions import DicomReadError


def load_dicom_files(files: list[str]) -> Sequence[pydicom.Dataset]:
    """
    Load DICOM files and return a list of pydicom Dataset objects.

    Args:
        files: List of file paths to DICOM files.

    Returns:
        List of pydicom Dataset objects.

    Raises:
        DicomReadError: If files cannot be read due to FileNotFoundError
            or InvalidDicomError.

    """
    try:
        dcms = [pydicom.dcmread(f) for f in files]
    except (FileNotFoundError, pydicom.errors.InvalidDicomError) as err:
        msg = f"Files could not be read due to {err}"
        raise DicomReadError(msg) from err

    return dcms
