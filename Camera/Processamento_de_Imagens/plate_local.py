import cv2
import cProfile, pstats,io

pr = cProfile.Profile()
pr.enable()
GH = 100 # horizontal gradient 
GV = 100 # vertical gradient

#kernel for morphological tophat
kernel_th = cv2.getStructuringElement(cv2.MORPH_RECT,(20,20))#need adjustment
#kernel for morphological opening
kernel_o = cv2.getStructuringElement(cv2.MORPH_RECT,(27,6))#need adjustment
#kernel for morphological closing
kernel_c = cv2.getStructuringElement(cv2.MORPH_RECT,(27,6))#need adjustment

#first load and grayscale
path = "/home/filipesfreitas/Controle_Rasp/Camera/Banco_de_Imagens/18_5_2019/16:34:55.jpg"
img_origin = cv2.imread(path)
img_op = img_origin
img_op = cv2.cvtColor(img_op, cv2.COLOR_BGR2GRAY)
#print(img_op.shape)
cv2.imwrite("img_op.jpg",img_op)
img_op = cv2.blur(img_op,(3,3))



# morphological top-hat
img_op = cv2.morphologyEx(img_op, cv2.MORPH_TOPHAT, kernel_th)
cv2.imwrite('img_op.jpg',img_op)

#Binarization with OTSU method
ret2,thr = cv2.threshold(img_op,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
cv2.imwrite('thr.jpg',thr) 

#Opening --> closing
opening = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel_o)
op_cl = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel_c)
cv2.imwrite('op_cl.jpg',op_cl)

IMG = cv2.Canny(op_cl,GH,GV)
contours, hierarchy = cv2.findContours(op_cl, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_L1 )
cv2.drawContours(img_origin, contours, -1, (0,255,0), 3)
cv2.imwrite('img_origin.jpg',img_origin)

pr.disable()
s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())