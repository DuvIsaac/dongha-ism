import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np

from time import sleep

form_class_1 = uic.loadUiType("main.ui")[0]
form_class_2 = uic.loadUiType("select.ui")[0]
form_class_3 = uic.loadUiType("explain.ui")[0]
form_class_4 = uic.loadUiType("capture.ui")[0]
# form_class_1 = uic.loadUiType("./page_ui/main.ui")[0]
# form_class_2 = uic.loadUiType("./page_ui/explain.ui")[0]
# form_class_3 = uic.loadUiType("./page_ui/select.ui")[0]
# form_class_4 = uic.loadUiType("./page_ui/capture.ui")[0]
# form_class_5 = uic.loadUiType("./page_ui/photo_select.ui")[0]
# form_class_6 = uic.loadUiType("./page_ui/goodbye.ui")[0]

class StartWindow(QMainWindow, form_class_1):
    def __init__(self):
        super(StartWindow, self).__init__()
        self.setupUi(self)
        self.start.clicked.connect(self.show_new_window)
        # self.start.clicked.connect(self.start)
        
    def show_new_window(self):
        self.w = SelectWindow()
        self.w.show()
        self.close()

class SelectWindow(QMainWindow, form_class_2):
    def __init__(self):
        super(SelectWindow, self).__init__()
        self.setupUi(self)
        self.move_next.clicked.connect(self.show_new_window)
        
    def show_new_window(self):
        self.w = ExplainWindow()
        self.w.show()
        self.close()

class ExplainWindow(QMainWindow, form_class_3):
    def __init__(self):
        super(ExplainWindow, self).__init__()
        self.setupUi(self)
        self.move_next.clicked.connect(self.show_new_window)
        
    def show_new_window(self):
        self.w = CaptureWindow()
        self.w.show()
        self.close()

class CaptureWindow(QMainWindow, form_class_4):
    def __init__(self):
        super(CaptureWindow, self).__init__()
        self.setupUi(self)
        print('s')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = StartWindow()
    myWindow.show()
    # myWindow.showFullScreen()
    app.exec_()
