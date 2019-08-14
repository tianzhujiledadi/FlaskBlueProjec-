#-*-coding:utf-8-*-
import os
BASE_DIR=os.path.abspath(os.path.dirname(__file__))
class  BaseConfig(object):
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SECRET_KEY="123456"#用来生成session_id和之后的csrf_token
    CACHE_TYPE="simple"#simple轻量级的#缓存类型是轻量级的
class  DebugConfig(BaseConfig):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "Student.sqlite")
    #SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:root@localhost/schools"
class OnlineConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/school"
