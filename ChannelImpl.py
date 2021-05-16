import multiprocessing
import sys
import threading
import time
import traceback

import numpy
from PyQt5.QtWidgets import QApplication

from FeaturesImpl import Stranger, Facemark
from FrameServiceInterface import FrameService
from InputDeviceInterface import Camera, Video, NetCamera
from ModeImpl import Monitor, DormIn, DormOut, ClassMode
from OutputDeviceInterface import OutputDevice
from WaterMarkInterface import WaterMark
from View.TestUI import TestWin


class ChannelCtlThread(threading.Thread):

    def __init__(self, channel):
        threading.Thread.__init__(self)
        self.daemon = True
        self.channel = channel


    def run(self):
        print("{0}通道的ChannelCtlThread一打开！".format(self.channel.channelID))
        try:
            while True:
                # 等待通道控制命令
                self.channel.channelDict[self.channel.channelID]["ChannelCtrThreadEvent"].wait()
                # 获取命令
                order = self.channel.channelDict[self.channel.channelID]["ChannelCtrThreadContent"][0]
                # 清空命令
                self.channel.channelDict[self.channel.channelID]["ChannelCtrThreadContent"][0] = ""
                print("{0}通道接受到{1}命令".format(self.channel.channelID, order))
                if order == "open":
                    self.channel.open()
                # self.channel.testE.set()
                self.channel.channelDict[self.channel.channelID]["ChannelCtrThreadEvent"].clear()
        except:
            error = traceback.fromat_exc()
            raise Exception(error)




class Channel:

    def __init__(self, channel,featuresList,channelID,channelDict):
        print("进入")
        # 开始标志位
        self.openFlag = False

        self.channelID = channelID
        self.channelDict = channelDict



        print("开始初始化通道{0}".format(self.channelID))

        # # 通道信息
        # self.channelInfo = None

        # inputDevice
        self.inputDevice = getInputDevice(str=channel[3], arg=channel[4])
        self.inputDevice.setChannel(self)

        # frameService
        self.frameService = getFrameService(channel[5], featuresList)
        self.frameService.setChannel(self)

        # outputDevice
        self.outputDevice = getOutputDevice()
        self.outputDevice.setChannel(self)

        # frame
        # frame[0]为原图
        # frame[1]为灰度处理图片
        self.frame = [0, 0]

        # 水印信息
        # watermark[0]为固定水印
        # watermark[1]为动态水印(人脸画框等)
        self.watermark = [0, 0]

        # orgMute为frame[1]的锁(原图)
        orgMute = threading.Lock()
        # graymute为frame[2]的锁(灰度图)
        grayMute = threading.Lock()
        # drawMute为frame[3]的锁(优先图)
        drawMute = threading.Lock()
        # 数据读写控制
        self.threadCtl = [orgMute, grayMute, drawMute]

        # orgEvent为原图事件
        orgEvent = threading.Event()
        # grayEvent为灰度图事件
        grayEvent = threading.Event()
        # drawEvent 为优先输出事件
        drawEvent = threading.Event()
        # 线程事件控制
        self.threadEvent = [orgEvent, grayEvent, drawEvent]

        # 线程优先级
        # getOrgEvent 为原图抢先权
        getOrgEvent = threading.Event()
        self.priorityEvent = [getOrgEvent]

        self.channelCtlThread =ChannelCtlThread(self)
        self.channelCtlThread.start()

        print("通道{0}已创建成功".format(self.channelID))

    # 通道打开
    def open(self):
        # 打开输入通道
        self.inputDevice.open()
        # 开启帧处理线程
        self.frameService.open()
        # 开启输出线程
        #self.outputDevice.open()

    # 通道暂停
    def pause(self):
        # 暂停通道
        pass

    # 通道销毁
    def close(self):
        pass

    # 设置输出窗口
    def setOutputLabel(self, qlabel):
        return self.outputDevice.setQLabel(qlabel, self)


def getInputDevice(str, arg):

    # 如果是Camera
    if str == "camera":
        # 根据设备号创建
        return Camera(arg)
    # 如果是本地视频
    elif str == "video":
        # 根据文件地址创建
        return Video(arg)
    # 如果是网络摄像头
    elif str == "netcamera":
        # 根据IP地址创建
        return NetCamera(arg)
        # 没有
    else:
        print("找不到InputDevice")

        # 返回一个FrameService实例化对象

def getFrameService(mode, features=[]):

    # 创建
    # 先创建模式
    thisMode = getMode(mode)
    # 添加功能到模式中
    for fstr in features:
        thisMode.addFeatures(getFeatures(fstr))

    # 创建帧处理对象
    thisFrameService = FrameService(thisMode)

    return thisFrameService

        # 返回一个OutputDevice对象

def getOutputDevice(qlabel=None):

    o = OutputDevice()
    if qlabel is None:
         pass
    else:
        o.setQLabel(qlabel)

    return o

    # 返回一个features对象

def getFeatures(str):

    if str == "facemark":
        return Facemark()
    elif str == "stranger":
        return Stranger()
    # 没有
    else:
        print("找不到Features")

        # 返回一个Mode实例化对象

def getMode(str):

    # 设置模式
    # 监控模式
    if str == "monitor":
        return Monitor()
    # 班级打卡
    elif str == "class":
        return ClassMode()
    # 宿舍进入
    elif str == "dormin":
        return DormIn()
    # 宿舍出
    elif str == "dormout":
         return DormOut()
    # 没有
    else:
        print("找不到Mode")

if __name__ == '__main__':
    # 创建QT窗口
    app = QApplication(sys.argv)
    # 实例化窗口
    form = TestWin()
    # 窗口显示
    form.show()

    # 创建通道
    c = Channel(Camera(0), FrameService(watermark=WaterMark()), OutputDevice())
    # 设置输出窗口
    print(c.setOutputLabel(form.testQLabel))
    # 通道打开
    c.open()

    # 进入程序的主循环，遇到退出情况，终止程序
    sys.exit(app.exec_())
