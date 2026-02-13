"""Matplotlib visualization logic for DICOM images."""

from __future__ import annotations

# Typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.image import AxesImage
    from numpy import ndarray
    from pydicom import Dataset


# Python imports
import logging
from collections.abc import Callable
from pathlib import Path

# Module imports
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.axes_grid1 import make_axes_locatable

from dicominfo.exceptions import NoPixelDataError
from dicominfo.utils import load_dicom_files

logger = logging.getLogger(__name__)


def _get_image_type(dcm: Dataset, pixel_array: ndarray) -> str:
    """Determine the type of DICOM image based on metadata.

    Args:
        dcm: PyDICOM dataset object
        pixel_array: Numpy array of pixel data

    Returns:
        One of: "2d_gray", "2d_rgb", "3d_volume", "unsupported"

    """
    samples_per_pixel = getattr(dcm, "SamplesPerPixel", 1)
    num_frames = getattr(dcm, "NumberOfFrames", None)

    # RGB/Color images: SamplesPerPixel > 1 means color channels
    # Shape should be (height, width, 3) or (height, width, 4)
    if samples_per_pixel > 1:
        if len(pixel_array.shape) == 3 and pixel_array.shape[2] in (3, 4):  # noqa: PLR2004
            return "2d_rgb"
        logger.warning(
            "Unexpected shape %s for SamplesPerPixel=%d",
            pixel_array.shape,
            samples_per_pixel,
        )
        return "unsupported"

    # Grayscale images
    if len(pixel_array.shape) == 2:  # noqa: PLR2004
        return "2d_gray"

    # 3D data: could be multi-frame 2D (temporal/cine) or true 3D volume
    # For now, treat multi-frame as navigable slices
    if len(pixel_array.shape) == 3:  # noqa: PLR2004
        # Verify shape is consistent with NumberOfFrames if present
        if num_frames is not None and pixel_array.shape[0] != num_frames:
            logger.warning(
                "NumberOfFrames (%d) doesn't match pixel_array.shape[0] (%d)",
                num_frames,
                pixel_array.shape[0],
            )
        return "3d_volume"

    # 4D or higher dimensional data
    return "unsupported"


def display_images(files: list[str], max_cols: int | None = None) -> None:
    """Display DICOM images with interactive controls."""
    dcms = load_dicom_files(files)

    # Check if any files have pixel data
    files_with_pixels = [
        (f, dcm)
        for f, dcm in zip(files, dcms, strict=True)
        if hasattr(dcm, "pixel_array")
    ]

    if not files_with_pixels:
        msg = "No DICOM files with pixel data found."
        raise NoPixelDataError(msg)

    # Create figure with subplots for each image
    num_images = len(files_with_pixels)
    max_cols = int(num_images**0.5) if max_cols is None else max_cols
    cols = min(num_images, max_cols)
    rows = (num_images - 1) // cols + 1
    fig = plt.figure(figsize=(5 * cols, 4 * rows))

    # Store references to manage 3D sliders
    sliders = []
    axes_images: list[tuple[Axes, AxesImage, Slider | None, ndarray | None]] = []

    for idx, (filepath, dcm) in enumerate(files_with_pixels, start=1):
        pixel_array = dcm.pixel_array
        filename = Path(filepath).name

        # Determine image type based on DICOM metadata
        image_type = _get_image_type(dcm, pixel_array)

        if image_type == "2d_gray":
            # 2D grayscale image - simple display
            ax = fig.add_subplot(rows, cols, idx)
            im = ax.imshow(pixel_array, cmap="gray")
            ax.set_title(filename)
            ax.axis("off")
            plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
            axes_images.append((ax, im, None, None))

        elif image_type == "2d_rgb":
            # 2D RGB/color image - display without grayscale colormap
            ax = fig.add_subplot(rows, cols, idx)
            im = ax.imshow(pixel_array)
            ax.set_title(filename)
            ax.axis("off")
            axes_images.append((ax, im, None, None))

        elif image_type == "3d_volume":
            # 3D volume or multi-frame 2D - display with slider
            ax = fig.add_subplot(rows, cols, idx)

            # Start with the first slice/frame
            initial_slice = 0
            im = ax.imshow(pixel_array[initial_slice], cmap="gray")
            ax.set_title(
                f"{filename}\nSlice {initial_slice + 1}/{pixel_array.shape[0]}"
            )
            ax.axis("off")

            # Create slider axes to the right of the image
            divider = make_axes_locatable(ax)
            slider_ax = divider.append_axes("right", size="5%", pad=0.1)
            slider = Slider(
                slider_ax,
                "Slice",
                0,
                pixel_array.shape[0] - 1,
                valinit=initial_slice,
                valstep=1,
                orientation="vertical",
            )

            # Update function for slider
            def make_update(
                image_obj: AxesImage,
                axis: Axes,
                data: ndarray,
                fname: str,
                sldr: Slider,
            ) -> Callable[[float], None]:
                def update(val: float) -> None:
                    slice_idx = int(sldr.val)
                    image_obj.set_data(data[slice_idx])
                    axis.set_title(f"{fname}\nSlice {slice_idx + 1}/{data.shape[0]}")
                    fig.canvas.draw_idle()
                    logger.debug("Slider at slice %f for %s", val, fname)

                return update

            slider.on_changed(make_update(im, ax, pixel_array, filename, slider))
            sliders.append(slider)
            axes_images.append((ax, im, slider, pixel_array))

        else:
            # Unsupported dimensions
            logger.warning(
                "%s has unsupported dimensions: %s", filename, pixel_array.shape
            )

    plt.tight_layout()
    if len(files_with_pixels) == 1 and axes_images[0][2] is not None:
        # Adjust layout for single 3D image with slider
        plt.subplots_adjust(bottom=0.15)

    plt.show()
