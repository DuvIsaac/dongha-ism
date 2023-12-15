import mss
import cv2
import numpy as np

with mss.mss() as sct:
    
    monitor_number = 2
    mon = sct.monitors[monitor_number]

    monitor = {
        "top": mon["top"],
        "left": mon["left"],
        "width": mon["width"],
        "height": mon["height"],
        "mon": monitor_number,
    }
    output = "sct-mon{mon}_{top}x{left}_{width}x{height}.png".format(**monitor)

    sct_img = sct.grab(monitor)
    img = np.array(sct.grab(monitor))
    
    x = 230
    y = 55
    w = 1460
    h = 950
    cropped_img = img[y: y + h, x: x + w]
    
    cv2.imshow("OpenCV", cropped_img)
    cv2.waitKey(0)