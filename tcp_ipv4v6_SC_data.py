from public_modular import *

'''
此文件程序为核心程序，用于建立IPV6连接以及转发IPV4数据
'''

class socketv4v6:
    #初始化socket套接字
    def __init__(self):
        tcp_sc_socket=socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
        self.bindprot = 9091
        while True:
            try:
                tcp_sc_socket.bind(("",self.bindprot))
                break
            except:
                self.bindprot += 1
        self.tcp_sc_socket = tcp_sc_socket
    
    def getPort(self):
        return self.bindprot
    
    #启动服务器端设置
    def ipv6client_s(self,CIp):
        self.tcp_sc_socket.listen(8)
        client_socket = self.tcp_sc_socket.accept()
        clientAddr = client_socket[1]
        if clientAddr[0] != "::1":
            for index,value in enumerate(CIp):
                if value == None:
                    CIp[index] = clientAddr
                    break
            client_socket_6 = client_socket[0]
            return client_socket_6
        else:
            return None
    
    def closeaccept(self):
        closeaccept=socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
        closeaccept.connect(("::1",self.bindprot))
        closeaccept.close()

    #客户端设置
    def ipv6client_c(self,IPinfo):
        self.__init__()
        self.tcp_sc_socket.connect(IPinfo)
        return self.tcp_sc_socket

class socketv4v6DataInOut(socketv4v6):
    #判断是否启用服务端或客户端
    def __init__(self): 
        super().__init__()
        self.stopsniff = False

    def ServerOnline(self,CIp,writeCIp):
        self.tcp_sc = super().ipv6client_s(CIp)
        if self.tcp_sc != None:
            writeCIp()

    def ClientOnline(self,IPinfo):
        print("1")
        self.tcp_sc = super().ipv6client_c(IPinfo)
        print("2")

    #接收数据处理
    def SCin(self):
        while True:
            try:
                recv_data = self.tcp_sc.recv(4096) 
                '''
                默认发送缓冲区是65536
                第二种情况是数据被分开了，可以拼接
                '''
                recv_data = Ether(eval(recv_data))
                sendp(recv_data)
            except SyntaxError:
                print("----------字符出错------------")
            except Exception as reportError:
                 print("错误报告：%s；防止继续出错关闭连接自终止程序"%(reportError))
                 self.stopsniff = True
                 send(IP(src="1.1.1.1",dst="0.0.0.0"))
                 self.tcp_sc.close()
                 break

    #发送数据
    def SCout(self,data):
        try:
            self.tcp_sc.send(str(data).encode())
        finally:
            return self.stopsniff

    def closerecv(self):
        self.stopsniff = True
        send(IP(src="1.1.1.1",dst="0.0.0.0"))
        self.tcp_sc.close()
        return "连接关闭"
    
    