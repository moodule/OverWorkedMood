import pattern
import book
from PIL import Image

# TODO describe the workflow :
#   find an appropriate image 
#   fit a pattern to the image
#   find the right book
#   fold !

pattern = pattern.Pattern('images/exemples/test.png')
pattern.preprocess(invert=False)
pattern.slice_image()
pattern.postprocess()
#pattern.show()
#pattern._generate_pattern_image(sheet_width=1)
#pattern.show()
print pattern
#print pattern._bands

book = book.Book()
book.set_size(1, 200, 0.2, 0.1)
book.set_pattern(pattern)
book.save_folding_table()
print book
print book.sheet_spacing()
print book.sheet_count()
print book.sheet_height()
