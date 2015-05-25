# USAGE
# python detect_circles.py --image images/simple.png

# import the necessary packages
import numpy as np
import argparse
import cv2
from SimpleCV import Image
from SimpleCV import *
import time
from scipy import misc
from scipy import ndimage
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread(args["image"])



#blurred_img = ndimage.gaussian_filter(image, sigma=3)
#gauss_denoised = ndimage.median_filter(image, 2)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = ndimage.median_filter(gray,9)

gray=cv2.threshold(gray,90,255,cv2.THRESH_BINARY)[1]
#gray = ndimage.binary_erosion(gray)
gray = ndimage.gaussian_filter(gray, sigma=5)

cv2.imshow("gray", gray )
#cv2.imshow('im',dilated)
#cv2.waitKey()
# detect circles in the image
time.sleep(2)
#cvMat = cv.fromarray(logo)
#output = np.asarray(cvMat)
circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT,1.8, 50)
print(circles)
output=image.copy()
# ensure at least some circles were found
if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
        
        # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
        cv2.circle(output, (x, y), r, (0, 255, 0), 2)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        print(r)
        # show the output image
#    cv2.imshow("output", np.hstack([image, output]))
    small = cv2.resize(output, (0,0), fx=0.5, fy=0.5)
    cv2.imshow("output", small)
    cv2.waitKey(0)