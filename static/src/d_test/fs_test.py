import sys
import psutil
import wmi
import socket
import platform

# reload(sys)
# sys.setencoding('utf-8')

c = wmi.WMI()

# 系统信息
print(u'操作系统名称' + platform.platform()[:-(len(platform.version()) + 1)])
print(u'操作系统版本号' + platform.version())
print(u'操作系统的位数' + platform.architecture()[0])
hostname = socket.getfqdn(socket.gethostname())
ip = socket.gethostbyname(hostname)
print('ip:' + ip)


class get_inp(object):
    # CPU信息
    def get_CPU(self):
        cpumsg = []
        for cpu in c.Win32_Processor():
            tmpmsg = {}
            tmpmsg['Name'] = cpu.Name
            cpumsg.append(tmpmsg)
        
        print(cpumsg)
    
    # 内存信息
    def get_PhysicalMemory(self):
        memorys = []
        for mem in c.Win32_PhysicalMemory():
            tmpmsg = {}
            tmpmsg['Tag'] = mem.Tag
            tmpmsg['ConfiguredClockSpeed'] = str(mem.ConfiguredClockSpeed) + 'MHz'
            memorys.append(tmpmsg)
        
        print(memorys)
    
    # 获取内存 2
    def printPhysicalMemory(self):
        memorys = []
        for mem in c.Win32_PhysicalMemory():
            tmpmsg = {}
            tmpmsg['UUID'] = mem.qualifiers['UUID'][1:-1]
            tmpmsg['BankLabel'] = mem.BankLabel
            tmpmsg['SerialNumber'] = mem.SerialNumber.strip()
            tmpmsg['ConfiguredClockSpeed'] = mem.ConfiguredClockSpeed
            tmpmsg['Capacity'] = mem.Capacity
            tmpmsg['ConfiguredVoltage'] = mem.ConfiguredVoltage
            memorys.append(tmpmsg)
        for m in memorys:
            print(m)
        return memorys
    
    # 获取硬盘
    def printDisk(self):
        disk = []
        for dis in c.Win32_DiskDrive():
            tmpmsg = {}
            tmpmsg['SerialNumber'] = dis.SerialNumber
            tmpmsg['DeviceID'] = dis.DeviceID
            tmpmsg['Caption'] = dis.Caption
            tmpmsg['Size'] = dis.Size
            tmpmsg['UUID'] = dis.qualifiers['UUID'][1:-1]
            disk.append(dis)
        print(disk)
        return disk
    
    # 显卡信息
    def get_video(self):
        videos = []
        for v in c.Win32_VideoController():
            tmpmsg = {}
            tmpmsg['Caption'] = v.Caption
            tmpmsg['AdapterRAM'] = str(abs(v.AdapterRAM) / (1024 ** 3)) + 'G'
            videos.append(tmpmsg)
        
        print(videos)
    
    # 网卡mac地址
    def get_MacAddress(self):
        macs = []
        for n in c.Win32_NetworkAdapter():
            mactmp = n.MACAddress
            if mactmp and len(mactmp.strip()) > 5:
                tmpmsg = {}
                tmpmsg['ProductName'] = n.ProductName
                tmpmsg['NetConnectionID'] = n.NetConnectionID
                tmpmsg['MACAddress'] = n.MACAddress
                macs.append(tmpmsg)
        
        print(macs)
    
    def get_netcard(self):
        """获取网卡名称和ip地址
        """
        netcard_info = []
        info = psutil.net_if_addrs()
        print(info.items())
        for k, v in info.items():
            for item in v:
                if item[0] == 2 and not item[1] == '127.0.0.1':
                    # 去除通过dhcp获取ip方式没获取时分配的的自动专有地址
                    if "169.254." not in item[1]:
                        # netcard_info.append((k, item[1]))
                        netcard_info.append(item[1])
            print("K", k)
        return netcard_info
    
    def main(self):
        # get_CPU()
        # get_PhysicalMemory()
        # printPhysicalMemory()
        # printDisk()
        # get_video()
        # get_MacAddress()
        print(self.get_netcard())


if __name__ == '__main__':
    get_inp().main()
    d = psutil.disk_partitions()
    # print(d)
    print(d[0][0], d[1][0], d[2][0])
    for p in d:
        pi = psutil.disk_usage(p[0])
        # print(type(p), p)
        print(str(p[0]) + ' 总量 :' + str(round(pi[0] / 1024 / 1024 / 1024, 1)) + 'GB')
        print(str(p[0]) + ' 使用量 :' + str(round(pi[1] / 1024 / 1024 / 1024, 1)) + 'GB')
        print(str(p[0]) + ' 空闲 :' + str(round(pi[2] / 1024 / 1024 / 1024, 1)) + 'GB')
        print(str(p[0]) + ' 使用百分百 :' + str(pi[3]) + '%')