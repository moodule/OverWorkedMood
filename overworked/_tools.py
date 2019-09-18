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
        name,
        path='',
        extension='',
        prefix='',
        suffix=''):
    """Piece together the full path of a file.

    The extension and path shouldn't appear in the string argument name.
    If the name string has already an extension, it is kept and the desired extension is appended.
    The '.' are kept in the output name and pushed at the end of the name, after the suffix.

    Args:
        name (str): the file name as seen in the containing directory
        path (str): path to the containing directory
        extension (str): the definitive extension of the output file
        prefix (str): tag placed before the actual name of the file
        suffix (str): tag placed after the actual name of the file

    Returns:
        A string containing the full path to the file, in UNIX notation.
    
    Raises:
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
