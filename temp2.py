# 사진 합성 완
# 찍고 사진 선택 완
# 사진 카메라 찍기 only python 힘들것 같은 찍는데 6~7초 걸림 camera2.py 참고
# 기존의 방법(사진 직접 출력까지는 가능)
# 사진 찍기전 실시간 미리보기에 프레임 씌워야함
# PPT 슬라이드 안바꿈

# 프레임 필요
# PyQt GUI PPT 생기면 바꿀 예정
# 프레임 먼저 선택으로 바꿀 필요 있음

# 실제환경 세팅
# 마우스 위치 설정
# 실시간 미리보기 위치 설정
# 사진 찍는거랑 실시간 미리보기 세팅 관리 모니터에서의 위치 조정 필요

# merge5.py 사진 자르기
# merge6.py 사진 합성(2컷)
# print.py 사진 출력

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


form_class_1 = uic.loadUiType("./page_ui_v3/main.ui")[0]
form_class_2 = uic.loadUiType("./page_ui_v3/explain.ui")[0]
form_class_3 = uic.loadUiType("./page_ui_v3/select.ui")[0]
form_class_4 = uic.loadUiType("./page_ui_v3/capture.ui")[0]
form_class_5 = uic.loadUiType("./page_ui_v3/photo_select.ui")[0]
form_class_6 = uic.loadUiType("./page_ui_v3/goodbye.ui")[0]
form_class_7 = uic.loadUiType("./page_ui_v3/frame_select.ui")[0]

global selected
selected = [0, 0]

global frame
frame = 0

class MainWindow(QMainWindow, form_class_1):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.start.clicked.connect(self.next_window)
        
    def next_window(self):
        
        mouse = Controller()
        # mouse.position = (100, 100)
        
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
        # mouse.position = (100, 100)
        
        self.w = MainWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_window(self):
        
        mouse = Controller()
        # mouse.position = (100, 100)
        
        self.w = FrameSelectWindow()
        self.w.showFullScreen()
        self.close()
        
class FrameSelectWindow(QMainWindow, form_class_7):
    def __init__(self):
        super(FrameSelectWindow, self).__init__()
        self.setupUi(self)
        mouse = Controller()
        self.move_2_next.clicked.connect(self.next_2_window)
        self.move_4_next.clicked.connect(self.next_4_window)
        
    def next_2_window(self):
        self.w = CaptureWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_4_window(self):
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
                
                # 1300 80 h 800 w 2200
                x = 460
                y = 93
                w = 1460
                h = 975
                img = img[y: y + h, x: x + w]
                # img = img[...,::-1].copy()
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (1400, 900))
                
                # img = cv2.fromarray(img)
                
                qImg = qimage2ndarray.array2qimage(img, normalize=False)
                pixmap = QPixmap.fromImage(qImg)
                pixmap = pixmap.scaled(self.label.width(), self.label.height(), aspectRatioMode=Qt.KeepAspectRatio)
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
        
        self.limit = 4
        self.numlimit = 4

        self.count = self.limit + 1
        self.num = 1
        
        self.c = 1
        
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.count_start)
    
    def count_start(self):
        if self.count > 1:
            self.count = self.count - 1
            self.count_label.setPixmap(QPixmap(f'./count/{self.count}.png'))
            
            if (self.num == 1)&(self.c):
                self.count_label_2.setPixmap(QPixmap('./count/1.png'))
                self.c = 0

        else:
            self.count_label.setPixmap(QPixmap())
            self.count = self.limit + 1
            self.num = self.num + 1
            self.capture()
            
            if self.num <= self.numlimit:
                self.count_label_2.setPixmap(QPixmap(f'./count/{self.num}.png'))

            else :
                self.count_label_2.setPixmap(QPixmap())
                
                self.running = False
                self.timer.stop()
                
                self.label_2.setPixmap(QPixmap('./loading.jpg'))
                
                self.timer = QTimer(self)
                self.timer.start(3000)
                self.timer.timeout.connect(self.next_window)
            
    def capture(self):
        print('capture!')
        
        self.mouse.position = (2226, 53) # 1.마우스 x,y 위치지정   
        self.mouse.press(Button.left) # 2.현재 마우스위치 클릭(누르고있는중)
        self.mouse.release(Button.left) # 3.현재 마우스위치 클릭(풀기)
        
        # time.sleep(1)
    
    def previous_window(self):
        mouse = Controller()
        # mouse.position = (100, 100)
        
        self.timer.stop()
        self.w = ExplainWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_window(self):
        mouse = Controller()
        # mouse.position = (100, 100)
        
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
        
        self.photo_dir = 'C:\digiCamControl\Session1'
        self.photos = os.listdir(self.photo_dir)
        
        self.photo_1.setPixmap(QPixmap(self.photo_dir + '/' + self.photos[-4]).scaled(QSize(450, 300)))
        self.photo_2.setPixmap(QPixmap(self.photo_dir + '/' + self.photos[-3]).scaled(QSize(450, 300)))
        self.photo_3.setPixmap(QPixmap(self.photo_dir + '/' + self.photos[-2]).scaled(QSize(450, 300)))
        self.photo_4.setPixmap(QPixmap(self.photo_dir + '/' + self.photos[-1]).scaled(QSize(450, 300)))
        
        global selected
        selected = [0, 0]
        
        self.selected = [0, 0, 0, 0]
        self.selected_sum = 3
        
        self.photo_choice_1.clicked.connect(self.photo_select_1)
        self.photo_choice_2.clicked.connect(self.photo_select_2)
        self.photo_choice_3.clicked.connect(self.photo_select_3)
        self.photo_choice_4.clicked.connect(self.photo_select_4)
    
    def photo_select_1(self):
        print('1')
        
        global selected
        
        if self.selected[-4] == 0:
            if self.selected_sum != 0:
                
                if (self.selected_sum == 1)|(self.selected_sum == 3):
                    print("(1)")
                    self.selected[-4] = 1
                    self.selected_sum = self.selected_sum - 1
                    selected[0] = self.photo_dir + '/' + self.photos[-4]
                
                else :
                    print("(2)")
                    self.selected[-4] = 2
                    self.selected_sum = self.selected_sum -2
                    selected[1] = self.photo_dir + '/' + self.photos[-4]
                
                self.photo_1.setStyleSheet("border: 4px solid #DA5451;")
        
        else :
            self.photo_1.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-4] - 1] = 0
            self.selected_sum = self.selected_sum + self.selected[-4]
            self.selected[-4] = 0
    
    def photo_select_2(self):
        print('2')
        
        global selected
        
        if self.selected[-3] == 0:
            if self.selected_sum != 0:
                
                if (self.selected_sum == 1)|(self.selected_sum == 3):
                    print("(1)")
                    self.selected[-3] = 1
                    self.selected_sum = self.selected_sum - 1
                    selected[0] = self.photo_dir + '/' + self.photos[-3]
                
                else :
                    print("(2)")
                    self.selected[-3] = 2
                    self.selected_sum = self.selected_sum -2
                    selected[1] = self.photo_dir + '/' + self.photos[-3]
                
                self.photo_2.setStyleSheet("border: 4px solid #DA5451;")
        
        else :
            self.photo_2.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-3] - 1] = 0
            self.selected_sum = self.selected_sum + self.selected[-3]
            self.selected[-3] = 0
    
    def photo_select_3(self):
        print('3')
        
        global selected
        
        if self.selected[-2] == 0:
            if self.selected_sum != 0:
                
                if (self.selected_sum == 1)|(self.selected_sum == 3):
                    print("(1)")
                    self.selected[-2] = 1
                    self.selected_sum = self.selected_sum - 1
                    selected[0] = self.photo_dir + '/' + self.photos[-2]
                
                else :
                    print("(2)")
                    self.selected[-2] = 2
                    self.selected_sum = self.selected_sum -2
                    selected[1] = self.photo_dir + '/' + self.photos[-2]
                
                self.photo_3.setStyleSheet("border: 4px solid #DA5451;")
        
        else :
            self.photo_3.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-2] - 1] = 0
            self.selected_sum = self.selected_sum + self.selected[-2]
            self.selected[-2] = 0
    
    def photo_select_4(self):
        print('4')
        
        global selected
        
        if self.selected[-1] == 0:
            if self.selected_sum != 0:
                
                if (self.selected_sum == 1)|(self.selected_sum == 3):
                    print("(1)")
                    self.selected[-1] = 1
                    self.selected_sum = self.selected_sum - 1
                    selected[0] = self.photo_dir + '/' + self.photos[-1]
                
                else :
                    print("(2)")
                    self.selected[-1] = 2
                    self.selected_sum = self.selected_sum -2
                    selected[1] = self.photo_dir + '/' + self.photos[-1]
                
                self.photo_4.setStyleSheet("border: 4px solid #DA5451;")
        
        else :
            self.photo_4.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-1] - 1] = 0
            self.selected_sum = self.selected_sum + self.selected[-1]
            self.selected[-1] = 0
        
    def skip_window(self):
        self.w = GoodbyeWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_window(self):
        mouse = Controller()
        # mouse.position = (100, 100)
        
        global selected
        if (selected[0] != 0) & (selected[1] != 0):
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

    def mergeImg(self, img, framePath):

        mask = cv2.imread(framePath, cv2.IMREAD_UNCHANGED)
        # img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
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
        
        return frame

    def mergeImg_2(self, imgPath_1, imgPath_2):
        
        img_1 = cv2.imread(imgPath_1, cv2.IMREAD_COLOR)
        img_2 = cv2.imread(imgPath_2, cv2.IMREAD_COLOR)
        
        img = cv2.vconcat([img_1, img_2])
        
        return img


    def select_frame(self, n):
        global selected
        global frame
        frame = f'./frame/{n}.png'
        img = self.mergeImg_2(selected[0], selected[1])
        
        # ************* 주석 처리 바꾸고 프레임 삽입 ***************
        res = self.mergeImg(img, './test_img/test_5.png')
        # res = self.mergeImg(img, frame)
        # ********************************************************
        
        res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        self.res = res
        res = cv2.resize(res, (0, 0), fx=0.1, fy=0.1, interpolation=cv2.INTER_NEAREST)
        
        h,w,c = res.shape
        qImg = QImage(res.data, w, h, w*c, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qImg)
        
        width = self.frame_preview.width()
        height = self.frame_preview.height()
        
        pixmap = pixmap.scaled(width, height, aspectRatioMode=Qt.KeepAspectRatio)
        
        self.frame_preview.setPixmap(pixmap)
    
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
        
        photo_dir = 'C:\digiCamControl\Session1'
        photos = os.listdir(photo_dir)
        
        num = int(photos[-1][-8:-4]) + 1
        name = (f"DSC_{ num : #05d}.jpg").replace(' ', '')
        
        temp = cv2.imread('./black.jpg')
        cv2.imwrite(f'C:\digiCamControl\Session1/{name}', temp)
        
        self.timer = QTimer(self)
        self.timer.start(5000)
        self.timer.timeout.connect(self.next_window)
        
    def next_window(self):
        mouse = Controller()
        # mouse.position = (100, 100)
        
        self.timer.stop()
        self.w = MainWindow()
        self.w.showFullScreen()
        self.close()

if __name__ == "__main__":
    
    mouse = Controller()
    # mouse.position = (100, 100)
        
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    # myWindow = CaptureWindow()
    # myWindow = PhotoSelectWindow()
    # myWindow.show()
    myWindow.showFullScreen()
    app.exec_()
