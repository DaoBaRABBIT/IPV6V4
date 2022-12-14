from Initialization_detection import getIPv64
from public_modular import *

'''
此文件程序为核心程序，用于建立IPV6连接以及转发IPV4数据
'''

class socketv4v6:
    #初始化socket套接字
    def __init__(self):
        tcp_sc_socket=socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
        tcp_sc_socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
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
    def ipv6client_s(self,SocketAll):
        self.tcp_sc_socket.listen(8)
        client_socket = self.tcp_sc_socket.accept()
        clientAddr = client_socket[1]
        if clientAddr[0] != "::1":
            for index,value in enumerate(SocketAll):
                if value == None:
                    SocketAll[index] = client_socket
                    return index
            return "full"
        else:
            return None
    
    def closeaccept(self):
        closeaccept=socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
        closeaccept.connect(("::1",self.bindprot))
        closeaccept.close()

    #客户端设置
    def ipv6client_c(self,IPinfo):
        self.tcp_sc_socket.connect(IPinfo)
        return self.tcp_sc_socket

class socketv4v6DataInOut(socketv4v6):
    #判断是否启用服务端或客户端
    def __init__(self,writeCIp,IPMACAGMAC,writeText_Tips,ErrorAStopC):
        super().__init__()
        self.writeCIp = writeCIp
        self.IPMACAGMAC = IPMACAGMAC
        self.writeText_Tips = writeText_Tips
        self.ErrorAStopC = ErrorAStopC
        self.cloC = 0
    # 启用服务器
    def ServerOnline(self,SocketAll,otherIPV4):
        self.tcp_s = SocketAll
        self.stopsniff = [False]*8
        while True:
            tcp_s_index = super().ipv6client_s(SocketAll)
            if tcp_s_index == None:
                break
            elif tcp_s_index == "full":
                continue
            otherIPV4[tcp_s_index] = self.SFirstConn(tcp_s_index)
            threading.Thread(target=self.Sin,args=(tcp_s_index,)).start()
            threading.Thread(target=self.sniffAyirmak,args=(tcp_s_index,otherIPV4[tcp_s_index])).start()
            self.writeCIp()
    
    # 首次连接需互相告知对方本地IPV4地址
    def SFirstConn(self,tcp_s_index):
        recv_data = self.tcp_s[tcp_s_index][0].recv(4096)
        if((recv_data.decode("gbk"))[:31] == "INeedYourIPV4AddressAndMyIPV4Is"):
            IPV4 = getIPv64()[0]
            self.tcp_s[tcp_s_index][0].send(("MyIPV4Is"+IPV4).encode("gbk"))
            return (recv_data.decode("gbk"))[31:]
        
    
    # 捕捉线程函数
    def sniffAyirmak(self,tcp_s_index,otherIPV4):
        dststr = "{0}.{0}.{0}.{0}".format(tcp_s_index)
        filterstr = "(src net 1.1.1.1 and dst net "+ dststr +") or dst net " + otherIPV4
        sniff(stop_filter=lambda data:self.Sout(data,tcp_s_index),filter=filterstr,count=0,timeout=None)
    

    # 启用客户端
    def ClientOnline(self,IPinfo):
        self.IPinfo = IPinfo
        super().__init__() 
        self.stopsniff = False
        self.tcp_c = super().ipv6client_c(IPinfo)
        otherIPV4add = self.CFirstConn()
        threading.Thread(target=self.Cin).start()
        filterstr = "(src net 1.1.1.1 and dst net 0.0.0.0) or dst net " + otherIPV4add
        threading.Thread(target=lambda: sniff(stop_filter=self.Cout,filter=filterstr,count=0,timeout=None)).start()
        return otherIPV4add
        '''stop_filter=function 返回值若为True则停止嗅探'''

    def CFirstConn(self):
        IPV4 = getIPv64()[0]
        self.tcp_c.send(("INeedYourIPV4AddressAndMyIPV4Is"+IPV4).encode("gbk"))
        recv_data = self.tcp_c.recv(4096)
        if((recv_data.decode("gbk"))[:8] == "MyIPV4Is"):
            return (recv_data.decode("gbk"))[8:]


    #接收数据处理
    def Cin(self):
        while True:
            try:
                recv_data = self.tcp_c.recv(65536) 
                '''
                默认发送缓冲区是65536
                '''
                recv_data = Ether(eval(recv_data))
                recv_data[0][0].src = self.IPMACAGMAC[1]
                recv_data[0][0].dst = self.IPMACAGMAC[0]
                sendp(recv_data)
            except SyntaxError:
                print("----------字符出错------------")
                print("----------拼接数据------------")
                while True:
                    try:
                        recv_data += self.tcp_c.recv(65536)
                        recv_data = Ether(eval(recv_data))
                        recv_data[0][0].src = self.IPMACAGMAC[1]
                        recv_data[0][0].dst = self.IPMACAGMAC[0]
                        sendp(recv_data)
                        break
                    except SyntaxError:
                        pass
                    except Exception as reportError:
                        print("133错误报告：%s"%(reportError))
                        self.writeText_Tips("133错误报告：%s"%(reportError))
                        break
                    
            except Exception as reportError:
                 print("138错误报告：%s"%(reportError))
                 self.writeText_Tips("138错误报告：%s"%(reportError))
                 self.stopsniff = True
                 send(IP(src="1.1.1.1",dst="0.0.0.0"))
                 self.tcp_c.close()
                 break

        frequency = 1
        while True:
            if self.cloC == 0:
                if frequency == 6:
                    self.writeText_Tips("尝试重新连接次数过多取消连接")
                    self.ErrorAStopC()
                    break
                else:
                    self.writeText_Tips("尝试重新连接-次数：%s"%frequency)
                    try:
                        self.ClientOnline(self.IPinfo)
                    except Exception as reportError:
                        frequency += 1
                        print("157错误报告：%s"%(reportError))
                        self.writeText_Tips("157错误报告：%s"%(reportError))
            else:
                self.cloC = 0
                break

    #发送数据
    def Cout(self,data):
        try:
            self.tcp_c.send(str(data).encode())
        except Exception as reportError:
            print("167错误报告：%s"%(reportError))
            self.writeText_Tips("168错误报告：%s"%(reportError))
        finally:
            return self.stopsniff

    def Sin(self,tcp_s_index):
        while True:
            try:
                recv_data = self.tcp_s[tcp_s_index][0].recv(65536) 
                '''
                默认发送缓冲区是65536
                '''
                recv_data = Ether(eval(recv_data))
                recv_data[0][0].src = self.IPMACAGMAC[1]
                recv_data[0][0].dst = self.IPMACAGMAC[0]
                sendp(recv_data)
            except SyntaxError:
                print("----------字符出错------------")
                print("----------拼接数据------------")
                while True:
                    try:
                        recv_data += self.tcp_s[tcp_s_index][0].recv(65536)
                        recv_data = Ether(eval(recv_data))
                        recv_data[0][0].src = self.IPMACAGMAC[1]
                        recv_data[0][0].dst = self.IPMACAGMAC[0]
                        sendp(recv_data)
                        break
                    except SyntaxError:
                        pass
                    except Exception as reportError:
                        print("197错误报告：%s"%(reportError))
                        self.writeText_Tips("198错误报告：%s"%(reportError))
                        break
                    
            except Exception as reportError:
                print("202错误报告：%s"%(reportError))
                self.writeText_Tips("202错误报告：%s"%(reportError))
                self.stopsniff[tcp_s_index] = True
                dststr = "{0}.{0}.{0}.{0}".format(tcp_s_index)
                send(IP(src="1.1.1.1",dst=dststr))
                self.tcp_s[tcp_s_index][0].close()
                self.tcp_s[tcp_s_index] = None
                time.sleep(0.5)
                self.stopsniff[tcp_s_index] = False
                self.writeCIp()
                break

    #发送数据
    def Sout(self,data,tcp_s_index):
        try:
            self.tcp_s[tcp_s_index][0].send(str(data).encode())
        except Exception as reportError:
            print("219错误报告：%s"%(reportError))
            self.writeText_Tips("219错误报告：%s"%(reportError))
        finally:
            return self.stopsniff[tcp_s_index]

    def closerecvC(self):
        self.cloC = 1
        self.stopsniff = True
        send(IP(src="1.1.1.1",dst="0.0.0.0"))
        self.tcp_c.close()

    def closerecvS(self):
        if self.tcp_s != None:
            for index,value in enumerate(self.tcp_s):
                if value != None:
                    try:
                        self.tcp_s[index][0].close()
                        self.tcp_sc_socket.close() #关掉服务器监听
                    except Exception as reportError: 
                        print("239错误报告：%s"%(reportError))
                        self.writeText_Tips("239错误报告：%s"%(reportError))
    