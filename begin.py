import pyshark
import pymysql
import catch
import Database


def main():
    #连接云服务器数据库
    db = pymysql.connect("39.108.102.157", "root", "123456", "network", charset='utf8' )
    print('database connect ')
    cap,num = catch.capturePackege(time = 5,inter = 'WLAN')

    catch.trafficCnt(db, cap, num)
    #关闭数据库

    db.close()
    print('database closed')

if __name__ == "__main__":
    main()