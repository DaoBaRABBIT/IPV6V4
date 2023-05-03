from scapy.all import *

class DataInSendp():
    def __init__(self,striface):
        self.striface = striface
    def datasend(self,data):
        try:
            data = Ether(eval(data))
            sendp(data,iface = self.striface)
            return 0

        except SyntaxError:
            return 1
        
        except Exception as reportError:
            return 2
            
