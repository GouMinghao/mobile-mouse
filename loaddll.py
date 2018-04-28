import ctypes
lib = ctypes.WinDLL('C:\Mega\Win32Project1.dll') 
a=lib.plus1('addfdks')
print(a)