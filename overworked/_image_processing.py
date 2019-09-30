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

from overworked._coordinates import (
    ratio_to_coordinate)

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
# COLOR SPACE
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
def convert_color_to_binary(
        image: Image.Image,
        threshold: numeric=85) -> Image.Image:
    return image.point(lambda x: 0 if x<threshold else 255, '1')

@checks
def reduce_color_space(
        image:Image.Image,
        colors: int=2) -> Image.Image:
    """
    The function convert_color_to_binary should be a specific
    use case of this function, with colors=2
    """
    return image

def invert(
        image: Image.Image,
        mode: str="pillow") -> Image.Image:
    if 'pil' in mode.lower():
        return ImageOps.invert(image.convert('L')).convert('1')
    else:
        return Image.fromarray(
            obj=np.invert(np.array(image)),
            mode='1')

#####################################################################
# IMAGE DIMENSION
#####################################################################

@checks
def crop_empty_spaces(
        image: Image.Image) -> Image.Image:
    __temp = np.invert(np.array(image))
    is_image_empty = np.sum(__temp) == 0.0
    
    if not is_image_empty:
        __x_array = np.array(np.nonzero(np.sum(__temp, axis=0)))
        __y_array = np.array(np.nonzero(np.sum(__temp, axis=1)))

        __min_x = __x_array.flat[0]
        __max_x = __x_array.flat[-1]

        __min_y = __y_array.flat[0]
        __max_y = __y_array.flat[-1]
    else:
        raise Exception('The provided image is empty !')
    
    return image.crop(box=(__min_x, __min_y, __max_x, __max_y))

#####################################################################
# FILTERS
#####################################################################

@checks
def emphasize(
        image: Image.Image) -> Image.Image:
    __temp = np.array(image)
    __min_level = np.amin(__temp)
    __max_level = np.amax(__temp)
    return image.point(lambda x: 255. * (x - __min_level) / (__max_level - __min_level))

def smooth(
        image: Image.Image) -> Image.Image:
    return image

#####################################################################
# PATTERN TO IMAGE
#####################################################################

@checks
def _convert_pixel_range_to_image_band(
        lower: int,
        upper: int,
        dimension: int) -> iterable:
    """The sheet is represented by [sheet_width] columns :
    - at the center is the actual paper, a line of 1 pixel
    - the other columns are left blank to represent the spacing of the sheets of paper"""
    return np.array(
        [
            0 if i>= lower and i<=upper # black pixels
            else 1 # white pixels
            for i in range(dimension)])

@checks
def _convert_pattern_slice_to_image_band(
        slice_: tuple,
        height: int) -> iterable:
    """
    

    Parameters
    ----------
    slice_: tuple :
        
    height: int :
        

    Returns
    -------

    """
    return _convert_pixel_range_to_image_band(
        lower=ratio_to_coordinate(slice_[0], height, reverse=False),
        upper=ratio_to_coordinate(slice_[1], height, reverse=False),
        dimension=height)

@checks
def generate_folding_pattern_preview_image(
        slices: iterable,
        height: int,
        spacing: int=1) -> Image.Image:
    """
    The sheet is surrounded by [spacing] columns :
    - at the center is the actual paper, a line of 1 pixel
    - the surrounding columns are white
    
    It's meant to represent the spacing of the sheets of paper,
    when the book is opened.

    Parameters
    ----------
    slices: iterable :
        
    height: int :
        
    spacing: int :
         (Default value = 1)

    Returns
    -------

    """
    __width = (
        spacing * (len(slices) + 1) # white spacing
        + len(slices)) # b & w slice

    return Image.fromarray(
        obj=np.array([
            _convert_pattern_slice_to_image_band(
                slice_=__slice,
                height=height)
            for __slice in slices]).transpose(),
        mode='1')

###############################################################################
# END TO END WORKFLOW
###############################################################################

@checks
def preprocess_image(
        image: Image.Image,
        colors: int=2,
        invert: bool=False) -> Image.Image:
    """
    

    Parameters
    ----------
    image: Image.Image :
        
    colors: int :
         (Default value = 2)
    invert: bool :
         (Default value = False)

    Returns
    -------

    """
    __temp = convert_color_to_binary(emphasize(
        convert_alpha_to_color(image).convert('L')))
    
    if invert:
        return smooth(crop_empty_spaces(invert(__temp)))
    else:
        return smooth(crop_empty_spaces(__temp))
