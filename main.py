# This is a sample Python script.
'''

import boxes as bx

r = bx.overlap_amount((1,1,2,2), (1,1,2,2))
print(r)
r = bx.overlap_amount((1,1,2,2), (4,4,5,5))
print(r)
r = bx.overlap_amount((1,1,2,2), (1,1,4,2))
print(r)
r = bx.overlap_amount((1,1,2,2), (0,0,5,5))
print(r)
'''
import detected_objects as obj


objects = obj.DetectedObjects()

'''
print('count = ', objects.count())  # expect count == 1

objects.clear_dark_objects()
objects.fade_objects()
print('count = ', objects.count())  # expect count == 0

objects.add_detection("apple", (1,1,2,2), 1.0)
print('count = ', objects.count())  # expect count == 1

objects.add_detection("apple", (1,1,2,2), 1.0)
print('count = ', objects.count())  # expect count == 1 (over writes the "apple" above)

objects.add_detection("apple", (4,4,5,5), 1.0)
print('count = ', objects.count())  # expect count == 2 (this is a different "apple")

objects.add_detection("car", (4.0,4.0,5.0,5.0), 0.85)
print('count = ', objects.count())  # expect count == 3 (this is a new class)

objects.add_detection("car", (4.1,4.1,5.1,5.1), 0.95)
print('count = ', objects.count())  # expect count == 3 (this is a new class)

objects.dump()
objects.fade_objects()
objects.dump()
print("\n")
objects.clear()
'''

f1 = [  ("cat", (1.0, 1.0, 4.0, 4.0), 0.81),
        ("dog", (5.0, 5.0, 8.0, 8.0), 0.75),
        ("ell", (7.0, 5.0, 12.1, 8.0), 0.75),
        ("dog", (15.0, 15.0, 18.0, 18.0), 0.70)
     ]
f2 = [  ("cat", (1.1, 1.1, 4.1, 4.1), 0.40),
        ("dog", (5.1, 5.1, 8.1, 8.1), 0.35),
        ("ell", (7.20, 5.0, 12.0, 8.0), 0.40),
        ("dog", (15.0, 15.0, 18.0, 18.0), 0.65)
     ]
f3 = [  ("cat", (1.3, 1.3, 4.3, 4.3), 0.60),
        ("dog", (5.1, 5.3, 8.3, 8.3), 0.95),
        ("ell", (7.1, 5.0, 12.5, 8.0), 0.70),
        ("dog", (14.0, 14.0, 17.0, 18.0), 0.74)
     ]
objects.add_detection_list(f1)
objects.dump()
objects.add_detection_list(f2)
objects.dump()
objects.add_detection_list(f3)


