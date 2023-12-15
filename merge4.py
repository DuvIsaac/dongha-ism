import cv2
import numpy as np

imgPath_1 = 'C:\digiCamControl\Session1\DSC_0020.jpg'
imgPath_2 = 'C:\digiCamControl\Session1\DSC_0021.jpg'

img_1 = cv2.imread(imgPath_1, cv2.IMREAD_COLOR)
img_2 = cv2.imread(imgPath_2, cv2.IMREAD_COLOR)

img = cv2.vconcat([img_1, img_2])

cv2.imwrite('./test_img/test_9.jpg', img)
