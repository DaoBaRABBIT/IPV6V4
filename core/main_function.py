from core.Initialization_detection import getIPMAC
from core.tcp_ipv4v6_SC_data import *
from tkinter import *
import threading

class main_function:

    def __init__(self,IPV4ADD,IPV6ADD,PCMACADD,PCGMACADD):
        self.controlSC = 0 #0为服务器，1为客户端模式
        self.MOD = 0 #0为虚拟环回地址通讯
        self.ErrorStop = True

        # 地址位置写入
        self.IPV4ADD = IPV4ADD
        self.IPV6ADD = IPV6ADD
        self.PCMACADD = PCMACADD
        self.PCGMACADD = PCGMACADD
        # 初始化写入获取IP和获取MAC地址

    # 存入main控件地址信息
    def setCIpPortState(self,
                        Listbox_conninfoIP,
                        Listbox_conninfoProt,
                        Listbox_conninfo,
                        Button_StopI6,
                        Button_ConnectionI6,
                        Label_OtherIPV4,
                        s_bottom_top_main_window,
                        c_bottom_top_main_window,
                        Button_ChangeS,
                        Text_Tips,
                        Label_explainPort):
        
        self.Listbox_conninfoIP = Listbox_conninfoIP
        self.Listbox_conninfoProt = Listbox_conninfoProt
        self.Listbox_conninfo = Listbox_conninfo
        self.Button_StopI6 = Button_StopI6
        self.Button_ConnectionI6 = Button_ConnectionI6
        self.Label_OtherIPV4 = Label_OtherIPV4
        self.s_bottom_top_main_window = s_bottom_top_main_window
        self.c_bottom_top_main_window = c_bottom_top_main_window
        self.Button_ChangeS = Button_ChangeS
        self.Text_Tips = Text_Tips
        self.Label_explainPort = Label_explainPort

        self.getIPMACset()

    # 写警告提示
    def writeText_Tips(self,Text):
        self.Text_Tips.insert(INSERT,Text+"\n")

    # 获取提示框地址后运行主程序以此来提示
    def getIPMACset(self):
        self.OKorNO = False

        if self.MOD == 0:
            self.IPV64ADD = getIPMAC.getIPv6()
            self.IPMACAGMAC = getIPMAC.getIPMACVMOD() 
        
        if self.MOD == 1:
            self.IPV64ADD = getIPMAC.getIPv64()
            self.IPMACAGMAC = getIPMAC.getIPMACAGMAC(self.IPV64ADD[0]) #0为网卡MAC地址 1为网关MAC地址
            self.ifaceName = getIPMAC.getifaceName(self.IPV64ADD[0])

        self.IPV4ADD.set(self.IPV64ADD[0]) #0为IPV4地址 1为IPV6地址
        self.IPV6ADD.set(self.IPV64ADD[1])
        self.PCMACADD.set(self.IPMACAGMAC[0]) #0为网卡MAC地址 1为网关MAC地址
        self.PCGMACADD.set(self.IPMACAGMAC[1])
        
        if self.IPV64ADD[0] == "获取失败" or self.IPV64ADD[1] == "获取失败":
            self.writeText_Tips("\n！！！！！！！！！！！！！！！！！！！！\n严重错误此软件无法正常运行\n请检查IP地址获取情况\n！！！！！！！！！！！！！！！！！！！！")
            self.OKorNO = False
        elif self.IPMACAGMAC[0] == "获取失败" or self.IPMACAGMAC[1] == "获取失败":
            self.writeText_Tips("\n！！！！！！！！！！！！！！！！！！！！\n严重错误此软件无法正常运行\n请检查MAC地址获取情况\n！！！！！！！！！！！！！！！！！！！！")
            self.OKorNO = False
        else:
           self.writeText_Tips("\n获取信息成功")
           self.OKorNO = True
    
    # 重置本机信息
    def Resetip(self):
        self.getIPMACset()

    # 清除提示
    def CleanText(self):
        self.Text_Tips.delete(1.0,END)

    # 有客户端连接后进行的操作
    def writeCIp(self,AllSocketInformation):
        self.Listbox_conninfoIP.delete(0,END)
        self.Listbox_conninfoProt.delete(0,END)
        self.Listbox_conninfo.delete(0,END)
        for index,value in enumerate(AllSocketInformation):
            if value != None:
                self.Listbox_conninfoIP.insert(END,AllSocketInformation[index][0])
                self.Listbox_conninfoProt.insert(END,AllSocketInformation[index][1])
                self.Listbox_conninfo.insert(END,AllSocketInformation[index][2])
        # 开始接受发送
    
    #-----------------------服务器操作-----------------------

    # 变更为服务器并启动服务
    def tStartupS(self):
        if self.OKorNO:
            if self.controlSC == 0:
                self.controlSC = 1
                self.MOD = 1
                self.getIPMACset()
                self.writeText_Tips("变更为实体网卡通讯模式")
                self.Button_ChangeS.configure(text="解散虚拟群组")
                self.s_bottom_top_main_window.pack(anchor="w")
                self.c_bottom_top_main_window.forget()
                self.writeText_Tips("虚拟群组创建中......")
                threading.Thread(target=self.StartupS).start()
                self.writeText_Tips("等待对方IPV6连接......")   
    # 变更为客户端
            elif self.controlSC == 1:
                self.controlSC = 0
                self.MOD = 0
                self.ErrorAStopS()
                self.getIPMACset()
                self.writeText_Tips("变更回虚拟网卡通讯")
                self.s_bottom_top_main_window.forget()
                self.c_bottom_top_main_window.pack(anchor="w")
                self.writeText_Tips("虚拟群组已解散")
                self.Button_ChangeS.configure(text="创建虚拟群组")
    
    def StartupS(self):
        self.ServerSocketListen = socketv4v6Server(self.IPV64ADD[0])
        self.Label_explainPort.configure(text="下方列表为对方连接信息-启用的监听端口为："+str(self.ServerSocketListen.getPort()))
        AllSocketInformation = self.ServerSocketListen.ListenAccept()
        self.writeCIp(AllSocketInformation)
        otherMACadd = self.ServerSocketListen.CFirstCONN()
        self.writeText_Tips("连接方的MAC地址为："+otherMACadd)

        tServerDataIn = threading.Thread(target=self.ServerSocketListen.ClientDataIn,args=(self.ifaceName,))
        tServerDataIn.start()
        tClientDataOut = threading.Thread(target=self.ServerSocketListen.ServerDataOut,args=(self.ifaceName,))
        tClientDataOut.start()

        tServerDataIn.join() #利用等待线程完成来判断线程是否被强制终止运行

        self.writeCIp(self.ServerSocketListen.AllSocketInformation)

    def ErrorAStopS(self):
        try:
            self.ServerSocketListen.closeServer()
        finally:
            self.Button_StopI6.grid_forget()
            self.Button_ConnectionI6.configure(state=ACTIVE,text="连接")
            self.Button_ChangeS.configure(state=ACTIVE)
            self.Button_ConnectionI6.grid(row=3,column=0,pady=5)

    #-----------------------客户端操作-----------------------

    #启用客户端线程     
    def tStartupC(self,IPV6ADDCONN,IPV6ADDCONNP):
        if self.OKorNO:
            threading.Thread(target=self.StartupC,args=(IPV6ADDCONN,IPV6ADDCONNP)).start()

    # 客户端连接开始
    def StartupC(self,IPV6ADDCONN,IPV6ADDCONNP):
        try:
            IPinfo = (IPV6ADDCONN,int(IPV6ADDCONNP))
            self.writeText_Tips("连接群组中......")
            self.Button_ConnectionI6.configure(state=DISABLED,text="连接中...")
            self.Button_ChangeS.configure(state=DISABLED)       #变更button的display
            self.ClientSocketCONN = socketv4v6Client(IPinfo,self.IPMACAGMAC[0])
            otherIPV4add = self.ClientSocketCONN.FirstCONNS()
            self.Label_OtherIPV4.configure(text=("对方主机的IPV4为："+otherIPV4add))
            tServerDataIn = threading.Thread(target=self.ClientSocketCONN.ServerDataIn,args=("LoopBack_VIP64",))
            tServerDataIn.start()
            tClientDataOut = threading.Thread(target=self.ClientSocketCONN.ClientDataOut,args=("LoopBack_VIP64",))
            tClientDataOut.start()
            # 启用线程

            self.Button_ConnectionI6.grid_forget()
            self.Button_StopI6.grid(row=3,column=0,pady=5)
            self.writeText_Tips("连接群组成功！！！")

            tServerDataIn.join() #利用等待线程完成来判断线程是否被强制终止运行

            if self.ErrorStop:
                self.ErrorAStopC(True)
                self.ErrorStop = True
            
        except Exception as reportError:
            self.writeText_Tips(str(reportError))
            self.Button_ConnectionI6.configure(state=ACTIVE,text="连接")
            self.Button_ChangeS.configure(state=ACTIVE)

    # 停止客户端连接
    def ErrorAStopC(self,Error=False):
        self.ErrorStop = False
        try:
            self.ClientSocketCONN.closeClient()
        finally:
            if Error:
                self.writeText_Tips("连接被强制中断")
            else:
                self.writeText_Tips("连接关闭")
            
            self.Button_StopI6.grid_forget()
            self.Button_ConnectionI6.configure(state=ACTIVE,text="连接")
            self.Button_ChangeS.configure(state=ACTIVE)
            self.Button_ConnectionI6.grid(row=3,column=0,pady=5)