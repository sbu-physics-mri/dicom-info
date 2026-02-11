"""Custom exception classes for dicom-info."""

from __future__ import annotations


class DicomInfoError(Exception):
    """Base exception for dicom-info errors."""

    pass


class DicomReadError(DicomInfoError):
    """Exception raised when DICOM files cannot be read."""

    pass


class NoPixelDataError(DicomInfoError):
    """Exception raised when DICOM files have no pixel data."""

    pass
