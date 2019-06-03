import cv2 
import numpy as np
from matplotlib import pyplot as plt

# Initiate FAST object with default values
fast = cv2.FastFeatureDetector_create()

# Load an color image in grayscale
img = cv2.imread('19_5_2019/18:21:13:743127.jpg',0)
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()

#copy of original image for preprocessing
img_canny = cv2.Canny(img,100,200)

plt.imshow(img_canny, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()


pre_img = img
