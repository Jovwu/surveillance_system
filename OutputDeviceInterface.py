import threading
import time

import cv2
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel

from View.MyQLabelImpl import MyQLabel

# class RefreshThread(QThread):
#
#     signal = pyqtSignal()
#
#     def __init__(self, channel):
#         super(RefreshThread, self).__init__()
#         # 通道类
#         self.channel = channel
#
#
#     def run(self):
#
#         while True:
#             # 等待优先图
#             self.channel.threadEvent[3].wait()
#             # 延时发送信号
#             time.sleep(0.001)
#             # 优先图准备好后发送信号
#             self.signal.emit()
#
#             # 通知优先图已输出
#             self.channel.threadEvent[3].set()

class OutputDevice:

    def __init__(self):
        self.channel = None
        self.qlabel = None
        #self.refreshThread = RefreshThread(self)

    # 绑定通道
    def setChannel(self,channel):
        self.channel = channel
        #self.refreshThread.channel = channel

    # 设置输出窗口
    def setQLabel(self, qlabel,channel):

        if type(qlabel) is MyQLabel:
            # 设置自己的qlabel
            self.qlabel = qlabel
            # 设置自己的channel
            self.channel = channel
            # 设置qlabel的channel
            self.qlabel.channel = channel
            # 获取qlabel的长宽
            self.channel.frame[0] = (int(self.qlabel.width()), int(self.qlabel.height()))
            # 连接信号
            self.refreshThread.signal.connect(self.qlabel.refreshCommon)
            return True
        else:
            return False

    def open(self):
        # 打开刷新线程
        self.refreshThread.start()




