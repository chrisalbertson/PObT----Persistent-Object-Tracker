import unittest

import bounding_box as bb
from detected_objects import Detection, ObjectTracker


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:

        self.objects = ObjectTracker()

        self.f1 = [Detection("cat", 0.81, bb.BoundingBox(2.0, 3.0, 4.0, 5.0)),
                   Detection("dog", 0.75, bb.BoundingBox(5.0, 8.0, 8.0, 9.0)),
                   Detection("dog", 0.55, bb.BoundingBox(15.0, 18.0, 15.0, 18.0))]

        self.f2 = [Detection("dog", 0.75, bb.BoundingBox(5.0, 8.0, 8.0, 9.0)),
                   Detection("dog", 0.55, bb.BoundingBox(15.0, 18.0, 15.0, 18.0))]

    def test_one_frame(self):

        self.objects.add_detection_list(self.f1)

        num_obj = self.objects.count
        self.assertEqual(num_obj, 3)

    def test_two_frames(self):

        # This simulated two frames of video processed by an object detection network
        self.objects.add_detection_list(self.f1)
        self.objects.add_detection_list(self.f2)

        num_obj = self.objects.count
        self.assertEqual(num_obj, 3)

        # After two video frames we ask for the objects brighter then 1.0 that have
        # been detected in 2 or more frames
        tracked = self.objects.get_tracked_objects(1.0, 2)

        # "tracked" should contain one object that looks like this:
        # TrackedObject(label='dog', brightness=1.1125, last_box=<BoundingBox 5.0, 8.0, 8.0, 9.0>, num_detections=2)
        self.assertEqual(len(tracked), 1)
        for t in tracked:
            self.assertGreater(t.brightness, 1.0, 'filter asked for >= 1.0')
            self.assertGreaterEqual(t.num_detections, 2, 'filter asked for >= 2')

    def test_clear(self):

        self.objects.add_detection_list(self.f1)

        num_obj = self.objects.count
        self.assertEqual(num_obj, 3)

        self.objects.clear()
        num_obj = self.objects.count
        self.assertEqual(num_obj, 0)


if __name__ == '__main__':
    unittest.main()
