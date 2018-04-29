# run on python3 windows 10 x86_64
import serial
import sys
import win32api
import win32con
import numpy as np



def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def rightClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)



if __name__ == '__main__':
    i = 0
    debug = True
    s = serial.Serial(sys.argv[1])
    # s.open()
    v = int(sys.argv[2])
    Thresh = int(sys.argv[3])
    print('Begin to calibrate, please put the mobile phone on the surface and do not move')
    # List to store the acceleration data for calibration
    caliAcc = []
    # The number of calibrated data
    numCali = 0
    while numCali < 100:
        byte = s.read(1)
        while(byte != bytes([22])):
            byte = s.read(1)
            if debug:
                print('byte:',byte)
        x0b = s.read(1)
        x1b = s.read(1)
        byte = s.read(1)
        y0b = s.read(1)
        y1b = s.read(1)
        byte = s.read(1)
        z0b = s.read(1)
        z1b = s.read(1)
        byte = s.read(1)
        if byte == bytes([25]):
            x0int = int.from_bytes(x0b,byteorder = 'big')-128
            x1int = int.from_bytes(x1b,byteorder = 'big')
            y0int = int.from_bytes(y0b,byteorder = 'big')-128
            y1int = int.from_bytes(y1b,byteorder = 'big')
            z0int = int.from_bytes(z0b,byteorder = 'big')-128
            z1int = int.from_bytes(z1b,byteorder = 'big')
            ax = x0int / 32.0 * 9.8 + x1int / 256 / 32.0 * 9.8
            ay = y0int / 32.0 * 9.8 + y1int / 256 / 32.0 * 9.8
            az = z0int / 32.0 * 9.8 + z1int / 256 / 32.0 * 9.8
            caliAcc.append([ax,ay,az])
            numCali += 1
            if debug:
                print(numCali,':',[ax,ay,az])
        else:
            if debug:
                print('byte check wrong,received',byte)
    print('Calibration Completed. If you change the working environment, please restart the program')
    arrayCaliAcc = np.array(caliAcc)
    axave = arrayCaliAcc[:,0].mean()
    ayave = arrayCaliAcc[:,1].mean()
    azave = arrayCaliAcc[:,2].mean()
    aveCaliAcc=[axave,ayave,azave]
    print('Calibration result:',aveCaliAcc)


    while(True):
        byte = s.read(1)
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
            # print('x0high:%.8f\tx0low:%.8f'%(x0int / 32.0 * 9.8,x1int / 256 / 32.0 * 9.8))
            if (abs(ax)> Thresh):
                pos = win32api.GetCursorPos()
                vx = np.exp((abs(ax) - Thresh) * v)
                if debug:
                    print('vx',vx)
                if debug:
                    print('original pos:',pos)
                if(ax > 0):
                    pos = (np.int(round(pos[0] - vx)), pos[1])
                if(ax < 0):
                    pos = (np.int(round(pos[0] + vx)), pos[1])
                if debug:
                    print('now pos:',pos)
                # if(ay > 0):
                #     pos = (pos[0], pos[1] + v)
                # if(ay < 0):
                #     pos = (pos[0], pos[1] - v)
                win32api.SetCursorPos(pos)
            if (abs(ay)> Thresh):
                pos = win32api.GetCursorPos()
                if debug:
                    print('original pos:',pos)
                # if(ax > 0):
                #     pos = (pos[0] - v, pos[1])
                # if(ax < 0):
                #     pos = (pos[0] + v, pos[1])
                vy = np.exp((abs(ay) - Thresh) * v)
                if debug:
                    print('vy',vy)
                if(ay > 0):
                    pos = (pos[0],np.int(round(pos[1] + vy)))
                if(ay < 0):
                    pos = (pos[0],np.int(round(pos[1] - vy)))
                if debug:
                    print('now pos:',pos)
                win32api.SetCursorPos(pos)
        elif byte == bytes([17]):
            byte == s.read(1)
            if byte == bytes([17]):
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        elif byte == bytes([18]):
            byte == s.read(1)
            if byte == bytes([18]):
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        elif byte == bytes([20]):
            byte == s.read(1)
            if byte == bytes([20]):
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
        elif byte == bytes([21]):
            byte == s.read(1)
            if byte == bytes([21]):
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
