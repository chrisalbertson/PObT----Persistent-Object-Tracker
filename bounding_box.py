class BoundingBox:
    """ A class to represent bounding boxes and compute some basic geometry on them. """

    def __init__(self,
                 x_min: float,
                 x_max: float,
                 y_min: float,
                 y_max: float):

        assert (x_min < x_max), 'x_min not less than x_max'
        assert (y_min < y_max), 'y_min not less than y_max'

        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max


    def __repr__(self):
        """Return a string that is a human readable represention of a bounding box

        Doctest Examle:
        >>> bb = BoundingBox(1.0, 2.0, 3.0, 4.0)
        >>> bb.__repr__()
        '<BoundingBox 1.0, 2.0, 3.0, 4.0>'
        """
        return f'<BoundingBox {self.x_min}, {self.x_max}, {self.y_min}, {self.y_max}>'

    @property
    def x_size(self):
        """Return the width in the X direction of a bounding box

        Doctest Examle:
        >>> bb = BoundingBox(1.0, 2.0, 1.0, 3.0)
        >>> bb.x_size
        1.0
        """
        return self.x_max - self.x_min

    @property
    def y_size(self):
        """Return the hight in the Y direction of a bounding box

        Doctest Examle:
        >>> bb = BoundingBox(1.0, 2.0, 1.0, 3.0)
        >>> bb.y_size
        2.0
        """
        return self.y_max - self.y_min

    @property
    def x_mid(self):
        """Return the mid point in the X direction of a bounding box

        Doctest Examle:
        >>> bb = BoundingBox(1.0, 2.0, 1.0, 3.0)
        >>> bb.x_mid
        1.5
        """
        return (self.x_max + self.x_min) / 2.0

    @property
    def y_mid(self):
        """Return the mid point in the Y direction of a bounding box

        Doctest Examle:
        >>> bb = BoundingBox(1.0, 2.0, 1.0, 3.0)
        >>> bb.y_mid
        2.0
        """
        return (self.y_max + self.y_min) / 2.0

    def overlap_amount(self, box2) -> float:
        """Determine how much, if any box1 intersects box2

        Overlap is defined here on a scale of 0.0 to 1.0 where 0.0 means the boxes
        do not intersect at all.  1.0 means the boxes are identical.

        Params:
            box2: another BoundingBox object

        Returns:
            float, intersection ratio

        Doctest Examle:
        >>> bb1 = BoundingBox(1.0, 3.0, 1.0, 3.0)
        >>> bb2 = BoundingBox(1.0, 3.0, 1.0, 3.0)
        >>> bb1.overlap_amount(bb2)
        1.0

        >>> bb1 = BoundingBox(1.0, 2.0, 1.0, 2.0)
        >>> bb2 = BoundingBox(3.0, 4.0, 3.0, 4.0)
        >>> bb1.overlap_amount(bb2)
        0.0

        >>> bb1 = BoundingBox(1,2,1,2)
        >>> bb2 = BoundingBox(1,4,1,2)
        >>> bb1.overlap_amount(bb2)
        0.5

        Verify that type checking works
        >>> bb1 = BoundingBox(0,3,1,2)
        >>> bb1.overlap_amount( 100.5 )
        Traceback (most recent call last):
        ...
        TypeError: box2 needs to be a BoundingBox
        """

        # Verify box2 is the correct type
        if not isinstance(box2, BoundingBox):
            raise TypeError('box2 needs to be a BoundingBox')

        # Check for horizontal overlap
        x1, x2 = range_overlap(self.x_min, self.x_max, box2.x_min, box2.x_max)
        if x1 == 0.0 and x2 == 0.0:
            return 0.0

        # Check for vertical overlap
        y1, y2 = range_overlap(self.y_min, self.y_max, box2.y_min, box2.y_max)
        if y1 == 0.0 and y2 == 0.0:
            return 0.0

        # Compute the boxes overlap amount.
        # We define this at the ratio as
        # 2 * the area of overlap over the sum of the box areas.
        # So if two boxes completely overlap the amount is 1.0
        self_area = (self.x_max - self.x_min) * (self.y_max - self.y_min)
        box2_area = (box2.x_max - box2.x_min) * (box2.y_max - box2.y_min)
        overlap_area = (x2 - x1) * (y2 - y1)
        ratio = (2.0 * overlap_area) / (self_area + box2_area)

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
    assert (a1 < a2), "a1 not < a2"
    assert (b1 < b2), "b1 not < b2"

    if (b1 <= a1 <= b2) and (b1 <= a2 <= b2):
        return a1, a2       # a is fully contained in b

    elif (a1 <= b1 <= a2) and (a1 <= b2 <= a2):
        return b1, b2       # b is fully contained in a

    elif b1 <= a1 <= b2:
        return a1, b2       # a is to the right

    elif b1 <= a2 <= b2:
        return b1, a2       # a is to the left

    else:
        return 0.0, 0.0      # no overlap

# If called from command line run the tests.
if __name__ == "__main__":
    import doctest
    doctest.testmod()
