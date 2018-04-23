"""
Tests for various useful tools / functions
"""

import numpy as nmp
from tools import nth_elt, h_index, rect_dimension, rect_list, int_list

def test_nth_elt():
    a = [9, 8, 3]

    assert nth_elt(a, 0) == 9
    assert nmp.isnan(nth_elt(a, 4)) == True

def test_h_index():
    a = [3, 0, 6, 1, 5]
    b = [10, 8, 5, 4, 3]

    assert h_index(a) == 3
    assert h_index(b) == 4

def test_rect_dimension():
    assert rect_dimension(9) == 3
    assert rect_dimension(17) == 4

def test_rect_list():
    l1 = list(range(0, 10))
    l2 = list(range(0, 17))
    assert rect_list(l1) == [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]
    assert rect_list(l2)[:-1] == [(0, 1, 2, 3),
                                      (4, 5, 6, 7),
                                      (8, 9, 10, 11),
                                      (12, 13, 14, 15)#,
                                    # (16, nan, nan, nan) # That's what we test for below
                                    ]
    assert rect_list(l2)[-1][0] == 16
    assert all(nmp.isnan(rect_list(l2)[-1][i]) for i in range(1,4)) == True

def test_int_list():
    l1 = ['a', 'a', 'b', 'c', 'd', 'd', 'd', 'e']

    assert int_list(l1) == [0, 0, 1, 2, 3, 3, 3, 4]
