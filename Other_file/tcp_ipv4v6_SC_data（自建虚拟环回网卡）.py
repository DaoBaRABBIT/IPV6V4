import socket
import threading
from scapy.all import *

'''
此文件程序为核心程序，用于建立IPV6连接以及转发IPV4数据
'''

class socketv4v6:
    #初始化socket套接字
    def __init__(self):
        tcp_sc_socket=socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
        tcp_sc_socket.bind(("",9091))
        self.tcp_sc_socket = tcp_sc_socket
    
    #服务器端设置
    def ipv6client_s(self):
        print("---等待对方IPV6连接---\n")
        self.tcp_sc_socket.listen(8)
        client_socket = self.tcp_sc_socket.accept()
        clientAddr = client_socket[1]
        print("连接方的IP地址为：%s;端口为：%s"%(clientAddr[0],clientAddr[1]))
        client_socket_6 = client_socket[0]
        return client_socket_6

    #客户端设置
    def ipv6client_c(self):
        server_ip = "240e:3b1:b259:6690:39ba:e502:fb00:3797"#input("请输⼊服务器IPV6地址：")
        server_sport = 9091#int(input("请输⼊服务器端口："))
        self.tcp_sc_socket.connect((server_ip,server_sport))
        return self.tcp_sc_socket

class socketv4v6DataInOut(socketv4v6):
    #判断是否启用服务端或客户端
    def __init__(self,SorC): 
        super().__init__()
        if SorC == 0:
            self.tcp_sc_socket = super().ipv6client_s()
        else:
            self.tcp_sc_socket = super().ipv6client_c()

    #接收数据处理
    def SCin(self):
        while True:
            try:
                recv_data = self.tcp_sc_socket.recv(65536) 
                '''
                默认发送缓冲区是65536，设置的那么大是因为这个程序只负责转发数据包，这是完整的数据包结构有地址和各种，所以不能用数据拼接的办法
                第二种情况是数据被分开了，可以拼接
                '''
                recv_data = Ether(eval(recv_data))
                sendp(recv_data,iface="Loop_backIP")
            except SyntaxError:
                print("----------字符出错------------")
            # except Exception as reportError:
            #     print("错误报告：%s；防止继续出错关闭连接自终止程序"%(reportError))
            #     self.tcp_sc_socket.close()
            #     quit()

    #发送数据
    def SCout(self,data):
        self.tcp_sc_socket.send(str(data).encode())

SorC = 1#int(input("请输入0启用服务端，输入1启用客户端："))
Test1 = socketv4v6DataInOut(SorC)

# 启用线程
tSin = threading.Thread(target=Test1.SCin)
tSin.start()

filterstrin = "192.168.110.112"#input("请输入对方的虚拟IPV4地址：")
filterstr = "dst net " + filterstrin
sniff(prn=Test1.SCout,filter=filterstr,iface="Loop_backIP",count=0,timeout=None) 

'''stop_filter=function 返回值若为True则停止嗅探'''