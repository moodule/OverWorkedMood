import numpy as np
import os
from PIL import Image
from PIL import ImageOps

# TODO normaliser / augmenter le contraste : plutot que d'avoir un critere absolu b&w
# TODO even the sheet spacing
# TODO sheet spacing modes = none, max, pgcd, repeat, space
# TODO warn when the whole page must be folded
# TODO band_count : [(s_0,e_0,b_c_0) (s_1,e_1,b_c_1) ...]
# TODO steps : [(s_0,e_0,step_0) (s_1,e_1,step_1) ...]
# TODO max band count : prevent the pattern from growing too big

class Pattern(object):

    def __init__(self, image_path):
        self.path, self.name = os.path.split(image_path)
        self.name, self._image_extension = os.path.splitext(self.name)
        self._image_extension  = self._image_extension.replace('.', '')
        self._image = Image.open(image_path)
        self._slices = np.empty((self._image.width,), dtype=object)
        self._bands = []
        self._update_attributes()

    def __str__(self):
        str_format = """Pattern :\n
        - min level count : {min_level_count}\n
        - max level count : {max_level_count}\n
        - cropped width : {cropped_width}\n
        - cropped height : {cropped_height}\n
        - unfolded width : {unfolded_with}\n
        - min sheet count : {min_slice_count}\n
        - max sheet count : {max_slice_count}\n
        - rec sheet count : {rec_sheet_count}"""

    def preprocess(self, invert=False):
        self._fill_background()
        self._transform_black_white()
        self._emphasize_image()
        self._transform_binary()
        self._crop_image()
        self._smooth_image()
        
        if invert:
            self._invert()

        self._update_attributes()

    def slice_image(self):
        self._slices = np.empty((self.width,),dtype=object)
        temp = np.array(self._image).transpose()
        for x in xrange(self.width):
            self._slices[x] = []
            previous_color = True   # white
            current_color = True    # white, the picture is encoded in binary
            current_start = -1
            current_end = -1
            for y in xrange(self.height):
                current_color = temp[x,y]
                if current_color != previous_color:
                    if current_color:
                        current_end = y - 1     # can't happen at y=0
                        self._slices[x].append((current_start, current_end))
                        current_start = -1
                        current_end = -1
                    else:
                        current_start = y
                if y >= (self.height - 1):
                    if current_color == False:
                        self._slices[x].append((current_start, self.height - 1))
                previous_color = current_color

    def postprocess(self):
        self._filter_bands()
        self._isolate_bands()
        self._generate_pattern_image()
        self.save_image()
        #self.save_pattern()
        self._update_attributes()

    def show(self, source='pattern'):
        if source == 'pattern':
            self._pattern_image.show()
        else:
            self._image.show()

    def save_image(self, image_path=None):
        saving_path = os.path.join('patterns/', self.name)
        if image_path is not None:
            if type(image_path) is str and image_path:
                saving_path = image_path
        saving_path, ext = os.path.splitext(saving_path)
        ext = ext.replace('.', '')
        if not ext:
            ext = self._image_extension
        ext = 'png'
        saving_path += '.' + ext.lower()
        self._pattern_image.save(saving_path, format=ext)

    def _generate_pattern_image(self, sheet_width=1):
        band_count = len(self._bands)
        pattern_image_width = 3 * sheet_width * band_count
        self._pattern_image = Image.new('1', (pattern_image_width, self.height), True)
        for i in xrange(band_count):
            self._fill_image_band(i, sheet_width)

    def _update_attributes(self):
        self.width = self._image.width
        self.height = self._image.height
        self.band_count = len(self._bands)

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
        for raw_slice in self._slices:
            new_slice = []
            for band in raw_slice:
                if (band[1]-band[0]) > (self.height // 300):
                    new_slice.append(band)
            raw_slice = new_slice

    def _even_slice_spacing(self):
        pass

    def _isolate_bands(self, step=1):
        self._bands = []
        for s in self._slices[::step]:
            self._bands += s

    def _fill_image_band(self, band_index, sheet_width=1):
        band = self._bands[band_index]
        for x in range(3 * band_index * sheet_width, (1 + 3*band_index) * sheet_width):
            for y in range(band[0], band[1]):
                self._pattern_image.putpixel((x,y), False)
