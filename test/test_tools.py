"""
Tests for various useful tools / functions
"""

from tools import nth_elt
import numpy as nmp

def test_nth_elt():
    a = [9, 8, 3]

    assert nth_elt(a, 0) == 9
    assert nmp.isnan(nth_elt(a, 4)) == True
