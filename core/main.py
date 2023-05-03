from core.main_function import main_function
from tkinter import *

class mianGUI():
    def __init__(self):
        #初始化
        main_window = Tk()
        main_window.title("VVIP64")
        #main_window.geometry("630x900")
        #main_window.resizable(0,0)

        IPV4ADD = StringVar()
        IPV6ADD = StringVar()
        PCMACADD = StringVar()
        PCGMACADD = StringVar()
        
        IPV6ADDCONN = StringVar()
        IPV6ADDCONNP = StringVar()
        IPV6ADDCONNP.set("9091")

        founction = main_function(IPV4ADD,IPV6ADD,PCMACADD,PCGMACADD)

        lightbackground = {'highlightbackground':'#cccccc','highlightcolor':'#cccccc','highlightthickness':'2','bd':'10'} #边框样式

        '''
        #顶部导航栏
        menu = Menu(main_window)
        MenumainSub = Menu(menu,tearoff=0)
        MenumainSub.add_command(label="Test1")
        MenumainSub.add_separator()
        MenumainSub.add_command(label="Test2")
        menu.add_cascade(label="Test",menu=MenumainSub)
        main_window.config(menu=menu)
        '''

        MaxBox_main = Frame(main_window)
        #创建一个子容器
        top_main_window = Frame(MaxBox_main)
        #创建一个“top_main_window”的子容器

        top_top_main_window = Frame(top_main_window,lightbackground,width=605,height=155)
        Label_IPv4add = Label(top_top_main_window,text="本机IPV4地址：").grid(row=0,column=0,sticky="w",pady=5)
        Entry_IPv4add = Entry(top_top_main_window,textvariable=IPV4ADD,width=50).grid(row=0,column=1,sticky="w",pady=5)

        Label_IPv6add = Label(top_top_main_window,text="本机IPV6地址：").grid(row=1,column=0,sticky="w",pady=5)
        Entry_IPv6add = Entry(top_top_main_window,textvariable=IPV6ADD,width=50).grid(row=1,column=1,sticky="w",pady=5)

        Label_MACadd = Label(top_top_main_window,text="物理网卡MAC地址：").grid(row=2,column=0,sticky="w",pady=5)
        Entry_MACadd = Entry(top_top_main_window,textvariable=PCMACADD,width=50).grid(row=2,column=1,sticky="w",pady=5)

        Label_GMACadd = Label(top_top_main_window,text="网关MAC地址：").grid(row=3,column=0,sticky="w",pady=5)
        Entry_GMACadd = Entry(top_top_main_window,textvariable=PCGMACADD,width=50).grid(row=3,column=1,sticky="w",pady=5)

        Button_Reset = Button(top_top_main_window,text="重置/更新地址",command=lambda:founction.Resetip()).grid(row=0,rowspan=4,column=2,padx=10,pady=5)
        top_top_main_window.pack()
        top_top_main_window.grid_propagate(0)
        

        center_top_main_window = Frame(top_main_window,lightbackground,width=605,height=100)
        Label_Change = Label(center_top_main_window,text="创建一个虚拟群组来让其他主机加入").pack(pady=5)
        Button_ChangeS = Button(center_top_main_window,text="创建虚拟群组",width=30,command=lambda:founction.tStartupS())
        Button_ChangeS.pack(pady=5)
        center_top_main_window.pack()
        center_top_main_window.pack_propagate(0)

        bottom_top_main_window = Frame(top_main_window,lightbackground,width=605,height=200)
        # 服务器内容
        s_bottom_top_main_window = Frame(bottom_top_main_window)
        Label_explainPort = Label(s_bottom_top_main_window,text="下方列表为对方连接信息")
        Label_explainPort.grid(row=0,column=0,sticky="w",pady=5)
        Listbox_Frame = Frame(s_bottom_top_main_window)
        Label(Listbox_Frame,text="地址").grid(row=0,column=0,sticky="w")
        Label(Listbox_Frame,text="端口").grid(row=0,column=1,sticky="w")
        Label(Listbox_Frame,text="对方IPV4地址").grid(row=0,column=2,sticky="w")
        Listbox_conninfoIP = Listbox(Listbox_Frame,width=40,height=8)
        Listbox_conninfoIP.grid(row=1,column=0)
        Listbox_conninfoProt = Listbox(Listbox_Frame,width=10,height=8)
        Listbox_conninfoProt.grid(row=1,column=1)
        Listbox_conninfo = Listbox(Listbox_Frame,width=15,height=8)
        Listbox_conninfo.grid(row=1,column=2)
        Listbox_Frame.grid(row=2,column=0)


        # 客户端内容
        c_bottom_top_main_window = Frame(bottom_top_main_window)
        Label_explain = Label(c_bottom_top_main_window,text="加入其他主机创建的虚拟群组").grid(row=0,column=0,sticky="w",pady=5)
        Label_ConnectionI6 = Label(c_bottom_top_main_window,text="输入需要加入的IPV6地址：").grid(row=1,column=0,sticky="w",pady=5)
        Entry_ConnectionI6 = Entry(c_bottom_top_main_window,width=50,textvariable=IPV6ADDCONN).grid(row=1,column=1,sticky="w")
        Label_ConnectionI6Port = Label(c_bottom_top_main_window,text="输入端口号：").grid(row=2,column=0,sticky="w",pady=5)
        Entry_ConnectionI6Port = Entry(c_bottom_top_main_window,textvariable=IPV6ADDCONNP).grid(row=2,column=1,sticky="w",pady=10)
        

        Button_StopI6 = Button(c_bottom_top_main_window,text="断开连接",width=20,height=1,command=lambda: founction.ErrorAStopC())
        Button_ConnectionI6 = Button(c_bottom_top_main_window,text="连接",width=20,height=1,command=lambda: founction.tStartupC(IPV6ADDCONN.get(),IPV6ADDCONNP.get()))
        Button_ConnectionI6.grid(row=3,column=0,pady=5,sticky="w")
        Button_ChangVE = Button(c_bottom_top_main_window,text="虚拟环回模式",width=20,height=1,command=None)
        Button_ChangVE.grid(row=3,column=1,pady=5,sticky="e")
        Label_OtherIPV4 = Label(c_bottom_top_main_window,text="对方主机的IPV4为：")
        Label_OtherIPV4.grid(row=4,column=0,columnspan=2,sticky="w",pady=5)
        c_bottom_top_main_window.pack(anchor="w")

        bottom_top_main_window.pack()
        bottom_top_main_window.pack_propagate(0)

        top_main_window.pack(anchor="w")


        bottom_main_window = Frame(MaxBox_main,lightbackground,width=605,height=265)
        Label_Tips = Label(bottom_main_window,text="提示输出：").grid(row=0,column=0,sticky="w")
        Button_Tips = Button(bottom_main_window,text="清空内容",command=lambda:founction.CleanText()).grid(row=0,column=1,columnspan=3,sticky="e")
        Scrollbar_Tips = Scrollbar(bottom_main_window)
        Scrollbar_Tips.grid(row=1,column=3,sticky="nsew",padx=(2,0),pady=(10,0))
        Text_Tips = Text(bottom_main_window,yscrollcommand=Scrollbar_Tips.set,height=15)
        Text_Tips.grid(row=1,column=0,columnspan=2,pady=(10,0))
        Text_Tips.insert(END,"启动程序\n")
        bottom_main_window.pack()
        bottom_main_window.grid_propagate(0)

        MaxBox_main.pack(padx=10,pady=10)

        founction.setCIpPortState(Listbox_conninfoIP,
                                  Listbox_conninfoProt,
                                  Listbox_conninfo,
                                  Button_StopI6,
                                  Button_ConnectionI6,
                                  Label_OtherIPV4,
                                  s_bottom_top_main_window,
                                  c_bottom_top_main_window,
                                  Button_ChangeS,
                                  Text_Tips,
                                  Label_explainPort)
        

        main_window.mainloop()