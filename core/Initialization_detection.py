from scapy.all import *
import socket
import os
import re

class getIPMAC():
    # 获取能够出网的地址
    def getIPv64():
        IPV64ADD = ["获取失败","获取失败"]
        try:
            connecttest4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connecttest4.connect(("cn.aliyun.com", 443))
            IPV64ADD[0] = connecttest4.getsockname()[0]
            connecttest6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            connecttest6.connect(("cn.aliyun.com", 443))
            IPV64ADD[1] = connecttest6.getsockname()[0]
            connecttest4.close()
            connecttest6.close()
        finally:
            return IPV64ADD

    # 出网网卡MAC地址和默认网关路由MAC地址
    def getIPMACAGMAC(IPV4ADD):
        try:
            IPMACAGMAC = ["获取失败","获取失败"]
            # 找出网网卡MAC地址
            IPtext = os.popen("ipconfig /all").read()
            IPposition = IPtext.find(IPV4ADD)
            for i in range(IPposition,-1,-1):
                if IPtext[i] == "-":
                    MACtext = IPtext[i-14:i+3]
                    MACtext = MACtext.replace("-",":")
                    IPMACAGMAC[0] = MACtext
                    break

            # 找网关地址
            GatewayIP = re.search(r'([0-9]{1,3}[.]){3}([0-9]{1,3})',IPtext[IPposition+100:IPposition+500]).group()

            # 找ARP表中网关MAC地址
            ARPtext = os.popen("arp -a").read()
            ARPPosition = ARPtext.find(GatewayIP + " ")
            for i in range(ARPPosition,ARPPosition+40):
                if ARPtext[i] == "-":
                    MACtext = ARPtext[i-2:i+15]
                    MACtext = MACtext.replace("-",":")
                    IPMACAGMAC[1] = MACtext
                    break
            
            # 验证正确性
            if len(IPMACAGMAC[0]) == 17 and len(IPMACAGMAC[1]) == 17:
                for i in IPMACAGMAC:
                    verificationMAC = re.match(r'([0-9a-fA-F]{2}:)*[0-9a-fA-F]{2}',i)
                    if verificationMAC == None:
                        IPMACAGMAC[i] = "获取失败"
            else:
                IPMACAGMAC = ["获取失败","获取失败"]
            
        finally:
            return IPMACAGMAC
        
    def getIPv6():
        IPV64ADD = ["启用的是虚拟环回模式","获取失败"]
        try:
            connecttest6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            connecttest6.connect(("cn.aliyun.com", 443))
            IPV64ADD[1] = connecttest6.getsockname()[0]
            connecttest6.close()
        finally:
            return IPV64ADD
    
    def getIPMACVMOD():
        try:
            IPMACAGMAC = ["获取失败","启用的是虚拟环回模式"]
            # 找出网网卡MAC地址
            IPtext = os.popen("ipconfig /all").read()
            IPposition = IPtext.find("LoopBack_VIP64")
            for i in range(IPposition,len(IPtext)):
                if IPtext[i] == "-":
                    MACtext = IPtext[i-14:i+3]
                    MACtext = MACtext.replace("-",":")
                    IPMACAGMAC[0] = MACtext
                    if len(IPMACAGMAC[0]) == 17:
                        verificationMAC = re.match(r'([0-9a-fA-F]{2}:)*[0-9a-fA-F]{2}',IPMACAGMAC[0])
                        if verificationMAC == None:
                            IPMACAGMAC[0] = "获取失败"
                        else:
                            break
                    else:
                        IPMACAGMAC[0] = "获取失败"
            
            # 验证正确性
        finally:
            return IPMACAGMAC
        
    def getifaceName(IPV4ADD):
        return conf.route.route("0.0.0.0")[0][8:]
        
    def verificationMAC(MAC):
        if len(MAC) == 17:
                verificationMAC = re.match(r'([0-9a-fA-F]{2}:)*[0-9a-fA-F]{2}',MAC)
                if verificationMAC == None:
                    return False
                else:
                    return True
        else:
            return False
