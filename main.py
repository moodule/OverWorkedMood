import pattern
from PIL import Image

test_image = Image.open('images/exemples/bike.png')

pattern = pattern.Pattern(test_image)
pattern.preprocess()
pattern.slice_image()
pattern.postprocess()
pattern.show()
