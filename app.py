import os
from flask import Flask,request,jsonify,render_template
from flask_cors import CORS  # 解决跨域的问题
from flask_sqlalchemy import SQLAlchemy
from config import Config
app = Flask(__name__)

#导入数据库配置
app.config.from_object(Config)
# 建立数据库对象
db = SQLAlchemy(app)
 # 初始化数据库链接
db.init_app(app) 

CORS(app, supports_credentials=True)

#数据库类定义
class UDPCnt(db.Model):
    # 定义表名
    __tablename__ = 'UDP流量统计'
    # 定义字段对象
    count = db.Column(db.Integer)
    ip = db.Column(db.String(255),primary_key=True)
    # 用于打印模型对象时显示的字符串信息
    def __repr__(self):
        return 'UDPcnt:%s %d'% (self.ip, self.count)

class TCPCnt(db.Model):
    __tablename__ = 'TCP流量统计'
    count = db.Column(db.Integer)
    ip = db.Column(db.String(255),primary_key=True)
    def __repr__(self):
        return 'TCPcnt:%s %d'% (self.ip, self.count)

class DirtyWordSet(db.Model):
    __tablename__ = '敏感词词库'
    No = db.Column(db.Integer,primary_key=True)
    敏感词 = db.Column(db.String(255),comment='敏感词')
    时间 = db.Column(db.String(255))
    def __repr__(self):
        return 'Dirty word set:%s'% (self.敏感词)

class DirtyWordInfo(db.Model):
    __tablename__ = '敏感词记录'
    No = db.Column(db.Integer,primary_key=True)
    来源ip = db.Column(db.String(255),comment='来源ip')
    敏感词 = db.Column(db.String(255),comment='敏感词')
    时间 = db.Column(db.String(255),comment='时间')
    def __repr__(self):
        return 'Dirty word record:%s %s %s'% (self.来源ip, self.敏感词, self.时间)

# 返回udp流量统计信息
@app.route('/cnt/udp', methods=["GET"])
def get_cnt_udp():
    alldata = UDPCnt.query.all()
    json = []
    tempdata = {}
    for data in alldata:
        tempdata['ip'] = data.ip
        tempdata['count'] = data.count
        json.append(tempdata)
        tempdata = {}
    return jsonify(json)

# 返回tcp流量统计信息
@app.route('/cnt/tcp', methods=["GET"])
def get_cnt_tcp():
    alldata = TCPCnt.query.all()
    json = []
    tempdata = {}
    for data in alldata:
        tempdata['ip'] = data.ip
        tempdata['count'] = data.count
        json.append(tempdata)
        tempdata = {}
    return jsonify(json)

# 返回敏感词检测信息
@app.route('/dirtyword', methods=["GET"])
def get_dirtyword_info():
    alldata = DirtyWordInfo.query.all()
    json = []
    tempdata = {}
    for data in alldata:
        tempdata['dirtyword'] = data.敏感词
        tempdata['sourceip'] = data.来源ip
        tempdata['time'] = data.时间
        json.append(tempdata)
        tempdata = {}
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


# 返回接入用户信息
@app.route('/user_data', methods=["GET"])
def get_user_data():
    data = [{
          'time': '2020-11-18',
          'username': 'Nuo',
          'ip': '192.168.0.1'
        },
        {
            'time': '2020-11-18',
            'username': 'Nuo',
            'ip': '192.168.0.1'
        },
    ]
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
