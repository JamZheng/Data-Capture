import pyshark
import pymysql
import catch
import Database
import time
import os

def main():
    #fill with usename and password
    db = pymysql.connect("39.108.102.157", "", "", "network", charset='utf8' )
    print('database connect ')
    # 总共运行时间
    run_t = 600 # time(s)
    begin_t = time.time()
    end_t = begin_t + run_t - 100
    # 设置抓包的接口以及过滤方式，这里嗅探时间设为0
    cap = catch.capturePackege(time = 0,inter = '本地连接* 1',filter = 'tcp||udp')
    cap.set_debug()
    # 获取自定义的敏感词匹配模式
    pattern = catch.getDirtyPattern(db)

    print(pattern)
    while end_t - begin_t < run_t:
        caplist = []
        for packet in cap.sniff_continuously(packet_count = 50):
            caplist.append(packet)

        # 将上面的包进行流量统计
        catch.trafficCnt(caplist, db)

        # 敏感词检测
        catch.dirtyWordDetect(db,caplist,pattern)
        
        #catch.gethttp(caplist)

        # 聊天室测试
        catch.testchatData(caplist)

        # 当前时间
        end_t = time.time()
        # 输出已运行时间  
        print(end_t - begin_t)
    
    #关闭数据库
    db.close()
    print('database closed')

    # 关闭LiveCapture
    cap.close()
    print("capture closed")
    
    return 

if __name__ == "__main__":
    main()