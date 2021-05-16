import threading
import time
import traceback

import cv2
import numpy as np


class GrayThread(threading.Thread):

    def __init__(self, channel=None):
        threading.Thread.__init__(self)
        self.daemon = True
        self.channel = channel

    def run(self):
        print("InputDevice类.GrayThread已打开")
        time.sleep(2)
        try:
            while True:
                # 等待原图输入
                self.channel.threadEvent[0].wait()

                # 获取原图
                # self.channel.threadCtl[1].acquire()
                org = self.channel.frame[0]
                # self.channel.threadCtl[1].release()

                print("灰度处理已得图")
                # 写入灰度图
                # self.channel.threadCtl[2].acquire()
                self.channel.frame[1] = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
                # self.channel.threadCtl[2].release()

                self.channel.threadEvent[0].clear()
                # 灰度图已处理完，通知相关线程
                self.channel.threadEvent[1].set()
        except:
            error = traceback.fromat_exc()
            raise Exception(error)



class OrgThread(threading.Thread):

    def __init__(self, channel=None, cap=None):
        threading.Thread.__init__(self)
        self.daemon = True
        self.channel = channel
        self.cap = cap

    def __del__(self):
        self.cap.release()

    def run(self):
        print("InputDevice类.OrgThread已打开")
        try:
            while True:
                start = time.time()
                # 输入原图
                ret, org = self.cap.read()
                # 通知获取原图
                # 优先Label输出
                self.channel.channelDict[self.channel.channelID]["frame"][0] = org
                self.channel.channelDict[self.channel.channelID]["RefreshThreadEvent"].set()
                end = time.time()
                print("原图处理时间为:{0}".format(end - start))
                # 通知灰度处理
                self.channel.frame[0] = org
                self.channel.threadEvent[0].set()

                # 等待优先图输出
                # self.channel.threadEvent[2].wait()
        except:
            error = traceback.fromat_exc()
            raise Exception(error)



class InputDevice:

    def __init__(self):
        self.channel = None

    def open(self):
        pass

    def close(self):
        pass

    def setChannel(self, channel):
        pass


# 摄像头
class Camera(InputDevice):

    def __init__(self, local_device_id):
        super().__init__()
        # 初始化设备ID
        self.local_device_id = int(local_device_id)
        # 先打开摄像头
        self.cap = cv2.VideoCapture(self.local_device_id)
        # 线程
        self.orgThread = OrgThread()
        self.grayThread = GrayThread()

    def __del__(self):
        self.__cap.release()
        cv2.destroyAllWindows()

    def setChannel(self, channel):
        self.channel = channel

        self.grayThread.channel = channel

        self.orgThread.channel = channel
        self.orgThread.cap = self.cap

    def open(self):
        # 打开摄像头
        # self.cap = cv2.VideoCapture(self.local_device_id)
        # 打开获取原图线程

        # 打开摄像头输入线程
        self.orgThread.start()
        # 打开灰度处理线程
        self.grayThread.start()

    # 将原始图片传入channelFrame[1]
    # def read(self):
    #
    #     self.channel.threadCtl[1].acquire()
    #     ret, self.channel.frame[1] = self.cap.read()
    #     self.channel.threadCtl[1].release()





# 视频
class Video(InputDevice):

    def __init__(self):
        super().__init__()


# 网络摄像头
class NetCamera(InputDevice):

    def __init__(self):
        super().__init__()


if __name__ == '__main__':

    c = Camera(0)
    t = [0, 0]
    c.open()
    while (1):
        time.sleep(0.01)
        # get a frame
        c.read(t)
        # show a frame
        cv2.imshow("capture", t[0])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    c.close()
    cv2.destroyAllWindows()
