import pattern
from PIL import Image

test_image = Image.open('images/monte-rosa.jpg')

pattern = pattern.Pattern(test_image)
pattern.preprocess()
