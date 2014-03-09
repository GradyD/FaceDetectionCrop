'''
Sources:
http://stackoverflow.com/questions/13211745/detect-face-then-autocrop-pictures
http://opencv.willowgarage.com/documentation/python/cookbook.html
http://www.lucaamore.com/?p=638
https://gist.github.com/astanin/3097851

Modified by:
		-Grady Duncan, @aDroidman
'''

import cv
import cv2
import numpy
import Image
import glob
import os

# Static
faceCascade = cv.Load('haarcascade_frontalface_alt.xml')
padding = -1


inputimg = raw_input('Please enter the entire path to the image folder:')
outputimg = raw_input('Please enter the entire path to the output folder:')
if not os.path.exists(outputimg):
    os.makedirs(outputimg)

while (padding < 0):
    padding = int(raw_input('Enter crop padding:'))

capture = cv2.VideoCapture(0)
cv2.namedWindow("Face Crop")
if capture.isOpened():
    frame = capture.read()

def DetectFace(image, faceCascade, returnImage=False):

    #variables    
    min_size = (50,50)
    haar_scale = 1.1
    min_neighbors = 3
    haar_flags = 0
    DOWNSCALE = 4

    # Equalize the histogram
    cv.EqualizeHist(image, image)

    # Detect the faces
    faces = cv.HaarDetectObjects(image, faceCascade, cv.CreateMemStorage(0),haar_scale, min_neighbors, haar_flags, min_size)

    # If faces are found
    if faces and returnImage:
        for ((x, y, w, h), n) in faces:
            # Convert bounding box to two CvPoints
            pt1 = (int(x), int(y))
            pt2 = (int(x + w), int(y + h))
            cv.Rectangle(image, pt1, pt2, cv.RGB(255, 0, 0), 5, 8, 0)

						# Start video frame
            minisize = (frame.shape[1]/DOWNSCALE,frame.shape[0]/DOWNSCALE)
            miniframe = cv2.resize(frame, minisize)
            faceCam = classifier.detectMultiScale(miniframe)
            for f in faceCam:
                x, y, w, h = [ v*DOWNSCALE for v in f ]
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255))
         
            cv2.putText(frame, "Press ESC to close.", (5, 25),
            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255))
            cv2.imshow("preview", frame)
         
            # get next frame
            frame = capture.read()         
            raw_input('Pause for testing')
            key = cv2.waitKey(20)
            if key in [27, ord('Q'), ord('q')]: # exit on ESC
                break

    if returnImage:
        return image
    else:
        return faces

def pil2cvGrey(pil_im):
    pil_im = pil_im.convert('L')
    cv_im = cv.CreateImageHeader(pil_im.size, cv.IPL_DEPTH_8U, 1)
    cv.SetData(cv_im, pil_im.tostring(), pil_im.size[0]  )
    return cv_im

def imgCrop(image, cropBox, boxScale=1):
    # Crop a PIL image with the provided box [x(left), y(upper), w(width), h(height)]
		
    # Calculate scale factors
    xPadding=max(cropBox[2]*(boxScale-1),int(padding))
    yPadding=max(cropBox[3]*(boxScale-1),int(padding))

    # Convert cv box to PIL box [left, upper, right, lower]
    PIL_box=[cropBox[0]-xPadding, cropBox[1]-yPadding, cropBox[0]+cropBox[2]+xPadding, cropBox[1]+cropBox[3]+yPadding]

    return image.crop(PIL_box)

def Crop(imagePattern,boxScale=1):
    imgList=glob.glob(imagePattern)
    if len(imgList)<=0:
        return
    else:
			for img in imgList:
					pil_im=Image.open(img)
					cv_im=pil2cvGrey(pil_im)
					faces=DetectFace(cv_im,faceCascade)
					if faces:
							n=1
							for face in faces:
									croppedImage=imgCrop(pil_im, face[0],boxScale=boxScale)
									fname,ext=os.path.splitext(img)
									fname = os.path.basename(fname)
									croppedImage.save(outputimg + '\\' + fname + ' -c' + ext)
									n+=1
							print 'Cropping:', fname
					else:
							print 'No faces found:', img

# Crop all images in a folder
Crop(inputimg + '\*.png', boxScale=1)
Crop(inputimg + '\*.jpg', boxScale=1)