"""Tests for dicominfo module."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from dicominfo import DicomReadError, NoPixelDataError, display_images, print_stats


class TestPrintStats:
    """Tests for print_stats function."""

    def test_raises_dicom_read_error_on_file_not_found(self):
        """Test that print_stats raises DicomReadError when file is not found."""
        with pytest.raises(DicomReadError, match="Files could not be read"):
            print_stats(["/nonexistent/file.dcm"])

    def test_raises_dicom_read_error_on_invalid_dicom(self, tmp_path):
        """Test that print_stats raises DicomReadError on invalid DICOM file."""
        # Create a non-DICOM file
        invalid_file = tmp_path / "invalid.dcm"
        invalid_file.write_text("This is not a DICOM file")
        
        with pytest.raises(DicomReadError, match="Files could not be read"):
            print_stats([str(invalid_file)])


class TestDisplayImages:
    """Tests for display_images function."""

    def test_raises_dicom_read_error_on_file_not_found(self):
        """Test that display_images raises DicomReadError when file is not found."""
        with pytest.raises(DicomReadError, match="Files could not be read"):
            display_images(["/nonexistent/file.dcm"])

    def test_raises_dicom_read_error_on_invalid_dicom(self, tmp_path):
        """Test that display_images raises DicomReadError on invalid DICOM file."""
        # Create a non-DICOM file
        invalid_file = tmp_path / "invalid.dcm"
        invalid_file.write_text("This is not a DICOM file")
        
        with pytest.raises(DicomReadError, match="Files could not be read"):
            display_images([str(invalid_file)])

    @patch("dicominfo.viewer.pydicom.dcmread")
    def test_raises_no_pixel_data_error_when_no_pixel_data(self, mock_dcmread):
        """Test that display_images raises NoPixelDataError when files have no pixel data."""
        # Mock a DICOM file without pixel_array attribute
        mock_dcm = MagicMock()
        del mock_dcm.pixel_array  # Ensure pixel_array doesn't exist
        mock_dcmread.return_value = mock_dcm
        
        with pytest.raises(NoPixelDataError, match="No DICOM files with pixel data found"):
            display_images(["mock_file.dcm"])


class TestMain:
    """Tests for main CLI function."""

    @patch("dicominfo.cli.print_stats")
    @patch("sys.argv", ["dicom-info", "/nonexistent/file.dcm"])
    def test_exits_with_code_1_on_dicom_read_error(self, mock_print_stats, capsys):
        """Test that main exits with code 1 when DicomReadError is raised."""
        from dicominfo import main
        
        # Mock print_stats to raise DicomReadError
        mock_print_stats.side_effect = DicomReadError("Test error message")
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Test error message" in captured.out

    @patch("dicominfo.viewer.display_images")
    @patch("dicominfo.cli.print_stats")
    @patch("sys.argv", ["dicom-info", "-d", "mock_file.dcm"])
    def test_exits_with_code_1_on_no_pixel_data_error(
        self, mock_print_stats, mock_display_images, capsys
    ):
        """Test that main exits with code 1 when NoPixelDataError is raised."""
        from dicominfo import main
        
        # Mock display_images to raise NoPixelDataError
        mock_display_images.side_effect = NoPixelDataError("No pixel data")
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "No pixel data" in captured.out
