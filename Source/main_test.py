#!/usr/bin/env python
"""
This file is the main test for the fits_header_extractor library.

@ Author: Moussouni, Yaël (MSc student)
@ Institution:  Université de Strasbourg, CNRS, Observatoire astronomique
                de Strasbourg, UMR 7550, F-67000 Strasbourg, France
@ Date: 2024-11-14
"""

from fits_header_extractor.core import FitsHeaderExtractor
from astropy.coordinates import SkyCoord
from astropy import units as u

fhe = FitsHeaderExtractor()

fhe.extract_header_directory(verbatim=True)
#fhe.print_header()
fhe.curate(resolve_name = False, verbatim=True)
fhe.make_moc(verbatim=True)
coord = SkyCoord(84*u.deg, -69.2*u.deg)
a = fhe.is_in_wcs(coord)
