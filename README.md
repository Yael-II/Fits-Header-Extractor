<!--[TLP:WHITE] FROM 2025-01-13-->

# FITS Header Extractor and Curator With Python
Author: Moussouni, Yaël (MSc student; yael.moussouni@etu.unistra.fr)

Institution: Université de Strasbourg, CNRS, Observatoire astronomique de Strasbourg, UMR 7550, F-67000 Strasbourg, France

Date: 2025-01-13

**Moved to https://codeberg.org/Yael-II/Fits-Header-Extractor/**
## Abstract

[FITS](https://en.wikipedia.org/wiki/FITS/) files are widely used in astronomy. The content of a FITS file is in two parts: the header and the data. The goal of this Python package is to explore FITS header. To this end, I created a python library: `fits_header_extractor`, providing a `FitsHeaderExtractor` class, and a notebook (see [this repository](https://github.com/Yael-II/MSc2-Project-FITS)).

## Requirements

The library requires `python` (tested with version 3.13.1), `setuptools`, `git`, a `bash` interpreter (`/usr/bin/env bash` by default), and at least 530 kiB of available space.

## Installation

1. **Create a virtual environment (optional):** Simply run `python3 -m venv venv` in your working directory. Then, activate this environment with `./venv/bin/activate`. You can deactivate the virtual environment with the `deactivate` command.
2. **Install the package:** The package can be installed from Github with pip and git, run (in your environment):
```bash
pip install git+https://github.com/Yael-II/Fits-Header-Extractor
```

## The `fits_header_extractor` library and `FitsHeaderExtractor` class
The `fits_header_extractor` contains a `FitsHeaderExtractor` class that can be imported in Python, and a new instance of the class invoked with:
```python
from fits_header_extractor import FitsHeaderExtractor
fhe = FitsHeaderExtractor()
```

To test the class, simply run:
```python
fhe.ping()
```
This should return `0` (and print `pong`).

## Documentation of the FitsHeaderExtractor class

### Variables

A number of variables are accessible but should not be modified directly or errors may be generated;
- `self.in_dir`: input directory (`str`, `./Input/` by default)
- `self.out_dir`: output directory (`str`, `./Output/` by default) - not used
- `self.header_list`: list of headers (list[astropy.io.fits.header.Header])
- `self.file_list`: list of files (`list` of `str`)
- `self.wcs_list`: list of WCS (`list` of `astropy.wcs.wcs.WCS`)
- `self.info_list`: list of other informations (`list` of `dict`)
- `self.moc_list`: list of MOC (`list` of `mocpy.moc.moc.MOC`)

The elements of `self.wcs_list` are dictionaries in the format: `{card: value}`, with cards in `OBJECT`, `OBJECT_NAME` (resolved) `DATE-OBS` (in ISO format), `EXPTIME`, `INSTRUME`, and `TELESCOP`

### Methods

- `__init__(in_dir, out_dir)`: Class initialization, setting the input directory and output directory variables
    - Parameters
        - `in_dir: str` (optional): input directory path (by default, `./Input/`) 
        - `out_dir: str` (optional): output directory path (by default, `./Output/`) - is not used in the current version

- `ping()`: A quick test, prints `pong`, and returns 0

- `status()`: Prints most the internal variables

- `print_header(index)`: Prints the content of one or multiple headers
    - Parameters
        - `index: int|list` (optional): index or list of indexes of headers to print (by default: None; prints all the header available)

- `get_index(name)`: Gives the index of the header from its name. Returns 
    - Parameters
        - `name: str`: name of the header to retrieve
    - Returns
        - `index` the index of the file `name` in the file list `self.file_list`

- `extract_header(filename, verbatim)`: Extracts the header from a file in the input directory
    - Parameters
        - `filename: str`: name of the FITS file to open. Must contain `.fit` or `.fits` (else, `.fit` is assumed)
        - `verbatim:bool` (optional): define the level of verbosity (see "Verbosity" section)
    - Returns
        - `head`: the header of the file (in the Astropy format); returns `None` if an error occurred.

- `extract_header_directory(verbatim):` Same as `extract_header()`, but for all FITS files in a directory
    - Parameters
        - `verbatim:bool` (optional): Define the level of verbosity (see "Verbosity" section)
    - Returns
        - `head`: the header of the file (in the Astropy format); returns `None` if an error occurred.

- `curate(resolve_name, verbatim)`: Curate the headers in the `self.header_list` into `self.WCS_list` and `self.info_list`
    - Parameters
        - `resolve_name: bool`: select if the object names should be resolved (using [Sesame](https://cds.unistra.fr/cgi-bin/Sesame))
        - `verbatim:bool` (optional): Define the level of verbosity (see "Verbosity" section)

- `make_moc(verbatim)`: Creates a MOC for each files in the file list
    - Parameters
        - `verbatim:bool` (optional): Define the level of verbosity (see "Verbosity" section)

- `is_in_wcs(sky_coord, index)`: Returns a Boolean describing if coordinates are in one of the WCS.
    - Parameters
        - `sky_coord: SkyCoord`: an `astropy.SkyCoord` object with the test coordinates
        - `index: int|list` (optional): an index or list of indexes of FITS files to consider (by default, all the files are tested)
    - Returns
        - `inside_list`: a list of Boolean, the same shape as index, with the values `True` (inside), `False` (outside) or `None` (Error)

- `get_footprint(index)`: Returns the footprint of a MOC from its index 
    - Parameters
        - `index: int|list` (optional): an index or list of indexes of FITS files to consider (by default, all the files are tested)
    - Returns
        - `footprints`: a list of footprints, the same shape as index (None if no footprint), where each element is a (4, 2) array of (x, y) coordinates, in clockwise order, starting with the bottom left corner.

## Verbosity

The `verbatim` arguments can be used to select the level of verbosity:
- 🟦 Info: only shown if `verbatim` is `True` (e.g. steps, success)
- 🟨 Warning: only shown if `verbatim` is `True` (e.g. non-standard format found, but corrected with no ambiguity)
- 🟥 Error: always shown. (e.g. non-standard format is not recognized, the file is ignored)

## Limitation and Corrections

The limitation of this package are the same as for `astropy.io`, except for date format, which are corrected manually and always set to ISO format. In particular, `DD/MM/YY` format is detected and corrected for ISO format, assuming 19YY if `YY ≥ 50` and `20YY` if `YY < 50`.

## Licence

**Fits Header Extractor [and Curator With Python]**

Copyright (C) 2025 Yaël Moussouni (yael.moussouni@etu.unistra.fr)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see [www.gnu.org/licenses/](https://www.gnu.org/licenses/).

## Acknoledgments

This work made use of [Astropy](http://www.astropy.org), a community-developed core Python package and an ecosystem of tools and resources for astronomy ([2013A&A...558A..33A](https://ui.adsabs.harvard.edu/abs/2013A%26A...558A..33A/abstract), [2018AJ....156..123A](https://ui.adsabs.harvard.edu/abs/2018AJ....156..123A/abstract), [2022ApJ...935..167A](https://ui.adsabs.harvard.edu/abs/2022ApJ...935..167A/abstract)); [MOCpy](https://github.com/cds-astro/mocpy/), a Python library developed by the CDS to easily create and manipulate MOCs; and [Numpy](https://numpy.org/), a fundamental package for scientific computing in Python ([DOI:10.1038/s41586-020-2649-2](https://doi.org/10.1038/s41586-020-2649-2)).

This project has been started in the context of a MSc2 Python project, at the Observatoire astronomique de Strasbourg.

The processing of one file without Sesame name resolving request takes around `0.34 s` (elapsed real time), with a `6.3 %` CPU load on a 2020 Apple M1.
