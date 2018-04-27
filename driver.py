# run on python3 windows 10 x86_64
import serial
import sys
if __name__ == '__main__':
    s = serial.Serial(sys.argv[1])
    # s.open()
    while(True):
        # print(sys.argv[1])
        inwait = s.in_waiting
        # print('inwait',inwait)
        if inwait > 100:
            char = s.read(inwait)
            print(char)
            print(type(char))
