from collections import namedtuple
import boxes as bx

# This class holds a detected detected object from a video frame.
Det = namedtuple('Det',
                 ['label',  # str
                  'box',    # (x1,y2,x2,y2)
                  'confidence'])

# This class holds one detected object and any "notes and book keeping" that are used
# to track objects between frames
Obj = namedtuple('Obj',
                 ['det',
                  'brightness'])


class DetectedObjects:
    def __init__(self):
        """creates a new empty list of objects"""
        d = Det('null', (0,0,0,0), 0.0)
        self.objects = [Obj(d, 0.0)]

    def add_detection_list(self,
                           detection_list):     #
        """
        Process a list of all objects detected in one frame.

        Params:
            detection_list      list of ('label', (x1,y1,x2,y2), confidence)

        Returns:
            none

        >>> objects = DetectedObjects()
        >>> objects.dump()
        Obj(det=Det(label='null', box=(0, 0, 0, 0), confidence=0.0), brightness=0.0)

        >>> objects.clear()
        >>> f1 = [  ("cat", (1.0, 1.0, 4.0, 4.0), 0.81),
        ...         ("dog", (5.0, 5.0, 8.0, 8.0), 0.75),        # first dog in frame
        ...         ("ell", (7.0, 5.0, 12.1, 8.0), 0.75),
        ...         ("dog", (15.0, 15.0, 18.0, 18.0), 0.70)]    # second dog in same frame
        >>> objects.add_detection_list(f1)
        >>> objects.dump()
        (Det(label='cat', box=(1.0, 1.0, 4.0, 4.0), confidence=0.81), 0.81)
        (Det(label='dog', box=(5.0, 5.0, 8.0, 8.0), confidence=0.75), 0.75)
        (Det(label='ell', box=(7.0, 5.0, 12.1, 8.0), confidence=0.75), 0.75)
        (Det(label='dog', box=(15.0, 15.0, 18.0, 18.0), confidence=0.7), 0.7)

        >>> objects.add_detection_list(f1)
        >>> objects.dump()
        (Det(label='cat', box=(1.0, 1.0, 4.0, 4.0), confidence=0.81), 1.2175)
        (Det(label='dog', box=(5.0, 5.0, 8.0, 8.0), confidence=0.75), 1.1125)
        (Det(label='ell', box=(7.0, 5.0, 12.1, 8.0), confidence=0.75), 1.1125)
        (Det(label='dog', box=(15.0, 15.0, 18.0, 18.0), confidence=0.7), 1.025)

        >>> objects.add_detection_list([])
        >>> objects.dump()
        (Det(label='cat', box=(1.0, 1.0, 4.0, 4.0), confidence=0.81), 0.713125)
        (Det(label='dog', box=(5.0, 5.0, 8.0, 8.0), confidence=0.75), 0.6343750000000001)
        (Det(label='ell', box=(7.0, 5.0, 12.1, 8.0), confidence=0.75), 0.6343750000000001)
        (Det(label='dog', box=(15.0, 15.0, 18.0, 18.0), confidence=0.7), 0.5687499999999999)
        """

        self.fade_objects()
        self.clear_dark_objects()

        for d in detection_list:
            label, box, confidence = d
            self.add_detection(label, box, confidence)

    def add_detection(self,
                      class_label: str,
                      box,
                      confidence):
        """
        Add one detection to the list of detected objects

        Params:
            class_label, a string that contains the name of class the detection belongs to.
            box, (x1, y1, x2, y2) Bounding box for detection.
        """

        best_score = -1.0
        best_match_index = -1
        brightness = 0.0

        for i, obj in enumerate(self.objects):

            # Labels must match exactly.
            # todo: implement a class label match where perhaps cat matches animal
            d = Det("",(0,0,0,0),0.0)
            d = obj[0]
            if d.label == class_label:

                over = bx.overlap_amount(d.box, box)
                if over > 0.25:
                    current_score = d.confidence * over
                    if current_score > best_score:
                        best_score = current_score
                        best_match_index = i

        d = Det(class_label, box, confidence)

        if best_score > 0.0:
            current_brightness = self.objects[best_match_index][1]
            new_brightness = min(10.0, current_brightness + best_score)
            self.objects[best_match_index] = (d, new_brightness)
        else:
            self.objects.append((d, confidence))

    def bright_enough(self, obj) -> bool:
        """
        Apply a threshold.  Placeholder for something more complex later.
        """

        if obj[1] > 0.0:
            return True
        else:
            return False

    def clear_dark_objects(self) -> None:
        """
        remove all objects from list that have "expired".
        """
        self.objects = list(filter(self.bright_enough, self.objects))

    def fade_objects(self) -> None:
        """
        decrease the "brightness" of every tracked object.
        """
        # todo replace the for loop with a map function
        for i, obj in enumerate(self.objects):
            bright = max(0.0, 0.75 * obj[1] - 0.2)
            self.objects[i] = (obj[0], bright)

    def count(self) -> int:
        return len(self.objects)

    def clear(self) -> int:
        self.objects = []

    def dump(self) -> None:
        for obj in self.objects:
            print(obj)

if __name__ == "__main__":
    import doctest
    doctest.testmod()