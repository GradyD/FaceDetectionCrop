'''
Version 2.1.7

Created by:
    -Grady Duncan, @aDroidman

Sources:
http://stackoverflow.com/questions/13211745/detect-face-then-autocrop-pictures
https://gist.github.com/astanin/3097851
'''

import cv
import cv2
import numpy
import Image
import glob
import os
import time

print 'Version: 2.1.7'

# Static
faceCascade = cv.Load('haarcascade_frontalface_alt.xml')
padding = -1
boxScale = 1

# Needed for webcam CV2 section
HaarXML = 'haarcascade_frontalface_alt.xml'
classifier = cv2.CascadeClassifier(HaarXML)

def DetectFace(image, faceCascade, returnImage=False):

    # variables
    min_size = (50, 50)
    haar_scale = 1.1
    min_neighbors = 3
    haar_flags = 0
    DOWNSCALE = 4

    # Equalize the histogram
    cv.EqualizeHist(image, image)

    # Detect the faces
    faces = cv.HaarDetectObjects(image, faceCascade, cv.CreateMemStorage(0), haar_scale, min_neighbors, haar_flags, min_size)

    # If faces are found
    if faces and returnImage:
        for ((x, y, w, h), n) in faces:

            # Convert bounding box to two CvPoints
            pt1 = (int(x), int(y))
            pt2 = (int(x + w), int(y + h))
            cv.Rectangle(image, pt1, pt2, cv.RGB(255, 0, 0), 5, 8, 0)

    if returnImage:
        return image
    else:
        return faces

def pil2cvGrey(pil_im):
    pil_im = pil_im.convert('L')
    cv_im = cv.CreateImageHeader(pil_im.size, cv.IPL_DEPTH_8U, 1)
    cv.SetData(cv_im, pil_im.tostring(), pil_im.size[0])
    return cv_im

def imgCrop(image, cropBox, padding):

    # Crop a PIL image with the provided box [x(left), y(upper), w(width), h(height)]
    # Calculate scale factors
    xPadding = max(cropBox[2] * (boxScale - 1), int(padding))
    yPadding = max(cropBox[3] * (boxScale - 1), int(padding))

    # Convert cv box to PIL box [left, upper, right, lower]
    PIL_box = [cropBox[0] - xPadding, cropBox[1] - yPadding, cropBox[0] + cropBox[2] + xPadding, cropBox[1] + cropBox[3] + yPadding]

    return image.crop(PIL_box)
    
def webCrop():
    # Verify image
    # savedPath = outputimg + '\\' + fname + ' -c' + ext
    # verify = cv2.imread(savedPath, 0)
    # cv2.imshow('Saved Image', verify)
    print 'Please open the file manually to check crop.'
    print 'Are you happy with the final crop?'
    finalCheck = raw_input('Enter y or n: ')
    if finalCheck == 'y':
        check = False
    elif finalCheck == 'n':
        padding = int(raw_input('Enter crop padding: '))
    else:
        print 'Not a valid input'
    print 'Do you have more pictures to take?'
    again = raw_input('Enter y or n: ')
    if again == 'y':
        WebcamConfig(padding)
    else:
        print 'Closing application'
        time.sleep(1)
        raise SystemExit

def Crop(imagePattern, outputimg, padding, check):
    imgList = glob.glob(imagePattern)
    if len(imgList) <= 0:
        return
    else:
        # Crop images
        for img in imgList:
            pil_im = Image.open(img)
            cv_im = pil2cvGrey(pil_im)
            faces = DetectFace(cv_im, faceCascade)
            if faces:
                n = 1
                for face in faces:
                    croppedImage = imgCrop(pil_im, face[0], padding)
                    (fname, ext) = os.path.splitext(img)
                    fname = os.path.basename(fname)
                    croppedImage.save(outputimg + '\\' + fname + ' -c' + ext)
                    n += 1
                print 'Cropping:', fname
            else:
                print 'No faces found:', img
                print 'Closing application'
                time.sleep(1)
                raise SystemExit
    # Send only if capturing from webcam            
    if check:
        webcrop()

def CropSetup(padding, check):
    inputimg = raw_input('Please enter the entire path to the image folder:')

    # Input folder check
    if not os.path.exists(inputimg):
        print 'Input Folder not found'
    outputimg = raw_input('Please enter the entire path to the output folder:')

    # Create output folder if missing
    if not os.path.exists(outputimg):
        os.makedirs(outputimg)

    # Get padding for crop
    while padding < 0:
        padding = int(raw_input('Enter crop padding:'))

    # Sent to Crop function
    Crop(inputimg + '\*.png', outputimg, padding, check)
    Crop(inputimg + '\*.jpg', outputimg, padding, check)

def WebCrop(name, padding):
    print 'Output Folder does not need to be created'
    outputimg = raw_input('Please enter the entire path to the output folder:')

    # Create output folder if missing
    if not os.path.exists(outputimg):
        os.makedirs(outputimg)

    # Get padding for crop
    while padding < 0:
        padding = int(raw_input('Enter crop padding:'))

    Crop(name, outputimg, padding, check)

def WebcamConfig(padding, check):
    webcamIndex = int(raw_input('Please enter Camera Index (0, 1, 2): '))
    webcam = cv2.VideoCapture(webcamIndex)
    name = raw_input('Plese enter name of file: ')
    name = name + '.jpg'
    if webcam.isOpened():
        (mainCam, frame) = webcam.read()
    else:
        mainCam = False
        print 'Webcam not found, please try a different Index number.'
        WebcamConfig(padding, check)

    while mainCam:
        cv2.imshow('Face Crop', frame)

        key = cv2.waitKey(10)
        if key in [99]:  # c to capture
            cv2.imwrite(name, frame)
            print 'Image saved'
            cv2.destroyWindow('Face Crop')
            WebCrop(name, padding)

        # get next frame
        (mainCam, frame) = webcam.read()

        if key in [27, ord('Q'), ord('q')]:  # exit on ESC
            break

print 'Option 1: Detect image from Webcam'
print 'Option 2: Crop saved images'
option = int(raw_input('Please enter 1 or 2: '))

if option == 1:
    check = True
    WebcamConfig(padding, check)
elif option == 2:
    check = False
    CropSetup(padding, check)
else:
    print 'Not a valid input'
