networkSeg = '192.168.137'

website = ['chat.vvvip.top','course.xmu.edu.cn','ssfw.xmu.edu.cn']

class Config(object):
    DEBUG = True
    SECRET_KEY = ""
    # 数据库链接配置 = 数据库名称://登录账号:登录密码@数据库主机IP:数据库访问端口/数据库名称?charset=编码类型
    SQLALCHEMY_DATABASE_URI = "mysql://root:@49.234.108.161:3306/network?charset=utf8"
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True