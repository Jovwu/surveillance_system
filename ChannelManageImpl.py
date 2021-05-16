import sys
import threading
import time
import multiprocessing

import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication

from ChannelImpl import Channel
from FeaturesImpl import Facemark, Stranger
from FrameServiceInterface import FrameService
from InputDeviceInterface import Camera
from ModeImpl import Monitor, DormIn, DormOut, ClassMode
from OutputDeviceInterface import OutputDevice
from WaterMarkInterface import WaterMark

from InputDeviceInterface import Video, NetCamera
from View.TestUI import TestWin
import gobal_data as gd

from multiprocessing import Process, Queue

from channel_dao_impl import ChannelDaoImpl


class RefreshThread(QThread):
    signal = pyqtSignal()

    def __init__(self, channelID,event,channelDict,labelAndChannelDict):
        super(RefreshThread, self).__init__()

        # 通道事件 ->一个通道和一个线程 绑定一个事件 不会修改
        self.event = event

        # label标志位：1.M_label  2.C_label  3.A_label
        self.labelFlag = 2

        # 所属通道
        self.channelID = channelID

        # 通道字典
        self.channelDict = channelDict

        print(self.channelDict)

        # 将自己添加到通道字典
        tmp = self.channelDict[channelID]
        tmp["RefreshThread"] = self
        self.channelDict[channelID] = tmp
        # self.channelDict[channelID]["RefreshThread"] = self
        print("添加后：{0}".format(self.channelDict[channelID]))

        # label 字典
        self.labelAndChannelDict = labelAndChannelDict

        # 设置自己的label
        self.label = self.labelAndChannelDict["C_label"][self.channelID]

        # 连接信号
        self.signal.connect(self.label.refreshCommon)

        # 计算Label的size
        self.channelDict[channelID]["labelsize"] = (int(self.label.width()), int(self.label.height()))


    def setLabelFlag(self,flag):

        # 断开原来的信号连接
        self.signal.disconnect(self.label.refreshCommon)
        # 设置标志位
        self.labelFlag = flag
        # 修改label
        if flag == 1:
            self.label = self.labelAndChannelDict["M_label"]
        elif flag == 2:
            self.label = self.labelAndChannelDict["C_label"][self.channelID]
        elif flag == 3:
            self.label = self.labelAndChannelDict["A_label"][self.channelID]
        # 重新连接
        self.signal.connect(self.label.refreshCommon)
        # 设置Label的图片获取地址
        self.label.setChannel(self.channelID)

    def run(self):
        print("RefreshThread已打开")
        while True:
            # 等待刷新
            self.event.wait()
            # 转
            self.org2Image()
            # 添加水印 -》有的话
            # 延时
            time.sleep(0.001)
            # 发送信号
            self.signal.emit()

    def org2Image(self):

        # 获得原图
        org = self.channelDict[self.channelID]["org"]

        # 图片转换
        shrink = cv2.resize(org, self.channelDict[self.channelID]["labelsize"], interpolation=cv2.INTER_AREA)

        # 更改编码
        shrink = cv2.cvtColor(shrink, cv2.COLOR_BGR2RGB)

        self.channelDict[self.channelID]["image"] = QImage(shrink.data,
                                                 shrink.shape[1],
                                                 shrink.shape[0],
                                                 shrink.shape[1] * 3,
                                                 QImage.Format_RGB888)
        # 添加水印...



class ChannelManage:

    def __init__(self,MANAGE,PROCESS_POOL,channelDict,labelAndChannelDict,channelCodeDict):

        self.PROCESS_POOL = PROCESS_POOL
        self.channelDict = channelDict
        self.labelAndChannelDict = labelAndChannelDict
        self.channelCodeDict = channelCodeDict
        self.MANAGE = MANAGE




    # 创建通道
    def createChannel(self, channelinfosql, featuresList,channelID,refreshEvent,channelCodeQueue):

        # 创建一个inputDevice
        thisInputDevice = self.getInputDevice(str=channelinfosql[3], arg=channelinfosql[4])

        # 创建FrameService
        thisFrameService = self.getFrameService(channelinfosql[5], featuresList,refreshEvent)

        # 创建OutputDevice
        thisOutputDevice = self.getOutputDevice()

        # 创建通道
        channel = Channel(thisInputDevice, thisFrameService, thisOutputDevice,channelID,self.channelDict,refreshEvent,channelCodeQueue)

    # 初始化所有通道(系统运行初期)
    def createAllChannel(self):

        CDL = ChannelDaoImpl()
        # 先从数据库获取信息
        allChannel = CDL.getAllChannel()
        # 通道数量
        channelCout = 0
        for channel in allChannel:
            # 获取功能列表
            featuresList = CDL.getFeaturesByChannelID(channel[0])
            print("{0}通道的配置为：{1},{2}".format(channel[0],channel,featuresList))
            # 创建字典
            self.channelDict[channel[0]] = self.MANAGE.dict()
            self.channelDict[channel[0]] = {
                # 基本信息

                "name":channel[1],
                "area":channel[2],
                "device":channel[3],
                "device_arg":channel[4],
                "mode":channel[5],
                "features":featuresList,
                # 运行信息
                "RefreshThread":None,
                "watermark":{"service":None,"current":None},
                "org":None,
                "image":None,
                "labelsize":None
            }

            print("{0}通道的字典为{1}".format(channel[0], self.channelDict[channel[0]]))
            # 创建一个事件
            refreshEvent = multiprocessing.Manager().Event()

            # 创建通道进程控制队列
            channelCodeQueue = multiprocessing.Manager().Queue()
            self.channelCodeDict[channel[0]] = channelCodeQueue

            # 添加信息
            self.PROCESS_POOL.apply_async(self.createChannel,
                                                 args=(channel, featuresList,channel[0],refreshEvent,channelCodeQueue))

            # 创建一个线程
            refreshThread = RefreshThread(channel[0],refreshEvent,self.channelDict,self.labelAndChannelDict)

            print("{0}通道创建成功".format(channel[0]))


    # 设置label
    def setLabel(self, channelid, mylabel):
        # 给label设置dict
        mylabel.channelDict = self.channelDict[channelid]
        # 设置labelsize
        self.channelDict[channelid]["labelsize"] = (int(mylabel.width()), int(mylabel.height()))
        # 设置信号连接
        self.labelCtrThreadDict[channelid].signal.connect(mylabel.refreshCommon)

    # 打开通道
    def openChannel(self, channelID=None):
        if channelID is None:
            # 打开所有通道
            pass
        else:
            # 打开指定通道
            # 找到通道字典
            self.channelDict[channelID]["通道管理线程命令"] = "开始"
            self.channelCtrEventDict[channelID].set()


    # 关闭通道
    def closeChannel(self):
        pass

    def getInputDevice(self, str, arg):

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

    def getFrameService(self, mode, features=[]):

        # 创建
        # 先创建模式
        thisMode = self.getMode(mode)
        # 添加功能到模式中
        for fstr in features:
            thisMode.addFeatures(self.getFeatures(fstr))

        # 创建帧处理对象
        thisFrameService = FrameService(thisMode)

        return thisFrameService

        # 返回一个OutputDevice对象

    def getOutputDevice(self, qlabel=None):

        o = OutputDevice()
        if qlabel is None:
            pass
        else:
            o.setQLabel(qlabel)

        return o

        # 返回一个features对象

    def getFeatures(self, str):

        if str == "facemark":
            return Facemark()
        elif str == "stranger":
            return Stranger()
        # 没有
        else:
            print("找不到Features")

        # 返回一个Mode实例化对象

    def getMode(self, str):

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

        # 创建业务信息字符串

    def getServiceInfo(self):
        # 根据数据库找到业务信息
        pass

    # 添加通道

    # 删除通道
    # 修改通道
    # 输出窗口更换


if __name__ == '__main__':
    # start = time.time()
    #
    # c = ChannelManage()
    # c.createAllChannel()
    #
    # end = time.time()
    #
    # print(end - start)
    #
    # while 1:
    #     pass

    # 创建QT窗口
    app = QApplication(sys.argv)
    # 实例化窗口
    form = TestWin()
    # 窗口显示
    form.show()

    c = ChannelManage()
    c.createAllChannel()

    # test
    c.setLabel(1001,form.testQLabel)

    time.sleep(3)
    # 开始
    c.openChannel(1001)



    # 进入程序的主循环，遇到退出情况，终止程序
    sys.exit(app.exec_())
