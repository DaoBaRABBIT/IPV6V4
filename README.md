<p><b>使用IPV6广域网搭建虚拟IPV4局域网（Using IPV6 wan to build virtual IPV4 LAN）</b></p>
<p>注意此程序为初期测试阶段---版本0.0.1</p>
<p>若需要使用此程序请遵照下方提示配置环境</p>
<ul>
<li>此程序仅在Windows OS下正常运行 --- 建议OS版本Windows 10</li>
<li>运行语言 --- Python3.7</li>
<li>第三方模块 --- Python-Scapy</li>
<li>Windows底层网络访问接口 --- Winpcap</li>
<li>IPV6 --- 请保持一个可供公网网络访问的IPV6地址</li>
</ul>
<p>此外此程序初期测试版本仅支持客户端为虚拟环回适配器模式进行通讯，请继续遵照下方提示设置</p>
<ul>
<li>充当连接方（客户端）在Windows OS下进入设备管理器
<br>-&#62; 网络适配器
<br>-&#62; 菜单栏操作
<br>-&#62; 添加过时硬件
<br>-&#62; 安装我手动从列表选择的硬件
<br>-&#62; 网络适配器
<br>-&#62; Microsoft
<br>-&#62; Microsoft KM-TEST 环回适配器
<br>-&#62; 安装虚拟环回适配器
</li>
<li>充当群组主机（服务器端）需要关闭硬件校验和在Windows OS下进入设备管理器
<br>-&#62; 网络适配器
<br>-&#62; 寻找主机的实体出网网卡设备名称 例：Realtek PCIe GbE Family Controller
<br>-&#62; 右键进入属性对话框
<br>-&#62; 高级
<br>-&#62; 分别关闭IPV4 硬件校验和、TCP硬件校验和（IPV4）、UDP硬件校验和（IPV4）
</li>
</ul>
<p style="color: red">！！！警告事项！！！</p>
<ul style="color: red">
<li>程序处在非常早期测试拥有许多错误及漏洞</li>
<li>虚拟环回适配器模式下使用程序进行通讯后会暴露充当群组主机（服务器端）的内网环境！！！ 这是危险行为！！！ 使用此程序请核实连接方！！！</li>
<li>程序目前IPV6-TCP通讯暂无加密，请注意通讯内容</li>
</ul>
<p style="color: blue">用途及原理</p>
<ul style="color: blue">
<li>利用IPV6公共地址的获取简易性，来进行点对点的TCP连接，运用TCP来构建隧道，传输IPV4数据包</li>
<li>IPV4数据包将会被完整的封装进IPV6数据包中的数据段中</li>
<li>当IPV6传输完IPV4数据包，IPV4数据包将会被发送至指定网卡</li>
<li>为了达到客户端接入进服务器内网，充当一个虚拟的内网主机的效果，ARP、DHCP、SSDP等数据包都将会被截取并转发至对方</li>
<li>利用此程序能够脱离IPV4公网服务器中介内网穿透等服务，实现纯净的点对点连接，接入服务器方内网，IPV4内网中的局域网通讯局域网设备发现都可以正常使用</li>
</ul>
