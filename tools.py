import numpy as nmp
import math

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

def square_dimension(integer):
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

def square_list(sequence):
    chunk = square_dimension(len(sequence))
    result = list(zip(*[iter(sequence)] * chunk))

    diff = len(sequence) % chunk
    if diff > 0:
        row = sequence[-diff:]

        # Add NAN to have a full row of elements
        missing = len(result[0]) - len(row)
        print(missing)
        row.extend([nmp.nan] * missing)
        print(row)

        result.append(tuple(row))

    return result
