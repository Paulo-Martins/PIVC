import numpy as np
import argparse
import cv2
import imutils


# convert escala cinza e aplica filtro blur + bilateral
image = cv2.imread('silver.jpg')
camera = cv2.VideoCapture(0)

while True:
    (grabbed, frame) = camera.read()
    
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    frame = imutils.resize(frame, width = 500)
    cv2.imshow("Face", frame)

camera.release()
image= frame.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#blurred = cv2.GaussianBlur(gray, (7, 7), 0)
blurred = cv2.bilateralFilter(gray, 25, 100, 200)

(T, blurred) = cv2.threshold(blurred, 110, 255, cv2.THRESH_BINARY)
#cv2.imshow("Image-blurr", cv2.resize(blurred, (0,0), fx=0.3, fy=0.3))



# encontra  arestas 20 abaixo e contorno 70- acima nao e
edged = cv2.Canny(blurred, 20, 130)
edged_show=cv2.resize(edged, (0,0), fx=0.5, fy=0.5)
#cv2.imshow("Edges", edged_show)
circles = cv2.HoughCircles(blurred, cv2.cv.CV_HOUGH_GRADIENT,2.6, 70 )
img_circs = image.copy()
if circles is not None:
    # converte para inteiro
    circles = np.round(circles[0, :]).astype("int")
    
    # loop circulos
    for (x, y, r) in circles:
        # desenha circulo e depois
        # um rect
        cv2.circle(img_circs, (x, y), r, (0, 0, 255), 2)
        cv2.rectangle(img_circs, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        print("raio = %d " % r)
    # mostra imagem
    #    cv2.imshow("output", np.hstack([image, output]))
#    img_circs = cv2.resize(img_circs, (0,0), fx=0.3, fy=0.3)
#    cv2.imshow("output", img_circs)
# Encontrar contornos na imagem de arestas
# usar copia pois e um metodo destrutivo

(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# qts contornos
print "%d contornos na imagem" % (len(cnts))

# redimensionar

cons = image.copy()
cv2.drawContours(cons, cnts, -1, (0, 255, 0), -1)
cons=cv2.resize(cons, (0,0), fx=0.5, fy=0.5)

cv2.imshow("Contornos + circulos", np.hstack([cons, cv2.resize(img_circs, (0,0), fx=0.5, fy=0.5)]))

cv2.imshow("Blur + Arestas ", np.hstack([cv2.resize(blurred, (0,0), fx=0.5, fy=0.5), edged_show]))
cv2.waitKey(0)

# percorrer contornos
for (i, c) in enumerate(cnts):
    # obter rect envolvente
    (x, y, w, h) = cv2.boundingRect(c)
    
    # fazer crop
    print "Contorno #%d ---- #%d" % (i + 1 , cv2.contourArea(c))
    con = image[y:y + h, x:x + w]
    cv2.imshow("Contorno", con)
    
    # mascarar
    mask = np.zeros(image.shape[:2], dtype = "uint8")
    ((centerX, centerY), radius) = cv2.minEnclosingCircle(c)
    cv2.circle(mask, (int(centerX), int(centerY)), int(radius), 255, -1)
    mask = mask[y:y + h, x:x + w]
    cv2.imshow("Contorno com Mask", cv2.bitwise_and(con, con, mask = mask))
    cv2.waitKey(0)
    