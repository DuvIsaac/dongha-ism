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

import pyautogui


pyautogui.displayMousePosition()

mouse = Controller()

print('capture!')

# # Auto Focus
# mouse.position = (2018, 53)
# mouse.press(Button.left)
# mouse.release(Button.left)

# Capture
# mouse.position = (2224, 53)
# mouse.press(Button.left)
# mouse.release(Button.left)