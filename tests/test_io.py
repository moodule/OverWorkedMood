#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `overworked` package."""

import pytest

from overworked._image_processing import (
    preprocess_image)
from overworked._io import (
    generate_folding_table)
from overworked.folding import (
    slice_image,
    postprocess_folding_pattern)

#####################################################################
# FOLDING TABLE
#####################################################################
