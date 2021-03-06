import fractions
import math
import numpy as np
import os
from PIL import Image
from PIL import ImageOps
import _tools

# TODO normaliser / augmenter le contraste : plutot que d'avoir un critere absolu b&w

PATTERN_STR = ''

class Pattern(object):

    def __init__(self, image_path):
        self._path, self._name = os.path.split(image_path)
        self._name, self._image_extension = os.path.splitext(self._name)
        self._image_extension  = self._image_extension.replace('.', '')
        self._image = Image.open(image_path)
        self._slices = np.empty((self._image.width,), dtype=object)
        self._bands = []
        self._min_band_count = 100
        self._max_band_count = 500
        self._band_ranges = []
        self._band_count = set()
        self._dropout_factor = 1
        self._step_ranges = []

    def __str__(self):
        str_format = """{pattern_name:=<050}
image ({image_width} x {image_height}) ratio {image_ratio}
pattern ({pattern_width} x {pattern_height}) ratio {pattern_ratio}"""
        return str_format.format(
                pattern_name='= Pattern ' + self._name + ' ',
                image_width=self.width(raw=True),
                image_height=self.height(raw=True),
                image_ratio=self.aspect_ratio(raw=True),
                pattern_width=self.width(raw=False),
                pattern_height=self.height(raw=False),
                pattern_ratio=self.aspect_ratio(raw=False))

    def name(self):
        return self._name

    def path(self):
        return self._path

    def width(self, raw=True):
        w = self._image.width
        if not raw:
            w = len(self._bands)
        return w

    def height(self, raw=True):
        h = self._image.height
        return h

    def aspect_ratio(self, raw=False):
        r = 1.0
        if raw and self.height(raw=True):
            r = float(self.width(raw=True)) / float(self.height(raw=True))
        elif not raw and self.height(raw=False):
            r = float(self.width(raw=False)) / float(self.height(raw=False))
        return r

    def vertical_coordinate_ratio(self, pixel_y, from_top=True, raw=False):
        r = 0.0
        if self.height(raw):
            r = float(pixel_y) / float(self.height(raw))
        if not from_top:
            r = 1.0 - r
        r = min(1.0, max(0.0, r))
        return r

    def horizontal_coordinate_ratio(self, pixel_x, from_left=True, raw=False):
        r = 0.0
        if self.width(raw):
            r = float(pixel_x) / float(self.width(raw))
        if not from_left:
            r = 1.0 - r
        r = min(1.0, max(0.0, r))
        return r

    def is_white_band(self, band):
        return (band[0] == band[1])

    def is_black_band(self, band):
        return (band[0] == 0) and (band[1] >= (self.height(raw=False) - 1))

    def preprocess(self, invert=False):
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

    def postprocess(self, wanted_width=None):
        self._filter_bands()
        self._even_slice_spacing(wanted_width)
        self._isolate_bands()
        self._generate_pattern_image()
        self._check_pattern()
        #self.save_pattern()

    def show(self, source='pattern'):
        if source == 'pattern':
            self._pattern_image.show()
        else:
            self._image.show()

    def save_image_preview(self, image_name='', image_path=''):
        saving_path = _tools.full_path_to_file(
                name=self.name if not image_name else image_name,
                path='./' if not image_path else image_path,
                extension='png')
        self._pattern_image.save(saving_path, format='png')

    def _generate_pattern_image(self, sheet_width=3):
        pattern_image_width = sheet_width * self.width(raw=False)
        self._pattern_image = Image.new('1', (pattern_image_width, self.height(raw=True)), True)
        for i in xrange(self.width(raw=False)):
            self._fill_image_band(i, sheet_width)

    def _fill_background(self):
        if self._image.mode == 'RGBA':
            self._image.load()
            temp = np.array(self._image)
            mask = (temp[:,:,3] == 0)
            temp[:,:,:4][mask] = [255, 255, 255, 255]
            self._image = Image.fromarray(temp)

    def _emphasize_image(self):
        temp = np.array(self._image)
        min_level = np.amin(temp)
        max_level = np.amax(temp)
        if max_level > min_level:
            self._image = self._image.point(lambda x: 255. * (x - min_level) / (max_level - min_level))

    def _transform_black_white(self):
        self._image = self._image.convert("L")
        
    def _transform_binary(self):
        self._image = self._image.point(lambda x: 0 if x<85 else 255, '1')

    def _crop_image(self):
        temp = np.invert(np.array(self._image))
        is_image_empty = np.sum(temp)
        is_image_empty = is_image_empty == 0.0
        
        if not is_image_empty:
            x_array = np.sum(temp, axis=1)
            x_array = np.transpose(np.nonzero(x_array))

            y_array = np.sum(temp, axis=0)
            y_array = np.transpose(np.nonzero(y_array))

            min_x = x_array[0]
            max_x = x_array[::-1][0]

            min_y = y_array[0]
            max_y = y_array[::-1][0]
        else:
            raise Exception('The provided image is empty !')
        
        self._image = self._image.crop((min_y, min_x, max_y, max_x))

    def _smooth_image(self):
        pass

    def _invert(self):
        self._image = self._image.convert('L')
        self._image = ImageOps.invert(self._image)
        self._image = self._image.convert('1')

    def _filter_bands(self):
        threshold = max((self.height(raw=True) // 40), 2)
        for i in range(len(self._slices)):
            raw_slice = self._slices[i]
            new_slice = []
            for band in raw_slice:
                if (band[1]-band[0]) > threshold:
                    new_slice.append(band)
            self._slices[i] = new_slice

    def _even_slice_spacing(self, wanted_width=None):
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

    def _calculate_dropout_factor(self, wanted_width=None):
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

    def _fill_image_band(self, band_index, sheet_width=1):
        """The sheet is represented by [sheet_width] columns :
        - at the center is the actual paper, a line of 1 pixel
        - the other columns are left blank to represent the spacing of the sheets of paper"""
        band = self._bands[band_index]
        x = band_index * sheet_width
        for y in range(band[0], band[1]):
            self._pattern_image.putpixel((x,y), False)
