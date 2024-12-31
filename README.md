# Fits Header Extractor and Curator With Python

## Abstract

[Fits](https://en.wikipedia.org/wiki/FITS) are widely used file formats in astronomy. The content of the file is in two parts: the header and the data. The goal of this Python project is to explore fits header. To this end, I created a python library: `fits_header_extractor`, providing a `FitsHeaderExtractor` class, and a notebook.

## Requirements

The library requires `python` (tested with version 3.13.1), with the `venv` module and `pip`, a `bash` interpreter (`/usr/bin/env bash` by default), and at least 611 kiB of available space.

## Installation

Place all the content of the archive in a directory. Then, in this directory, to create the virtual environment, run:
```
python3 -m venv ./venv
```
Then, install all the requirements using:
```
source activate.sh && ./venv/bin/python -m pip install -r requirements.txt && deactivate
```
Create the directories `./Input/` and `./Output/` if its not already done.

## The `fits_header_extractor` library and `FitsHeaderExtractor` class


