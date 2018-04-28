import threading  
def sayhello():
    global t        #Notice: use global variable!
    global a
    print('a=',a)
    a += 1  
    t = threading.Timer(1.0, sayhello)  
    t.start()  
a=0
t = threading.Timer(1.0, sayhello)  
t.start()