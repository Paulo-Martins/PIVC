import numpy as np
import argparse
import cv2
import imutils
from SimpleCV import *
import time
import math
fx= 0.3
fy= 0.3
parts=16
ofsetX=0
ofsetY=0
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
bin = cv2.bilateralFilter(bin, 30, 80, 120)
circles = cv2.cvtColor(bin,cv2.COLOR_BGR2GRAY)
img_circs = bin.copy()


gray = cv2.resize(gray, (0,0), fx=fx, fy=fy)
morph = cv2.resize(morph, (0,0), fx=fx, fy=fy)
bin = cv2.resize(bin, (0,0), fx=fx, fy=fy)




_, circles = cv2.threshold(circles, 20, 255, cv2.THRESH_BINARY)
circles =cv2.GaussianBlur(circles, (9, 9),0)
cv2.imshow("circles", circles)
circles = cv2.HoughCircles(circles, cv2.cv.CV_HOUGH_GRADIENT,2.1 , 40 )

cv2.imshow("resultado", np.hstack([gray, morph, bin]))


#img_circs = img_circs.getNumpyCv2()
if circles is not None:
    # converte para inteiro
    circles = np.round(circles[0, :]).astype("int")
    
    # loop circulos
    for (x, y, r) in circles:
        
        if (125 > r >  50) :
            Xi=y-r
            if Xi<0:
                Xi=0
                ofsetX=r-y
            Yi=x-r
            if Yi<0:
                Yi=0
                ofsetY=r-x
        # desenha circulo e depois
            # um rect
       
            cv2.circle(img_circs, (x, y), r, (0, 0, 255), 2)
            cv2.rectangle(img_circs, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            print("raio = %d  --- y =  %d -----x %d" % (r,y,x) )
            
            con = img_circs[Xi:y + r, Yi:x + r]
            print("larg = {0}".format(con.shape[0]))
            print("alt = {0}".format(con.shape[1]))
            for sec in xrange(0,parts):
                pixel = ((r-ofsetX)+math.sin(2*math.pi/parts*sec)*(r*0.90), (r-ofsetY )+math.cos(2*math.pi/parts*sec)*(r*0.90))
                print(" ---pixel {0} ".format(pixel))
                if (pixel[0]>0 and pixel[1]>0 and pixel[0]<(con.shape[0]) and pixel[1]<(con.shape[1])):
                    
                    print(" cor = %r " % (con[pixel]))
                    if con[pixel][0]==255:
                        print("lantejoula defeitutosa")
        #                    txt = "lantejoula defeitutosa"
        #                    con.drawText(txt)
                        cv2.putText(con, "Defeito", (r/2,r/2), cv2.FONT_HERSHEY_COMPLEX, 0.8,  (0,0,255), 3, cv2.CV_AA);
                        con[pixel]=(0,0,255)
                        
                        break;
                    con[pixel]=(0,255,255)
            cv2.imshow("Contorno", con)
            cv2.waitKey(0)
img_circs = cv2.resize(img_circs , (0,0), fx=fx, fy=fy)

cv2.imshow("circ", img_circs)
cv2.waitKey(0)



