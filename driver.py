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
        # char = byte.decode('utf-8')
        # if char == 'L':
        #     leftClick()
        # elif char == 'R':
        #     rightClick()
        if byte == bytes([22]):
            x0b = s.read(1)
            x1b = s.read(1)
            byte = s.read(1)
            if byte == bytes([23]):
                x0int = int.from_bytes(x0b,byteorder = 'big')-128
                x1int = int.from_bytes(x1b,byteorder = 'big')
                y0b = s.read(1)
                y1b = s.read(1)
                byte = s.read(1)
                if byte == bytes([24]):
                    y0int = int.from_bytes(y0b,byteorder = 'big')-128
                    y1int = int.from_bytes(y1b,byteorder = 'big')
                    z0b = s.read(1)
                    z1b = s.read(1)
                    byte = s.read(1)
                    if byte == bytes([25]):
                        z0int = int.from_bytes(z0b,byteorder = 'big')-128
                        z1int = int.from_bytes(z1b,byteorder = 'big')
                    else:
                        break
                else:
                    break
            else:
                break
            ax = x0int / 32.0 * 9.8 + x1int / 256 / 32.0 * 9.8
            ay = y0int / 32.0 * 9.8 + y1int / 256 / 32.0 * 9.8
            az = z0int / 32.0 * 9.8 + z1int / 256 / 32.0 * 9.8
            # print('x:',ax,'y:',ay,'z:',az)
            print('x0low')





