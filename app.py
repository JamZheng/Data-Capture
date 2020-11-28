import os
from flask import Flask
from flask import jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import request
from flask_sqlalchemy import SQLAlchemy
from config import Config
app = Flask(__name__)

#导入数据库配置
app.config.from_object(Config)
db = SQLAlchemy(app)
db.init_app(app)  # 初始化数据库链接

CORS(app, supports_credentials=True)

#数据库类定义
class UDPCnt(db.Model):
    # 定义表名
    __tablename__ = 'UDP流量统计'
    # 定义字段对象
    count = db.Column(db.Integer)
    ip = db.Column(db.String(255),primary_key=True)
    # repr()方法类似于django的__str__，用于打印模型对象时显示的字符串信息
    def __repr__(self):
        return 'UDPcnt:%s %d'% (self.ip, self.count)



@app.route('/cnt/udp', methods=["GET"])
def get_cnt_udp():
    
    data = UDPCnt.query.all()
    return jsonify(data)

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
