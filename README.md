The **OverWorked** moodule lets you generate patterns of book folding.
These can then be used to create a 3d shape close to a sculpture by folding the pages.

# Installation

# Quick Start

# Resources
The project can be accessed directly through a [web app](), without any installation.

# Process
[ ] read image
[ ] convert to grayscales
[ ] somehow filter / classify between b&w, the output image must be binary
[ ] intermediate grays could be interpreted as the slope of the folded pattern 
[ ] locate the boundaries, in pixels
[ ] infer the pattern dimensions in pixels
[ ] crop image to remove the white outside the actual picture frame
[ ] calculate the number of levels per slice
[ ] translate to a level (boundaries) matrix, in pixel unit
[ ] configure the pattern : book height, book pages (rec), margins
[ ] calculate the flattened width of the image in pixels (a slice with 3 levels counts as 3 slices)
[ ] give a recommendation for the min pages
[ ] convert pixel height to book mark (in cm, taking into account the margins)
[ ] determine the frequency of the slices
[ ] output the table of folds, for each sheet of paper, in cm

greater slopes are darker (?)
