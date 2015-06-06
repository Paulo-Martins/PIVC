import numpy as np
import argparse
import cv2
import imutils
from SimpleCV import *
import time
fx= 0.3
fy= 0.3
# convert escala cinza e aplica filtro blur + bilateral
image = cv2.imread('silver.jpg')
camera = Camera(0)
frame = camera.getImage()

display = Display()

while not display.isDone():
    frame = camera.getImage()
#    frame.show()
    thumbnail = frame.copy()
    if display.mouseLeft:
        break

    frame.save(display)
#    frame = imutils.resize(frame, width = 500)

#    cv2.imshow('test',image )
#frame.show()
frame.save("frame.png")
#frame=frame.equalize()
gray = frame.toGray()

#morph= gray.erode(1)
#morph= morph.dilate(1)
morph= gray.morphOpen()
morph= morph.morphClose()
#morph=morph.equalize()

bin = morph.binarize(120).invert()
gray.save("nail.png")
gray = gray.getNumpyCv2()
morph=morph.getNumpyCv2()
bin=bin.getNumpyCv2()
circles = cv2.cvtColor(bin,cv2.COLOR_BGR2GRAY)


gray = cv2.resize(gray, (0,0), fx=fx, fy=fy)
morph = cv2.resize(morph, (0,0), fx=fx, fy=fy)
bin = cv2.resize(bin, (0,0), fx=fx, fy=fy)
cv2.imshow("resultado", np.hstack([gray, morph, bin]))

_, circles = cv2.threshold(circles, 5, 255, cv2.THRESH_BINARY)
circles = cv2.HoughCircles(circles, cv2.cv.CV_HOUGH_GRADIENT,3.4, 30 )

img_circs = frame.copy()
img_circs = img_circs.getNumpyCv2()
if circles is not None:
    # converte para inteiro
    circles = np.round(circles[0, :]).astype("int")
    
    # loop circulos
    for (x, y, r) in circles:
        if r < 80 :
        # desenha circulo e depois
            # um rect
            cv2.circle(img_circs, (x, y), r, (0, 0, 255), 2)
            cv2.rectangle(img_circs, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            print("raio = %d " % r)

            con = img_circs[y-r:y + r, x-r:x + r]
            cv2.imshow("Contorno", con)
            cv2.waitKey(0)
img_circs = cv2.resize(img_circs , (0,0), fx=fx, fy=fy)

cv2.imshow("circ", img_circs)
cv2.waitKey(0)
