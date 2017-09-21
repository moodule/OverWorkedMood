import pattern
from PIL import Image

test_image = Image.open('images/firebase.png')

pattern = pattern.Pattern(test_image)
pattern.preprocess()
