import multiprocessing
import threading
import time


class pT(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.c = 1


    def run(self):

        while True:
            time.sleep(1)
            print("我的数据为“{0}".format(self.c))

class cT(threading.Thread):
    def __init__(self,pT):
        threading.Thread.__init__(self)
        self.pT = pT


    def run(self):

        while True:
            time.sleep(1)
            self.pT.c+=1

if __name__ == '__main__':

    # p = pT()
    # p.start()
    # c = cT(p)
    # c.start()
    dic =dict()
    dic["que"] = multiprocessing.Manager().Queue()

    dic["que"].put(1)
    print(dic["que"].get(True))
