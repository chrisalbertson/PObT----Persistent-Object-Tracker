

def overlap_amount(box1, box2) -> float:
    """
    Determine how much, if any box1 intersects box2

    Params:
        box1: (x1, y1, x2, y2)
        box2: (x1, y1, x2, y2)

    Returns:
        float, intersection ratio

    >>> overlap_amount((1.0, 1.0, 3.0, 3.0), (1.0, 1.0, 3.0, 3.0))
    1.0

    >>> overlap_amount((1.0, 1.0, 2.0, 2.0), (3.0, 3.0, 4.0, 4.0))
    0.0

    >>> overlap_amount((1,1,2,2), (1,1,4,2))
    0.5

    >>> overlap_amount((0,1,3,2), (1,0,2,3))
    0.3333333333333333

    """

    box1x1, box1y1, box1x2, box1y2 = box1
    box2x1, box2y1, box2x2, box2y2 = box2

    # Check for horizontal overlap
    h1, h2 = range_overlap(box1x1, box1x2, box2x1, box2x2)
    if h1 == 0.0 and h2 == 0.0 :
        return 0.0

    # Check for vertical overlap
    v1, v2 = range_overlap(box1y1, box1y2, box2y1, box2y2)
    if v1 == 0.0 and v2 == 0.0 :
        return 0.0

    # Compute the boxes overlap amount.
    # We define this at the ratio as
    # 2 * the area of overlap over the sum of the box areas.
    # So if two boxes completely overlap the amount is 1.0
    box1_area = (box1x2 - box1x1) * (box1y2 - box1y1)
    box2_area = (box2x2 - box2x1) * (box2y2 - box2y1)
    overlap_area = (h2 - h1) * (v2 - v1)
    ratio = 2.0 * overlap_area / (box1_area + box2_area)

    return ratio



def range_overlap(a1: float, a2: float,
                 b1: float, b2: float) -> (float, float):
    """
    Given two ranges, compute and return their intersection

    Params:
        a1  low end of first range
        a2  high end of first range
        b1  low end of second range
        b2  high end of second range

    Returns:
        A tuple, (float, float) that gives the intersection

    Doctest Examples:

    >>> range_overlap(1.0, 4.0, 2.0, 6.0)
    (2.0, 4.0)

    >>> range_overlap(2.0, 6.0, 1.0, 4.0)
    (2.0, 4.0)

    >>> range_overlap(1.0, 6.0, 2.0, 5.0)
    (2.0, 5.0)

    >>> range_overlap(2.0, 5.0, 1.0, 6.0)
    (2.0, 5.0)
    """

    # Validate params
    if a1 >= a2 :
        raise ValueError("a1 not < a2")
    if b1 >= b2 :
        raise ValueError("b1 not < b2")

    if   (b1 <= a1 <= b2) and (b1 <= a2 <= b2) :
        return a1, a2       # a is fully contained in b

    elif (a1 <= b1 <= a2) and (a1 <= b2 <= a2) :
        return b1, b2       # b is fully contained in a

    elif b1 <= a1 <= b2 :
        return a1, b2       # a is to the right

    elif b1 <= a2 <= b2 :
        return b1, a2       # a is to the left

    else:
        return 0.0, 0.0      # no overlap


if __name__ == "__main__":
    import doctest
    doctest.testmod()