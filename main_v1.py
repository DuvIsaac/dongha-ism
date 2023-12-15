import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtTest import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import os


import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np

form_class_1 = uic.loadUiType("./page_ui/main.ui")[0]
form_class_2 = uic.loadUiType("./page_ui/explain.ui")[0]
form_class_3 = uic.loadUiType("./page_ui/select.ui")[0]
form_class_4 = uic.loadUiType("./page_ui/capture.ui")[0]
form_class_5 = uic.loadUiType("./page_ui/photo_select.ui")[0]
form_class_6 = uic.loadUiType("./page_ui/goodbye.ui")[0]


class MainWindow(QMainWindow, form_class_1):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.start.clicked.connect(self.next_window)
        
    def next_window(self):
        self.w = ExplainWindow()
        self.w.show()
        self.close()

class ExplainWindow(QMainWindow, form_class_2):
    def __init__(self):
        super(ExplainWindow, self).__init__()
        self.setupUi(self)
        self.move_next.clicked.connect(self.next_window)
        self.move_previous.clicked.connect(self.previous_window)
        
    def previous_window(self):
        self.w = MainWindow()
        self.w.show()
        self.close()
        
    def next_window(self):
        self.w = SelectWindow()
        self.w.show()
        self.close()

class SelectWindow(QMainWindow, form_class_3):
    def __init__(self):
        super(SelectWindow, self).__init__()
        self.setupUi(self)
        self.move_next.clicked.connect(self.next_window)
        self.move_previous.clicked.connect(self.previous_window)
        
    def previous_window(self):
        self.w = ExplainWindow()
        self.w.show()
        self.close()
        
    def next_window(self):
        self.w = CaptureWindow()
        self.w.show()
        self.close()

class CaptureWindow(QMainWindow, form_class_4):
    def __init__(self):
        super(CaptureWindow, self).__init__()
        self.setupUi(self)

        self.count = 10
        
        self.count_label.setPixmap(QPixmap(f'./count/{self.count}.png'))
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.count_start)
    
    def count_start(self):
        if self.count != 0:
            self.count = self.count - 1
            self.count_label.setPixmap(QPixmap(f'./count/{self.count}.png'))
        else:
            self.count = 10
            self.count_label.setPixmap(QPixmap(f'./count/{self.count}.png'))
            self.capture()
            
    def capture(self):
        print('capture!')
    
    def previous_window(self):
        self.timer.stop()
        self.w = SelectWindow()
        self.w.show()
        self.close()
        
    def next_window(self):
        self.timer.stop()
        self.w = PhotoSelectWindow()
        self.w.show()
        self.close()

class PhotoSelectWindow(QMainWindow, form_class_5):
    def __init__(self):
        super(PhotoSelectWindow, self).__init__()
        self.setupUi(self)
        self.print_photo.clicked.connect(self.next_window)
        self.non_print_photo.clicked.connect(self.next_window)
        
        
        photo_dir = 'C:/Users/chhch/Pictures/digiCamControl/Session1'
        photos = os.listdir(photo_dir)
        
        self.photo_1.setPixmap(QPixmap(photo_dir + '/' + photos[-4]).scaled(QSize(361, 251)))
        self.photo_2.setPixmap(QPixmap(photo_dir + '/' + photos[-3]).scaled(QSize(361, 251)))
        self.photo_3.setPixmap(QPixmap(photo_dir + '/' + photos[-2]).scaled(QSize(361, 251)))
        self.photo_4.setPixmap(QPixmap(photo_dir + '/' + photos[-1]).scaled(QSize(361, 251)))
        
    def previous_window(self):
        self.w = CaptureWindow()
        self.w.show()
        self.close()
        
    def next_window(self):
        self.w = GoodbyeWindow()
        self.w.show()
        self.close()

class GoodbyeWindow(QMainWindow, form_class_6):
    def __init__(self):
        super(GoodbyeWindow, self).__init__()
        self.setupUi(self)
        
        self.timer = QTimer(self)
        self.timer.start(5000)
        self.timer.timeout.connect(self.next_window)
        
    def previous_window(self):
        self.w = PhotoSelectWindow()
        self.w.show()
        self.close()
        
    def next_window(self):
        self.timer.stop()
        self.w = MainWindow()
        self.w.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    # myWindow.showFullScreen()
    app.exec_()
