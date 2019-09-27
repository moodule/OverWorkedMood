# -*- coding: utf-8 -*-

"""
================
Internal Toolbox
================

Utility functions for the specific purposes of this project.
"""

from __future__ import division, print_function, absolute_import

import os

from typical import checks

###############################################################################
# PATH & FILE MANIPULATIONS
###############################################################################

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
def _fill_background(
        image: Image.Image) -> Image.Image:
    """
    Paints the background of an image in white.

    Parameters
    ----------
    image:
        An image object, opened with PIL.

    Returns
    -------
        Another image object, with a white BG.

    Raises
    ------
    """
    if image.mode == 'RGBA':
        image.load()
        temp = np.array(image)
        mask = (temp[:,:,3] == 0)
        temp[:,:,:4][mask] = [255, 255, 255, 255]
        return Image.fromarray(temp)

@checks
def _transform_black_white(
        image: Image.Image) -> Image.Image:
    """
    Represent the image in B&W color scale.
    
    Parameters
    ----------
    image:
        A PIL image object.

    Returns
    -------
        A new image object, in B&W.

    Raises
    ------
    """
    return image.convert("L")

def _emphasize_image(self):
    temp = np.array(self._image)
    min_level = np.amin(temp)
    max_level = np.amax(temp)
    if max_level > min_level:
        self._image = self._image.point(lambda x: 255. * (x - min_level) / (max_level - min_level))
    
def _transform_binary(self):
    self._image = self._image.point(lambda x: 0 if x<85 else 255, '1')

def _crop_image(self):
    temp = np.invert(np.array(self._image))
    is_image_empty = np.sum(temp)
    is_image_empty = is_image_empty == 0.0
    
    if not is_image_empty:
        x_array = np.sum(temp, axis=1)
        x_array = np.transpose(np.nonzero(x_array))

        y_array = np.sum(temp, axis=0)
        y_array = np.transpose(np.nonzero(y_array))

        min_x = x_array[0]
        max_x = x_array[::-1][0]

        min_y = y_array[0]
        max_y = y_array[::-1][0]
    else:
        raise Exception('The provided image is empty !')
    
    self._image = self._image.crop((min_y, min_x, max_y, max_x))

def _smooth_image(self):
    pass

def _invert(self):
    self._image = self._image.convert('L')
    self._image = ImageOps.invert(self._image)
    self._image = self._image.convert('1')

def _fill_image_band(band_index, sheet_width=1):
    """The sheet is represented by [sheet_width] columns :
    - at the center is the actual paper, a line of 1 pixel
    - the other columns are left blank to represent the spacing of the sheets of paper"""
    band = self._bands[band_index]
    x = band_index * sheet_width
    for y in range(band[0], band[1]):
        self._pattern_image.putpixel((x,y), False)
