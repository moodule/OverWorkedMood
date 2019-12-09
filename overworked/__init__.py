# -*- coding: utf-8 -*-

"""
==========
Overworked
==========

A toolbox to plan and visualize the upcycling process of old items. 

Examples
--------
    >>> ...
"""

from __future__ import division, print_function, absolute_import

from overworked._image_processing import (
	generate_folding_pattern_preview_image,
	preprocess_image,)
from overworked._io import (
	generate_folding_table,)
from overworked.folding import (
	map_folding_pattern_to_book,
	postprocess_folding_pattern,
	slice_image)

__author__ = 'David Mougeolle'
__email__ = 'moodule@protonmail.com'
__version__ = '0.6.2'
__title__ = 'overworked'
__description__ = 'Generate blueprints to upcycle old items into art.'
__url__ = 'https://github/moodule/overworked'
__license__ = 'MIT license'

__all__ = [
	'generate_folding_pattern_preview_image',
	'generate_folding_table',
	'map_folding_pattern_to_book',
	'postprocess_folding_pattern',
	'preprocess_image',
	'slice_image',]
