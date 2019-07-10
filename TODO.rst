Project
-------

- [ ] restructure the repository : docs, tests etc (cf (Kenneth Reitz)[https://github.com/requests/requests])
- [ ] unit test everything
- [ ] segregate the internal tools so that they're not exported
- [ ] write the documentation
- [ ] export the documentation on readthedocs
- [ ] use the latest boilerplate autoations
- [ ] write in the functional paradigm style, better suited

Interface
---------

- [ ] describe the workflow(s) to get a book folding art
- [ ] create a jupyter notebook to walk the user through the process
- [ ] add a cli with Click
- [ ] put a web app on my website

Image processing
----------------

- [x] read image
- [x] convert to grayscales
- [x] crop image to remove the white outside the actual picture frame
- [x] filter out small objects
- [x] somehow filter / classify between b&w, the output image must be binary
- [ ] intermediate grays could be interpreted as the slope of the folded pattern
- [ ] divide gray values into several (3 ?) levels : white, shadow, black

Pattern generation
------------------

- [x] infer the pattern dimensions in pixels
- [x] translate the image to a matrix of boundaries, in pixel unit
- [x] calculate the number of levels per slice
- [x] calculate the flattened width of the image in pixels (a slice with 3 levels counts as 3 slices)
- [x] filter and dropout the slices to even the slice spacing (when slices are sprayed out on multiple sheets)
- [x] convert pixel height to book mark (in cm, taking into account the margins)

Book folding
------------

- [x] calculate the optimal book margins from the pattern size
- [x] calculate the book opening from the pattern size
- [x] give a recommendation for the min pages
- [ ] calculate an intermediate folding for shadow grays
- [x] exception for the fully black pages : no folding at all

Visualisation
-------------

- [x] preview the folded pattern, with the space between paper sheets
- [ ] interprete the layer bounds as (x, y) graphs and display them

Output
------

- [x] save the image preview of the pattern
- [x] output the table of folds, for each sheet of paper, in cm
