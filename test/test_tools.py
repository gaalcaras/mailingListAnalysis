"""
Tests for various useful tools / functions
"""

import numpy as nmp
from tools import nth_elt, h_index

def test_nth_elt():
    a = [9, 8, 3]

    assert nth_elt(a, 0) == 9
    assert nmp.isnan(nth_elt(a, 4)) == True

def test_h_index():
    a = [3, 0, 6, 1, 5]
    b = [10, 8, 5, 4, 3]

    assert h_index(a) == 3
    assert h_index(b) == 4
