'''
Version 1.5

Modified by:
		-Grady Duncan, @aDroidman
		
Sources:
http://stackoverflow.com/questions/13211745/detect-face-then-autocrop-pictures
http://opencv.willowgarage.com/documentation/python/cookbook.html
http://www.lucaamore.com/?p=638
https://gist.github.com/astanin/3097851
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
boxScale = 1
# Needed for webcam CV2 section
HaarXML = "haarcascade_frontalface_alt.xml"
classifier = cv2.CascadeClassifier(HaarXML)
downScale = 4
webcam = cv2.VideoCapture(0)

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

def Crop(imagePattern,boxScale,outputimg):
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
								
def CropSetup(padding, boxScale):
		inputimg = raw_input('Please enter the entire path to the image folder:')
		outputimg = raw_input('Please enter the entire path to the output folder:')
		
		# Create output folder if missing
		if not os.path.exists(outputimg):
				os.makedirs(outputimg)
		
		# Get padding for crop
		while (padding < 0):
				padding = int(raw_input('Enter crop padding:'))
		
		# Crop images
		Crop(inputimg + '\*.png', boxScale, outputimg)
		Crop(inputimg + '\*.jpg', boxScale, outputimg)

def Webcam(webcam, classifier, downScale):
		
		if webcam.isOpened():
				rval, frame = webcam.read()
		else:
				rval = False

		while rval:
				# detect faces and draw bounding boxes
				minisize = (frame.shape[1]/downScale,frame.shape[0]/downScale)
				miniframe = cv2.resize(frame, minisize)
				faces = classifier.detectMultiScale(miniframe)
				for f in faces:
						x, y, w, h = [ v*downScale for v in f ]
						cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255))
		 
				cv2.putText(frame, "Press ESC to close.", (5, 25),
										cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255))
				cv2.imshow("Face Crop", frame)
		 
				# get next frame
				rval, frame = webcam.read()
		 
				key = cv2.waitKey(10)
				if key in [27, ord('Q'), ord('q')]: # exit on ESC
						break	
				
print 'Version: 1.5'				
print 'Option 1: Detect image from Webcam'
print 'Option 2: Crop saved images'
option = int(raw_input('Please enter 1 or 2: '))					
			
if option == 1:
		Webcam(webcam, classifier, downScale)
elif option == 2:
		CropSetup(padding, boxScale)
else:
		print 'Not a valid input'
