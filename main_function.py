from Initialization_detection import *
from tcp_ipv4v6_SC_data import *

class main_function:
    def __init__(self,IPV4ADD,IPV6ADD,IPV6PORT):
        self.controlSC = 0
        self.SocketAll = [None]*8
        self.otherIPV4 = [None]*8

        # 地址写入位置
        self.IPV4ADD = IPV4ADD
        self.IPV6ADD = IPV6ADD
        self.IPV6PORT = IPV6PORT

        # 初始化写入获取IP和获取MAC地址
        
    # 获取提示框地址后运行主程序以此来提示
    def setText_Tips(self,Text_Tips):
        self.Text_Tips = Text_Tips

        IPV64ADD = getIPv64()
        self.IPV4ADD.set(IPV64ADD[0]) #0为IPV4地址 1为IPV6地址
        self.IPV6ADD.set(IPV64ADD[1])
        
        IPMACAGMAC = getIPMACAGMAC(IPV64ADD[0]) #0为网卡MAC地址 1为网关MAC地址
        
        if IPV64ADD[0] == "获取失败" or IPV64ADD[1] == "获取失败":
            self.writeText_Tips("\n！！！！！！！！！！！！！！！！！！！！\n\n严重错误此软件无法正常运行\n请检查IP地址获取情况\n\n！！！！！！！！！！！！！！！！！！！！")
            self.SocketCONN = None
        else:
            if IPMACAGMAC == None :
                self.writeText_Tips("\n！！！！！！！！！！！！！！！！！！！！\n\n严重错误此软件无法正常运行\n请检查MAC地址获取情况\n\n！！！！！！！！！！！！！！！！！！！！")
                self.SocketCONN = None
            else:
                self.SocketCONN = socketv4v6DataInOut(self.writeCIp,IPMACAGMAC,self.writeText_Tips,self.ErrorAStopC)
                self.IPV6PORT.set(self.SocketCONN.getPort())
    
    # 写警告提示
    def writeText_Tips(self,Text):
        self.Text_Tips.insert(INSERT,Text+"\n")

    # 存接入客户端的信息
    def setCIpPortState(self,Listbox_conninfoIP,Listbox_conninfoProt,Listbox_conninfo,Button_StopI6,Button_ConnectionI6):
        self.Listbox_conninfoIP = Listbox_conninfoIP
        self.Listbox_conninfoProt = Listbox_conninfoProt
        self.Listbox_conninfo = Listbox_conninfo
        self.Button_StopI6 = Button_StopI6
        self.Button_ConnectionI6 = Button_ConnectionI6
    
    # 重置本机信息
    def Resetip(self):
        if self.SocketCONN != None:
            IPV64ADD = getIPv64()
            self.IPV4ADD.set(IPV64ADD[0])
            self.IPV6ADD.set(IPV64ADD[1])
            self.IPV6PORT.set(self.SocketCONN.getPort())

    # 清除提示
    def CleanText(self):
        self.Text_Tips.delete(1.0,END)

    # 有客户端连接后进行的操作
    def writeCIp(self):
        self.Listbox_conninfoIP.delete(0,END)
        self.Listbox_conninfoProt.delete(0,END)
        self.Listbox_conninfo.delete(0,END)
        for index,value in enumerate(self.SocketAll):
            if value != None:
                self.Listbox_conninfoIP.insert(END,self.SocketAll[index][1][0])
                self.Listbox_conninfoProt.insert(END,self.SocketAll[index][1][1])
                self.Listbox_conninfo.insert(END,self.otherIPV4[index])
        # 开始接受发送
    
    # 变更为服务器并启动服务
    def ChangeS(self,s_bottom_top_main_window,c_bottom_top_main_window):
        if self.SocketCONN != None:
            if self.controlSC == 0:
                self.controlSC = 1
                s_bottom_top_main_window.pack(anchor="w")
                c_bottom_top_main_window.forget()
                self.writeText_Tips("服务器启动中......")
                tlisten = threading.Thread(target=lambda: self.SocketCONN.ServerOnline(self.SocketAll,self.otherIPV4))
                tlisten.start()
                self.writeText_Tips("等待对方IPV6连接......")
        
        
    # 变更为客户端
    def ChangeC(self,s_bottom_top_main_window,c_bottom_top_main_window):
        if self.SocketCONN != None:
            if self.controlSC == 1:
                self.controlSC = 0
                s_bottom_top_main_window.forget()
                c_bottom_top_main_window.pack(anchor="w")
                self.writeText_Tips("关闭服务器......")
                self.SocketCONN.closeaccept()
                self.SocketCONN.closerecvS()
            
    def tStartupC(self,IPV6ADDCONN,IPV6ADDCONNP,Label_OtherIPV4):
        if self.SocketCONN != None:
            threading.Thread(target=self.StartupC,args=(IPV6ADDCONN,IPV6ADDCONNP,Label_OtherIPV4)).start()

    # 客户端连接开始
    def StartupC(self,IPV6ADDCONN,IPV6ADDCONNP,Label_OtherIPV4):
        try:
            IPinfo = (IPV6ADDCONN,int(IPV6ADDCONNP))
            self.writeText_Tips("连接服务器中......")
            self.Button_ConnectionI6.configure(state=DISABLED,text="连接中...")
            otherIPV4add = self.SocketCONN.ClientOnline(IPinfo)
            Label_OtherIPV4.configure(text=("对方主机的IPV4为："+otherIPV4add))
            self.Button_ConnectionI6.grid_forget()
            self.Button_StopI6.grid(row=3,column=0,columnspan=2,pady=5)
            self.writeText_Tips("连接服务器成功！！！")
            # 启用线程
            
        except Exception as reportError:
            self.writeText_Tips(str(reportError))
            self.Button_ConnectionI6.configure(state=ACTIVE,text="连接")

    # 停止客户端连接
    def ErrorAStopC(self):
        try:
            self.SocketCONN.closerecvC()
        finally:
            self.writeText_Tips("连接关闭")
            self.Button_StopI6.grid_forget()
            self.Button_ConnectionI6.configure(state=ACTIVE,text="连接")
            self.Button_ConnectionI6.grid(row=3,column=0,columnspan=2,pady=5)