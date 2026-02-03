"""Main entry point into the dicom-info CLI."""

# ruff: noqa: T201

from __future__ import annotations

# Typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.image import AxesImage
    from numpy import ndarray


# Python imports
import argparse
import logging
import sys
from pathlib import Path
from typing import Callable

# Module imports
import matplotlib.pyplot as plt
import pydicom
import pydicom.errors
from matplotlib.widgets import Slider
from mpl_toolkits.axes_grid1 import make_axes_locatable

logger = logging.getLogger(__name__)


def print_stats(files: list[str]) -> None:
    """Print DICOM information for the files."""
    try:
        dcms = [pydicom.dcmread(f) for f in files]

    except (FileNotFoundError, pydicom.errors.InvalidDicomError) as err:
        print(f"Files could not be read due to {err}")
        sys.exit(1)

    for f, dcm in zip(files, dcms, strict=True):
        banner = "*" * 5 + f" {f} " + "*" * 5
        print(banner, dcm, sep="\n")


def display_images(
    files: list[str],
    max_cols: int | None = None,
) -> None:
    """Display DICOM images with interactive controls."""
    try:
        dcms = [pydicom.dcmread(f) for f in files]

    except (FileNotFoundError, pydicom.errors.InvalidDicomError) as err:
        print(f"Files could not be read due to {err}")
        sys.exit(1)

    # Check if any files have pixel data
    files_with_pixels = [
        (f, dcm) for f, dcm in zip(files, dcms, strict=True)
        if hasattr(dcm, "pixel_array")
    ]

    if not files_with_pixels:
        print("No DICOM files with pixel data found.")
        sys.exit(1)

    # Create figure with subplots for each image
    num_images = len(files_with_pixels)
    max_cols = int(num_images ** .5) if max_cols is None else max_cols
    cols = min(num_images, max_cols)
    rows = (num_images - 1) // cols + 1
    fig = plt.figure(figsize=(5 * cols, 4 * rows))

    # Store references to manage 3D sliders
    sliders = []
    axes_images: list[
        tuple[Axes, AxesImage, Slider | None, ndarray | None]
    ] = []

    for idx, (filepath, dcm) in enumerate(files_with_pixels, start=1):
        pixel_array = dcm.pixel_array
        filename = Path(filepath).name

        # Determine if 2D or 3D
        if len(pixel_array.shape) == 2: # noqa: PLR2004
            # 2D image - simple display
            ax = fig.add_subplot(rows, cols, idx)
            im = ax.imshow(pixel_array, cmap="gray")
            ax.set_title(filename)
            ax.axis("off")
            plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
            axes_images.append((ax, im, None, None))

        elif len(pixel_array.shape) == 3: # noqa: PLR2004
            # 3D image - display with slider
            ax = fig.add_subplot(rows, cols, idx)

            # Start with the first slice
            initial_slice = 0
            im = ax.imshow(pixel_array[initial_slice], cmap="gray")
            ax.set_title(
                f"{filename}\nSlice {initial_slice + 1}/{pixel_array.shape[0]}",
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
                    axis.set_title(
                        f"{fname}\nSlice {slice_idx + 1}/{data.shape[0]}",
                    )
                    fig.canvas.draw_idle()
                    logger.debug("Slider at slice %f for %s", val, fname)

                return update

            slider.on_changed(
                make_update(im, ax, pixel_array, filename, slider),
            )
            sliders.append(slider)
            axes_images.append((ax, im, slider, pixel_array))

        else:
            logger.warning(
                "%s has unsupported dimensions: %s",
                filename,
                pixel_array.shape,
            )

    plt.tight_layout()
    if len(files_with_pixels) == 1 and axes_images[0][2] is not None:
        # Adjust layout for single 3D image with slider
        plt.subplots_adjust(bottom=0.15)

    plt.show()


def main() -> None:
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Print DICOM file information.",
     )

    parser.add_argument(
        "file",
        help="Path to the DICOM file(s).",
        nargs="+",
        type=str,
    )

    parser.add_argument(
        "-d",
        "--display",
        help="Display DICOM images instead of printing metadata.",
        action="store_true",
    )

    parser.add_argument(
        "-c",
        "--columns",
        help="Maximum number of columns for image display.",
        type=int,
        default=None,
    )

    args = parser.parse_args()

    # Display images or print dicom info
    if args.display:
        display_images(args.file, max_cols=args.columns)
    else:
        print_stats(args.file)


if __name__ == "__main__":
    main()
