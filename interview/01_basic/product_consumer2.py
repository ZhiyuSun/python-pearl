import time

def consumer(name):
    print('{}准备吃包子了！'.format(name))
    while True:
        baozi = yield  #在它就收到内容的时候后就把内容传给baozi
        print('包子【{}】来了，被【{}】吃了'.format(baozi,name))

def producer():
    c1 = consumer('A')  #它只是把c1变成一个生成器
    c2 = consumer('B')
    c1.__next__() #第一个next只是会走到yield然后停止
    c2.__next__()
    print('开始做包子了')
    for i in range(1,10):
        time.sleep(0.5)
        print('三秒做了两个包子')
        c1.send(i)
        c2.send(i+1)

producer()