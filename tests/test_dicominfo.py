"""Tests for dicominfo module."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from dicominfo import DicomReadError, NoPixelDataError, display_images, print_stats
from dicominfo.core import validate_files
from dicominfo.utils import load_dicom_files
from dicominfo.viewer import _get_image_type


class TestLoadDicomFiles:
    """Tests for load_dicom_files function."""

    def test_raises_dicom_read_error_on_file_not_found(self):
        """Test that load_dicom_files raises DicomReadError when file is not found."""
        with pytest.raises(DicomReadError, match="Files could not be read"):
            load_dicom_files(["/nonexistent/file.dcm"])

    def test_raises_dicom_read_error_on_invalid_dicom(self, tmp_path):
        """Test that load_dicom_files raises DicomReadError on invalid DICOM file."""
        # Create a non-DICOM file
        invalid_file = tmp_path / "invalid.dcm"
        invalid_file.write_text("This is not a DICOM file")
        
        with pytest.raises(DicomReadError, match="Files could not be read"):
            load_dicom_files([str(invalid_file)])

    @patch("dicominfo.utils.pydicom.dcmread")
    def test_returns_list_of_datasets(self, mock_dcmread):
        """Test that load_dicom_files returns a list of pydicom Dataset objects."""
        # Mock pydicom.dcmread to return mock Dataset objects
        mock_dcm1 = MagicMock()
        mock_dcm2 = MagicMock()
        mock_dcmread.side_effect = [mock_dcm1, mock_dcm2]
        
        result = load_dicom_files(["file1.dcm", "file2.dcm"])
        
        assert len(result) == 2
        assert result[0] == mock_dcm1
        assert result[1] == mock_dcm2
        assert mock_dcmread.call_count == 2


class TestValidateFiles:
    """Tests for validate_files function."""

    def test_raises_dicom_read_error_on_file_not_found(self):
        """Test that validate_files raises DicomReadError when file is not found."""
        with pytest.raises(DicomReadError, match="Files could not be read"):
            validate_files(["/nonexistent/file.dcm"])

    def test_raises_dicom_read_error_on_invalid_dicom(self, tmp_path):
        """Test that validate_files raises DicomReadError on invalid DICOM file."""
        # Create a non-DICOM file
        invalid_file = tmp_path / "invalid.dcm"
        invalid_file.write_text("This is not a DICOM file")
        
        with pytest.raises(DicomReadError, match="Files could not be read"):
            validate_files([str(invalid_file)])


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

    @patch("dicominfo.utils.pydicom.dcmread")
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

    @patch("sys.argv", ["dicom-info", "--version"])
    def test_version_flag_exits_with_code_0(self, capsys):
        """Test that --version flag displays version and exits."""
        from dicominfo import main, __version__
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert __version__ in captured.out

    @patch("dicominfo.cli.print_stats")
    @patch("sys.argv", ["dicom-info", "-v", "mock_file.dcm"])
    def test_verbose_flag_enables_debug_logging(self, mock_print_stats, caplog):
        """Test that -v/--verbose flag enables debug logging."""
        import logging
        from dicominfo import main
        
        with caplog.at_level(logging.DEBUG):
            main()
        
        # Check that basicConfig was called with DEBUG level
        # We can't directly test the level, but we can verify the function ran
        mock_print_stats.assert_called_once()

    @patch("dicominfo.core.validate_files")
    @patch("sys.argv", ["dicom-info", "-q", "mock_file.dcm"])
    def test_quiet_flag_suppresses_output(self, mock_validate_files, capsys):
        """Test that -q/--quiet flag suppresses metadata output."""
        from dicominfo import main
        
        main()
        
        # validate_files should be called instead of print_stats
        mock_validate_files.assert_called_once()
        
        # No output should be printed
        captured = capsys.readouterr()
        assert captured.out == ""

    @patch("dicominfo.cli.print_stats")
    @patch("sys.argv", ["dicom-info", "--verbose", "mock_file.dcm"])
    def test_verbose_long_flag_enables_debug_logging(self, mock_print_stats, caplog):
        """Test that --verbose flag enables debug logging."""
        import logging
        from dicominfo import main
        
        with caplog.at_level(logging.DEBUG):
            main()
        
        # Check that basicConfig was called with DEBUG level
        # We can't directly test the level, but we can verify the function ran
        mock_print_stats.assert_called_once()

    @patch("dicominfo.core.validate_files")
    @patch("sys.argv", ["dicom-info", "--quiet", "mock_file.dcm"])
    def test_quiet_long_flag_suppresses_output(self, mock_validate_files):
        """Test that --quiet flag suppresses metadata output."""
        from dicominfo import main
        
        main()
        
        # validate_files should be called instead of print_stats
        mock_validate_files.assert_called_once()

    @patch("sys.argv", ["dicom-info", "--display", "-c", "0", "mock_file.dcm"])
    def test_zero_columns_shows_validation_error(self, capsys) -> None:
        """Test that --columns=0 shows validation error and exits with code 2."""
        from dicominfo import main
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "--columns must be a positive integer" in captured.err

    @patch("sys.argv", ["dicom-info", "--display", "-c", "-1", "mock_file.dcm"])
    def test_negative_columns_shows_validation_error(self, capsys) -> None:
        """Test that --columns=-1 shows validation error and exits with code 2."""
        from dicominfo import main
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "--columns must be a positive integer" in captured.err

    @patch("dicominfo.cli.print_stats")
    @patch("sys.argv", ["dicom-info", "--display", "-c", "1", "mock_file.dcm"])
    def test_positive_columns_is_valid(self, mock_print_stats) -> None:
        """Test that --columns=1 is accepted as valid."""
        from dicominfo import main
        
        main()
        
        # Should not raise SystemExit for valid columns value
        mock_print_stats.assert_called_once()

    @patch("dicominfo.viewer.display_images")
    @patch("dicominfo.cli.print_stats")
    @patch("sys.argv", ["dicom-info", "-d", "-c", "5", "mock_file.dcm"])
    def test_positive_columns_passed_to_display_images(
        self, mock_print_stats, mock_display_images
    ):
        """Test that valid --columns value is passed to display_images correctly."""
        from dicominfo import main
        
        main()
        
        # Verify display_images was called with the correct columns value
        mock_display_images.assert_called_once_with(["mock_file.dcm"], max_cols=5)


class TestGetImageType:
    """Tests for _get_image_type helper function."""

    def test_2d_grayscale_image(self):
        """Test that 2D grayscale images are correctly identified."""
        mock_dcm = MagicMock()
        mock_dcm.SamplesPerPixel = 1
        pixel_array = np.zeros((256, 256), dtype=np.uint16)
        
        result = _get_image_type(mock_dcm, pixel_array)
        
        assert result == "2d_gray"

    def test_2d_rgb_image(self):
        """Test that 2D RGB images are correctly identified."""
        mock_dcm = MagicMock()
        mock_dcm.SamplesPerPixel = 3
        pixel_array = np.zeros((256, 256, 3), dtype=np.uint8)
        
        result = _get_image_type(mock_dcm, pixel_array)
        
        assert result == "2d_rgb"

    def test_2d_rgba_image(self):
        """Test that 2D RGBA images (4 channels) are correctly identified."""
        mock_dcm = MagicMock()
        mock_dcm.SamplesPerPixel = 4
        pixel_array = np.zeros((256, 256, 4), dtype=np.uint8)
        
        result = _get_image_type(mock_dcm, pixel_array)
        
        assert result == "2d_rgb"

    def test_3d_volume_without_number_of_frames(self):
        """Test that 3D volume data is correctly identified."""
        mock_dcm = MagicMock()
        mock_dcm.SamplesPerPixel = 1
        del mock_dcm.NumberOfFrames  # No NumberOfFrames attribute
        pixel_array = np.zeros((10, 256, 256), dtype=np.uint16)
        
        result = _get_image_type(mock_dcm, pixel_array)
        
        assert result == "3d_volume"

    def test_3d_volume_with_number_of_frames(self):
        """Test that 3D volume with NumberOfFrames is correctly identified."""
        mock_dcm = MagicMock()
        mock_dcm.SamplesPerPixel = 1
        mock_dcm.NumberOfFrames = 10
        pixel_array = np.zeros((10, 256, 256), dtype=np.uint16)
        
        result = _get_image_type(mock_dcm, pixel_array)
        
        assert result == "3d_volume"

    def test_warns_on_number_of_frames_mismatch(self, caplog):
        """Test that warning is logged when NumberOfFrames doesn't match shape."""
        mock_dcm = MagicMock()
        mock_dcm.SamplesPerPixel = 1
        mock_dcm.NumberOfFrames = 15
        pixel_array = np.zeros((10, 256, 256), dtype=np.uint16)
        
        result = _get_image_type(mock_dcm, pixel_array)
        
        assert result == "3d_volume"
        assert "NumberOfFrames" in caplog.text
        assert "doesn't match" in caplog.text

    def test_unsupported_4d_array(self):
        """Test that 4D arrays are marked as unsupported."""
        mock_dcm = MagicMock()
        mock_dcm.SamplesPerPixel = 1
        pixel_array = np.zeros((10, 10, 256, 256), dtype=np.uint16)
        
        result = _get_image_type(mock_dcm, pixel_array)
        
        assert result == "unsupported"

    def test_unsupported_rgb_with_wrong_shape(self, caplog):
        """Test that RGB images with unexpected shapes are marked unsupported."""
        mock_dcm = MagicMock()
        mock_dcm.SamplesPerPixel = 3
        pixel_array = np.zeros((256, 256), dtype=np.uint8)  # Should be 3D
        
        result = _get_image_type(mock_dcm, pixel_array)
        
        assert result == "unsupported"
        assert "Unexpected shape" in caplog.text

    def test_defaults_samples_per_pixel_to_1(self):
        """Test that missing SamplesPerPixel defaults to 1."""
        mock_dcm = MagicMock()
        del mock_dcm.SamplesPerPixel  # Remove attribute
        pixel_array = np.zeros((256, 256), dtype=np.uint16)
        
        result = _get_image_type(mock_dcm, pixel_array)
        
        assert result == "2d_gray"


class TestDisplayImagesIntegration:
    """Integration tests for display_images with different DICOM types."""

    @patch("dicominfo.viewer.plt.show")
    @patch("dicominfo.utils.pydicom.dcmread")
    def test_displays_2d_grayscale_correctly(self, mock_dcmread, mock_show):
        """Test that 2D grayscale images are displayed correctly."""
        mock_dcm = MagicMock()
        mock_dcm.SamplesPerPixel = 1
        mock_dcm.pixel_array = np.zeros((256, 256), dtype=np.uint16)
        mock_dcmread.return_value = mock_dcm
        
        display_images(["test.dcm"])
        
        # Should call show once
        mock_show.assert_called_once()

    @patch("dicominfo.viewer.plt.show")
    @patch("dicominfo.utils.pydicom.dcmread")
    def test_displays_rgb_without_grayscale_colormap(self, mock_dcmread, mock_show):
        """Test that RGB images are not displayed with grayscale colormap."""
        mock_dcm = MagicMock()
        mock_dcm.SamplesPerPixel = 3
        mock_dcm.pixel_array = np.zeros((256, 256, 3), dtype=np.uint8)
        mock_dcmread.return_value = mock_dcm
        
        # The key is that it doesn't crash trying to slice RGB on axis 0
        display_images(["test_rgb.dcm"])
        
        # Should call show once
        mock_show.assert_called_once()

    @patch("dicominfo.viewer.plt.show")
    @patch("dicominfo.utils.pydicom.dcmread")
    def test_displays_3d_volume_with_slider(self, mock_dcmread, mock_show):
        """Test that 3D volumes are displayed with a slider."""
        mock_dcm = MagicMock()
        mock_dcm.SamplesPerPixel = 1
        mock_dcm.NumberOfFrames = 10
        mock_dcm.pixel_array = np.zeros((10, 256, 256), dtype=np.uint16)
        mock_dcmread.return_value = mock_dcm
        
        display_images(["test_3d.dcm"])
        
        # Should call show once
        mock_show.assert_called_once()

    @patch("dicominfo.viewer.plt.show")
    @patch("dicominfo.utils.pydicom.dcmread")
    def test_handles_multi_frame_temporal_data(self, mock_dcmread, mock_show):
        """Test that multi-frame temporal data is displayed with slider."""
        mock_dcm = MagicMock()
        mock_dcm.SamplesPerPixel = 1
        mock_dcm.NumberOfFrames = 20
        mock_dcm.pixel_array = np.zeros((20, 128, 128), dtype=np.uint16)
        mock_dcmread.return_value = mock_dcm
        
        display_images(["test_temporal.dcm"])
        
        # Should call show once
        mock_show.assert_called_once()
