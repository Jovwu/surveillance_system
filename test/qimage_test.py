# ceshi
import multiprocessing

from PyQt5.QtGui import QImage

if __name__ == '__main__':
    ma = multiprocessing.Manager()
    d = ma.dict()
    d["a"] = ma.Event()


    print(d)