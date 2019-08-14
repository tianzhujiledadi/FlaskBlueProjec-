
#cache=Cache()#实例化缓存类
from flask  import  Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect#从flask自带的forms包导入
import pymysql
from  flask_cache  import Cache#从flask自带的缓存模块导入缓存类
pymysql.install_as_MySQLdb()
#惰性加载
csrf=CSRFProtect()
models=SQLAlchemy()
#cache=Cache()#实例化缓存类
def  create_app(config_name):
    #创建app实例
    app=Flask(__name__)
    app.config.from_object("settings.DebugConfig")
    #app惰性加载插件
    #app.run(threaded=True)
    #Flask项目需要小规模的优化只需要将命令配置当中的threaded改为True就可以了
    csrf.init_app(app)#惰性加载
    models.init_app(app)
    #cache.init_app(app)
    #注册蓝图
    from  .main  import  main as  main_blueprint#导入main包下的main蓝图
    from .api import api_main#导入api包下的api_main蓝图
    app.register_blueprint(main_blueprint)#注册蓝图
    app.register_blueprint(api_main)#注册蓝图
    return app









