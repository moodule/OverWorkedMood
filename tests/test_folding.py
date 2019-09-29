#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `overworked` package."""

import os
import pytest

import numpy as np
from PIL import Image

from overworked.folding import preprocess, slice_image

#####################################################################
# _
#####################################################################

@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')

def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

#####################################################################
# FIX
#####################################################################

IMAGE_PATHS = {
    'binary': [
        'tests/data/binary/github.png']}

#####################################################################
# PREPROCESSING
#####################################################################

def test_preprocess_binary_images():
    for __path in IMAGE_PATHS['binary']:
        with Image.open(__path) as __image:
            preprocess(
                image=__image,
                invert=False).save(
                fp=(
                    '.processed'.join(os.path.splitext(__path))
                    + '.jpg'),
                format='JPEG')

#####################################################################
# SLICING
#####################################################################

def test_sliced_image_size():
    for __path in IMAGE_PATHS['binary']:
        with preprocess(Image.open(__path)) as __image:
            assert (
                np.shape(slice_image(__image))[0] # number of ranges
                <= np.shape(__image)[1]) # width
