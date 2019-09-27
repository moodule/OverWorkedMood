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
    Calculates the aspect ratio of an image or a pattern.

    Parameters
    ----------
    width:
        The width of the image in pixels.
        Or the width of the pattern as a slice count.
    height:
        The height of the image / pattern in pixels.

    Returns
    -------
        The aspect ratio of the image or pattern.
    """
    return float(width) / float(height)

@checks
def coordinate_ratio(
        coordinate: numeric,
        dimension: numeric,
        reverse: bool=True) -> numeric:
    """
    Calculates the relative position of a pixel.

    Parameters
    ----------
    coordinate:
        The position as a pixel count.
    dimension:
        The size of the object as a pixel count.
    reverse:
        Whether to count from the lower or upper bound.

    Returns
    -------
        The position as a ratio.
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
        angle: numeric=math.pi):
    return radius * angle

#####################################################################
# BOOK
#####################################################################

@checks
def _available_sheet_count(
        last_page: int,
        first_page: int=1,
        margin: int=0) -> int:  # the actual number of pages used in the pattern
    return max(
        0,
        (
            int(math.ceil(float(last_page - first_page + 1) / 2.0))
             - 2 * margin))

@checks
def _available_sheet_height(
        height: float,
        margin: float=0.0) -> float:
    return round(
        max(
            0.0,
            height - 2.0 * margin),
        3)

@checks
def sheet_ordinate(
        ratio: numeric,
        height: numeric,
        margin: numeric=0.0) -> numeric:
    return margin + ratio * _available_sheet_height(
    	height=height,
    	margin=margin)
