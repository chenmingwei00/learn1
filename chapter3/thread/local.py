import threading

mydata=threading.local()
mydata.number=50
print(mydata.number)


log=[]

def f():
    mydata.number=30
    log.append(mydata.number)

thread=threading.Thread(target=f)
thread.start()

thread.join()
print(log)
print(mydata.number)

"""本地线程希望不同线程对于内容修改只在线程内发挥作用，线程之间爱你
彩色的 码在，threading.current_thread(*)__dict__里添加一个对象mydata的id值以及key
来保存不同线程的状态
 """