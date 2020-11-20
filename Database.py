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
    print('add new')
    db = database
    ip = str(ip)
    protocol = str(protocol)
    cnt = str(cnt)
    cursor = db.cursor()
    print('add new')
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


# test
'''
# 打开数据库连接
db = pymysql.connect("39.108.102.157", "root", "123456",
                     "network", charset='utf8')
# 关闭数据库连接
db.close()
'''