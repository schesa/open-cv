# Open CV augmentation Project


Tkinter was used to create a GUI to select a folder of images that will be augmented into a new folder with the same name, but ending in _aug.


In config.ini augmentation details can be specified. Available configuration keys are:


* Blur ex. 5
* Brightness ex. 30
* Contrast ex. 1.2
* Gamma ex. 2.0
* Scale ex. 0.6 
* Rotation ex. 0-clockwise, 1-180 degrees, 2-counterclockwise
* Padding ex. 100(px)
* Shear ex. 10


In the default configuration group are specified configurations that will be applied solo for each image in the set. 
Additional, combo configuration groups can be added. For each group an augmented image will be generated using a combination of all specified configuration keys.
