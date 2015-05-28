from matplotlib import pyplot as plt
import numpy as np
import argparse
import cv2


###################      carrega imagem         #######################
image = cv2.imread('silver2.jpg')

###################       imagem em tons de cinzento        ################
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

###################      redimensiona imagem         #######################
small = cv2.resize(image, (0,0), fx=0.5, fy=0.5)

###################      mostra imagem         #######################
cv2.imshow("Original", small)


###################      calcula histograma da imagem         ###############
hist = cv2.calcHist([image], [0], None, [256], [0, 256])

###################  gráfico com o histograma    #######################
plt.figure()
plt.title("Grayscale Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")
plt.plot(hist)
plt.xlim([0, 256])
plt.show()

###################  fim gráfico com o histograma #######################

cv2.imshow("Histogram Equalization", np.hstack([image, eq]))
cv2.waitKey()
cv2.destroyAllWindows()