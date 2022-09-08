from public_modular import *

def getIPv64():
    IPV64ADD = ["获取失败","获取失败"]
    try:
        connecttest4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connecttest4.connect(("cn.aliyun.com", 443))
        IPV64ADD[0] = connecttest4.getsockname()[0]
        connecttest6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        connecttest6.connect(("cn.aliyun.com", 443))
        IPV64ADD[1] = connecttest6.getsockname()[0]
    finally:
        connecttest4.close()
        connecttest6.close()
        return IPV64ADD