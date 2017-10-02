import pattern
from PIL import Image

pattern = pattern.Pattern('images/exemples/bike.png')
pattern.preprocess(invert=False)
pattern.slice_image()
pattern.postprocess()
pattern.show()
