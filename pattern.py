import numpy as np
from PIL import Image

# TODO normaliser / augmenter le contraste : plutot que d'avoir un critere absolu b&w
# TODO even the sheet spacing : if a 

class Pattern(object):

    def __init__(self, image):
        self._image = image
        self._image.load()
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

    def preprocess(self):
        self._fill_background()
        self._transform_black_white()
        self._image.show()
        self._emphasize()
        self._image.show()
        self._transform_binary()
        self._image.show()
        self._crop()
        self._update_attributes()

    def postprocess(self):
        self._smooth_pattern()
        self._update_attributes()

    def _update_attributes(self):
        self.width = self._image.width
        self.height = self._image.height

    def _fill_background(self):
        if self._image.mode == 'RGBA':
            self._image.load()
            white_bg_image = Image.new('RGBA', self._image.size, (255,255,255))
            self._image = white_bg_image.paste(self._image, mask=self._image.split()[3])

    def _emphasize(self):
        temp = np.array(self._image)
        min_level = np.amin(temp)
        max_level = np.amax(temp[temp < 255])
        if max_level > min_level:
            self._image = self._image.point(lambda x: 255. * (x - min_level) / (max_level - min_level))

    def _transform_black_white(self):
        self._image = self._image.convert("L")
        
    def _transform_binary(self):
        self._image = self._image.point(lambda x: 0 if x<85 else 255, '1')

    def _crop(self):
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

    def _smooth_pattern(self):
        pass

    def _even_slice_spacing(self):
        pass
