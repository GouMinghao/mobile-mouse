class pid:
    def __init__(self,p,i,d,itime = 10):
        self.p = p
        self.i = i
        self.d = d
        self.itime = itime
    def print(self):
        print(self.itime)
