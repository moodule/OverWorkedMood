#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `overworked` package."""

import os
import pytest

import numpy as np
from PIL import Image

from overworked._image_processing import (
    generate_folding_pattern_preview_image,
    invert,
    preprocess_image)
from overworked.folding import (
	postprocess_folding_pattern,
	slice_image)

#####################################################################
# FIX
#####################################################################

IMAGE_PATHS = {
    'binary': [
        'tests/data/binary/github.png']}

#####################################################################
# COLOR SPACE
#####################################################################

def test_invert_self_reversible():
    for __path in IMAGE_PATHS['binary']:
        with Image.open(__path) as __image:
            __temp = __image.convert('1')
            assert np.all(np.array(__temp) == np.array(invert(invert(__temp))))

#####################################################################
# PREPROCESSING
#####################################################################

def test_preprocess_binary_images():
    for __path in IMAGE_PATHS['binary']:
        with Image.open(__path) as __image:
            preprocess_image(
                image=__image,
                invert=False).save(
                fp=(
                    '.processed'.join(os.path.splitext(__path))
                    + '.jpg'),
                format='JPEG')

#####################################################################
# DATAVIZ
#####################################################################

def test_folding_pattern_preview():
    for __path in IMAGE_PATHS['binary']:
        with Image.open(__path) as __image:
            generate_folding_pattern_preview_image(
                slices=postprocess_folding_pattern(slice_image(preprocess_image(
                    image=__image,
                    invert=False))),
                height=__image.height,
                spacing=1).save(
                fp=(
                    '.pattern'.join(os.path.splitext(__path))
                    + '.jpg'),
                format='JPEG')
