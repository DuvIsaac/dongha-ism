import cv2
import numpy as np

framePath = './test_img/test_5.png'
imgPath = './test_img/test_4.jpg'

mask = cv2.imread(framePath, cv2.IMREAD_UNCHANGED)
img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
maskY, maskX, _ = mask.shape
imgY, imgX, _ = img.shape
m = imgY/maskY

mask = cv2.resize(mask[:, :, 3], None,  None, m, m, cv2.INTER_CUBIC)
y, x = mask.shape

frame = cv2.imread(framePath, cv2.IMREAD_COLOR)
frame = cv2.resize(frame, None,  None, m, m, cv2.INTER_CUBIC)

lp = (x-imgX)//2
rp = lp + ((x-imgX)%2)

img_crop = np.pad(img, ([0, 0], [lp, rp], [0, 0]),
                'constant', constant_values=0)

mask = cv2.bitwise_not(mask)
cv2.copyTo(img_crop, mask, frame)

cv2.imwrite('./test_img/test_8.jpg', frame)