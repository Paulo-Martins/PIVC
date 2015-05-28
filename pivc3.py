import cv2
import numpy as np
from scipy import ndimage

im = cv2.imread('silver2.jpg')

gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
gray = ndimage.median_filter(gray,9)
gray=cv2.threshold(gray,90,255,cv2.THRESH_BINARY)[1]

#gray = ndimage.gaussian_filter(gray, sigma=5)
cv2.imshow('gray',gray)
cv2.waitKey()
cv2.destroyWindow('gray')
contours,hierarchy = cv2.findContours(gray,cv2.RETR_LIST ,4   )
i=0
MY_COLORS={'BLUE':[255,0,0],'GREEN':[0,255,0], 'RED':[0,0,255],'LARANJA':[0,128,255],'MAR':[255,255,0],'ROSA':[255,0,255],'CINZA':[128,128,128],'AMARELO':[0,255,255],'VIOLETA':[102,0,51]}
COLORS = ['BLUE','RED','GREEN','MAR','ROSA','LARANJA','CINZA','AMARELO','VIOLETA']
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 1000:
        hull= cv2.convexHull(cnt, returnPoints = False)
        defects= cv2.convexityDefects(cnt, hull)
        (x,y),raio = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        raio= int(raio)
        
#        H_area = cv2.contourArea(hull)
        k = cv2.isContourConvex(cnt)
#        cv2.circle(im,center,raio,(0,255,0),2)
        print("Area",COLORS[i],":" , area , "---- Convex: " , k)
#        print("Hull Area",COLORS[i],":" , H_area )

        cv2.drawContours(im,[cnt],0,MY_COLORS[COLORS[i]],-1)
#        cv2.drawContours(im,[hull],0,(255,255,255),2)
        i+=1
        if i == 8:
            i=0
        if defects is not None:
            for x in range(defects.shape[0]):
                s,e,f,d = defects[x,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                cv2.circle(im, far, 5, [0,128,255],-2)
                cv2.line(im, start,end,[255,255,255],2)
                dist=cv2.pointPolygonTest(cnt,far,False)
                print(dist)


small = cv2.resize(im, (0,0), fx=0.5, fy=0.5)
cv2.imshow('im',small)
cv2.waitKey()
cv2.destroyAllWindows()