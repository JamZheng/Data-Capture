import pyshark
import Database as data
import pymysql

#not done,for test
def trafficCnt(capture,db,number):
    tcp_capture = transportFilter(capture, protocol = 'TCP', number = number)
    udp_capture = transportFilter(capture, protocol = 'UDP', number = number)

    src_ip_dic, des_ip_dic = addressCnt(tcp_capture)
    ips = des_ip_dic.keys()
    for ip in ips:
        data.updateIP(db, ip, des_ip_dic[ip], 'TCP')

    return


def capturePackege(time,inter = 'WLAN'):
    
    capture = pyshark.LiveCapture(interface = inter)
    capture.clear()
    capture.sniff(timeout=time)
    num = len(capture)
    print(num)
    #cap = pyshark.FileCapture('temp.cap')
    '''
    for packet in capture.sniff_continuously():
        print ('Just arrived:', packet)
    '''
    print(capture)
    return capture,num

def protocolFilter(capture):
    return 

def addressCnt(capture,number):
    src_ip_dic = {}
    des_ip_dic = {}
    for i in range(number):
        packet = capture[i]
        if 'ip' in packet:
            print(packet.ip.src)
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

    print(src_ip_dic.items())

    return src_ip_dic, des_ip_dic


def testData(capture,number):
    for i in range(number):
        packet = capture[i]
        if 'http' in packet:
            print(packet.http)

def transportFilter(capture, protocol,number):
    filter = []
    for i in range(number):
        packet = capture[i]
        if packet.transport_layer == protocol:
            filter.append(packet)
    return filter

def getHighestLayer(capture):
    layers = []
    for packege in capture:
       layers.append(packege.highest_layer)
    return layers 

'''
if __name__ == "__main__":
    db = pymysql.connect("39.108.102.157", "root", "123456", "network", charset='utf8' )

    cap = capturePackege(time = 5,inter = 'WLAN')

    trafficCnt(db, cap)
    #关闭数据库

    db.close()
    capture = capturePackege(10)
    tcp_capture = transportFilter(capture, protocol = 'TCP')
    udp_capture = transportFilter(capture, protocol = 'UDP')
'''