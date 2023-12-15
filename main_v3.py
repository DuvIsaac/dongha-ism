# digiCamControl 열고 라이브로 띄우기, 실시간 화면 전체로 바꾸고 라이브 하나 더 띄우기 위치 조정하기 (실시간 화면 위치 + Capture 버튼 위치)
# 사진 선택화면에서 선택지 이미지 깨짐

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
import time

from PIL import Image, ImageWin, ImageOps
import win32ui
import win32print


form_class_1 = uic.loadUiType("./page_ui_v3/main.ui")[0]
form_class_2 = uic.loadUiType("./page_ui_v3/explain.ui")[0]
form_class_3 = uic.loadUiType("./page_ui_v3/select.ui")[0]
form_class_4 = uic.loadUiType("./page_ui_v3/capture.ui")[0]
form_class_5 = uic.loadUiType("./page_ui_v3/photo_select_4.ui")[0]
form_class_6 = uic.loadUiType("./page_ui_v3/goodbye.ui")[0]
form_class_7 = uic.loadUiType("./page_ui_v3/frame_size_select.ui")[0]
form_class_8 = uic.loadUiType("./page_ui_v3/num_select.ui")[0]
form_class_9 = uic.loadUiType("./page_ui_v3/frame_select_2.ui")[0]
form_class_10 = uic.loadUiType("./page_ui_v3/frame_select_4.ui")[0]
form_class_11 = uic.loadUiType("./page_ui_v3/photo_select_2.ui")[0]

global selected
selected = [0, 0]

global frame
frame = './frame_v2/2frame/7.png'

global size
size = 2

global frame_c
frame_c = 7

global print_num
print_num = 1

global printer_name
printer_name = "Canon SELPHY CP1300"

class MainWindow(QMainWindow, form_class_1):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.start.clicked.connect(self.next_window)
        mouse = Controller()
    
    def next_window(self):
        self.w = ExplainWindow()
        self.w.showFullScreen()
        self.close()

class ExplainWindow(QMainWindow, form_class_2):
    def __init__(self):
        super(ExplainWindow, self).__init__()
        self.setupUi(self)
        mouse = Controller()
        self.move_next.clicked.connect(self.next_window)
        self.move_previous.clicked.connect(self.previous_window)
        
    def previous_window(self):
        self.w = MainWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_window(self):
        self.w = FrameSizeSelectWindow()
        self.w.showFullScreen()
        self.close()
        
class FrameSizeSelectWindow(QMainWindow, form_class_7):
    def __init__(self):
        super(FrameSizeSelectWindow, self).__init__()
        self.setupUi(self)
        mouse = Controller()
        self.move_next.clicked.connect(self.next_window)
        self.move_2_next.clicked.connect(self.next_2_window)
        self.move_4_next.clicked.connect(self.next_4_window)
        global size
        size = 0
        
    def next_window(self):
        global size
        size = 0
        self.w = ExplainWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_2_window(self):
        global size
        size = 2
        self.w = NumSelectWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_4_window(self):
        global size
        size = 4
        self.w = NumSelectWindow()
        self.w.showFullScreen()
        self.close()
        
class NumSelectWindow(QMainWindow, form_class_8):
    
    def __init__(self):
        super(NumSelectWindow, self).__init__()
        self.setupUi(self)
        self.mouse = Controller()
        
        self.max_num = 4
        
        global print_num
        print_num = 1
        
        self.label_plus.setPixmap(QPixmap('./img/print_num/plus.png'))
        self.label.setPixmap(QPixmap(f'./count/{print_num}.png'))
        
        self.move_previous.clicked.connect(self.previous_window)
        self.move_next.clicked.connect(self.next_window)
        self.plus.clicked.connect(self.plus_num)
        self.minus.clicked.connect(self.minus_num)
        
    def plus_num(self):
        global print_num
        if print_num < self.max_num:
            print_num += 1
            self.label.setPixmap(QPixmap(f'./count/{print_num}.png'))
            self.label_plus.setPixmap(QPixmap('./img/print_num/plus.png'))
            self.label_minus.setPixmap(QPixmap('./img/print_num/minus.png'))
        
        if print_num == self.max_num:
            self.label_plus.setPixmap(QPixmap())
            self.label_minus.setPixmap(QPixmap('./img/print_num/minus.png'))
            
            
    def minus_num(self):
        global print_num
        if print_num > 1:
            print_num -= 1
            self.label.setPixmap(QPixmap(f'./count/{print_num}.png'))
            self.label_plus.setPixmap(QPixmap('./img/print_num/plus.png'))
            self.label_minus.setPixmap(QPixmap('./img/print_num/minus.png'))
        
        if print_num == 1:
            self.label_minus.setPixmap(QPixmap())
            self.label_plus.setPixmap(QPixmap('./img/print_num/plus.png'))
        
    def previous_window(self):
        mouse = Controller()
        self.w = FrameSizeSelectWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_window(self):
        global size
        if size == 2:
            self.w = FrameSelectWindow_2()
        if size == 4:
            self.w = FrameSelectWindow_4()
        self.w.showFullScreen()
        self.close()
        
class FrameSelectWindow_2(QMainWindow, form_class_9):
    def __init__(self):
        super(FrameSelectWindow_2, self).__init__()
        self.setupUi(self)
        self.mouse = Controller()
        
        global frame
        frame = 0
        
        global frame_c
        frame_c = 0
        
        self.move_previous.clicked.connect(self.previous_window)
        self.move_next.clicked.connect(self.next_window)
        
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
        self.frame_choice_11.clicked.connect(self.select_11)
    
    def select_frame(self, n):
        global size
        global frame
        global frame_c
        self.border(n)
        frame = f'./frame_v2/{size}frame/{n}.png'
        frame_c = n
    
    def border(self, n):
        self.frame_1.setPixmap(QPixmap())
        self.frame_2.setPixmap(QPixmap())
        self.frame_3.setPixmap(QPixmap())
        self.frame_4.setPixmap(QPixmap())
        self.frame_5.setPixmap(QPixmap())
        self.frame_6.setPixmap(QPixmap())
        self.frame_7.setPixmap(QPixmap())
        self.frame_8.setPixmap(QPixmap())
        self.frame_9.setPixmap(QPixmap())
        self.frame_10.setPixmap(QPixmap())
        self.frame_11.setPixmap(QPixmap())
        if n==1:
            self.frame_1.setPixmap(QPixmap('./img/print_num/check.png'))
            self.frame_1.setScaledContents(True)
        if n==2:
            self.frame_2.setPixmap(QPixmap('./img/print_num/check.png'))
            self.frame_2.setScaledContents(True)
        if n==3:
            self.frame_3.setPixmap(QPixmap('./img/print_num/check.png'))
            self.frame_3.setScaledContents(True)
        if n==4:
            self.frame_4.setPixmap(QPixmap('./img/print_num/check.png'))
            self.frame_4.setScaledContents(True)
        if n==5:
            self.frame_5.setPixmap(QPixmap('./img/print_num/check.png'))
            self.frame_5.setScaledContents(True)
        if n==6:
            self.frame_6.setPixmap(QPixmap('./img/print_num/check.png'))
            self.frame_6.setScaledContents(True)
        if n==7:
            self.frame_7.setPixmap(QPixmap('./img/print_num/check.png'))
            self.frame_7.setScaledContents(True)
        if n==8:
            self.frame_8.setPixmap(QPixmap('./img/print_num/check.png'))
            self.frame_8.setScaledContents(True)
        if n==9:
            self.frame_9.setPixmap(QPixmap('./img/print_num/check.png'))
            self.frame_9.setScaledContents(True)
        if n==10:
            self.frame_10.setPixmap(QPixmap('./img/print_num/check.png'))
            self.frame_10.setScaledContents(True)
        if n==11:
            self.frame_11.setPixmap(QPixmap('./img/print_num/check.png'))
            self.frame_11.setScaledContents(True)
        
    
    def select_1(self):
        self.select_frame(1)
    def select_2(self):
        self.select_frame(2)
    def select_3(self):
        self.select_frame(3)
    def select_4(self):
        self.select_frame(4)
    def select_5(self):
        self.select_frame(5)
    def select_6(self):
        self.select_frame(6)
    def select_7(self):
        self.select_frame(7)
    def select_8(self):
        self.select_frame(8)
    def select_9(self):
        self.select_frame(9)
    def select_10(self):
        self.select_frame(10)
    def select_11(self):
        self.select_frame(11)
    
    def previous_window(self):
        self.w = NumSelectWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_window(self):
        global frame
        if frame != 0:
            self.w = CaptureWindow()
            self.w.showFullScreen()
            self.close()
        else:
            QMessageBox.about(self,'충곽한컷','프레임을 선택해주세요')
        
class FrameSelectWindow_4(QMainWindow, form_class_10):
    def __init__(self):
        super(FrameSelectWindow_4, self).__init__()
        self.setupUi(self)
        self.mouse = Controller()
        
        global frame
        frame = 0
        
        global frame_c
        frame_c = 0
        
        self.move_previous.clicked.connect(self.previous_window)
        self.move_next.clicked.connect(self.next_window)
        
        self.frame_choice_1.clicked.connect(self.select_1)
        self.frame_choice_2.clicked.connect(self.select_2)
        self.frame_choice_3.clicked.connect(self.select_3)
    
    def select_frame(self, n):
        global size
        global frame
        global frame_c
        self.border(n)
        frame = f'./frame_v2/{size}frame/{n}.png'
        frame_c = n
    
    def border(self, n):
        self.frame_1.setPixmap(QPixmap())
        self.frame_2.setPixmap(QPixmap())
        self.frame_3.setPixmap(QPixmap())
        if n==1:
            self.frame_1.setPixmap(QPixmap('./img/print_num/check.png'))
            self.frame_1.setScaledContents(True)
        if n==2:
            self.frame_2.setPixmap(QPixmap('./img/print_num/check.png'))
            self.frame_2.setScaledContents(True)
        if n==3:
            self.frame_3.setPixmap(QPixmap('./img/print_num/check.png'))
            self.frame_3.setScaledContents(True)
    
    def select_1(self):
        self.select_frame(1)
    def select_2(self):
        self.select_frame(2)
    def select_3(self):
        self.select_frame(3)
    
    def previous_window(self):
        self.w = NumSelectWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_window(self):
        global frame
        if frame != 0:
            self.w = CaptureWindow()
            self.w.showFullScreen()
            self.close()
        else:
            QMessageBox.about(self,'충곽한컷','프레임을 선택해주세요')
        

class CaptureWindow(QMainWindow, form_class_4):
    
    def cut(self, img):
        global size
        
        if size == 2:
            target_ratio = 92 / 64
        if size == 4:
            target_ratio = 45 / 64
        
        height, width, _ = img.shape
        current_ratio = width / height
        
        if current_ratio > target_ratio:
            new_width = int(height * target_ratio)
            start_x = (width - new_width) // 2
            img = img[:, start_x:start_x + new_width]
        
        else:
            new_height = int(width / target_ratio)
            start_y = (height - new_height) // 2
            img = img[start_y:start_y + new_height, :]
            
        return img
    
    def cut_2(self, img):
        image = img
        
        target_ratio = 1404 / 900

        height, width, _ = image.shape
        
        current_ratio = width / height

        if current_ratio > target_ratio:
            new_width = int(height * target_ratio)
            start_x = (width - new_width) // 2
            cropped_image = image[:, start_x:start_x + new_width]
        else:
            new_height = int(width / target_ratio)
            start_y = (height - new_height) // 2
            cropped_image = image[start_y:start_y + new_height, :]
            
        return cropped_image
    
    def mergeImg(self, frame_path, img, frame_cut):
        main_image = cv2.imread('./no.png', cv2.IMREAD_COLOR)
        insert_image_1 = self.cut_2(img)
        insert_image_2 = self.cut_2(frame_cut)

        frame = cv2.imread(frame_path, cv2.IMREAD_COLOR)

        mask = cv2.imread(frame_path, cv2.IMREAD_UNCHANGED)
        mask = mask[:, :, 3]
        mask = cv2.bitwise_not(mask)

        m = 0.415
        insert_image_1 = cv2.resize(insert_image_1, None, None, m, m, cv2.INTER_CUBIC)
        insert_image_2 = cv2.resize(insert_image_2, None, None, m, m, cv2.INTER_CUBIC)

        insert_height, insert_width, _ = insert_image_1.shape

        main_image[0:0 + insert_height, 0:0 + insert_width] = insert_image_1
        main_image[0:0 + insert_height, 0:0 + insert_width] = insert_image_2

        cv2.copyTo(main_image, mask, frame)
        cv2.imwrite('./test_img/res29.jpg', frame)
        return frame
    
    def run(self):
        global size
        global frame_c
        # cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture(1)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        while self.running:
            
            with mss.mss() as sct:
    
                # monitor_number = 1
                monitor_number = 2
                # monitor_number = 3
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
                x = 365
                y = 90
                w = 1367
                h = 911
                img = img[y: y + h, x: x + w]
                # img = img[...,::-1].copy()
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (1400, 900))
                
                img = self.cut(img)
                
                h, w, _ = img.shape
                
                main_img = cv2.imread('./white_4.png', cv2.IMREAD_UNCHANGED)
                
                main_img[0:h, 700-(w//2):700-(w//2) + w, 0:3] = img
                main_img[0:h, 700-(w//2):700-(w//2) + w, 3] = 255
                
                qImg = qimage2ndarray.array2qimage(main_img, normalize=False)
                pixmap = QPixmap.fromImage(qImg)
                self.label.setPixmap(pixmap)
                
                if (size == 2)&(frame_c >= 3)&(frame_c<=10):
                    main_frame = cv2.imread('./no.png', cv2.IMREAD_UNCHANGED)
                    frame_img = cv2.imread(f'./frame_v2/frame_capture/{frame_c}_{self.ver}.png', cv2.IMREAD_UNCHANGED)
                    
                    frame_img = cv2.resize(frame_img, (1181, 757))
                    
                    mask = cv2.resize(frame_img[:, :, 3], None,  None, 1, 1, cv2.INTER_CUBIC)
                    
                    frame_img = cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB)
                    
                    frame_img = cv2.resize(frame_img, (1400, 900))
                    mask = cv2.resize(mask, (1400, 900))
                    
                    
                    main_frame = cv2.resize(main_frame, (1400, 900))
                    main_frame[0:h, 702-(w//2):702-(w//2) + w, 0:3] = img
                    main_frame[:, :, :3] = frame_img
                    main_frame[:, :, 3] = mask
                    
                    qImg_f = qimage2ndarray.array2qimage(main_frame, normalize=False)
                    
                    pixmap_f = QPixmap.fromImage(qImg_f)
                    self.label_3.setPixmap(pixmap_f)
                    
                
        cap.release()
        print("Thread end.")
    
    def __init__(self):
        super(CaptureWindow, self).__init__()
        self.setupUi(self)
        mouse = Controller()
        
        self.mouse = Controller()
        
        self.running = True

        th = threading.Thread(target=self.run)
        th.start()
        
        self.timelimit = 10
        self.numlimit = 6

        self.count = self.timelimit + 1
        self.num = 1
        
        self.c = 1
        
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.count_start)
        
        self.ver = 1
        
        global size
    
    def count_start(self):
        if self.count > 1:
            self.count = self.count - 1
            self.count_label.setPixmap(QPixmap(f'./count/{self.count}.png'))
            
            if (self.num == 1)&(self.c):
                self.count_label_2.setPixmap(QPixmap('./count/1.png'))
                self.c = 0

        else:
            self.count_label.setPixmap(QPixmap())
            self.count = self.timelimit + 1
            self.num = self.num + 1
            
            if self.num == 4:
                self.ver = 2
            
            self.capture()
            
            if self.num <= self.numlimit:
                self.count_label_2.setPixmap(QPixmap(f'./count/{self.num}.png'))

            else :
                self.count_label_2.setPixmap(QPixmap())
                
                self.running = False
                self.timer.stop()
                
                self.label_2.setPixmap(QPixmap('./img/pages_v4/슬라이드8.png'))
                
                self.timer = QTimer(self)
                self.timer.start(3000)
                self.timer.timeout.connect(self.next_window)
            
    def capture(self):
        self.mouse.position = (2226, 69)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)
        
        time.sleep(1)
        
        photo_dir = 'C:\digiCamControl\Session1'
        photos = os.listdir(photo_dir)
        img = cv2.imread(f'{photo_dir}/{photos[-1]}')
        cv2.imwrite(f'{photo_dir}/{photos[-1]}', cv2.flip(img, 1))
    
    def previous_window(self):
        self.timer.stop()
        self.w = ExplainWindow()
        self.w.showFullScreen()
        self.close()
        
    def next_window(self):
        global size
        self.timer.stop()
        
        photo_dir = 'C:\digiCamControl\Session1'
        photos = os.listdir(photo_dir)
        img = cv2.imread(f'{photo_dir}/{photos[-1]}')
        cv2.imwrite(f'{photo_dir}/{photos[-1]}', cv2.flip(img, 1))
        
        if size == 2:
            self.w = PhotoSelectWindow_2()
        if size == 4:
            self.w = PhotoSelectWindow_4()
        self.w.showFullScreen()
        self.close()

class PhotoSelectWindow_2(QMainWindow, form_class_11):
    def __init__(self):
        super(PhotoSelectWindow_2, self).__init__()
        self.setupUi(self)
        mouse = Controller()
        
        self.photo_dir = 'C:\digiCamControl\Session1'
        self.photos = os.listdir(self.photo_dir)
        
        img_dir = 'C:\digiCamControl\Session2'
        
        img = os.listdir(img_dir)
        num = int(img[-1][-8:-4]) + 1
        name = (f"CUT_{ num : #05d}.jpg").replace(' ', '')
        temp = self.cut(f'{self.photo_dir}/{self.photos[-6]}')
        cv2.imwrite(f'C:\digiCamControl\Session2/{name}', temp)
        
        img = os.listdir(img_dir)
        num = int(img[-1][-8:-4]) + 1
        name = (f"CUT_{ num : #05d}.jpg").replace(' ', '')
        temp = self.cut(f'{self.photo_dir}/{self.photos[-5]}')
        cv2.imwrite(f'C:\digiCamControl\Session2/{name}', temp)
        
        img = os.listdir(img_dir)
        num = int(img[-1][-8:-4]) + 1
        name = (f"CUT_{ num : #05d}.jpg").replace(' ', '')
        temp = self.cut(f'{self.photo_dir}/{self.photos[-4]}')
        cv2.imwrite(f'C:\digiCamControl\Session2/{name}', temp)
        
        img = os.listdir(img_dir)
        num = int(img[-1][-8:-4]) + 1
        name = (f"CUT_{ num : #05d}.jpg").replace(' ', '')
        temp = self.cut(f'{self.photo_dir}/{self.photos[-3]}')
        cv2.imwrite(f'C:\digiCamControl\Session2/{name}', temp)
        
        img = os.listdir(img_dir)
        num = int(img[-1][-8:-4]) + 1
        name = (f"CUT_{ num : #05d}.jpg").replace(' ', '')
        temp = self.cut(f'{self.photo_dir}/{self.photos[-2]}')
        cv2.imwrite(f'C:\digiCamControl\Session2/{name}', temp)
        
        img = os.listdir(img_dir)
        num = int(img[-1][-8:-4]) + 1
        name = (f"CUT_{ num : #05d}.jpg").replace(' ', '')
        temp = self.cut(f'{self.photo_dir}/{self.photos[-1]}')
        cv2.imwrite(f'C:\digiCamControl\Session2/{name}', temp)
        
        img = os.listdir(img_dir)
        
        self.photo.setPixmap(QPixmap('./white.png'))
        self.photo_1.setPixmap(QPixmap(img_dir + '/' + img[-6]).scaled(QSize(450, 300)))
        self.photo_2.setPixmap(QPixmap(img_dir + '/' + img[-5]).scaled(QSize(450, 300)))
        self.photo_3.setPixmap(QPixmap(img_dir + '/' + img[-4]).scaled(QSize(450, 300)))
        self.photo_4.setPixmap(QPixmap(img_dir + '/' + img[-3]).scaled(QSize(450, 300)))
        self.photo_5.setPixmap(QPixmap(img_dir + '/' + img[-2]).scaled(QSize(450, 300)))
        self.photo_6.setPixmap(QPixmap(img_dir + '/' + img[-1]).scaled(QSize(450, 300)))
        3
        global selected
        selected = [0, 0]
        
        self.selected = [0, 0, 0, 0, 0, 0]
        self.selected_sum = 3
        self.res = 0
        
        self.photo_preview()
        
        self.photo_choice_1.clicked.connect(self.photo_select_1)
        self.photo_choice_2.clicked.connect(self.photo_select_2)
        self.photo_choice_3.clicked.connect(self.photo_select_3)
        self.photo_choice_4.clicked.connect(self.photo_select_4)
        self.photo_choice_5.clicked.connect(self.photo_select_5)
        self.photo_choice_6.clicked.connect(self.photo_select_6)
        
        self.move_next.clicked.connect(self.next_window)
    
    def cut(self, file_path):
        image = cv2.imread(file_path)
        
        image = cv2.resize(image, (2736, 1824), cv2.INTER_CUBIC)

        target_ratio = 92 / 64

        height, width, _ = image.shape
        current_ratio = width / height

        if current_ratio > target_ratio:
            new_width = int(height * target_ratio)
            start_x = (width - new_width) // 2
            cropped_image = image[:, start_x:start_x + new_width]
        else:
            new_height = int(width / target_ratio)
            start_y = (height - new_height) // 2
            cropped_image = image[start_y:start_y + new_height, :]
            
        return cropped_image
    
    def mergeImg(self, frame_path, file_path_1, file_path_2):
        main_image = cv2.imread('./white.png', cv2.IMREAD_COLOR)
        if file_path_1 == 0:
            file_path_1 = './white_5.png'
        if file_path_2 == 0:
            file_path_2 = './white_5.png'
        insert_image_1 = self.cut(file_path_1)
        insert_image_2 = self.cut(file_path_2)

        frame = cv2.imread(frame_path, cv2.IMREAD_COLOR)

        mask = cv2.imread(frame_path, cv2.IMREAD_UNCHANGED)
        mask = mask[:, :, 3]
        mask = cv2.bitwise_not(mask)

        m = 0.415
        insert_image_1 = cv2.resize(insert_image_1, None, None, m, m, cv2.INTER_CUBIC)
        insert_image_2 = cv2.resize(insert_image_2, None, None, m, m, cv2.INTER_CUBIC)

        x_1 = 47
        y_1 = 165

        x_2 = 47
        y_2 = 944

        insert_height, insert_width, _ = insert_image_1.shape

        main_image[y_1:y_1 + insert_height, x_1:x_1 + insert_width] = insert_image_1
        main_image[y_2:y_2 + insert_height, x_2:x_2 + insert_width] = insert_image_2

        cv2.copyTo(main_image, mask, frame)
        
        return frame
    
    def photo_preview(self):
        global frame
        
        img_1 = selected[0]
        img_2 = selected[1]
        res = self.mergeImg(frame, img_1, img_2)
        
        self.res = res
        res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        res = cv2.resize(res, (510, 740))
        
        h, w, c = res.shape
        qImg = QImage(res.data, w, h, w*c, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qImg)
        
        self.photo.setPixmap(pixmap)
    
    def photo_select_1(self):
        global selected
        
        if self.selected[-6] == 0:
            if self.selected_sum != 0:
                
                if (self.selected_sum == 1)|(self.selected_sum == 3):
                    self.selected[-6] = 1
                    self.selected_sum = self.selected_sum - 1
                    selected[0] = self.photo_dir + '/' + self.photos[-6]
                
                else :
                    self.selected[-6] = 2
                    self.selected_sum = self.selected_sum -2
                    selected[1] = self.photo_dir + '/' + self.photos[-6]
                
                self.photo_1.setStyleSheet("border: 4px solid #DA5451;")
        
        else :
            self.photo_1.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-6] - 1] = 0
            self.selected_sum = self.selected_sum + self.selected[-6]
            self.selected[-6] = 0
        
        self.photo_preview()
    
    def photo_select_2(self):
        global selected
        
        if self.selected[-5] == 0:
            if self.selected_sum != 0:
                
                if (self.selected_sum == 1)|(self.selected_sum == 3):
                    self.selected[-5] = 1
                    self.selected_sum = self.selected_sum - 1
                    selected[0] = self.photo_dir + '/' + self.photos[-5]
                
                else :
                    self.selected[-5] = 2
                    self.selected_sum = self.selected_sum -2
                    selected[1] = self.photo_dir + '/' + self.photos[-5]
                
                self.photo_2.setStyleSheet("border: 4px solid #DA5451;")
        
        else :
            self.photo_2.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-5] - 1] = 0
            self.selected_sum = self.selected_sum + self.selected[-5]
            self.selected[-5] = 0
        
        self.photo_preview()
    
    def photo_select_3(self):
        global selected
        
        if self.selected[-4] == 0:
            if self.selected_sum != 0:
                
                if (self.selected_sum == 1)|(self.selected_sum == 3):
                    self.selected[-4] = 1
                    self.selected_sum = self.selected_sum - 1
                    selected[0] = self.photo_dir + '/' + self.photos[-4]
                
                else :
                    self.selected[-4] = 2
                    self.selected_sum = self.selected_sum -2
                    selected[1] = self.photo_dir + '/' + self.photos[-4]
                
                self.photo_3.setStyleSheet("border: 4px solid #DA5451;")
        
        else :
            self.photo_3.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-4] - 1] = 0
            self.selected_sum = self.selected_sum + self.selected[-4]
            self.selected[-4] = 0
        
        self.photo_preview()
    
    def photo_select_4(self):
        global selected
        
        if self.selected[-3] == 0:
            if self.selected_sum != 0:
                
                if (self.selected_sum == 1)|(self.selected_sum == 3):
                    self.selected[-3] = 1
                    self.selected_sum = self.selected_sum - 1
                    selected[0] = self.photo_dir + '/' + self.photos[-3]
                
                else :
                    self.selected[-3] = 2
                    self.selected_sum = self.selected_sum -2
                    selected[1] = self.photo_dir + '/' + self.photos[-3]
                
                self.photo_4.setStyleSheet("border: 4px solid #DA5451;")
        
        else :
            self.photo_4.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-3] - 1] = 0
            self.selected_sum = self.selected_sum + self.selected[-3]
            self.selected[-3] = 0
        
        self.photo_preview()
    
    def photo_select_5(self):
        global selected
        
        if self.selected[-2] == 0:
            if self.selected_sum != 0:
                
                if (self.selected_sum == 1)|(self.selected_sum == 3):
                    self.selected[-2] = 1
                    self.selected_sum = self.selected_sum - 1
                    selected[0] = self.photo_dir + '/' + self.photos[-2]
                
                else :
                    self.selected[-2] = 2
                    self.selected_sum = self.selected_sum -2
                    selected[1] = self.photo_dir + '/' + self.photos[-2]
                
                self.photo_5.setStyleSheet("border: 4px solid #DA5451;")
        
        else :
            self.photo_5.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-2] - 1] = 0
            self.selected_sum = self.selected_sum + self.selected[-2]
            self.selected[-2] = 0
        
        self.photo_preview()
    
    def photo_select_6(self):
        global selected
        
        if self.selected[-1] == 0:
            if self.selected_sum != 0:
                
                if (self.selected_sum == 1)|(self.selected_sum == 3):
                    self.selected[-1] = 1
                    self.selected_sum = self.selected_sum - 1
                    selected[0] = self.photo_dir + '/' + self.photos[-1]
                
                else :
                    self.selected[-1] = 2
                    self.selected_sum = self.selected_sum -2
                    selected[1] = self.photo_dir + '/' + self.photos[-1]
                
                self.photo_6.setStyleSheet("border: 4px solid #DA5451;")
        
        else :
            self.photo_6.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-1] - 1] = 0
            self.selected_sum = self.selected_sum + self.selected[-1]
            self.selected[-1] = 0
        
        self.photo_preview()
        
    def next_window(self):
        global selected
        if (selected[0] != 0) & (selected[1] != 0):
            now = datetime.datetime.now()
            now_str = now.strftime('%Y%m%d%H%M%S')
            
            cv2.imwrite(f'./result/{now_str}.jpg', self.res)
            
            self.w = GoodbyeWindow()
            self.w.showFullScreen()
            self.close()
        else:
            QMessageBox.about(self,'충곽한컷','사진을 선택해주세요')

class PhotoSelectWindow_4(QMainWindow, form_class_5):
    def __init__(self):
        super(PhotoSelectWindow_4, self).__init__()
        self.setupUi(self)
        mouse = Controller()
        
        self.photo_dir = 'C:\digiCamControl\Session1'
        self.photos = os.listdir(self.photo_dir)
        
        img_dir = 'C:\digiCamControl\Session2'
        
        img = os.listdir(img_dir)
        num = int(img[-1][-8:-4]) + 1
        name = (f"CUT_{ num : #05d}.jpg").replace(' ', '')
        temp = self.cut(f'{self.photo_dir}/{self.photos[-6]}')
        cv2.imwrite(f'C:\digiCamControl\Session2/{name}', temp)
        
        img = os.listdir(img_dir)
        num = int(img[-1][-8:-4]) + 1
        name = (f"CUT_{ num : #05d}.jpg").replace(' ', '')
        temp = self.cut(f'{self.photo_dir}/{self.photos[-5]}')
        cv2.imwrite(f'C:\digiCamControl\Session2/{name}', temp)
        
        img = os.listdir(img_dir)
        num = int(img[-1][-8:-4]) + 1
        name = (f"CUT_{ num : #05d}.jpg").replace(' ', '')
        temp = self.cut(f'{self.photo_dir}/{self.photos[-4]}')
        cv2.imwrite(f'C:\digiCamControl\Session2/{name}', temp)
        
        img = os.listdir(img_dir)
        num = int(img[-1][-8:-4]) + 1
        name = (f"CUT_{ num : #05d}.jpg").replace(' ', '')
        temp = self.cut(f'{self.photo_dir}/{self.photos[-3]}')
        cv2.imwrite(f'C:\digiCamControl\Session2/{name}', temp)
        
        img = os.listdir(img_dir)
        num = int(img[-1][-8:-4]) + 1
        name = (f"CUT_{ num : #05d}.jpg").replace(' ', '')
        temp = self.cut(f'{self.photo_dir}/{self.photos[-2]}')
        cv2.imwrite(f'C:\digiCamControl\Session2/{name}', temp)
        
        img = os.listdir(img_dir)
        num = int(img[-1][-8:-4]) + 1
        name = (f"CUT_{ num : #05d}.jpg").replace(' ', '')
        temp = self.cut(f'{self.photo_dir}/{self.photos[-1]}')
        cv2.imwrite(f'C:\digiCamControl\Session2/{name}', temp)
        
        img = os.listdir(img_dir)
        self.photo.setPixmap(QPixmap('./white.png'))
        self.photo_1.setPixmap(QPixmap(img_dir + '/' + img[-6]).scaled(QSize(450, 300)))
        self.photo_2.setPixmap(QPixmap(img_dir + '/' + img[-5]).scaled(QSize(450, 300)))
        self.photo_3.setPixmap(QPixmap(img_dir + '/' + img[-4]).scaled(QSize(450, 300)))
        self.photo_4.setPixmap(QPixmap(img_dir + '/' + img[-3]).scaled(QSize(450, 300)))
        self.photo_5.setPixmap(QPixmap(img_dir + '/' + img[-2]).scaled(QSize(450, 300)))
        self.photo_6.setPixmap(QPixmap(img_dir + '/' + img[-1]).scaled(QSize(450, 300)))
        
        global selected
        selected = [0, 0, 0, 0]
        
        self.selected = [-1, -1, -1, -1, -1, -1]
        self.res = 0
        
        self.photo_preview()
        
        self.photo_choice_1.clicked.connect(self.photo_select_1)
        self.photo_choice_2.clicked.connect(self.photo_select_2)
        self.photo_choice_3.clicked.connect(self.photo_select_3)
        self.photo_choice_4.clicked.connect(self.photo_select_4)
        self.photo_choice_5.clicked.connect(self.photo_select_5)
        self.photo_choice_6.clicked.connect(self.photo_select_6)
        
        self.move_next.clicked.connect(self.next_window)
    
    def cut(self, file_path):
        image = cv2.imread(file_path)
        
        image = cv2.resize(image, (2736, 1824), cv2.INTER_CUBIC)
        
        target_ratio = 45 / 64 

        height, width, _ = image.shape
        current_ratio = width / height

        if current_ratio > target_ratio:
            new_width = int(height * target_ratio)
            start_x = (width - new_width) // 2
            cropped_image = image[:, start_x:start_x + new_width]
        else:
            new_height = int(width / target_ratio)
            start_y = (height - new_height) // 2
            cropped_image = image[start_y:start_y + new_height, :]
            
        return cropped_image
    
    def mergeImg(self, frame_path, file_path_1, file_path_2, file_path_3, file_path_4):
        main_image = cv2.imread('./white.png', cv2.IMREAD_COLOR)
        if file_path_1 == 0:
            file_path_1 = './white_5.png'
        if file_path_2 == 0:
            file_path_2 = './white_5.png'
        if file_path_3 == 0:
            file_path_3 = './white_5.png'
        if file_path_4 == 0:
            file_path_4 = './white_5.png'
        insert_image_1 = self.cut(file_path_1)
        insert_image_2 = self.cut(file_path_2)
        insert_image_3 = self.cut(file_path_3)
        insert_image_4 = self.cut(file_path_4)

        frame = cv2.imread(frame_path, cv2.IMREAD_COLOR)

        mask = cv2.imread(frame_path, cv2.IMREAD_UNCHANGED)
        mask = mask[:, :, 3]
        mask = cv2.bitwise_not(mask)

        m = 0.415
        insert_image_1 = cv2.resize(insert_image_1, None, None, m, m, cv2.INTER_CUBIC)
        insert_image_2 = cv2.resize(insert_image_2, None, None, m, m, cv2.INTER_CUBIC)
        insert_image_3 = cv2.resize(insert_image_3, None, None, m, m, cv2.INTER_CUBIC)
        insert_image_4 = cv2.resize(insert_image_4, None, None, m, m, cv2.INTER_CUBIC)

        x_1 = 47
        y_1 = 165

        x_2 = 47
        y_2 = 944
        
        x_3 = 602
        y_3 = 165
        
        x_4 = 602
        y_4 = 944

        insert_height, insert_width, _ = insert_image_1.shape

        main_image[y_1:y_1 + insert_height, x_1:x_1 + insert_width] = insert_image_1
        main_image[y_2:y_2 + insert_height, x_2:x_2 + insert_width] = insert_image_2
        main_image[y_3:y_3 + insert_height, x_3:x_3 + insert_width] = insert_image_3
        main_image[y_4:y_4 + insert_height, x_4:x_4 + insert_width] = insert_image_4

        cv2.copyTo(main_image, mask, frame)
        
        return frame
    
    def photo_preview(self):
        global frame
        img_1 = selected[0]
        img_2 = selected[1]
        img_3 = selected[2]
        img_4 = selected[3]
        res = self.mergeImg(frame, img_1, img_2, img_3, img_4)
        
        self.res = res
        res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        res = cv2.resize(res, (510, 740))
        
        h, w, c = res.shape
        qImg = QImage(res.data, w, h, w*c, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qImg)
        
        self.photo.setPixmap(pixmap)
    
    def photo_select_1(self):
        global selected
        
        if self.selected[-6] == -1:
            q = -1
            for i in range(4):
                if selected[i] == 0:
                    q = i
                    break
            
            if q!=-1:
                self.selected[-6] = q
                selected[q] = self.photo_dir + '/' + self.photos[-6]
                self.photo_1.setStyleSheet("border: 4px solid #DA5451;")
                
        else :
            self.photo_1.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-6]] = 0
            self.selected[-6] = -1
        
        self.photo_preview()
    
    def photo_select_2(self):
        global selected
        
        if self.selected[-5] == -1:
            q = -1
            for i in range(4):
                if selected[i] == 0:
                    q = i
                    break
            
            if q!=-1:
                self.selected[-5] = q
                selected[q] = self.photo_dir + '/' + self.photos[-5]
                self.photo_2.setStyleSheet("border: 4px solid #DA5451;")
                
        else :
            self.photo_2.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-5]] = 0
            self.selected[-5] = -1
        
        self.photo_preview()
    
    def photo_select_3(self):
        global selected
        
        if self.selected[-4] == -1:
            q = -1
            for i in range(4):
                if selected[i] == 0:
                    q = i
                    break
            
            if q!=-1:
                self.selected[-4] = q
                selected[q] = self.photo_dir + '/' + self.photos[-4]
                self.photo_3.setStyleSheet("border: 4px solid #DA5451;")
                
        else :
            self.photo_3.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-4]] = 0
            self.selected[-4] = -1
        
        self.photo_preview()
    
    def photo_select_4(self):
        global selected
        
        if self.selected[-3] == -1:
            q = -1
            for i in range(4):
                if selected[i] == 0:
                    q = i
                    break
            
            if q!=-1:
                self.selected[-3] = q
                selected[q] = self.photo_dir + '/' + self.photos[-3]
                self.photo_4.setStyleSheet("border: 4px solid #DA5451;")
                
        else :
            self.photo_4.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-3]] = 0
            self.selected[-3] = -1
        
        self.photo_preview()
    
    def photo_select_5(self):
        global selected
        
        if self.selected[-2] == -1:
            q = -1
            for i in range(4):
                if selected[i] == 0:
                    q = i
                    break
            
            if q!=-1:
                self.selected[-2] = q
                selected[q] = self.photo_dir + '/' + self.photos[-2]
                self.photo_5.setStyleSheet("border: 4px solid #DA5451;")
                
        else :
            self.photo_5.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-2]] = 0
            self.selected[-2] = -1
        
        self.photo_preview()
    
    def photo_select_6(self):
        global selected
        
        if self.selected[-1] == -1:
            q = -1
            for i in range(4):
                if selected[i] == 0:
                    q = i
                    break
            
            if q!=-1:
                self.selected[-1] = q
                selected[q] = self.photo_dir + '/' + self.photos[-1]
                self.photo_6.setStyleSheet("border: 4px solid #DA5451;")
                
        else :
            self.photo_6.setStyleSheet("border: 0px solid red;")
            selected[self.selected[-1]] = 0
            self.selected[-1] = -1
        
        self.photo_preview()
        
    def next_window(self):
        global selected
        if (selected[0] != 0) & (selected[1] != 0) & (selected[2] != 0) & (selected[3] != 0):
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
        mouse = Controller()
        
        photo_dir = 'C:\digiCamControl\Session1'
        photos = os.listdir(photo_dir)
        
        num = int(photos[-1][-8:-4]) + 1
        name = (f"DSC_{ num : #05d}.jpg").replace(' ', '')
        
        temp = cv2.imread('./black.jpg')
        cv2.imwrite(f'C:\digiCamControl\Session1/{name}', temp)
        
        self.img_dir = './result'
        self.imgs = os.listdir(self.img_dir)
        self.img = self.imgs[-1]
        self.img_path = f'./result/{self.img}'
        
        self.print_printer(self.img_path)
        
        self.timer = QTimer(self)
        self.timer.start(5000)
        self.timer.timeout.connect(self.next_window)
    
    def print_printer(self, file_path):
        global print_num
        global printer_name
        try:
            img = Image.open(file_path)
            img = img.rotate(90, expand=True)
            
            move_left = 40
            move_up = 38
            rotated_image = ImageOps.expand(img, border=(move_left, move_up, 0, 0), fill='white')

            printer = win32print.OpenPrinter(printer_name)
            hprinter = win32print.GetPrinter(printer, 2)['pPrinterName']
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(printer_name)
            
            for _ in range(print_num):
                hdc.StartDoc('Print Job')
                hdc.StartPage()
                dib = ImageWin.Dib(rotated_image)
                dib.draw(hdc.GetHandleOutput(), (0, 0, rotated_image.size[0], rotated_image.size[1]))
                hdc.EndPage()
                hdc.EndDoc()
            
            hdc.DeleteDC()
            win32print.ClosePrinter(printer)
        
        except Exception as e:
            print("ERROR:", e)
    
    def next_window(self):
        self.timer.stop()
        self.w = MainWindow()
        self.w.showFullScreen()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    # myWindow = CaptureWindow()
    # myWindow = FrameSelectWindow_4()
    # myWindow = PhotoSelectWindow_2()
    # myWindow = PhotoSelectWindow_4()
    # myWindow.show()
    myWindow.showFullScreen()
    app.exec_()