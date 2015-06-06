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
# le argumentos
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

# carrega imagem
image = cv2.imread(args["image"])



#blurred_img = ndimage.gaussian_filter(image, sigma=3)
#gauss_denoised = ndimage.median_filter(image, 2)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = ndimage.median_filter(gray,9)

gray=cv2.threshold(gray,90,255,cv2.THRESH_BINARY)[1]
#gray = ndimage.binary_erosion(gray)
gray = ndimage.gaussian_filter(gray, sigma=5)
small1 = cv2.resize(gray, (0,0), fx=0.5, fy=0.5)
cv2.imshow("gray", small1 )
#cv2.imshow('im',dilated)
#cv2.waitKey()
# detect circles in the image
time.sleep(2)
#cvMat = cv.fromarray(logo)
#output = np.asarray(cvMat)
circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT,1.8, 50)
print(circles)
output=image.copy()
# se ha circulos
if circles is not None:
    # converte para inteiro
    circles = np.round(circles[0, :]).astype("int")
        
        # loop circulos
    for (x, y, r) in circles:
            # desenha circulo e depois
            # um rect
        cv2.circle(output, (x, y), r, (0, 255, 0), 2)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        print(r)
        # mostra imagem
#    cv2.imshow("output", np.hstack([image, output]))
    small = cv2.resize(output, (0,0), fx=0.5, fy=0.5)
    cv2.imshow("output", small)
    cv2.waitKey(0)