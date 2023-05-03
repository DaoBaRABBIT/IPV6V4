'''
此文件程序为核心程序，用于建立IPV6连接以及转发IPV4数据
'''
from core.DataInSendp import DataInSendp
from core.sniffAyirmak import sniffAyirmak
import socket

class socketv4v6:
    #初始化socket套接字
    def __init__(self):
        self.tcp_sc_socket=socket.socket(socket.AF_INET6,socket.SOCK_STREAM)  
        #tcp_sc_socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1) #启用nagle算法，延迟等待数据包合并发送以减少数据包
        self.bindprot = 9091
        while True:
            try:
                self.tcp_sc_socket.bind(("",self.bindprot))
                break
            except:
                self.bindprot += 1
    
    def getPort(self):
        return self.bindprot
    

class socketv4v6Server(socketv4v6):
    def __init__(self,IPV4ADD):
        super().__init__()
        self.IPV4ADD = IPV4ADD

        self._Allsocket = [None]*4  #最大记录4个连接套接字
        self.AllSocketInformation = [[None,None,None]]*4  #记录4个连接记录

    #服务器监听
    def ListenAccept(self):
        self.tcp_sc_socket.listen(4)
        self.server_socket = self.tcp_sc_socket.accept()
        self.serverAddr = self.server_socket[1]
        self.server_socket_IPV6 = self.server_socket[0]

        self.AllSocketInformation[0] = list(self.serverAddr) + [None]

        return self.AllSocketInformation
    
    #服务器核验校对
    def CFirstCONN(self):
        self.server_socket_IPV6.send(("INeedYourMACAddressAndMyIPV4Is"+self.IPV4ADD).encode("UTF-8"))
        recv_data = self.server_socket_IPV6.recv(4096)
        recv_data = recv_data.decode("UTF-8")
        if(recv_data[:7] == "MyMACIs"):
            # 缺验证MAC格式
            self.CMACadd = recv_data[7:]
            self.server_socket_IPV6.send(("VVIP64start").encode("UTF-8"))
            return self.CMACadd
    
    #服务器数据包抓取输出
    def ServerDataOut(self,iface):
        sniffAyirmak("ether dst host "+ self.CMACadd +" or (not ether src host "+ self.CMACadd +" and ether dst host ff:ff:ff:ff:ff:ff)",
                     iface,self.server_socket_IPV6)
    
    #客户端数据包接收转发
    def ClientDataIn(self,striface):
        DataInSendpsl = DataInSendp(striface)
        try:
            while True:
                recv_data = self.server_socket_IPV6.recv(65535)
                while True:
                    report = DataInSendpsl.datasend(recv_data.decode("UTF-8"))
                    if(report == 0):
                        break

                    if(report == 1):
                        print("----------字符出错------------")
                        print("----------拼接数据------------")
                        recv_data += self.server_socket_IPV6.recv(65535)
                    
                    if(report == 2):
                        #缺多次数据包处理错误直接断开连接，并汇报错误
                        pass
        except:
            self._Allsocket[0] = [None]  #最大记录4个连接套接字
            self.AllSocketInformation[0] = [None,None,None]
    

    def closeServer(self):
        try:
            self.tcp_sc_socket.close()

            self.Allsocket = [None]*4  #最大记录4个连接套接字
            self.AllSocketInformation = [[None,None,None]]*4  #记录4个连接记录
            
        except:
            pass


class socketv4v6Client(socketv4v6):
    def __init__(self,IPinfo,PCMACADD):
        super().__init__()
        self.PCMACADD = PCMACADD
        self.tcp_sc_socket.connect(IPinfo)

    #客户端核验校对
    def FirstCONNS(self):
        recv_data = self.tcp_sc_socket.recv(4096)
        recv_data = recv_data.decode("UTF-8")
        if(recv_data[:30] == "INeedYourMACAddressAndMyIPV4Is"):
            # 缺验证IPV4地址格式
            SIPV4add = recv_data[30:]
            self.tcp_sc_socket.send(("MyMACIs"+self.PCMACADD).encode("UTF-8"))
        recv_data = self.tcp_sc_socket.recv(4096)
        recv_data = recv_data.decode("UTF-8")
        if(recv_data == "VVIP64start"):
            return SIPV4add
    
    #客户端数据包抓取输出
    def ClientDataOut(self,LoopbackORno):
        sniffAyirmak("ether src host "+self.PCMACADD,LoopbackORno,
                     self.tcp_sc_socket)
    
    #服务器数据包接收转发
    def ServerDataIn(self,striface):
        DataInSendpsl = DataInSendp(striface)
        while True:
            recv_data = self.tcp_sc_socket.recv(65535)
            while True:
                report = DataInSendpsl.datasend(recv_data.decode("UTF-8"))
                if(report == 0):
                    break

                if(report == 1):
                    print("----------字符出错------------")
                    print("----------拼接数据------------")
                    recv_data += self.tcp_sc_socket.recv(65535)
                
                if(report == 2):
                    #缺多次数据包处理错误直接断开连接，并汇报错误
                    pass
    
    def closeClient(self):
        try:
            self.tcp_sc_socket.close()
        except:
            pass
