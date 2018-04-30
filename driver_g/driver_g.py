# run on python3 windows 10 x86_64
import serial
import sys
import win32api
import win32con
import numpy as np
import time

# the function is used in control strategy
def reverseSigmoid(x):
    return (np.exp(-x))/(1 + np.exp(-x))

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def rightClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)

if __name__ == '__main__':
    # Set debug = True to print some information needed for debugging
    debug = True
    s = serial.Serial(sys.argv[1])
    # command line input should be as the following format
    # python driver_g.py [serial port number] [cursor move speed] [threshhold for moving]
    # ------------- Windows -----------------
    # for windows user, one example is:
    # python driver_g.py COM3 1 3
    # it means the driver will use COM3 serial port, the moving speed is and the smallest acceleration for moving cursor is 3(m/s^2)
    # ------------- Linux -------------------
    # for linux user, one example is:
    # python driver_g.py COM3 1 3
    # it means the driver will use COM3 serial port, the moving speed is and the smallest acceleration for moving cursor is 3(m/s^2)
    # however, linux is not supportted now because of mouse api problem
    if len(sys.argv) >= 3:
        v = int(sys.argv[2])
    else:
        v = 1
    if len(sys.argv) >= 4:
        Thresh = int(sys.argv[3])
    else:
        Thresh = 3
    print('Begin to calibrate, please put the mobile phone on the surface and do not move')
    t1 = time.clock()
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

    print('Calibration result:',axave,ayave,azave)
    t2 = time.clock()
    print('Time:',t2 - t1,'seconds')
    # the list to store the recent acceleration data
    alist = []

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
            # decode the acceleration data and calibrate it using the data in the calibration step
            ax = x0int / 32.0 * 9.8 + x1int / 256 / 32.0 * 9.8 - axave
            ay = y0int / 32.0 * 9.8 + y1int / 256 / 32.0 * 9.8 - ayave
            az = z0int / 32.0 * 9.8 + z1int / 256 / 32.0 * 9.8 - azave
            if (abs(ax)> Thresh):
                pos = win32api.GetCursorPos() # The cursor posotion now
                vx = np.exp((abs(ax) - Thresh) * v)
                if debug:
                    print('vx',vx)
                if debug:
                    print('original pos:',pos)
                # update the position
                if(ax > 0):
                    pos = (np.int(round(pos[0] - vx)), pos[1])
                if(ax < 0):
                    pos = (np.int(round(pos[0] + vx)), pos[1])
                if debug:
                    print('now pos:',pos)
                # move the cursor
                win32api.SetCursorPos(pos)
            if (abs(ay)> Thresh):
                pos = win32api.GetCursorPos()
                # the cursor position now
                if debug:
                    print('original pos:',pos)
                # the moving speed, we using exp function
                vy = np.exp((abs(ay) - Thresh) * v)
                if debug:
                    print('vy',vy)
                if(ay > 0):
                    pos = (pos[0],np.int(round(pos[1] + vy)))
                if(ay < 0):
                    pos = (pos[0],np.int(round(pos[1] - vy)))
                if debug:
                    print('now pos:',pos)
                # update cursor position
                win32api.SetCursorPos(pos)



        # deal with click
        elif byte == bytes([17]):
            byte == s.read(1)
            # double check in case that it is the acceleration data byte
            # although we do the check, there is still a little chance to have something wrong
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
