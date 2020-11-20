import pyshark
import Database as data
import pymysql

#not done,for test
def trafficCnt(capture,db):
    tcp_capture = transportFilter(capture, protocol = 'TCP')
    udp_capture = transportFilter(capture, protocol = 'UDP')
    
    #tpc
    src_ip_dic, des_ip_dic = addressCnt(tcp_capture)
    for ip in des_ip_dic.keys():
        data.updateIP(db, ip, des_ip_dic[ip], 'TCP')
        
    for ip in src_ip_dic.keys():
        data.updateIP(db, ip, des_ip_dic[ip], 'TCP')

    #udp
    src_ip_dic, des_ip_dic = addressCnt(udp_capture)
    for ip in des_ip_dic.keys():
        data.updateIP(db, ip, des_ip_dic[ip], 'UDP')
        
    for ip in src_ip_dic.keys():
        data.updateIP(db, ip, des_ip_dic[ip], 'UDP')

    return


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
    print(capture)
    return capture

def protocolFilter(capture):
    return 

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


def testData(capture):
    for packet in capture:
        if 'http' in packet:
            print(packet.http)

def transportFilter(capture, protocol):
    filter = []
    for packet in capture:
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