# run on python3 windows 10 x86_64
import serial
import sys
import win32api
import win32con
def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def rightClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)



if __name__ == '__main__':
    s = serial.Serial(sys.argv[1])
    # s.open()
    while(True):
        byte = s.read(1)
        char = byte.decode('utf-8')
        if char == 'L':
            leftClick()
        elif char == 'R':
            rightClick()
    



