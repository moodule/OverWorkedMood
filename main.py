import pattern
import book
from PIL import Image

# TODO describe the workflow :
#   find an appropriate image 
#   fit a pattern to the image
#   find the right book
#   fold !
# actually it can go both ways

pattern = pattern.Pattern('images/examples/github.png')
pattern.preprocess(invert=False)
pattern.slice_image()
pattern.postprocess(300)
print pattern
pattern.show()
print pattern._dropout_factor

book = book.Book()
book.set_size(1, 600, 0.2, 0.1)
book.set_pattern(pattern)
book.save_folding_table()
print book
print book.sheet_spacing()
print book.sheet_count()
print book.sheet_height()
