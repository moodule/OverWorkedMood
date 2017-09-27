import pattern
from PIL import Image

test_image = Image.open('images/tensorflow.jpg')

pattern = pattern.Pattern(test_image)
pattern.preprocess()
pattern.slice_image()
pattern.postprocess()
pattern.show()
print pattern._band_to_pixel_columns((10,45),2)
