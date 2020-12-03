# 数据库操作文件
import pymysql



'''
flag = 0 添加新的ip流量信息
flag = 1 更新已存在的ip流量
'''
def updateIP(database, ip, cnt, protocol):
    db = database
    ip = str(ip)
    protocol = str(protocol)
    cnt = str(cnt)
    cursor = db.cursor()

    sql = "SELECT COUNT(*) FROM %s流量统计 WHERE IP = '%s';" % (protocol, ip)
    try:
        cursor.execute(sql)
        flag = cursor.fetchall()
    except:
        print("error when select count")
    flag = str(flag)
    if flag == '((0,),)':
        addNewIP(database, ip, cnt, protocol)
    else:
        addOldip(database, ip, cnt, protocol)


def addNewIP(database, ip, cnt, protocol):
    db = database
    ip = str(ip)
    protocol = str(protocol)
    cnt = str(cnt)
    cursor = db.cursor()
    if protocol == 'UDP':
        sql = "INSERT INTO UDP流量统计(IP,count) VALUES ('%s', %s)" % (ip, cnt)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    if protocol == 'TCP':
        sql = "INSERT INTO TCP流量统计(IP,count) VALUES ('%s', %s)" % (ip, cnt)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

    return


def addOldip(database, ip, cnt, protocol):
    db = database
    ip = str(ip)
    protocol = str(protocol)
    cnt = str(cnt)
    cursor = db.cursor()

    if protocol == 'UDP':
        sql = "UPDATE UDP流量统计 SET count = count + %s WHERE ip = '%s'" % (cnt, ip)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    if protocol == 'TCP':
        sql = "UPDATE TCP流量统计 SET count = count + %s WHERE ip = '%s'" % (cnt, ip)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

    return

def dirtyWordRecord(database, ip, dirtyword):
    print('dirty word!')
    db = database
    ip = str(ip)
    dw = str(dirtyword)
    cursor = db.cursor()

    sql = "INSERT INTO 敏感词记录(来源ip,敏感词) VALUES ('%s', '%s')" % (ip, dw)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    return

def getDirtyWordList(database):
    db = database
    cursor = db.cursor()

    sql = "SELECT 敏感词 FROM 敏感词词库"
    try:
        cursor.execute(sql)
        dirtywordlist = cursor.fetchall()
    except:
        print("error when get list")
    
    return dirtywordlist

def clearTable(database,tablename):
    db = database
    cursor = db.cursor()

    sql = "truncate table %s;" % tablename
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    return


def updateConnected(database,ip,number):
    db = database
    ip = str(ip)
    number = str(number)
    cursor = db.cursor()

    sql = "INSERT INTO 当前设备(No,ip) VALUES (%s,'%s')" % (number, ip)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    return

# test
'''
# 打开数据库连接
db = pymysql.connect("39.108.102.157", "", "",
                     "network", charset='utf8')
# 关闭数据库连接
db.close()
'''