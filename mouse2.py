from pynput import mouse

from pynput.mouse import Button, Controller
 
def on_move(x,y):
    print('Pointer moved to {0}'.format((x, y)))
 

mousea = Controller()
        
# mousea.position = (2226, 69) # 1.마우스 x,y 위치지정
 
with mouse.Listener(
        on_move=on_move) as listener:
    listener.join()