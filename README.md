# Fits Header Extractor and Curator With Python

## Abstract

[Fits](https://en.wikipedia.org/wiki/FITS) are widely used file formats in astronomy. The content of the file is in two parts: the header and the data. The goal of this Python project is to explore fits header. To this end, I created a python library: `fits_header_extractor`, providing a `FitsHeaderExtractor` class, and a notebook.

## Requirements

The library requires `python` (tested with version 3.13.1), `setuptools`, `git`, a `bash` interpreter (`/usr/bin/env bash` by default), and at least 530 kiB of available space.

## Installation

1. **Create a virtual environment (optional):** Simply run `python3 -m venv venv` in your working directory. Then, activate this environment with `./venv/bin/activate`. You can deactivate the virtual environment with the `deactivate` command.
2. **Install the package:** The package can be installed from Github with pip and git, run (in your environment):
```bash
pip install git+https://github.com/Yael-II/Fits_Header_Extractor
```

## The `fits_header_extractor` library and `FitsHeaderExtractor` class
The `fits_header_extractor` contains a `FitsHeaderExtractor` class that can be imported in Python, and a new instance of the class invoked with:
```python
from fits_header_extractor import FitsHeaderExtractor
fhe = FitsHeaderExtractor()
```

To test the class, simply run:
```
fhe.ping()
```
This should return `0` (and print `pong`).
