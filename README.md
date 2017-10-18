The **OverWorked** moodule lets you generate patterns of book folding.
These can then be used to create a 3d shape close to a sculpture by folding the pages.

# Installation

# Quick Start

# Resources
The project can be accessed directly through a [web app](), without any installation.

# Process
- [x] read image
- [x] convert to grayscales
- [x] filter out small objects
- [x] somehow filter / classify between b&w, the output image must be binary
- [ ] intermediate grays could be interpreted as the slope of the folded pattern 
- [ ] divide gray values into several (3 ?) levels : white, shadow, black
- [ ] calculate an intermediate folding for shadow grays
- [x] locate the boundaries, in pixels
- [x] infer the pattern dimensions in pixels
- [x] crop image to remove the white outside the actual picture frame
- [x] calculate the number of levels per slice
- [x] translate to a level (boundaries) matrix, in pixel unit
- [x] calculate the optimal book margins from the pattern size
- [x] calculate the book opening from the pattern size
- [x] calculate the flattened width of the image in pixels (a slice with 3 levels counts as 3 slices)
- [x] give a recommendation for the min pages
- [x] convert pixel height to book mark (in cm, taking into account the margins)
- [x] filter and dropout the slices to even the slice spacing (when slices are sprayed out on multiple sheets)
- [x] output the table of folds, for each sheet of paper, in cm
- [ ] exception for the fully black pages : no folding at all
- [ ] interprete the layer bounds as (x, y) graphs and display them
- [ ] describe the workflow(s) to get a book folding art
- [ ] put everything into a notebook

greater slopes are more bright (?)
