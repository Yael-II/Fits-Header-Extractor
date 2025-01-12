#!/usr/bin/env python
# [TLP:RED] UNDER EMBARGO UNTIL 2025-01-13!
"""
FITS header extractor is a python library to extract the header of FITS.

@ Author: Moussouni, Yaël (MSc student; yael.moussouni@etu.unistra.fr)
@ Institution:  Université de Strasbourg, CNRS, Observatoire astronomique
                de Strasbourg, UMR 7550, F-67000 Strasbourg, France
@ Date: 2025-01-01

Content: 
    - FitsHeaderExtractor class

        Variables:
        - self.in_dir: input directory
        - self.out_dir: output directory
        - self.header_list: list of headers
        - self.file_list: list of files
        - self.wcs_list: list of WCS
        - self.info_list: list of other informations
        - self.moc_list: list of MOC
        
        Methods:
        - ping(): A quick test.
        - status(): Prints all the internal variables.
        - print_header(): prints the header in the terminal
        - get_index(): retrieve the index of a header from the name
        - extract_header(): Get the header of a fit(s) file.
        - extract_header_directory(): Get the header of all fit(s) files 
                                      in a directory.
        - curate(): curate data into two lists (WCS and other informations)
        - make_moc(): create MOC for each fits file
        - is_in_wcs(): test if a point is in any fits file coverage

Usage: 
    ### Example of usage ###
    from fits_header_extractor import FitsHeaderExtractor # Imports the library
    
    fhe = FitsHeaderExtractor() # Initialize an instance of the library
    fhe.ping() # If the library is correctly imported, "pong" is printed
    # ...
    ### End of the example ###

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

import warnings
import os
from urllib.request import urlopen
from xml.etree import ElementTree 

import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs import FITSFixedWarning
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy import units as u
from mocpy import MOC

DEFAULT_IN_DIR = "./Input/"
DEFAULT_OUT_DIR = "./Output"

COLOUR_DEFAULT = "\033[0m" # Default
COLOUR_IN = "\033[32m" # Green
COLOUR_OUT = "\033[36m" # Cyan
COLOUR_INFO = "\033[34m" # Blue
COLOUR_WARNING = "\033[33m" # Yellow
COLOUR_ERROR = "\033[31m" # Red

MOC_ORDER = 10

SESAME_URL = "https://cds.unistra.fr/cgi-bin/nph-sesame/-ox/~A?"

CARDS = ["OBJECT", 
         "OBJECT_NAME",
         "DATE-OBS", 
         "EXPTIME",
         "INSTRUME", 
         "TELESCOP"]

ALT_CARDS = ["MJD", "MJD_OBS", "MJD-OBS"]

DEFAULT_INFO = {card: None for card in CARDS}


class FitsHeaderExtractor:
    def __init__(self, 
                 in_dir: str = DEFAULT_IN_DIR, 
                 out_dir: str = DEFAULT_OUT_DIR):
        """
        Initialize a FitsHeaderExtractor class instance
        @params:
            - in_dir: input directory
            - out_dir: output directory
        """
        if in_dir[-1] != "/":
            in_dir += "/"
        if out_dir[-1] != "/":
            out_dir += "/"
        self.in_dir = in_dir
        self.out_dir = out_dir
        self.header_list = []
        self.file_list = []
        self.wcs_list = []
        self.info_list = []
        self.moc_list = []
        return None

    def ping(self):
        """A quick test."""
        print(COLOUR_INFO + "pong" + COLOUR_DEFAULT)
        return 0

    def status(self):
        """Prints all the internal variables."""
        print(COLOUR_INFO + "=== [ Status ] ===" + COLOUR_DEFAULT)
        print(COLOUR_INFO + "Input directory: " 
              + COLOUR_DEFAULT + self.in_dir)
        print(COLOUR_INFO + "Output directory: " 
              + COLOUR_DEFAULT +  self.out_dir)
        print(COLOUR_INFO + "File list: " 
              + COLOUR_DEFAULT +  str(self.file_list))
        return 0

    def print_header(self,
                     index: int|list = None):
        """
        Print the content of the current list of headers
        @ params:
            - index: index or list of index of headers to print
        """
        if index is None:
            N_file_list = len(self.file_list)
            N_header_list = len(self.header_list)
            N = np.min([N_file_list, N_header_list]) # Just in case...
            index = np.array(range(N))
        elif np.ndim(index) == 0:
            index = np.array([index])
        else:
            index = np.array(index).flatten()
        for i in index:
            filename = self.file_list[i]
            header = repr(self.header_list[i])
            head_lines = header.split("\n")
            print("\n"
                  + COLOUR_OUT
                  + "="*80 + "\n"
                  + "File: " 
                  + COLOUR_DEFAULT
                  + filename
                  + "\n"
                  + COLOUR_OUT
                  + "="*80
                  + COLOUR_DEFAULT)
            for line in head_lines:
                j = 0
                while j < len(line): # Locate comments but not / in data
                    if line[j] == "/":
                        if np.char.count(line[:j], "\'") % 2 == 0:
                            line = line[:j] + "\033[90m" + line[j:]
                            j = 100000000 # A way to exit the loop...
                    j += 1
                print(COLOUR_OUT + line[0:8], end="")
                print(COLOUR_DEFAULT + line[8:], end="")
                print(COLOUR_DEFAULT)
        return 0

    def get_index(self,
                  name: str):
        """
        gives the index of the header from its name
        @params:
            - name: name of the header
        @returns:
            - index: the index of the header (None if not found)
        """
        index = 0
        while index < len(self.filelist):
            if self.filelist[index] == header:
                return index
            else:
                index += 1
        return None

    def extract_header(self, 
                       filename: str,
                       directory: str = None,
                       verbatim: bool = False) -> list:
        """
        Get the header of a fit(s) file.
        @params:
            - filename: name of the file
            - directory: input directory
        @returns:
            - head: the header (None if an error occurred)
        """
        if directory is None:
            directory = self.in_dir
        # Test and correct for directory name
        if directory[-1] != "/":
            directory[-1] += "/"
        # Test and correct for file name
        if not ".fit" in filename.lower(): # Works for .fit and .fits
            filename += ".fit" # Assumes filename.fit
            print(COLOUR_WARNING
                  + "Warning: Please include the extension in the file name."
                  + " Assuming \"{}\" instead.".format(filename)
                  + COLOUR_DEFAULT)
        try:
            head = fits.getheader(directory + filename)
            self.header_list.append(head)
            self.file_list.append(filename)
        except FileNotFoundError as error:
            print(COLOUR_ERROR
                  + ("Error! I cannot open \"{}\" "
                     "in the \"{}\" directory").format(filename, directory)
                  + COLOUR_DEFAULT)
            head = None
        except Exception as error:
            msg = str(error).replace("\n", " ")
            if msg[-1] != ".":
                msg += "."
            print(COLOUR_ERROR
                  + ("Error! {} ({})").format(msg, filename)
                  + COLOUR_DEFAULT)
            print(COLOUR_ERROR 
                  + "\"{}\" will be ignored.".format(filename)
                  + COLOUR_DEFAULT)
            head = None
        return head

    def extract_header_directory(self,
                                 directory: str = None,
                                 verbatim: bool = False) -> list:
        """
        Get the header of all fit(s) files in a directory.
        @params:
            - directory: input directory with all the fits files
        @returns:
            - head_list: the header list (empty list if an error occurred)
        """
        if directory is None:
            directory = self.in_dir
        filelist = [fname for fname in os.listdir(directory) 
                    if ".fit" in fname] # Works for .fit and .fits
        if verbatim:
            print(COLOUR_INFO 
                  + "Filelist: "
                  + str(filelist)
                  + COLOUR_DEFAULT)
        header_list = []
        for filename in filelist:
            if verbatim:
                print(COLOUR_INFO 
                      + "Current file: {} - ".format(filename)
                      + COLOUR_DEFAULT, end="")
            head = self.extract_header(filename, directory, verbatim)
            if head != None:
                if verbatim:
                    print(COLOUR_INFO + "success." + COLOUR_DEFAULT)
                header_list.append(head)
        return header_list

    def curate(self, resolve_name: bool = True, verbatim: bool = False):
        """
        Curate the headers into WCS_list and info_list
        @ params:
            - verbatim: display info and warnings
        @ output:
            - 0
        """
        N_file_list = len(self.file_list)
        N_header_list = len(self.header_list)
        N = np.min([N_file_list, N_header_list]) # Just in case...
        index = np.array(range(N))
        for i in index:
            header = self.header_list[i]
            filename = self.file_list[i]
            try:
                if verbatim:
                    with warnings.catch_warnings(record=True) as warn_list:
                        header_WCS = WCS(header)
                        if len(warn_list) > 0:
                            for warn in warn_list:
                                print(COLOUR_WARNING 
                                      + "Warning: "
                                      + str(warn.message).replace("\n", "")
                                      + " ("
                                      + (str(warn.category)
                                         .replace("astropy.", "")
                                         .replace("wcs.", "")
                                         .replace("<class ", "")
                                         .replace(">", "")
                                         .replace("\'", ""))
                                      + ")"
                                      + COLOUR_DEFAULT)
                else:
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore', FITSFixedWarning)
                        header_WCS = WCS(header)
            except ValueError as error:
                msg = str(error).replace("\n", " ")
                print(COLOUR_ERROR + "Error! " + msg + COLOUR_DEFAULT)
                print(COLOUR_ERROR 
                      + "\"{}\" will be ignored.".format(filename)
                      + COLOUR_DEFAULT)
                header_WCS = None
            except Exception as error:
                msg = str(error).replace("\n ", " ")
                print(COLOUR_ERROR + "Error! " + COLOUR_DEFAULT + msg)
                print(COLOUR_ERROR 
                      + "\"{}\" will be ignored.".format(filename)
                      + COLOUR_DEFAULT)
                header_WCS = None
            if header_WCS != None:
                head_lines = repr(header).split("\n")
                header_info = DEFAULT_INFO
                for line in head_lines:
                    j = 0
                    while j < len(line): # Locate and delete comments
                        if line[j] == "/":
                            if np.char.count(line[:j], "\'") % 2 == 0:
                                line = line[:j] 
                                j = 100000000 # A way to exit the loop...
                        j += 1
                    card = line[:8].replace(" ", "")
                    if card in CARDS or card in ALT_CARDS:
                        if "DATE-OBS" in card or "MJD" in card:
                            time_str = (line[9:]
                                        .replace(" ", "")
                                        .replace("\'", ""))
                            time_str = self.__preformat_time(time_str)
                            time = self.__format_time(time_str)
                            header_info["DATE-OBS"] = time
                        elif "EXPTIME" in card:
                            exptime = float(line[9:]
                                            .replace(" ", "")
                                            .replace("\'", ""))
                            header_info["EXPTIME"] = exptime
                        elif "OBJECT" in card:
                            if resolve_name:
                                obj = self.__resolve(line[9:], 
                                                     verbatim=verbatim)
                            else:
                                obj = line[9:]
                            header_info["OBJECT"] = (line[9:]
                                                   .replace("\'", "")
                                                   .strip())
                            header_info["OBJECT_NAME"] = obj
                        else:# card in CARDS:
                            header_info[card] = (line[9:]
                                               .replace("\'", "")
                                               .strip())
            self.wcs_list.append(header_WCS)
            self.info_list.append(header_info)
        return 0

    def make_moc(self, verbatim: bool = False):
        """
        Creates a MOC for each fits files in the file list.
        @ params:
            - verbatim: display info and warnings
        @ returns:
            - 0
        """
        for i in range(len(self.wcs_list)):
            wcs = self.wcs_list[i]
            filename = self.file_list[i]
            if wcs != None:
                try: 
                    coords = wcs.calc_footprint()
                    ra = coords[:,0]
                    dec = coords[:,1]
                    sky = SkyCoord(ra, dec, unit=u.deg)
                    moc = MOC.from_polygon_skycoord(sky, max_depth=MOC_ORDER)
                except Exception as error:
                    moc = None
                    msg = str(error)
                    if msg[-1] != ".":
                        msg += "."
                    print(COLOUR_ERROR
                          + "Error! "
                          + msg
                          + " (in make_moc)"
                          + COLOUR_DEFAULT)
                    print(COLOUR_ERROR
                          + "\"{}\" ".format(filename)
                          + "MOC will be ignored."
                          + COLOUR_DEFAULT)
            else:
                moc = None
            self.moc_list.append(moc)
        return 0

    def is_in_wcs(self, 
                  sky_coord: SkyCoord, 
                  index: int|list = None):
        """
        Returns a Boolean describing if coordinates are in one of the WCS.
        @ params:
            - sky_coord: a SkyCoord object with the test coordinates
            - index: an index or list of index of fits to consider
                     (by default, all the files are tested)
        @ returns:
            - inside_list: a list of Boolean, the same shape as index, with the
                           values True (inside), False (outside) or None (Error)
        """
        if index is None:
            N_file_list = len(self.file_list)
            N_header_list = len(self.header_list)
            N_info_list = len(self.info_list)
            N_wcs_list = len(self.wcs_list)
            N_moc_list = len(self.moc_list)
            N_list = [N_file_list,
                      N_header_list,
                      N_info_list,
                      N_wcs_list,
                      N_moc_list]
            N = np.min([N_list])
            index = np.array(range(N))
        elif np.ndim(index) == 0:
            index = np.array([index])
        else:
            index = np.array(index).flatten()

        inside_list = []
        for i in index:
            wcs = self.wcs_list[i]
            moc = self.moc_list[i]
            filename = self.file_list[i]
            if wcs is not None and moc is not None:
                inside = wcs.footprint_contains(sky_coord)
            else: 
                inside = None
            inside_list.append(inside)
        return inside_list



    def __preformat_time(self, time_str: str):
        """Converts DD/MM/YY formats to YYYY-MM-DD"""
        time_split = []
        if "/" in time_str:
            time_split = time_str.split("/")
        elif "-" in time_str:
            time_split = time_str.split("-")
        if len(time_split) == 3:
            if (len(time_split[0]) == 2
                and len(time_split[1]) == 2
                and len(time_split[2]) == 2):
                if time_split[2][0] in [str(i) for i in range(5,10)]:
                    time_split[2] = "19" + time_split[2]
                else:
                    time_split[2] = "20" + time_split[2]
                time_str = "-".join(time_split[::-1])
        return time_str


    def __format_time(self, time_str: str):
        """Format time using astropy"""
        try:
            time = Time(time_str)
        except ValueError:
            try:
                time = Time(time_str, format="mjd")
            except Exception as error:
                msg = str(error).replace("\n", " ")
                time = None
                print(COLOUR_ERROR
                      + "Error! "
                      + msg
                      + COLOUR_DEFAULT)
                print(COLOUR_ERROR
                      + ("\"{}\" time will be ignored."
                         .format(filename))
                      + COLOUR_DEFAULT)
        except Exception as error:
            msg = str(error).replace("\n", " ")
            time = None
            print(COLOUR_ERROR
                  + "Error! "
                  + msg
                  + COLOUR_DEFAULT)
            print(COLOUR_ERROR
                  + ("\"{}\" time will be ignored."
                     .format(filename))
                  + COLOUR_DEFAULT)
        time.format = "isot"
        return time
    
    def __resolve(self, 
                  obj: str, 
                  url: str = SESAME_URL, 
                  verbatim: bool = False):
        """Resolve and object name (from URL Sesame XML format)"""
        obj = obj.replace(" ", "").replace("\'", "")
        try:
            if verbatim:
                print(COLOUR_INFO 
                      + "Starting Sesame query for \"{}\"...".format(obj)
                      + COLOUR_DEFAULT)
            with urlopen(url+obj) as html:
                if verbatim:
                    print(COLOUR_INFO + "done!" + COLOUR_DEFAULT)
                xml = html.read().decode('utf-8').replace("\n", "")
                root = ElementTree.fromstring(xml)
                tags = root.findall('Target/Resolver/oname')
                if len(tags) > 0:
                    oname = tags[0].text
                    resolved_obj = oname
                else:
                    resolved_obj = None

        except Exception as error:
            resolved_obj = None
            msg = str(error).replace("\n ", " ")
            print(COLOUR_ERROR 
                  + "Error! "
                  + msg
                  + COLOUR_DEFAULT)
        return resolved_obj

