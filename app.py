import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # 解决跨域的问题
from flask_sqlalchemy import SQLAlchemy
from config import Config, networkSeg
from gethost import getIP
import time
import threading
app = Flask(__name__)

# 连接用户更新间隔时间
updateTime = 20

userIP, userAR = getIP()

# 多线程，持续更新在线列表


def getDevice(t):
    global userIP, userAR
    while True:
        userIP, userAR = getIP()
        print('列表更新')
        time.sleep(t)


# 导入数据库配置
app.config.from_object(Config)
# 建立数据库对象
db = SQLAlchemy(app)
# 初始化数据库链接
db.init_app(app)

CORS(app, supports_credentials=True)

# 数据库类定义


class UDPCnt(db.Model):
    # 定义表名
    __tablename__ = 'UDP流量统计'
    # 定义字段对象
    count = db.Column(db.Integer)
    IP = db.Column(db.String(255), primary_key=True) 
    # 用于打印模型对象时显示的字符串信息

    def __repr__(self):
        return 'UDPcnt:%s %d' % (self.ip, self.count)


class TCPCnt(db.Model):
    __tablename__ = 'TCP流量统计'
    count = db.Column(db.Integer)
    IP = db.Column(db.String(255), primary_key=True)

    def __repr__(self):
        return 'TCPcnt:%s %d' % (self.ip, self.count)


class DirtyWordSet(db.Model):
    __tablename__ = '敏感词词库'
    No = db.Column(db.Integer, primary_key=True)
    敏感词 = db.Column(db.String(255), comment='敏感词')
    时间 = db.Column(db.String(255))

    def __repr__(self):
        return 'Dirty word set:%s' % (self.敏感词)


class DirtyWordInfo(db.Model):
    __tablename__ = '敏感词记录'
    No = db.Column(db.Integer, primary_key=True)
    来源ip = db.Column(db.String(255), comment='来源ip')
    敏感词 = db.Column(db.String(255), comment='敏感词')
    时间 = db.Column(db.String(255), comment='时间')

    def __repr__(self):
        return 'Dirty word record:%s %s %s' % (self.来源ip, self.敏感词, self.时间)

class ConnectedDevice(db.Model):
    __tablename__ = '当前设备'
    No = db.Column(db.Integer, primary_key=True)
    物理地址 = db.Column(db.String(255))
    ip = db.Column(db.String(255))

    def __repr__(self):
        return '设备地址:%s' % (self.物理地址)


# 返回udp流量统计信息
@app.route('/cnt/udp', methods=["GET"])
def get_cnt_udp():
    json = []
    tempdata = []
    for ip in userIP:
        data = UDPCnt.query.filter(UDPCnt.IP == ip).first()
        if data:
            tempdata.append(data.count)
        else:
            tempdata.append(0)
    json = [userIP, tempdata]
    return jsonify(json)

# 返回tcp流量统计信息
@app.route('/cnt/tcp', methods=["GET"])
def get_cnt_tcp():
    json = []
    tempdata = []
    for ip in userIP:
        data = TCPCnt.query.filter(TCPCnt.IP == ip).first()
        if data:
            tempdata.append(data.count)
        else:
            tempdata.append(0) 
    json = [userIP, tempdata]
    return jsonify(json)

# 返回敏感词检测信息


@app.route('/dirtyword', methods=["GET"])
def get_dirtyword_info():
    alldata = DirtyWordInfo.query.all()
    json = []
    tempdata = {}
    for data in alldata:
        if networkSeg in data.来源ip:
            tempdata = {}
            tempdata['dirtyword'] = data.敏感词
            tempdata['sourceip'] = data.来源ip
            tempdata['time'] = data.时间
            json.append(tempdata)
    return jsonify(json)


# 增加敏感词
@app.route('/dirtyword/add/<dw>', methods=["GET"])
def add_dirtyword(dw):
    # 增加：
    article = DirtyWordSet(敏感词=str(dw))
    db.session.add(article)
    db.session.commit()
    return str(dw)


# 获取当前敏感词检测词汇库
@app.route('/dirtyword/get', methods=["GET"])
def get_dirtyword():
    alldata = DirtyWordSet.query.all()
    json = []
    tempdata = {}
    for data in alldata:
        # 这里返回的中文编码有bug
        tempdata['dirtyword'] = data.敏感词
        tempdata['updatetime'] = data.时间
        json.append(tempdata)
        tempdata = {}
    return jsonify(json)


# 返回接入用户信息（本地版）
'''
@app.route('/user_data', methods=["GET"])
def get_user_data():
    data = []
    for i in range(len(userIP)):
        dic = {}
        dic["ip"] = userIP[i]
        dic["address"] = userAR[i]
        data.append(dic)
    return jsonify(data)
'''

# 返回用户接入信息（数据库）
@app.route('/user_data', methods=["GET"])
def get_user_data():
    alldata = ConnectedDevice.query.all()
    json = []
    userIP = []
    userAR = []
    for data in alldata:
        dic = {}
        dic["ip"] = data.ip
        userIP.append(data.ip)
        dic["address"] = data.物理地址
        userAR.append(data.物理地址)
        json.append(dic)
    return jsonify(json)


if __name__ == '__main__':
    #th_get = threading.Thread(target=getDevice, args=(updateTime,))
    #th_get.start()

    app.run(debug=True)
