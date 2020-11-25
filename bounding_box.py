class BoundingBox:
    def __init__(self,
                 x_min: float,
                 x_max: float,
                 y_min: float,
                 y_max: float):

        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max


    def __repr__(self):
        """

        Returns:

        >>> bb = BoundingBox(1.0, 2.0, 3.0, 4.0)
        >>> bb.__repr__()
        '<BoundingBox 1.0, 2.0, 3.0, 4.0>'
        """
        return f'<BoundingBox {self.x_min}, {self.x_max}, {self.y_min}, {self.y_max}>'

    @property
    def x_size(self):
        """

        Returns:

        >>> bb = BoundingBox(1.0, 2.0, 1.0, 3.0)
        >>> bb.x_size
        1.0
        """
        return self.x_max - self.x_min

    @property
    def y_size(self):
        """

        Returns:

        >>> bb = BoundingBox(1.0, 2.0, 1.0, 3.0)
        >>> bb.y_size
        2.0
        """
        return self.y_max - self.y_min

    @property
    def x_mid(self):
        """

        Returns:

        >>> bb = BoundingBox(1.0, 2.0, 1.0, 3.0)
        >>> bb.x_mid
        1.5
        """
        return (self.x_max + self.x_min) / 2.0

    @property
    def y_mid(self):
        """

        Returns:

        >>> bb = BoundingBox(1.0, 2.0, 1.0, 3.0)
        >>> bb.y_mid
        2.0
        """
        return (self.y_max + self.y_min) / 2.0

    def overlap_amount(self, box2) -> float:
        """
        Determine how much, if any box1 intersects box2

        Params:
            box2: another BoundingBox object

        Returns:
            float, intersection ratio

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

    >>> bb1 = BoundingBox(0,3,1,2)
    >>> bb2 = BoundingBox(1,2,0,3)
    >>> bb1.overlap_amount(bb2)
    0.3333333333333333
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

# If called from command line run the tests.
if __name__ == "__main__":
    import doctest
    doctest.testmod()
