import numpy as np
import argparse
import cv2
import imutils
from SimpleCV import *
import time
import math
fx= 0.3
fy= 0.3
parts=10
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
frame=frame.equalize()
gray = frame.toGray()

#morph= gray.erode(1)
#morph= morph.dilate(1)
morph= gray.morphOpen()
morph= morph.morphClose()
#morph=morph.equalize()

bin = morph.binarize(60).invert()
gray.save("nail.png")
gray = gray.getNumpyCv2()
morph=morph.getNumpyCv2()
bin=bin.getNumpyCv2()
bin = cv2.bilateralFilter(bin, 25, 80, 120)
circles = cv2.cvtColor(bin,cv2.COLOR_BGR2GRAY)


gray = cv2.resize(gray, (0,0), fx=fx, fy=fy)
morph = cv2.resize(morph, (0,0), fx=fx, fy=fy)
bin = cv2.resize(bin, (0,0), fx=fx, fy=fy)




_, circles = cv2.threshold(circles, 15, 255, cv2.THRESH_BINARY)
circles =cv2.GaussianBlur(circles, (9, 9),0)
cv2.imshow("circles", circles)
circles = cv2.HoughCircles(circles, cv2.cv.CV_HOUGH_GRADIENT,2.1 , 40 )

cv2.imshow("resultado", np.hstack([gray, morph, bin]))

img_circs = frame.copy()
img_circs = img_circs.getNumpyCv2()
if circles is not None:
    # converte para inteiro
    circles = np.round(circles[0, :]).astype("int")
    
    # loop circulos
    for (x, y, r) in circles:
#        if r < 80 :
        # desenha circulo e depois
            # um rect
            cv2.circle(img_circs, (x, y), r, (0, 0, 255), 2)
            cv2.rectangle(img_circs, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            print("raio = %d  --- y =  %d -----x %d" % (r,y,x) )
            Xi=y-r
            if Xi<0:
                Xi=0
            Yi=x-r
            if Yi<0:
                Yi=0
            con = img_circs[Xi:y + r, Yi:x + r]
            for sec in xrange(0,parts):
                pixel = (r+math.sin(2*math.pi/parts*sec)*(r-r*0.20), r+math.cos(2*math.pi/parts*sec)*(r-r*0.20))
                if con[pixel][0]==255:
                    print("lantejoula defeitutosa")
#                    txt = "lantejoula defeitutosa"
#                    con.drawText(txt)
                    cv2.putText(con, "Defeito", (r-50,r-50), cv2.FONT_HERSHEY_COMPLEX, 0.8,  (0,0,255), 3, cv2.CV_AA);
                    
                    break
                con[pixel]=(0,255,255)
            cv2.imshow("Contorno", con)
            cv2.waitKey(0)
img_circs = cv2.resize(img_circs , (0,0), fx=fx, fy=fy)

cv2.imshow("circ", img_circs)
cv2.waitKey(0)



