import pyshark


def capturePackege(time):

    capture = pyshark.LiveCapture(interface='WLAN', output_file='data.cap')
    capture.sniff(timeout=time)
    '''
    for packet in capture.sniff_continuously():
        print ('Just arrived:', packet)
    '''
    print(capture)
    return capture


def addressCnt(capture):
    src_ip_dic = {}
    des_ip_dic = {}
    for i in range(len(capture)):
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


def testData(capture):
    for i in range(len(capture)):
        packet = capture[i]
        if 'data' in packet:
            print(packet.data)


if __name__ == "__main__":
    capture = capturePackege(10)
    # print(capture[1].ip.src)
    addressCnt(capture)
    # print(len(capture))
    # print(capture[3])
