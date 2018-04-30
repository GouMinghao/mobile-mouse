import ctypes
lib = ctypes.WinDLL('C:\Mega\Win32Project1.dll') 
lib.plus1('a')
lib.plus1('b')
# print(a)