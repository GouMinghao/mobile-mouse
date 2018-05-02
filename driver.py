# run on python3 windows 10 x86_64
# this version can be run using the driver_g apk
import serial
import sys
import win32api
import win32con
import numpy as np
import time


# Kalman Filter
# input the newdata(data)
# the previous data(predata)
# the variance last time(var)
# constant Q and constant R
# returns the outputData, the variance
def kalmanFilter(data,preData,var,Q,R):
    preVar = var + Q
    K = preVar / (preVar + Q)
    outputData = preData + K * (data - preData)
    var = (1- K) * preVar
    preData = outputData
    return (outputData,var)

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def rightClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)

if __name__ == '__main__':
    # Set debug = True to print some information needed for debugging
    debug = False
    s = serial.Serial(sys.argv[1])
    # command line input should be as the following format
    # python driver.py [serial port number] [cursor move speed] [threshhold for moving] [damp rate] [Q] [R]
    # ------------- Windows -----------------
    # for windows user, one example is:
    # python driver.py COM3 20 0.4 0.8 0.1 0.25
    # it means the driver will use COM3 serial port, the moving speed is 20, the smallest acceleration for moving cursor is 0.4(m/s^2)
    # the damp rate is 0.8, Q = 0.1 and R = 0.25
    # it's OK just to give the first few parameter and the following is set the default value
    # ------------- Linux -------------------
    # for linux user, one example is:
    # python driver.py /tty/... 1 3
    # it means the driver will use COM3 serial port, the moving speed is and the smallest acceleration for moving cursor is 3(m/s^2)
    # however, linux is not supportted now because of mouse api problem
    if len(sys.argv) >= 3:
        v = int(sys.argv[2])
    else:
        v = 20
    if len(sys.argv) >= 4:
        Thresh = float(sys.argv[3])
    else:
        Thresh = 0.4
    if len(sys.argv) >= 5:
        dampRate = float(sys.argv[4])
    else:
        dampRate = 0.8

    # initialization for kalman filter
    preData = 0
    var = 0
    if len(sys.argv) >= 6:
        Q = sys.argv[5]
    else:
        Q = 0.1
    if len(sys.argv) >= 7:
        R = sys.argv[6]
    else:
        R = 0.25

    xPreData = 0
    yPreData = 0
    xVar = 0
    yVar = 0

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
        y0b = s.read(1)
        x0int = int.from_bytes(x0b,byteorder = 'big')-128
        y0int = int.from_bytes(y0b,byteorder = 'big')-128
        ax = x0int / 32.0 * 9.8
        ay = y0int / 32.0 * 9.8
        caliAcc.append([ax,ay])
        numCali += 1
        if debug:
            print(numCali,':',[ax,ay])
        else:
            if debug:
                print('byte check wrong,received',byte)
    print('Calibration Completed. If you change the working environment, please restart the program')
    arrayCaliAcc = np.array(caliAcc)
    axave = arrayCaliAcc[:,0].mean()
    ayave = arrayCaliAcc[:,1].mean()

    print('Calibration result:',axave,ayave)
    t2 = time.clock()
    print('Time:',t2 - t1,'seconds')
    print('It is now available to use your mobile phone to control the cursor')
    # the list to store the recent acceleration data
    alist = []
    # set the initial speed of the cursor to zero
    vx = 0
    vy = 0
    t0 = 1
    t1 = 0
    while(True):
        if debug:
            t0 = time.time()
            if t0 - t1 > 0:
                print('frequency:',1/(t0 - t1))
            t1 = time.time()
        byte = s.read(1)
        if byte == bytes([22]):
            x0b = s.read(1)
            y0b = s.read(1)
            x0int = int.from_bytes(x0b,byteorder = 'big')-128
            y0int = int.from_bytes(y0b,byteorder = 'big')-128
            # decode the acceleration data and calibrate it using the data in the calibration step
            ax = x0int / 32.0 * 9.8 - axave
            ay = y0int / 32.0 * 9.8 - ayave
            ax, xVar = kalmanFilter(ax,xPreData,xVar,Q,R)
            ay, yVar = kalmanFilter(ay,yPreData,yVar,Q,R)
            # damp the speed
            vx = vx * dampRate
            vy = vy * dampRate
            if debug:
                print('vx:%.4f\t vy:%.4f' %(vx,vy))

            # change the speed if the acceleration exceed the threshhold
            if (abs(ax) > Thresh):
                dvx = np.exp(-abs(vx)) * ax * v
                vx = vx + dvx
                # if debug:
                #     print('dvx:',dvx)
                #     print('vx:',vx)
            if (abs(ay) > Thresh):
                dvy = np.exp(-abs(vy)) * ay * v
                vy = vy + dvy
                # if debug:
                #     print('dvy:',dvy)
                #     print('vy:',vy)
            
            # update the position of the cursor
            pos = win32api.GetCursorPos()
            pos = (np.int(round(pos[0] + vx)),np.int(round(pos[1] - vy)))
            win32api.SetCursorPos(pos)

        # deal with click
        elif byte == bytes([17]):
            if debug:
                print('left down')
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        elif byte == bytes([18]):
            if debug:
                print('left up')
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        elif byte == bytes([20]):
            if debug:
                print('right down')
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
        elif byte == bytes([21]):
            if debug:
                print('right up')
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)