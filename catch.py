import pyshark
import Database as data
import pymysql
import re
import time 

#流量统计函数，将抓取到的数据包根据UDP以及TCP协议分别进行对应IP的数量统计
def trafficCnt(capture,db):
    #根据协议过滤数据包
    tcp_capture = transportFilter(capture, protocol = 'TCP')
    udp_capture = transportFilter(capture, protocol = 'UDP')
    
    #更新数据库
    #tpc
    src_ip_dic, des_ip_dic = addressCnt(tcp_capture)
    for ip in des_ip_dic.keys():
        data.updateIP(db, ip, des_ip_dic[ip], 'TCP')
        
    for ip in src_ip_dic.keys():
        data.updateIP(db, ip, src_ip_dic[ip], 'TCP')

    #udp
    src_ip_dic, des_ip_dic = addressCnt(udp_capture)
    for ip in des_ip_dic.keys():
        data.updateIP(db, ip, des_ip_dic[ip], 'UDP')
        
    for ip in src_ip_dic.keys():
        data.updateIP(db, ip, src_ip_dic[ip], 'UDP')

    return


# 用于抓取数据包，创建LiveCapture
def capturePackege(time = 0,inter = 'WLAN',filter = ''):
    capture = pyshark.LiveCapture(interface = inter,bpf_filter = filter)
    capture.clear()
    capture.sniff(timeout=time)
    num = len(capture)
    print('packet :',num)
    #cap = pyshark.FileCapture('temp.cap')
    '''
    for packet in capture.sniff_continuously():
        print ('Just arrived:', packet)
    '''
    capture.set_debug()
    return capture


def protocolFilter(capture):
    return 

# 根据数据包来源以及目的地址计算流量
def addressCnt(capture):
    src_ip_dic = {}
    des_ip_dic = {}
    for packet in capture:
        if 'ip' in packet:
            src = str(packet.ip.src)
            dst = str(packet.ip.dst)
            if src_ip_dic.__contains__(src):
                src_ip_dic[src] += 1
            else:
                src_ip_dic[src] = 1
            if des_ip_dic.__contains__(dst):
                des_ip_dic[dst] += 1
            else:
                des_ip_dic[dst] = 1

    return src_ip_dic, des_ip_dic


def testchatData(capture):
    ip = '139.224.42.221'
    for packet in capture:
        if packet.ip.src == ip or packet.ip.dst == ip:
            print(packet)

# 根据传输层协议过滤数据包
def transportFilter(capture, protocol):
    filter = []
    for packet in capture:
        if packet.transport_layer == protocol:
            filter.append(packet)
    return filter

# 获取数据包最高层协议
def gethttp(capture):
    layers = []
    for packege in capture:
        if packege.highest_layer == 'URLENCODED-FORM':
            print(packege)
        #print(packege.http)
    return layers 

# 敏感词检测（待优化
def dirtyWordDetect(db,capture,pattern):
    for packege in capture:
        string = str(packege)
        result = re.findall(pattern, string, flags=0)
        if result:
            # 记录下这个敏感词内容以及来源
            #t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  #获取当前时间(改为直接用数据库的时间戳)
            for dirtyword in result:
                data.dirtyWordRecord(db,packege.ip.src,dirtyword)

    return 

#从数据库取出敏感词列表处理后作为匹配模式
def getDirtyPattern(db):
    pattern = 'shit'
    wordlist = data.getDirtyWordList(db)
    for word in wordlist:
        # 按照或的形式取出
        pattern = pattern + '|' + word[0]
    return pattern


'''
if __name__ == "__main__":
    db = pymysql.connect("39.108.102.157", "", "", "network", charset='utf8' )

    print(getDirtyPattern(db))

    db.close()
'''