from pynput.mouse import Button, Controller
import time
 
sl_time = 2
mouse = Controller()
 
mouse.position = (300,500) # 1.마우스 x,y 위치지정
time.sleep(sl_time)
 
mouse.press(Button.left) # 3.현재 마우스위치 클릭(누르고있는중)
mouse.release(Button.left) # 4.현재 마우스위치 클릭(풀기)
time.sleep(sl_time)