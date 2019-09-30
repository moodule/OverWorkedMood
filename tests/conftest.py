#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `overworked` package."""

import pytest

from PIL import Image

#####################################################################
# PATHS
#####################################################################

IMAGE_PATHS = {
    'binary': [
        'tests/fixtures/data/binary/github.png',
        'tests/fixtures/data/binary/chardon.png']}

#####################################################################
# ACTUAL IMAGES
#####################################################################

@pytest.fixture
def binary_images():
    __temp = [Image.open(__path) for __path in IMAGE_PATHS['binary']]
    yield __temp
    for __image in __temp:
        __image.close()
