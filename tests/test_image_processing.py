#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `overworked` package."""

import os
import pytest

import numpy as np
from PIL import Image

from overworked._image_processing import (
    invert)

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
