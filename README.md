# PObT----Persistent-Object-Tracker

This software system will maintain a list of all objects that are detected by video cameras and other sensors.  It makes this list of objects, their identities, and predicted motions available to other system components.

PObT uses a simple algorithm inspired by older analog radar systems.  Each time a target is detected it is made brighter on the radar screen by an amount proportionate to the confidence in the object's detection and how well it matches previous detections.  At the same time, the object's brightness slowly fades over time.

### Roadmap.
The first versions will allow experiments witht e libray API, build and unit test systems.  After this is stable work will start on more advanced object matching


### Versions
#### 0.1 -- Oct 23, 2020
This is the initial release.  The software does not yet track objects through 3D space.  This release implements a simple frame-to-frame matching that uses class labels and the degree to which bounding boxes overlap.

The API is simple.  There is a function to be called and passed to a list of all detections made by a typical object detector such as Yolo or SSD.  This is called after each frame is processed by the object detector.   There is a second function that may be called at any time that returns a list of all the objects that were seen in the last several frames.

#### 0.2 --
Change the way a bounding box is defined from (x1,y1,x2,y2) to (Xmin, Xmax, Ymin, Ymax) to be concistent with other systms.


