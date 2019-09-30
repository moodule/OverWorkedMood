#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `overworked` package."""

import pytest

import numpy as np

from overworked._image_processing import (
    preprocess_image)
from overworked.folding import (
    slice_image)

#####################################################################
# SLICING
#####################################################################

def test_sliced_image_size(binary_images):
    for __image in binary_images:
        with preprocess_image(__image) as __input:
            assert (
                np.shape(slice_image(__input))[0] # number of ranges
                <= np.shape(__input)[1]) # width
