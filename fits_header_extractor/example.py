#!/usr/bin/env python
# [TLP:RED] UNDER EMBARGO UNTIL 2025-01-13!
"""
This file is the main test for the fits_header_extractor library.

@ Author: Moussouni, Yaël (MSc student; yael.moussouni@etu.unistra.fr)
@ Institution:  Université de Strasbourg, CNRS, Observatoire astronomique
                de Strasbourg, UMR 7550, F-67000 Strasbourg, France
@ Date: 2025-01-01

Licence:
Fits Header Extractor [and Curator With Python]
Copyright (C) 2025 Yaël Moussouni (yael.moussouni@etu.unistra.fr)

__init.py__
Copyright (C) 2025 Yaël Moussouni (yael.moussouni@etu.unistra.fr)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see https://www.gnu.org/licenses/.
"""

from fits_header_extractor.core import FitsHeaderExtractor
from astropy.coordinates import SkyCoord
from astropy import units as u

fhe = FitsHeaderExtractor()

fhe.extract_header_directory(verbatim=True)
fhe.print_header()
fhe.curate(resolve_name = True, verbatim=True)
fhe.make_moc(verbatim=True)
coord = SkyCoord(84*u.deg, -69.2*u.deg)
a = fhe.is_in_wcs(coord)
