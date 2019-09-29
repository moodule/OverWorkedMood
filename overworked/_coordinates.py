# -*- coding: utf-8 -*-

"""
===========
Coordinates
===========

Tools to navigate in the book / image / pattern spaces.
"""

from __future__ import division, print_function, absolute_import

import math

from typical import (
	checks,
	numeric)

#####################################################################
# GENERIC
#####################################################################

@checks
def aspect_ratio(
        width: numeric,
        height: numeric) -> numeric:
    """
    Parameters
    ----------
    width: numeric :
        The width of the image in pixels.
        Or the width of the pattern as a slice count.
    height: numeric :
        The height of the image / pattern in pixels.

    Returns
    -------
        The aspect ratio of an image or a pattern.
    """
    return float(width) / float(height)

@checks
def coordinate_ratio(
        coordinate: numeric,
        dimension: numeric,
        reverse: bool=False) -> numeric:
    """
    Parameters
    ----------
    coordinate: numeric :
        The position as a pixel count.
    dimension: numeric :
        The size of the object as a pixel count.
    reverse: bool :
        (Default value = True)
        Whether to count from the lower or upper bound.

    Returns
    -------
        The relative position of a pixel.
    """
    __r =  min(
        1.0,
        max(
            0.0,
            float(coordinate) / float(dimension)))
    if reverse:
        return 1.0 - __r
    else:
        return __r

@checks
def arc_length(
        radius: numeric,
        angle: numeric=math.pi) -> numeric:
    """
    Parameters
    ----------
    radius: numeric :
        The radius of the arc.
    angle: numeric :
        The arc opening angle.

    Returns
    -------
        The arc length.
    """
    return radius * angle

#####################################################################
# PATTERN
#####################################################################

@checks
def range_length(
        lower: numeric,
        upper: numeric) -> numeric:
    """
    Parameters
    ----------
    lower: numeric :
        The lower.bound of the range.
    upper: numeric :
        The upper bound of the range.

    Returns
    -------
        The length of the range.
    """
    return math.abs(upper - lower)

#####################################################################
# BOOK
#####################################################################

@checks
def _available_sheet_count(
        last_page: int,
        first_page: int=1,
        margin: int=0) -> int:  # the actual number of pages used in the pattern
    """
    Parameters
    ----------
    last_page: int:
        The number of the last page in the book.
    first_page: int:
        (Default value = 1)
        The number of the first page in the book.
    margin: numeric:
        (Default value = 0)
        The number of book sheet before and after the pattern.

    Returns
    -------
        The number of book sheet available for folding.
    """
    return max(
        0,
        (
            int(math.ceil(float(last_page - first_page + 1) / 2.0))
             - 2 * margin))

@checks
def _available_sheet_height(
        height: numeric,
        margin: numeric=0.0,
        as_ratio: bool=False) -> numeric:
    """
    Parameters
    ----------
    height: numeric:
        The total height of a book sheet.
    margin: numeric:
        (Default value = 0.0)
        The vertical space before and after the pattern.
    as_ratio: bool:
        (Default value = False)
        Whether to represent the output as a metric length or a ratio.

    Returns
    -------
        The vertical portion of the page available for the pattern.
    """
    __available = max(
        0.0,
        height - 2.0 * margin)
    if as_ratio:
        __available = __available / float(height)
    return round(__available, 3)

@checks
def sheet_ordinate(
        ratio: numeric,
        height: numeric,
        margin: numeric=0.0) -> numeric:
    """
    Parameters
    ----------
    ratio: numeric:
        The vertical position as a ratio..
    height: numeric:
        The total height of a book sheet.
    margin: numeric:
        (Default value = 0.0)
        The vertical space before and after the pattern.

    Returns
    -------
        The vertical position as a metric length from the bottom.
    """
    return margin + ratio * _available_sheet_height(
    	height=height,
    	margin=margin,
        as_ratio=False)
