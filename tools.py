import numpy as nmp

def nth_elt(elts, nth):
    """Return nth element of list of elts, nan if nth element does not exist"""
    return elts[nth] if len(elts) >= nth + 1 else nmp.nan
