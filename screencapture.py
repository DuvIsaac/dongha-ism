import cv2 as cv
import numpy as np
import pyautogui



cv.namedWindow("result");

while 1:
    # pic = pyautogui.screenshot(region=(220, -1283, 1596, -300))
    # pic = pyautogui.screenshot(region=(-3000, -3000, 1596, 1800))
    pic = pyautogui.screenshot()
    img_frame = np.array(pic)
    img_frame  = cv.cvtColor(img_frame, cv.COLOR_RGB2BGR)

    cv.imshow('result', img_frame)
    
    key = cv.waitKey(1)
    if key == 27:
        break