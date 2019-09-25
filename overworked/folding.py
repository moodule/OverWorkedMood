# -*- coding: utf-8 -*-

"""
===========
Folding Art
===========

Calculate how to fold pages to print an image into the depth of a book.
"""

from __future__ import division, print_function, absolute_import

from PIL import Image

from typical import checks, numeric

###############################################################################
# OUTPUT CONSTANTS
###############################################################################

IMAGE_SPECIFICATIONS_STR = """image ({width} x {height}) ratio {ratio}"""

PATTERN_SPECIFICATIONS_STR = """pattern ({width} x {height}) ratio {ratio}"""

###############################################################################
# SPECIFICATIONS
###############################################################################

@checks
def aspect_ratio(
        width: int,
        height: int) -> numeric:
    """
    Calculates the aspect ratio of an image or a pattern.

    Parameters
    ----------
    width:
        The width of the image in pixels.
        Or the width of the pattern as a slice count.
    height:
        The height of the image / pattern in pixels.

    Returns
    -------
        The aspect ratio of the image or pattern.
    """
    return float(width / height)

@checks
def coordinate_ratio(
        coordinate: int,
        dimension: int,
        reverse: bool=True) -> numeric:
    """
    Calculates the relative position of a pixel.

    Parameters
    ----------
    coordinate:
        The position as a pixel count.
    dimension:
        The size of the object as a pixel count.
    reverse:
        Whether to count from the lower or upper bound.

    Returns
    -------
        The position as a ratio.
    """
    __r =  min(
        1.0,
        max(
            0.0,
            float(coordinate) /float(dimension)))
    if reverse:
        return 1.0 - __r
    else:
        return __r

###############################################################################
# PATTERN
###############################################################################

@checks
def is_white_band(
        band_start: int,
        band_end: int) -> bool:
    """
    Says whether a pattern band is blank.
    """
    return (band_start == band_end)

@checks
def is_black_band(
        band_start: int,
        band_end: int,
        band_length) -> bool:
    """
    Says whether a pattern band is black.
    """
    return ((band_start <= 0)
        and (band_end >= (band_length - 1)))

#####################################################################
# VIEWING & EXPORTING
#####################################################################

Image.show()
Image.save(
    fp='path',
    format='png')

def _generate_pattern_image(sheet_width=3):
    pattern_image_width = sheet_width * self.width(raw=False)
    self._pattern_image = Image.new('1', (pattern_image_width, self.height(raw=True)), True)
    for i in xrange(self.width(raw=False)):
        self._fill_image_band(i, sheet_width)

#####################################################################
# VIEWING & EXPORTING
#####################################################################

def postprocess(wanted_width=None):
    self._filter_bands()
    self._even_slice_spacing(wanted_width)
    self._isolate_bands()
    self._generate_pattern_image()
    self._check_pattern()
    #self.save_pattern()

def _filter_bands(self):
    threshold = max((self.height(raw=True) // 40), 2)
    for i in range(len(self._slices)):
        raw_slice = self._slices[i]
        new_slice = []
        for band in raw_slice:
            if (band[1]-band[0]) > threshold:
                new_slice.append(band)
        self._slices[i] = new_slice

def _even_slice_spacing(wanted_width=None):
    self._identify_band_ranges()
    self._calculate_dropout_factor(wanted_width)
    self._calculate_step_ranges()

def _identify_band_ranges(self):
    self._band_ranges = []
    current_count = len(self._slices[0])
    current_start = 0
    for i, s in enumerate(self._slices):
        if s:
            self._band_count.add(len(s))
        else:
            self._band_count.add(1) # an empty slice (blank column) counts as a single band
        if len(s) != current_count:
            self._band_ranges.append((current_start, i, current_count))
            current_start = i
            current_count = len(s)
        if i == len(self._slices) - 1:
            self._band_ranges.append((current_start, len(self._slices), current_count))

def _calculate_dropout_factor(wanted_width=None):
    """Once evened the pattern has roughly the same width as the original image.
    Number of bands ~= number of slices = image width"""
    self._dropout_factor = 1
    if wanted_width is not None:
        self._dropout_factor = float(self.width(raw=True)) / float(wanted_width)
        self._dropout_factor = int(math.ceil(self._dropout_factor))
        self._dropout_factor = max(1, self._dropout_factor)

def _calculate_step_ranges(self):
    for (s, e, c) in self._band_ranges:
        if c:
            self._step_ranges.append((s, e, self._dropout_factor * c))
        else:
            self._step_ranges.append((s, e, self._dropout_factor))

def _check_pattern(self):
    if self.width(False) < self._min_band_count:
        print '! Warning ! The resolution of the pattern might be too low'
    if self.width(False) > self._max_band_count:
        print '! Warning ! The pattern will require a huge number of pages to fold'

def _isolate_bands(self):
    self._bands = []
    for (i_s, i_e, step) in self._step_ranges:
        for s in self._slices[i_s:i_e:step]:
            self._bands += s
            if len(s) == 0:     # if the slice is blank we represent it by an empty band
                self._bands.append((0,0))       # otherwise the pattern would skip the blank parts

###############################################################################
# END TO END WORKFLOW
###############################################################################

def preprocess(invert=False):
    self._fill_background()
    self._transform_black_white()
    self._emphasize_image()
    self._transform_binary()
    self._crop_image()
    self._smooth_image()
    
    if invert:
        self._invert()

def slice_image(self):
    self._slices = np.empty((self.width(raw=True),),dtype=object)
    temp = np.array(self._image).transpose()
    for x in xrange(self.width(raw=True)):
        self._slices[x] = []
        previous_color = True   # white
        current_color = True    # white, the picture is encoded in binary
        current_start = -1
        current_end = -1
        for y in xrange(self.height(raw=True)):
            current_color = temp[x, y]
            if current_color != previous_color:
                if current_color:
                    current_end = y - 1     # can't happen at y=0
                    self._slices[x].append((current_start, current_end))
                    current_start = -1
                    current_end = -1
                else:
                    current_start = y
            if y >= (self.height(raw=True) - 1):
                if current_color == False:
                    self._slices[x].append((current_start, self.height(raw=True) - 1))
            previous_color = current_color

def postprocess(wanted_width=None):
    self._filter_bands()
    self._even_slice_spacing(wanted_width)
    self._isolate_bands()
    self._generate_pattern_image()
    self._check_pattern()
    #self.save_pattern()
