import pyshark
import pymysql
import catch
import Database
import time

def main():
    #fill with usename and password
    db = pymysql.connect("39.108.102.157", "", "", "network", charset='utf8' )
    print('database connect ')

    run_t = 180 # time(s)
    begin_t = time.time()
    end_t = begin_t + run_t - 100

    cap = catch.capturePackege(time = 0,inter = 'WLAN',filter = 'tcp||udp')
    while end_t - begin_t < run_t:
        caplist = []
        for packet in cap.sniff_continuously(packet_count = 30):
            caplist.append(packet)

        catch.trafficCnt(caplist, db)
        end_t = time.time()
    
    #关闭数据库
    db.close()
    print('database closed')
    cap.close()
    print("capture closed")
    return 

if __name__ == "__main__":
    main()