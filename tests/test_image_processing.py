#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `overworked` package."""

import os
import pytest

import numpy as np

from overworked._image_processing import (
    generate_folding_pattern_preview_image,
    invert,
    preprocess_image)
from overworked.folding import (
    postprocess_folding_pattern,
    slice_image)

#####################################################################
# COLOR SPACE
#####################################################################

def test_invert_self_reversible(binary_images):
    for __image in binary_images:
        __temp = __image.convert('1')
        assert np.all(np.array(__temp) == np.array(invert(invert(__temp))))

#####################################################################
# PREPROCESSING
#####################################################################

def test_preprocess_binary_imagess(binary_images):
    for __image in binary_images:
        preprocess_image(
            image=__image,
            invert=False).save(
            fp=(
                '.processed'.join(os.path.splitext(__image.filename))
                + '.jpg'),
            format='JPEG')

#####################################################################
# DATAVIZ
#####################################################################

def test_folding_pattern_preview(binary_images):
    for __image in binary_images:
        generate_folding_pattern_preview_image(
            slices=postprocess_folding_pattern(slice_image(preprocess_image(
                image=__image,
                invert=False))),
            height=__image.height,
            spacing=1).save(
            fp=(
                '.pattern'.join(os.path.splitext(__image.filename))
                + '.jpg'),
            format='JPEG')
