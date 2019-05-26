# -*- coding: utf-8 -*-
import cv2

#Leitura da Imagem
img = cv2.imread("18:21:13:743127.jpg", 0) 

#Suavização da Imagem
img_suav = cv2.GaussianBlur(img, (5,5), 0)
cv2.imwrite("limiar_20_comsuv.jpg", img_suav)

#Equalização do Histograma

#Binarização da Imagem

#Filtro de Sobel no eixo x
sobelx = cv2.Sobel(img_suav, cv2.CV_64F, 1, 0, ksize = 5)
sobelx = cv2.normalize(sobelx, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype= cv2.CV_8U)

cv2.imwrite("limiar_20_sobelx.jpg", sobelx)

edges = cv2.Canny(img_suav,250,300)

cv2.imwrite("limiar_20_edges.jpg", edges)

Limiar, img_bin = cv2.threshold(edges, 20, 255, cv2.THRESH_BINARY)
cv2.imwrite("limiar_20_binarizado.jpg", img_bin)

#kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(17,13))
#morphDx = cv2.dilate(img_bin, kernel,1)
#contours1, hierarch = cv2.findContours(morphDx, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#contorn = cv2.drawContours(img, contours, -1, (0,255,0), 3)
#cv2.imwrite("limiar_20_contorno.jpg", hierarch)
#cv2.imshow("limiar_20_contorno.jpg", hierarch)

#laplacian = cv2.Laplacian(img_bin,cv2.CV_64F)
#cv2.imwrite("laplacian_20.jpg", laplacian)
#laplacian1 = cv2.Laplacian(img_bin1,cv2.CV_64F)
#cv2.imwrite("laplacian_20.jpg", laplacian1)

cv2.waitKey(0)
cv2.destroyAllWindows()
