
from typing import NamedTuple, Any, Callable, Union
from recordclass import RecordClass
import bounding_box as bb

# Detections are not mutable.  They remain whatever the object detection network
# thinks it detected.
class Detection(NamedTuple):
    label: str
    confidence: float
    box: bb.BoundingBox

# Tracked objects are mutable.  They chance over time as they are seen
# in more or less frames
class TrackedObject(RecordClass):
    label:          str
    brightness:     float
    last_box:       bb.BoundingBox
    num_detections: int


class ObjectTracker:
    """
    A class that maintains a list of tracked objects by tracking objects across many video frames

    Doctest Example:
    >>> objects = ObjectTracker()
    >>> frame_1 = [Detection("cat", 0.81, bb.BoundingBox(2.0, 3.0, 4.0, 5.0)),
    ...            Detection("dog", 0.75, bb.BoundingBox(5.0, 8.0, 8.0, 9.0))]
    >>> objects.add_detection_list(frame_1)
    >>> objects.get_tracked_objects(0.8, 1)
    [TrackedObject(label='cat', brightness=0.81, last_box=<BoundingBox 2.0, 3.0, 4.0, 5.0>, num_detections=1)]
    """
    def __init__(self):
        """creates a new empty list of tracked objects"""

        self._tracked_objects = []   # list of TrackedObject
        self.min_confidence = 0.25  # TODO: This number is just a guess
        self.min_overlap = 0.25     # TODO: This number is just a guess
        self.min_brightness = 0.01  # TODO: This number is just a guess

    def add_detection_list(self,
                           detection_list):  #
        """
        Process a list of all objects detected in one frame.

        Params:
            detection_list      list of 'Detection'

        Returns:
            none
        """

        # Reduce the "brightness" of every tracked objectself.fade_objects
        self._fade_objects()

        # Clear "dark" tracked objects from the list
        self._tracked_objects = list(filter(self._bright_enough, self._tracked_objects))

        for d in detection_list:
            if d.confidence >= self.min_confidence:
                self._apply_detection(d)

    def get_tracked_objects(self,
                            min_brightness: float,
                            min_detections: int):
        """ Returns a list of tracked objects that meet a filter criteria"""

        selected = lambda obj: (obj.brightness >= min_brightness) and \
                               (obj.num_detections >= min_detections)

        objects = list(filter(selected, self._tracked_objects))
        return objects

    def _apply_detection(self,
                         det: Detection):
        """Add one detection to the list of detected objects"""

        assert (isinstance(det, Detection)), 'must be Detection'

        best_score = -1.0
        best_match_index = -1
        brightness = 0.0

        for i, t_obj in enumerate(self._tracked_objects):

            # Labels must match exactly.
            # todo: implement a label match where perhaps cat matches animal
            if t_obj.label == det.label:

                overlap = t_obj.last_box.overlap_amount(det.box)
                if overlap > self.min_overlap:

                    # todo: How to rate the degree of match is a big deal needs to be smarter
                    current_score = det.confidence * overlap
                    if current_score > best_score:
                        best_score = current_score
                        best_match_index = i

        # Did the above for loop find a match?
        if best_score > 0.0:
            # yes, we got a match so update the tracked object with this new data.
            self._tracked_objects[best_match_index].brightness += best_score
            self._tracked_objects[best_match_index].last_box = det.box
            self._tracked_objects[best_match_index].num_detections += 1
        else:
            # no match was found so treat this as a new tracked object
            tracked_obj = TrackedObject(det.label,
                                        det.confidence,
                                        det.box,
                                        1)
            self._tracked_objects.append(tracked_obj)

    def _bright_enough(self, obj: TrackedObject) -> bool:
        """Apply a threshold.  Placeholder for something more complex later."""

        if obj.brightness >= self.min_brightness:
            return True
        else:
            return False

    def _fade_objects(self) -> None:
        """decrease the "brightness" of every tracked object."""

        for i, trkobj in enumerate(self._tracked_objects):
            bright = max(0.0, 0.75 * trkobj.brightness - 0.2)
            self._tracked_objects[i].brightness = bright

    @property
    def count(self) -> int:
        """Returns the number of objects that are currently being tracked"""
        return len(self._tracked_objects)

    def clear(self) -> None:
        """
        Clears the list of tracked objects

        This might be used when a video feed is cut or moved to view a new location
        so that all the older objects are invalidated.
        """
        self._tracked_objects = []

    def dump(self) -> None:
        """Print list of tracked objects.  Used for debugging and test"""
        for obj in self._tracked_objects:
            print(obj)


if __name__ == "__main__":
    import doctest
    doctest.testmod()