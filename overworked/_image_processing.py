# -*- coding: utf-8 -*-

"""
================
Image Processing
================

Utility functions for the specific purposes of this project.
"""

from __future__ import division, print_function, absolute_import

import os

import numpy as np
from PIL import Image, ImageOps

from typical import checks, iterable, numeric

###############################################################################
# IO
###############################################################################

# Image.show()
# Image.save(
#     fp='path',
#     format='png')

@checks
def full_path_to_file(
        name: str,
        path: str='',
        extension: str='',
        prefix: str='',
        suffix: str=''):
    """Piece together the full path of a file.

    The extension and path shouldn't appear in the string argument name.
    If the name string has already an extension, it is kept and the desired extension is appended.
    The '.' are kept in the output name and pushed at the end of the name, after the suffix.

    Parameters
    ----------
    name:
        The file name as seen in the containing directory.
    path:
        Path to the containing directory.
        Can be either relative or absolute.
    extension:
        The definitive extension of the output file.
    prefix:
        Tag placed before the actual name of the file.
    suffix:
        Tag placed after the actual name of the file.

    Returns
    -------
        A string containing the full path to the file, in UNIX notation.
    
    Raises
    ------
    """
    file_path, file_name = os.path.split(name)
    file_name, file_extension = os.path.splitext(file_name)
   
    if prefix:
        file_name = prefix + '_' + file_name
    if suffix:
        file_name = file_name + '_' + suffix
    
    file_name = file_name + file_extension
    if extension:
        file_name = file_name + '.' + extension.replace('.', '').lower()
    
    file_path = os.path.join(path, file_path, file_name)
    
    return file_path

#####################################################################
# IMAGE PROCESSING
#####################################################################

@checks
def convert_alpha_to_color(
        image: Image.Image,
        color: tuple=(255, 255, 255)) -> Image.Image:
    """
    Paints the transparent background of an image in a given color.

    Parameters
    ----------
    image:
        An image object, opened with PIL.
    color:
        The replacement color for the alpha channel.

    Returns
    -------
        Another image object, with a colored BG.

    Raises
    ------
    """
    if image.mode == 'RGBA':
        return Image.alpha_composite(
            Image.new('RGBA', image.size, color),
            image)
    else:
        return image

@checks
def emphasize(
        image: Image.Image) -> Image.Image:
    __temp = np.array(image)
    __min_level = np.amin(__temp)
    __max_level = np.amax(__temp)
    return image.point(lambda x: 255. * (x - __min_level) / (__max_level - __min_level))
    
@checks
def convert_color_to_binary(
        image: Image.Image,
        threshold: numeric=85) -> Image.Image:
    return image.point(lambda x: 0 if x<threshold else 255, '1')

@checks
def crop_empty_spaces(
        image: Image.Image) -> Image.Image:
    __temp = np.invert(np.array(image))
    is_image_empty = np.sum(__temp) == 0.0
    
    if not is_image_empty:
        __x_array = np.sum(__temp, axis=1)
        __x_array = np.transpose(np.nonzero(__x_array))

        __y_array = np.sum(__temp, axis=0)
        __y_array = np.transpose(np.nonzero(__y_array))

        __min_x = __x_array[0]
        __max_x = __x_array[-1]

        __min_y = __y_array[0]
        __max_y = __y_array[-1]
    else:
        raise Exception('The provided image is empty !')
    
    return image.crop((__min_y, __min_x, __max_y, __max_x))

def smooth(
        image: Image.Image) -> Image.Image:
    pass

def invert(
        image: Image.Image) -> Image.Image:
    return ImageOps.invert(image.convert('L')).convert('1')

def convert_range_to_band(
        lower: int,
        upper: int,
        dimension: int) -> iterable:
    """The sheet is represented by [sheet_width] columns :
    - at the center is the actual paper, a line of 1 pixel
    - the other columns are left blank to represent the spacing of the sheets of paper"""
    return np.array(
        [
            0 if i>= lower and i<=upper
            else 1
            for i in range(dimension)])
