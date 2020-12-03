# 用于获取已连接设备的ip地址
# 数据直接返回后端
from __future__ import print_function
import os
import re
import pymysql
import Database as data
import ctypes, sys
import time
#ping 优化


def getIP():
    # 获取arp记录前清除该接口arp缓存(未完成)
    arpall = os.popen("arp -a")
    arpall = arpall.read()
    ips = re.findall(r"192.168.137.{0,4} ", arpall)
    #ips = re.findall(r"192.168.56.{0,4} ", arpall)
    userip = []
    userIP = []
    for ip in ips:
        temp = ip.split('.')
        if temp[3] != '255 ' and temp[3] != '1 ':
            ip = ip.strip()
            userip.append(ip)
    #通过ping测试连接
    for iptest in userip:
        result = os.popen("ping %s" % iptest)
        result = result.read()
        #匹配ping的回复中0%丢失字段
        if re.findall("回复",result):
            userIP.append(iptest)
    AR = re.findall(r"..-..-..-..-..-..", arpall)
    AR = AR[:len(userIP)]
    return userIP,AR


def main():
    db = pymysql.connect("39.108.102.157", "","","network", charset='utf8')
    while True:
        # 打开数据库连接
        iplist = getIP()
        data.clearTable(db,'当前连接设备')
        for i in range(len(iplist)):
            ip = iplist[i]
            data.updateConnected(db,ip,i+1)
        time.sleep(60)
    db.close()        
    return

'''
if __name__ == "__main__":
    main()
'''
