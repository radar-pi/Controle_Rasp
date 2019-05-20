import cv2

#Leitura da Imagem
img = cv2.imread("16:2:57:27968.jpg", 0) 

#Suavização da Imagem
img_suav = cv2.blur(img, (2,2))
cv2.imwrite("limiar_20_comsuv.jpg", img_suav)

#Equalização do Histograma

#Binarização da Imagem

#Filtro de Sobel no eixo x
sobelx = cv2.Sobel(img_suav, cv2.CV_64F, 1, 0, ksize = 5)
sobelx = cv2.normalize(sobelx, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype= cv2.CV_8U)
sobely = cv2.Sobel(sobelx, cv2.CV_64F, 0, 1, ksize = 5)
sobely = cv2.normalize(sobely, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype= cv2.CV_8U)
cv2.imwrite("limiar_20_sobelx.jpg", sobelx)
cv2.imwrite("limiar_20_sobely.jpg", sobely)


Limiar, img_bin = cv2.threshold(sobely, 130, 255, cv2.THRESH_BINARY)
cv2.imwrite("limiar_20_binarizado.jpg", img_bin)
#edges = cv2.Canny(img_bin,100,200)
#edges = cv2.Canny(img_bin1,100,200)


#cv2.imwrite("limiar_20.jpg", edges1)
 
#laplacian = cv2.Laplacian(img_bin,cv2.CV_64F)
#cv2.imwrite("laplacian_20.jpg", laplacian)
#laplacian1 = cv2.Laplacian(img_bin1,cv2.CV_64F)
#cv2.imwrite("laplacian_20.jpg", laplacian1)
cv2.waitKey(0)
cv2.destroyAllWindows()
