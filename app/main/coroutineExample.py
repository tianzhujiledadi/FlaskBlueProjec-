#-*-coding:utf-8-*-
"""
协程
"""
#生成器
# def  hello():
#     for  i in  (1,10):
#         key=yield i
#         print(key)
#         print("hello  world",i)
# h=hello()#生成器
# print(next(h))
# #send方法
# print(h.send(1))#第一次不能用send
#send一般用于两个函数及以上,在实际工作中，协程至少需要两个函数

def  getContent():#获取内容方法
    while True:
        url=yield "I HAVA  CONTENT"
        print("get  content from url:%s"%url)
def  getUrl(g):
    url_list=["url1","url2","url3"]
    for i in url_list:
        print("#######################################")
        g.send(i)#发送url，URL2,URL3到url=yield.......输出("get  content from url:%s"%url)
        print("#######################################")
if __name__ == '__main__':
    g=getContent()
    print(next(g))#输出("get  content from url:%s"%url)
    getUrl(g)#给函数传递参数
def getContent():#获取内容方法
    while  True:
        url=yield  "I hava  content"
        print("get content from url%s"%url)
def getUrl(g):
    url_list=["url1","url2","url3"]
    for i in url_list:
        print("+++++++++++++++++++++++++++++++++++++++")
        g.send(i)
        print("#######################################")
if __name__ == '__main__':
    g=getContent()
    print(next(g))#
    getUrl(g)#给函数传递参数

import  gevent#导入协程#gevent框架实现协程
from gevent.lock  import Semaphore#semaphore打旗语，发信号
#lock锁，锁上,lock
sem=Semaphore(1)
def  fun1():
    for i in range(5):
        sem.acquire()#acquire获得取得
        print("I am fun 1 this is %s"%i)
        gevent.sleep(1)
        sem.release()#release释放，发射；release释放，发射；
def fun2():
    for i in range(5):
        sem.acquire()
        print("I am fun 2 this is %s"%i)
        gevent.sleep(1)
        sem.release()
t1=gevent.spawn(fun1)#spawn大量生产，造成
t2=gevent.spawn(fun2)
gevent.joinall([t1,t2])
# #协程能解决IO I input  O output
