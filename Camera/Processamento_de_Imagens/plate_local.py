import cv2
from matplotlib import pyplot as plt
import numpy as np

GH = 50 # horizontal gradient 
GV = 50 # vertical gradient

#kernel for morphological tophat
kernel_th = cv2.getStructuringElement(cv2.MORPH_RECT,(38,20))#need adjustment
#kernel for morphological opening
kernel_o = cv2.getStructuringElement(cv2.MORPH_RECT,(18,10))#need adjustment
#kernel for morphological closing
kernel_c = cv2.getStructuringElement(cv2.MORPH_RECT,(18,10))#need adjustment

#first load and grayscale
path = "/home/filipesfreitas/Controle_Rasp/Camera/Banco_de_Imagens/19_5_2019/18:29:23:931065.jpg"
img_origin = cv2.imread(path)
img_op = img_origin
img_op = cv2.cvtColor(img_op, cv2.COLOR_BGR2GRAY)
print(img_op.shape)

img_op = cv2.blur(img_op,(5,5))
# morphological top-hat
img_op = cv2.morphologyEx(img_op, cv2.MORPH_TOPHAT, kernel_th)



#Binarization with OTSU method
ret2,thr = cv2.threshold(img_op,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

plt.imshow(thr, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.title("Binarization INV + OTSU")
plt.show()

#Opening --> closing
opening = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel_o)
op_cl = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel_c)

IMG = cv2.Canny(op_cl,GH,GV)
contours, hierarchy = cv2.findContours(op_cl, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_L1 )
cv2.drawContours(img_origin, contours, -1, (0,255,0), 3)

plt.imshow(img_origin)
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.title("Opening --> Closing")
plt.show()