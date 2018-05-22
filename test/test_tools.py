"""
Tests for various useful tools / functions
"""

import numpy as np
from tools import nth_elt, h_index, rect_dimension, rect_list, int_list, is_patch
from tools import gini

def test_nth_elt():
    a = [9, 8, 3]

    assert nth_elt(a, 0) == 9
    assert np.isnan(nth_elt(a, 4)) == True

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
    assert all(np.isnan(rect_list(l2)[-1][i]) for i in range(1,4)) == True

def test_int_list():
    l1 = ['a', 'a', 'b', 'c', 'd', 'd', 'd', 'e']

    assert int_list(l1) == [0, 0, 1, 2, 3, 3, 3, 4]

def test_is_patch():
    assert is_patch('[PATCH 0/2] Fix crashes due to real_pathdup() potentially returning NULL') == True
    assert is_patch('[RFC PATCH v2 0/9] Improve merge recursive performance') == True
    assert is_patch('[PATCH V2 1/2] Fix delta integer overflows') == True
    assert is_patch('[RFC for GIT] pull-request: add praise to people doing QA') == True

    assert is_patch('patch proposal') == False

def test_gini():
    test1 = np.array([1, 1, 1])

    test2 = np.zeros(1000)
    test2[0] = 10

    test3 = np.random.uniform(-1, 0, 1000)

    assert gini(np.array([1, 1, 1])) == 0
    assert round(gini(test2), 1) == 1
    assert round(gini(test3), 2) == 0.33
