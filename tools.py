import os
import pandas as pd
import numpy as np
import math
import re

def nth_elt(elts, nth):
    """Return nth element of list of elts, nan if nth element does not exist"""
    return elts[nth] if len(elts) >= nth + 1 else np.nan

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

def int_list(sequence):
    """Given a sorted list A of elements, return a sorted list B of integers
    starting at 0, where each unique value in A has one and only one equivalent
    in B"""

    result = list(range(0, len(sequence)))

    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i-1]:
            result[i] = result[i-1]
        else:
            result[i] = result[i-1]+1

    return result

def rect_dimension(integer):
    """Find dimension x of a rectangle that can contain all values of
    a range from 1 to integer while keeping rectangle as close to a square as
    possible"""

    sqrt = math.floor(math.sqrt(integer))
    m1 = 0

    for i in reversed(range(1, sqrt+1)):
        remainder = integer % i

        if remainder == 0:
            m1 = i
            break

    # Prime numbers
    if m1 == 1:
        m1 = sqrt

    return m1

def rect_list(sequence):
    chunk = rect_dimension(len(sequence))
    result = list(zip(*[iter(sequence)] * chunk))

    diff = len(sequence) % chunk
    if diff > 0:
        row = sequence[-diff:]

        # Add NAN to have a full row of elements
        missing = len(result[0]) - len(row)
        print(missing)
        row.extend([np.nan] * missing)
        print(row)

        result.append(tuple(row))

    return result

def save_fig(fig, *args):
    """Export a matplotlib figure to a svg file, with path given as a list
    of arguments.

    :fig: matplotlib figure
    :args: path (e.g. 'dir', 'to', 'file')"""

    path = os.path.join(*[str(a) for a in args])

    dirname = os.path.dirname(path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    fig.savefig('{}.svg'.format(path))

def is_patch(subject):
    """Returns True if subject appears to be a patch.

    :subject: subject of an email (str)
    """
    if pd.isnull(subject):
        return False

    patch = re.compile(r'\[[^\]]*(PATCH|RFC)[^\]]*\]')

    if patch.match(subject):
        return True

    return False

def gini(array):
    """Calculate the Gini coefficient of a numpy array.
    Adapted from https://github.com/oliviaguest/gini

    :array: numpy array
    """

    array = array.flatten()
    if np.amin(array) < 0:
        # Values cannot be negative:
        array -= np.amin(array)

    # Values cannot be nan, inf or 0:
    array = np.nan_to_num(array)
    array = np.add(0.0000001, array, casting='unsafe')

    # Values must be sorted:
    array = np.sort(array)

    # Index per array element:
    index = np.arange(1, array.shape[0]  +1)

    # Number of array elements:
    n = array.shape[0]

    return (np.sum((2 * index - n - 1) * array)) / (n * np.sum(array))
