"""Custom exception classes for dicom-info."""

from __future__ import annotations


class DicomInfoError(Exception):
    """Base exception for dicom-info errors."""


class DicomReadError(DicomInfoError):
    """Exception raised when DICOM files cannot be read."""


class NoPixelDataError(DicomInfoError):
    """Exception raised when DICOM files have no pixel data."""

