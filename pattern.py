import numpy as np
from PIL import Image as Pimage

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
        self._transform_black_white()
        self._crop()
        self._update_attributes()
        self._image.show()

    def postprocess(self):
        self._smooth_pattern()
        self._update_attributes()
        self._image.show()

    def _update_attributes(self):
        self.width = self._image.width
        self.height = self._image.height

    def _transform_black_white(self):
        self._image = self._image.convert("L")
        self._image = self._image.point(lambda x: 0 if x<85 else 255, '1')

    def _crop(self):
        x_array = np.array(self._image)
        x_array = np.sum(x_array, axis=1)
        x_array = np.nonzero(x_array)[0]

        y_array = np.array(self._image)
        y_array = np.sum(y_array, axis=0)
        y_array = np.nonzero(y_array)[0]
        
        #self._image.crop((min_x, max_y, max_x, min_y))

    def _smooth_pattern(self):
        pass

    def _even_slice_spacing(self):
        pass
