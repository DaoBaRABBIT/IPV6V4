from Initialization_detection import *
from tcp_ipv4v6_SC_data import *

class main_function:
    def __init__(self,IPV4ADD,IPV6ADD,IPV6PORT):
        self.controlSC = 0
        self.CIp = [None]*8
        self.IPV4ADD = IPV4ADD
        self.IPV6ADD = IPV6ADD
        self.IPV6PORT = IPV6PORT
        IPV64ADD = getIPv64()
        IPV4ADD.set(IPV64ADD[0])
        IPV6ADD.set(IPV64ADD[1])
        self.SocketCONN = socketv4v6DataInOut()
        IPV6PORT.set(self.SocketCONN.getPort())

    def setText_Tips(self,Text_Tips):
        self.Text_Tips = Text_Tips

    def setCIpPortState(self,Listbox_conninfoIP,Listbox_conninfoProt,Listbox_conninfo):
        self.Listbox_conninfoIP = Listbox_conninfoIP
        self.Listbox_conninfoProt = Listbox_conninfoProt
        self.Listbox_conninfo = Listbox_conninfo
    
    # 重置本机信息
    def Resetip(self):
        IPV64ADD = getIPv64()
        self.IPV4ADD.set(IPV64ADD[0])
        self.IPV6ADD.set(IPV64ADD[1])
        self.IPV6PORT.set(self.SocketCONN.getPort())

    # 清除提示
    def CleanText(self):
        self.Text_Tips.delete(1.0,END)

    # 有客户端连接后进行的操作
    def writeCIp(self):
        for index,value in enumerate(self.CIp):
            if value != None:
                self.Listbox_conninfoIP.insert(END,self.CIp[index][0])
                self.Listbox_conninfoProt.insert(END,self.CIp[index][1])
                self.Listbox_conninfo.insert(END,"已连接")
        # 开枪接受发送
        self.OpenInAOut()
    
    # 变更为服务器并启动服务
    def ChangeS(self,s_bottom_top_main_window,c_bottom_top_main_window):
        if self.controlSC == 0:
            self.controlSC = 1
            s_bottom_top_main_window.pack(anchor="w")
            c_bottom_top_main_window.forget()
            self.Text_Tips.insert(INSERT,"服务器启动中......\n")
            tlisten = threading.Thread(target=lambda: self.SocketCONN.ServerOnline(self.CIp,self.writeCIp))
            tlisten.start()
            self.Text_Tips.insert(INSERT,"---等待对方IPV6连接---\n")
        
        
    # 变更为客户端
    def ChangeC(self,s_bottom_top_main_window,c_bottom_top_main_window):
        if self.controlSC == 1:
            self.controlSC = 0
            s_bottom_top_main_window.forget()
            c_bottom_top_main_window.pack(anchor="w")
            self.SocketCONN.closeaccept()
            
    
    # 客户端连接开始
    def StartupC(self,IPV6ADDCONN,IPV6ADDCONNP,Button_ConnectionI6,Button_StopI6):
        try:
            IPinfo = (IPV6ADDCONN,int(IPV6ADDCONNP))
            self.Text_Tips.insert(INSERT,"连接服务器中......\n")
            Button_ConnectionI6.configure(state=DISABLED,text="连接中...")
            self.SocketCONN.ClientOnline(IPinfo)
            Button_ConnectionI6.grid_forget()
            Button_StopI6.grid(row=3,column=0,columnspan=2,pady=5)
            self.Text_Tips.insert(INSERT,"连接服务器成功！！！\n")
            self.OpenInAOut()
            # 启用线程
            
        except Exception as reportError:
            self.Text_Tips.insert(INSERT,str(reportError)+"\n")
            Button_ConnectionI6.configure(state=ACTIVE,text="连接")

    # 停止客户端连接
    def ErrorAStopC(self,Button_StopI6,Button_ConnectionI6):
        report = self.SocketCONN.closerecv()
        self.Text_Tips.insert(INSERT,report + "\n")
        Button_StopI6.grid_forget()
        Button_ConnectionI6.configure(state=ACTIVE,text="连接")
        Button_ConnectionI6.grid(row=3,column=0,columnspan=2,pady=5)
    
    def OpenInAOut(self):
            tSin = threading.Thread(target=self.SocketCONN.SCin)
            tSin.start()
            filterstrin = "192.168.110.112"#input("请输入对方的虚拟IPV4地址：")
            filterstr = "(src net 1.1.1.1 and dst net 0.0.0.0) or dst net " + filterstrin
            tsniff = threading.Thread(target=lambda: sniff(stop_filter=self.SocketCONN.SCout,filter=filterstr,count=0,timeout=None))
            tsniff.start()
            '''stop_filter=function 返回值若为True则停止嗅探'''