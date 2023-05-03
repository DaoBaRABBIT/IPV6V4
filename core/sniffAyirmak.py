from scapy.all import *

class sniffAyirmak():
    def __init__(self,filterstr,striface,socketSC):
        self.socketSC = socketSC
        sniff(stop_filter=self.Outdata,filter=filterstr,count=0,timeout=None,iface=striface)

    def Outdata(self,data):
        #缺加密措施
        self.socketSC.send(str(data).encode("UTF-8"))