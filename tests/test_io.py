#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `overworked` package."""

import os
import pytest

import numpy as np
from PIL import Image

from overworked._image_processing import (
    preprocess_image,)
from overworked.folding import (
    slice_image,
    postprocess_folding_pattern)

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
# 
#####################################################################
