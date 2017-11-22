import ...overworked.pattern as pattern
import ...overworked.book as book
from PIL import Image

# TODO describe the workflow :
#   find an appropriate image 
#   fit a pattern to the image
#   find the right book
#   fold !
# actually it can go both ways

pattern = pattern.Pattern('github/github.png')
pattern.preprocess(invert=False)
pattern.slice_image()
pattern.postprocess(160)
print pattern
pattern.save_image_preview(image_name='preview', image_path='github')
pattern.show()
#print pattern._dropout_factor

book = book.Book()
book.set_size(1, 589, 0.2, 0.15)
book.set_pattern(pattern)
book.save_folding_table(pattern_name='pattern', pattern_path='github')
print book
print book.sheet_spacing()
print book.sheet_count()
print book.sheet_height()
