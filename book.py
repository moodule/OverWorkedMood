class Book(object):
    """Models the whole book"""
    
    def __init__(self):
        self.page_count = 100           # no unit, the total page count, equals last page number
        self.sheet_margin_s = 10        # no unit, it is the number of sheets left both before and after the pattern
        self.paper_margin_m = 0.01      # in meters, the blank space left both above and under the pattern
