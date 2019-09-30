# -*- coding: utf-8 -*-

"""
===========
Folding Art
===========

Calculate how to fold pages to print an image into the depth of a book.

Jargon:
- an image band is a 1-pixel wide vertical portion of the image 
- a pattern slice is a continuous stroke of a single color in an image band
Each pattern slice is meant to map a book sheet.

It is chosen to match the aspect ratio of the pattern, which is considered fixed.
To adjust the aspect ratio of the folded pattern, you can play with :
    - the book size (sheet size, number of pages)
    - the margins around the folded pattern (optimal values are calculated)
    - the opening of the book (3 cases : 90, 180 and 360)
"""

from __future__ import division, print_function, absolute_import

import math

import numpy as np
from PIL import Image

from typical import checks, iterable, numeric

from overworked._coordinates import (
    arc_length,
    aspect_ratio,
    coordinate_to_ratio,
    range_length,
    ratio_to_coordinate)

#####################################################################
# SLICE THE IMAGE
#####################################################################

@checks
def _image_band_to_pattern_slice(
        band: iterable) -> iterable:
    """
    Works only on binary images: there's no color information in the output
    ranges. The folding ranges are always black in this case.

    Parameters
    ----------
    band: iterable :
        

    Returns
    -------

    """
    __slice = []
    __height = np.size(band)
    __current_color = True   # white
    __current_start = -1.0

    # scan the band for continuous ranges of black pixels
    for __y in range(np.size(band)): # works on base iterable types as well arrays
        # close a continuous black range
        if band[__y] and not __current_color:
            __slice.append((
                __current_start,
                coordinate_to_ratio(
                    coordinate=__y, # upper bound excluded from the range, last=y-1
                    dimension=__height,
                    reverse=False)))
        elif not band[__y] and __current_color:
            __current_start = coordinate_to_ratio(
                coordinate=__y,
                dimension=__height,
                reverse=False)
        __current_color = band[__y]

    # finished scanning the band
    if not __current_color: # close the last open black range
        __slice.append((__current_start, 1.0))
    elif __current_color and __current_start == -1.0:
        __slice.append((0.0, 0.0)) # white page / slice / image band

    return __slice

@checks
def _flatten_pattern_slices(
        slices: iterable) -> iterable:
    """
    One range per sheet of paper.

    Parameters
    ----------
    slices: iterable :
        

    Returns
    -------

    """
    return [
        __band
        for __slice in slices
        for __band in __slice]

@checks
def _filter_pattern_slices(
        slices: iterable,
        threshold: float=0.05) -> iterable:
    """
    Filter out the small slices: they make the pattern wider and don't render
    well as folded pages.

    Parameters
    ----------
    slices: iterable :
        
    threshold: float :
         (Default value = 0.05)

    Returns
    -------

    """
    return [
        (0.0, 0.0) if range_length(__slice[0], __slice[1]) < threshold
        else __slice
        for __slice in slices]

###############################################################################
# MAP THE IMAGE TO THE BOOK
###############################################################################

@checks
def _calculate_pattern_slice_dropout_factor(
        original_width: int,
        wanted_width: int) -> int:
    """
    Once evened the pattern has roughly the same width as the original image.
    Number of bands ~= number of slices = image width

    Parameters
    ----------
    original_width: int :
        
    wanted_width: int :
        

    Returns
    -------

    """
    return max(
        1,
        math.ceil(float(original_width) / float(wanted_width)))

def _calculate_margins():
    """ """
    _calculate_horizontal_margin()
    _calculate_book_opening()
    _calculate_vertical_margin()

def _calculate_horizontal_margin():
    """ """
    _horizontal_margin = 0
    if _pattern is not None:
        _horizontal_margin = sheet_count()[3] - _pattern.width(raw=False)
        _horizontal_margin = max(0, _horizontal_margin) // 2

def _calculate_book_opening():
    """ """
    _book_opening = 180
    if _pattern is not None:
        pattern_width_360 = sheet_spacing()[2] * float(sheet_count()[1])
        pattern_height_360 = pattern_width_360 / _pattern.aspect_ratio(raw=True)
        pattern_to_sheet_ratio = pattern_height_360 / sheet_height()[3]
        if pattern_to_sheet_ratio < 1.0:
            _book_opening = 360
        elif pattern_to_sheet_ratio < 2.0:
            _book_opening = 180
        else:
            _book_opening = 90

def _calculate_vertical_margin():
    """ """
    _vertical_margin = 0.0
    if _pattern is not None:
        pattern_width_360 = sheet_spacing()[2] * float(sheet_count()[1])
        pattern_height_360 = pattern_width_360 / _pattern.aspect_ratio(raw=True)
        _vertical_margin = 0.5 * sheet_height()[3]
        if _book_opening == 360:
            _vertical_margin -= 0.5 * pattern_height_360
        elif _book_opening == 180:
            _vertical_margin -= 0.25 * pattern_height_360
        else:
            _vertical_margin -= 0.125 * pattern_height_360
        _vertical_margin = max(0.0, _vertical_margin)
        _vertical_margin = round(_vertical_margin, 3)

###############################################################################
# END TO END WORKFLOW
###############################################################################

@checks
def slice_image(
        image: Image.Image) -> iterable:
    """
    

    Parameters
    ----------
    image: Image.Image :
        

    Returns
    -------

    """
    return [
        _image_band_to_pattern_slice(__band)
        for __band in np.array(image).transpose()] # transpose so that second dimension is y

@checks
def postprocess_folding_pattern(
        slices: iterable) -> iterable:
    """
    

    Parameters
    ----------
    slices: iterable :
        

    Returns
    -------

    """
    return _filter_pattern_slices(
        slices=_flatten_pattern_slices(slices=slices),
        threshold=0.05)

@checks
def map_folding_pattern_to_book(wanted_width=None):
    """
    

    Parameters
    ----------
    wanted_width :
         (Default value = None)

    Returns
    -------

    """
    _generate_pattern_image()
    _check_pattern()
    #save_pattern()
