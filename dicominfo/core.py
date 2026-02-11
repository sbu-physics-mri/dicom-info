"""Core DICOM reading and metadata extraction functionality."""

# ruff: noqa: T201

from __future__ import annotations

# Typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pydicom

# Python imports
import logging

# Module imports
import pydicom as _pydicom
import pydicom.errors

from dicominfo.exceptions import DicomReadError

logger = logging.getLogger(__name__)


def read_dicom_files(files: list[str]) -> list[pydicom.FileDataset]:
    """Read DICOM files and return a list of datasets.
    
    Args:
        files: List of file paths to read.
        
    Returns:
        List of DICOM datasets.
        
    Raises:
        DicomReadError: If files cannot be read.
    """
    try:
        return [_pydicom.dcmread(f) for f in files]
    except (FileNotFoundError, _pydicom.errors.InvalidDicomError) as err:
        raise DicomReadError(f"Files could not be read due to {err}") from err


def print_stats(files: list[str]) -> None:
    """Print DICOM information for the files.
    
    Args:
        files: List of file paths to print stats for.
        
    Raises:
        DicomReadError: If files cannot be read.
    """
    dcms = read_dicom_files(files)

    for f, dcm in zip(files, dcms, strict=True):
        banner = "*" * 5 + f" {f} " + "*" * 5
        print(banner, dcm, sep="\n")
