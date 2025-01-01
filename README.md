<!--[TPL:RED] UNDER EMBARGO UNTIL 2025-01-06!-->
```diff
- [TPL:RED] UNDER EMBARGO UNTIL 2025-01-06!
```

# Fits Header Extractor and Curator With Python
Author: Moussouni, Yaël (MSc student; `yael.moussouni@etu.unistra.fr`)
Institution: Université de Strasbourg, CNRS, Observatoire astronomique de Strasbourg, UMR 7550, F-67000 Strasbourg, France
Date: 2025-01-01

## Abstract

[Fits](https://en.wikipedia.org/wiki/FITS/) are widely used file formats in astronomy. The content of the file is in two parts: the header and the data. The goal of this Python package is to explore fits header. To this end, I created a python library: `fits_header_extractor`, providing a `FitsHeaderExtractor` class, and a notebook.

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
```
fhe.ping()
```
This should return `0` (and print `pong`).

## Licence

**Fits Header Extractor [and Curator With Python]**

Copyright (C) 2025 Yaël Moussouni (yael.moussouni@etu.unistra.fr)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see [www.gnu.org/licenses/](https://www.gnu.org/licenses/).
