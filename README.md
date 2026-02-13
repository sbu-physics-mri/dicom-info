# dicom-info

[![CI](https://github.com/sbu-physics-mri/dicom-info/actions/workflows/ci.yml/badge.svg)](https://github.com/sbu-physics-mri/dicom-info/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checking: mypy](https://img.shields.io/badge/type%20checking-mypy-blue.svg)](https://github.com/python/mypy)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A command-line tool for displaying DICOM file information.

## Description

dicom-info is a simple Python utility that reads and displays information from DICOM (Digital Imaging and Communications in Medicine) files. It provides a straightforward way to inspect DICOM file metadata from the command line, and can also display DICOM images interactively.

## Requirements

- Python >= 3.13
- pydicom >= 3.0.1
- matplotlib >= 3.7.0 (for image display)
- numpy >= 1.24.0 (for image display)

## Installation

With uv:

```bash
uvx dicom-info
```

or pip

```bash
pip install dicom-info
```

## Usage

The basic syntax is:

```
dicom-info FILE [FILE ...]
```

### Displaying Metadata

To display DICOM file metadata:

```bash
dicom-info path/to/file.dcm
dicom-info file1.dcm file2.dcm file3.dcm
```

The tool will display information for each DICOM file, including all available metadata and attributes.

### Displaying Images

To display DICOM images interactively, use the `--display` or `-d` flag:

```bash
dicom-info --display path/to/file.dcm
dicom-info -d file1.dcm file2.dcm file3.dcm
```

Image display features:
- **2D images**: Displayed as grayscale plots with a colorbar
- **3D images**: Displayed with an interactive slider to navigate through slices
- **Multiple files**: Each image is shown in its own subplot with the filename as the title

## Error Handling

The tool will exit with status code 1 if:
- Files are not found
- Files are not valid DICOM files
- When using `--display`, if no files contain pixel data

## License

This project is licensed under the GNU GPL version 3 license which can be found [here](LICENSE).

## Development

### Setup

This project uses [uv](https://astral.sh/uv) for dependency management. To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/sbu-physics-mri/dicom-info.git
cd dicom-info

# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install the package with dev dependencies
make install
```

### Running Tests and Checks

This project uses a Makefile as the single source of truth for development commands. All commands can be run locally and are also used in CI.

```bash
# Run all CI checks (format, lint, type, coverage)
make ci

# Individual commands:
make lint      # Run ruff linting
make format    # Check code formatting
make type      # Run mypy type checking
make test      # Run pytest
make coverage  # Run tests with coverage report (80% minimum)

# Apply fixes:
make fix       # Auto-fix linting issues and apply formatting
```

### CI/CD

The project uses GitHub Actions for continuous integration. On every pull request and push to `main`, the following checks run in parallel:
- **lint**: Code quality checks with ruff
- **format**: Code formatting validation
- **type**: Type checking with mypy
- **test**: Test suite with coverage (minimum 80%)

All checks must pass before merging.

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
