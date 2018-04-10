import numpy as nmp

def nth_elt(elts, nth):
    """Return nth element of list of elts, nan if nth element does not exist"""
    return elts[nth] if len(elts) >= nth + 1 else nmp.nan

def h_index(degrees):
    """Returns h-index for a given list of degrees (a thread has index h if
    h of its messages have at least a degree of h).

    :degrees: list of int degrees
    :returns: int (h-index)
    """

    d = degrees
    d.sort(reverse=True)

    h_index = 0

    for deg in degrees:
        if deg >= h_index+1:
            h_index += 1
        else:
            break

    return h_index
