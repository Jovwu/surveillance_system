# FrameService类
import threading
import time
import traceback

import cv2
from PyQt5.QtGui import QImage

from face import getFaceLocations
from tools import getCurTime

class DrawThread(threading.Thread):
    def __init__(self,channel = None):
        threading.Thread.__init__(self)
        self.daemon = True
        self.channel = channel


    def run(self):
        time.sleep(2)
        print("FrameService类.DrawThread已打开")
        while True:

            # 等待原图
            self.channel.threadEvent[0].wait()

            # 获得原图
            #self.channel.threadCtl[1].acquire()
            org = self.channel.frame[0]
            #self.channel.threadCtl[1].release()
            print("优先处理已得图")

            # 获得原图后告诉灰度处理线程可以用了
            self.channel.priorityEvent[0].set()

            # 图片转换
            shrink = cv2.resize(org, self.channel.channelDict["labelsize"], interpolation=cv2.INTER_AREA)
            # 更改编码
            shrink = cv2.cvtColor(shrink, cv2.COLOR_BGR2RGB)

            # 输入优先图
            #self.channel.threadCtl[3].acquire()
            self.channel.channelDict["优先图"] = QImage(shrink.data,
                                           shrink.shape[1],
                                           shrink.shape[0],
                                           shrink.shape[1] * 3,
                                           QImage.Format_RGB888)
            #self.channel.threadCtl[3].release()

            # 通知优先图已经准备好
            self.channel.labelCtrEvent.set()

            # 通知输入设备可以接着输入了
            self.channel.threadEvent[2].set()


            # 等待优先图输出完
            #self.channel.threadEvent[2].wait()

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
                # self.channel.threadCtl[2].acquire()
                gray = self.channel.frame[1]
                # self.channel.threadCtl[2].release()

                # 再进行处理
                # print(getFaceLocations(self.channel.frame[1]))
                # print(type(gray))
                # 处理完添加水印 1.加锁修改水印

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
        #self.drawThread.channel = channel

    # 开启帧处理线程
    def open(self):
        self.frameThread.start()
        #self.drawThread.start()

    # 线程暂停
    def pause(self):
        pass
        # self.frameThread.join()
        # self.drawThread.join()







