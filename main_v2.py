import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtTest import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import mss

import cv2

import os

import numpy as np

import threading

from pynput.mouse import Button, Controller

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import qimage2ndarray

import datetime

import numpy as np

import time

form_class_1 = uic.loadUiType("./page_ui_v2/main.ui")[0]
form_class_2 = uic.loadUiType("./page_ui_v2/explain.ui")[0]
form_class_3 = uic.loadUiType("./page_ui_v2/select.ui")[0]
form_class_4 = uic.loadUiType("./page_ui_v2/capture.ui")[0]
form_class_5 = uic.loadUiType("./page_ui_v2/photo_select.ui")[0]
form_class_6 = uic.loadUiType("./page_ui_v2/goodbye.ui")[0]

global selected
selected = 0
global frame
frame = 0

class MainWindow(QMainWindow, form_class_1):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.start.clicked.connect(self.next_window)
        
    def next_window(self):
        
        mouse = Controller()
        mouse.position = (100, 100)
        
        self.w = ExplainWindow()
        self.w.showFullScreen()
        self.close()

class ExplainWindow(QMainWindow, form_class_2):
    def __init__(self):
        super(ExplainWindow, self).__init__()
        self.setupUi(self)
        self.move_next.clicked.connect(self.next_window)
        self.move_previous.clicked.connect(self.previous_window)
        
    def previous_window(self):
        
        mouse = Controller()
        mouse.position = (100, 100)
        
        self.w = MainWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_window(self):
        
        mouse = Controller()
        mouse.position = (100, 100)
        
        self.w = CaptureWindow()
        self.w.showFullScreen()
        self.close()

class CaptureWindow(QMainWindow, form_class_4):
    
    def run(self):
        # cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture(1)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        while self.running:
            
            with mss.mss() as sct:
    
                # monitor_number = 1
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
                img = img[y: y + h, x: x + w]
                # img = img[...,::-1].copy()
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # img = cv2.fromarray(img)
                
                qImg = qimage2ndarray.array2qimage(img, normalize=False)
                pixmap = QPixmap.fromImage(qImg)
                self.label.setPixmap(pixmap)
            
            # try:
            #     ret, img = cap.read()
            #     if ret:
            #         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    
            #         img  = cv2.resize(img, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
            #         h,w,c = img.shape
            #         qImg = QImage(img.data, w, h, w*c, QImage.Format_RGB888)
            #         pixmap = QPixmap.fromImage(qImg)
            #         self.label.setPixmap(pixmap)
            # except:
            #     pass
        cap.release()
        
        print("Thread end.")
    
    def __init__(self):
        super(CaptureWindow, self).__init__()
        self.setupUi(self)
        
        self.mouse = Controller()
        
        self.running = True

        th = threading.Thread(target=self.run)
        th.start()
        
        

        self.count = 11
        self.num = 0
        
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.count_start)
    
    def count_start(self):
        if self.count > 1:
            self.count = self.count - 1
            self.count_label.setPixmap(QPixmap(f'./count/{self.count}.png'))
        else:
            self.count_label.setPixmap(QPixmap())
            self.count = 11
            self.num = self.num + 1
            self.capture()

            if self.num == 4:
                self.running = False
                self.timer.stop()
                
                self.label_2.setPixmap(QPixmap('./loading.jpg'))
                
                self.timer = QTimer(self)
                self.timer.start(3000)
                self.timer.timeout.connect(self.next_window)
            
    def capture(self):
        print('capture!')
        
        # mouse.position = (-2540,-650) # 1.마우스 x,y 위치지정   (-3785,-919)
        self.mouse.position = (-3785,-919) # 1.마우스 x,y 위치지정   
        self.mouse.press(Button.left) # 3.현재 마우스위치 클릭(누르고있는중)
        self.mouse.release(Button.left) # 4.현재 마우스위치 클릭(풀기)
        
        # time.sleep(1)
    
    def previous_window(self):
        
        mouse = Controller()
        mouse.position = (100, 100)
        
        self.timer.stop()
        self.w = ExplainWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_window(self):
        
        
        mouse = Controller()
        mouse.position = (100, 100)
        
        self.timer.stop()
        self.w = PhotoSelectWindow()
        self.w.showFullScreen()
        self.close()

class PhotoSelectWindow(QMainWindow, form_class_5):
    def __init__(self):
        
        
        super(PhotoSelectWindow, self).__init__()
        self.setupUi(self)
        self.print_photo.clicked.connect(self.next_window)
        self.non_print_photo.clicked.connect(self.skip_window)
        
        self.photo_dir = 'C:/Users/chhch/Pictures/digiCamControl/Session1'
        self.photos = os.listdir(self.photo_dir)
        
        self.photo_1.setPixmap(QPixmap(self.photo_dir + '/' + self.photos[-4]).scaled(QSize(450, 300)))
        self.photo_2.setPixmap(QPixmap(self.photo_dir + '/' + self.photos[-3]).scaled(QSize(450, 300)))
        self.photo_3.setPixmap(QPixmap(self.photo_dir + '/' + self.photos[-2]).scaled(QSize(450, 300)))
        self.photo_4.setPixmap(QPixmap(self.photo_dir + '/' + self.photos[-1]).scaled(QSize(450, 300)))
        
        global selected
        selected = 0
        
        self.photo_choice_1.clicked.connect(self.photo_select_1)
        self.photo_choice_2.clicked.connect(self.photo_select_2)
        self.photo_choice_3.clicked.connect(self.photo_select_3)
        self.photo_choice_4.clicked.connect(self.photo_select_4)
    
    def photo_select_1(self):
        print('1')
        
        global selected
        selected = self.photo_dir + '/' + self.photos[-4]
        self.photo_1.setStyleSheet("border: 0px solid red;")
        self.photo_2.setStyleSheet("border: 0px solid red;")
        self.photo_3.setStyleSheet("border: 0px solid red;")
        self.photo_4.setStyleSheet("border: 0px solid red;")
        
        self.photo_1.setStyleSheet("border: 4px solid #DA5451;")
    
    def photo_select_2(self):
        print('2')
        
        global selected
        selected = self.photo_dir + '/' + self.photos[-3]
        self.photo_1.setStyleSheet("border: 0px solid red;")
        self.photo_2.setStyleSheet("border: 0px solid red;")
        self.photo_3.setStyleSheet("border: 0px solid red;")
        self.photo_4.setStyleSheet("border: 0px solid red;")
        
        self.photo_2.setStyleSheet("border: 4px solid #DA5451;")
    
    def photo_select_3(self):
        print('3')
        
        global selected
        selected = self.photo_dir + '/' + self.photos[-2]
        self.photo_1.setStyleSheet("border: 0px solid red;")
        self.photo_2.setStyleSheet("border: 0px solid red;")
        self.photo_3.setStyleSheet("border: 0px solid red;")
        self.photo_4.setStyleSheet("border: 0px solid red;")
        
        self.photo_3.setStyleSheet("border: 4px solid #DA5451;")
    
    def photo_select_4(self):
        print('4')
        
        global selected
        selected = self.photo_dir + '/' + self.photos[-1]
        self.photo_1.setStyleSheet("border: 0px solid red;")
        self.photo_2.setStyleSheet("border: 0px solid red;")
        self.photo_3.setStyleSheet("border: 0px solid red;")
        self.photo_4.setStyleSheet("border: 0px solid red;")
        
        self.photo_4.setStyleSheet("border: 4px solid #DA5451;")
        
    def skip_window(self):
        self.w = GoodbyeWindow()
        self.w.showFullScreen()
        self.close()
        
    def previous_window(self):
        
        mouse = Controller()
        mouse.position = (100, 100)
        
        self.w = CaptureWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_window(self):
        
        mouse = Controller()
        mouse.position = (100, 100)
        
        global selected
        if selected != 0:
            self.w = SelectWindow()
            self.w.showFullScreen()
            self.close()
        else:
            QMessageBox.about(self,'충곽한컷','사진을 선택해주세요')

class SelectWindow(QMainWindow, form_class_3):
    def __init__(self):
        super(SelectWindow, self).__init__()
        self.setupUi(self)
        self.move_next.clicked.connect(self.next_window)
        self.move_previous.clicked.connect(self.previous_window)
        
        self.frame_choice_1.clicked.connect(self.select_1)
        self.frame_choice_2.clicked.connect(self.select_2)
        self.frame_choice_3.clicked.connect(self.select_3)
        self.frame_choice_4.clicked.connect(self.select_4)
        self.frame_choice_5.clicked.connect(self.select_5)
        self.frame_choice_6.clicked.connect(self.select_6)
        self.frame_choice_7.clicked.connect(self.select_7)
        self.frame_choice_8.clicked.connect(self.select_8)
        self.frame_choice_9.clicked.connect(self.select_9)
        self.frame_choice_10.clicked.connect(self.select_10)
        
        
        global frame
        frame = 0


    def mergeImg(self, imgPath, framePath):
        mask = cv2.imread(framePath, cv2.IMREAD_UNCHANGED)
        img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
        maskY, maskX, _ = mask.shape
        imgY, imgX, _ = img.shape
        m = imgY/maskY

        mask = cv2.resize(mask[:, :, 3], None,  None, m, m, cv2.INTER_CUBIC)
        y, x = mask.shape

        frame = cv2.imread(framePath, cv2.IMREAD_COLOR)
        frame = cv2.resize(frame, None,  None, m, m, cv2.INTER_CUBIC)

        if x > imgX:
            if (x-imgX) % 2 == 1:
                lp = int((x-imgX-1)/2)
                rp = lp+1
            else:
                lp = int((x-imgX)/2)
                rp = lp
            img_crop = np.pad(img, ([0, 0], [lp, rp], [0, 0]),
                            'constant', constant_values=0)
        else:
            img_crop = img[0:y, int(imgX/2-x/2):int(imgX/2+x/2)]

        mask = cv2.bitwise_not(mask)
        cv2.copyTo(img_crop, mask, frame)
        return frame


    def select_frame(self, n):
        global selected
        global frame
        frame = f'./frame/{n}.png'
        
        res = self.mergeImg(selected, frame)
        
        res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        self.res = res
        res  = cv2.resize(res, (0, 0), fx=0.1, fy=0.1, interpolation=cv2.INTER_NEAREST)
        
        h,w,c = res.shape
        qImg = QImage(res.data, w, h, w*c, QImage.Format_RGB888)
                
        self.frame_preview.setPixmap(QPixmap.fromImage(qImg))
        
    
    def select_1(self):
        self.select_frame(1)
        print('1')
    def select_2(self):
        self.select_frame(2)
        print('2')
    def select_3(self):
        self.select_frame(3)
        print('3')
    def select_4(self):
        self.select_frame(4)
        print('4')
    def select_5(self):
        self.select_frame(5)
        print('5')
    def select_6(self):
        self.select_frame(6)
        print('6')
    def select_7(self):
        self.select_frame(7)
        print('7')
    def select_8(self):
        self.select_frame(8)
        print('8')
    def select_9(self):
        self.select_frame(9)
        print('9')
    def select_10(self):
        self.select_frame(10)
        print('10')
        
    def previous_window(self):
        self.w = PhotoSelectWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_window(self):
        
        global frame
        if frame != 0:
            self.res = cv2.cvtColor(self.res, cv2.COLOR_BGR2RGB)
            
            now = datetime.datetime.now()
            now_str = now.strftime('%Y%m%d%H%M%S')
            
            cv2.imwrite(f'./result/{now_str}.jpg', self.res)
            
            self.w = GoodbyeWindow()
            self.w.showFullScreen()
            self.close()
        else:
            QMessageBox.about(self,'충곽한컷','사진을 선택해주세요')
            

class GoodbyeWindow(QMainWindow, form_class_6):
    def __init__(self):
        super(GoodbyeWindow, self).__init__()
        self.setupUi(self)
        
        photo_dir = 'C:/Users/chhch/Pictures/digiCamControl/Session1'
        photos = os.listdir(photo_dir)
        
        num = int(photos[-1][-8:-4]) + 1
        name = (f"DSC_{ num : #05d}.jpg").replace(' ', '')
        
        temp = cv2.imread('./black.jpg')
        cv2.imwrite(f'C:/Users/chhch/Pictures/digiCamControl/Session1/{name}', temp)
        
        self.timer = QTimer(self)
        self.timer.start(5000)
        self.timer.timeout.connect(self.next_window)
        
    def previous_window(self):
        
        mouse = Controller()
        mouse.position = (100, 100)
        
        self.w = PhotoSelectWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_window(self):
        
        mouse = Controller()
        mouse.position = (100, 100)
        
        self.timer.stop()
        self.w = MainWindow()
        self.w.showFullScreen()
        self.close()


if __name__ == "__main__":
    
    mouse = Controller()
    mouse.position = (100, 100)
        
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    # myWindow.show()
    myWindow.showFullScreen()
    app.exec_()
