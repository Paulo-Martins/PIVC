from matplotlib import pyplot as plt
import numpy as np
import argparse
import cv2
import imutils

###################      carrega imagem         #######################
image = cv2.imread('silver.jpg')
camera = cv2.VideoCapture(1)

while True:
    (grabbed, frame) = camera.read()
    
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    frame = imutils.resize(frame, width = 500)
    cv2.imshow("Face", frame)

camera.release()
###################       imagem em tons de cinzento        ################
image =frame.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

###################      redimensiona imagem         #######################

gblur= cv2.GaussianBlur(image, (7, 7),0)

blur= cv2.blur(image, (7, 7))

###################      mostra imagem         #######################
#cv2.imshow("Original", small)





###################  fim grafico com o histograma #######################
eq = cv2.bilateralFilter(image, 25, 80, 150)
(T, eq) = cv2.threshold(eq, 80, 255, cv2.THRESH_BINARY)
#eq=cv2.adaptiveThreshold(eq, 255,                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 1)
eq = cv2.resize(eq, (0,0), fx=0.3, fy=0.3)
blurred = np.hstack([
                     cv2.GaussianBlur(image, (7,7), 0),
                     cv2.blur(image, (7,7)),
                     cv2.medianBlur(image, 7),
                     cv2.bilateralFilter(image, 55, 80, 100)])
blurred = cv2.resize(blurred, (0,0), fx=0.3, fy=0.3)

cv2.imshow("Blur com diferentes tecnicas", np.hstack([blurred, eq]))

###################      calcula histograma da imagem         ###############
hist = cv2.calcHist([eq], [0], None, [256], [0, 256])

###################  grafico com o histograma    #######################
plt.figure()
plt.title("Grayscale Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")
plt.plot(hist)
plt.xlim([0, 256])
plt.show()
cv2.waitKey()
cv2.destroyAllWindows()