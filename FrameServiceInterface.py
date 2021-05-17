# FrameService类
import threading
import time
import traceback

import cv2
from PyQt5.QtGui import QImage

from face import getFaceLocations, getFaceEncode
from tools import getCurTime

class GrayThread(threading.Thread):
    def __init__(self,channel = None):
        threading.Thread.__init__(self)
        self.daemon = True
        self.channel = channel


    def run(self):
        print("FrameService类.GrayThread已打开")
        # 等待事件触发
        try:
            while True:
                # 等待灰度图
                self.channel.threadEvent[1].wait()

                # 先获得灰度图
                gray = self.channel.frame[1]
                # 获得人脸位置
                faceLocation = getFaceLocations(gray)
                # 获得人脸位置
                if len(faceLocation) == 0:
                    print("没有人脸")
                    self.channel.threadEvent[1].clear()
                    continue
                else:
                    # 获得人脸编码 # .repeat(3, 2)
                    faceEncoding = getFaceEncode(gray,faceLocation)
                    print("人脸编码为：{0}".format(faceEncoding))

                    pass




                # 通知水印。。
                self.channel.threadEvent[1].clear()
        except:
            error = traceback.fromat_exc()
            raise Exception(error)





class FrameService:

    def __init__(self,mode):

        self.channel = None
        self.mode = mode

        self.frameThread = GrayThread()
        #self.drawThread = DrawThread()

    def setChannel(self, channel):

        self.channel = channel
        self.mode.setChannel(channel)
        self.frameThread.channel = channel


    # 开启帧处理线程
    def open(self):
        self.frameThread.start()


    # 线程暂停
    def pause(self):
        pass








