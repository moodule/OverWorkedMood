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

from overworked.folding import (
	preprocess_image,
	slice_image_into_pattern,
	postprocess_folding_pattern,
	export_folding_pattern)

__author__ = 'David Mougeolle'
__email__ = 'moodule@protonmail.com'
__version__ = '0.6.2'
__title__ = 'overworked'
__description__ = 'Generate blueprints to upcycle old items into art.'
__url__ = 'http://github/moodule/overworked'
__license__ = 'MIT license'

__all__ = [
	'preprocess_image',
	'slice_image_into_folding_pattern',
	'postprocess_folding_pattern',
	'export_folding_pattern' ]
