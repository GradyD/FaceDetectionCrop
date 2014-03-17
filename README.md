FaceDetectionCrop
==========
This is a python script to crop images based facial recognition. It has two options, create from a web cam or 
from a saved image (jpg or png). It is using OpenCV to detect the facial region and PIP to crop the image.

Pyinstaller is being used to compile the script into a runnable EXE. Currently you must have the HaarCascade 
in the same directory for the script to run. A runnable EXE can be found the release section of this project.

Please submit all bugs, feature requests and questions under the Report Issue section of this project. You can find a running change log listed below.

Versions
==================
1.0 - crop local images

1.3 - code fixes and clean up 

1.5 - Created working web cam function

2.0 - Created working save and crop from web cam

2.1 - Correct formatting, removed display copped image, fixed no faces found bug

2.1.6 - Fixed logic issues, added more safeguards to prevent random closes, updated variable names, created new functions to streamline sections of code
2.1.7 - Name changed to prevent copyright issues.