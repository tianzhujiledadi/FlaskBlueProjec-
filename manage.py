#-*-coding:utf-8-*-
#manage.py调动main.py
from  app  import  create_app,models#从app包中导入初始化文件中的create_app类,和models类
from  flask_script  import  Manager#manager经理管理人员manager#命令行蓝图
from  flask_migrate  import Migrate#用来同步数据库
from  flask_migrate  import  MigrateCommand#用来同步数据库的命令
from  gevent  import  monkey
monkey.patch_all()#猴子补丁，将之前代码当中所有不契合协程的代码修改为契合
app=create_app("running")#实例化app
manager=Manager(app)#命令行封装app
migrate=Migrate(app,models)#绑定可以管理的数据库模型
manager.add_command("db",MigrateCommand)#加载数据库管理命令#command命令
#Flask+gevent高效部署：当前优化适用于io访问频繁的项目，算法类型不适用
#大型项目按照这个方法解决，有多个APP
@manager.command#command命令
def runserver_gevent():
    from gevent import pywsgi#gevent
    server=pywsgi.WSGIServer(("127.0.0.1",5000),app)
    server.serve_forever()
if __name__ == '__main__':
    #manager.run()#命令行运行
    app.run()#项目运行

