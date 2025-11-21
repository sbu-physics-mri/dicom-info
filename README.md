# dicom-info

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

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
