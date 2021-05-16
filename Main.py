# 创建QT窗口
import multiprocessing
import sys
import threading
import time
import traceback

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QImage
from cv2 import cv2

import gobal_data as gd
import ChannelManageImpl as CMI
from PyQt5.QtWidgets import QApplication

from ChannelImpl import Channel
from FeaturesImpl import Stranger, Facemark
from FrameServiceInterface import FrameService
from InputDeviceInterface import Camera, Video, NetCamera
from ModeImpl import DormOut, ClassMode, Monitor, DormIn
from OutputDeviceInterface import OutputDevice
from View.MyQLabelImpl import MyQLabel
from View.TestUI import TestWin
from View.main_win import MyMainForm
from channel_dao_impl import ChannelDaoImpl
class RefreshThread(QThread):
    signal = pyqtSignal()

    def __init__(self, channelID,channelDict,labelDict,ChannelRefreshThreadDict):
        super(RefreshThread, self).__init__()
        self.daemon = True

        self.labelSize = None

        ChannelRefreshThreadDict[channelID] = self

        # label标志位：1.M_label  2.C_label  3.A_label
        self.labelFlag = 2
        # 所属通道
        self.channelID = channelID

        # 通道字典
        self.channelDict = channelDict

        # # label 字典
        self.labelDict = labelDict
        #
        # 设置自己的label
        self.label = self.labelDict["C_label"][self.channelID]

        # 设置label的通道
        self.label.channelID = channelID

        # 连接信号
        self.signal.connect(self.label.refreshCommon)
        #
        # 计算Label的size
        self.labelSize = (int(self.label.width()), int(self.label.height()))

        print("{0}通道的RefreshThread创建成功！".format(self.channelID))

    def setLabelFlag(self,flag):

        # 断开原来的信号连接
        self.signal.disconnect(self.label.refreshCommon)
        # 设置标志位
        self.labelFlag = flag
        # 修改label
        if flag == 1:
            self.label = self.labelDict["M_label"]
        elif flag == 2:
            self.label = self.labelDict["C_label"][self.channelID]
        elif flag == 3:
            self.label = self.labelDict["A_label"][self.channelID]
        # 设置label的通道
        self.label.channelID = channelID
        # 重新连接
        self.signal.connect(self.label.refreshCommon)

    def run(self):
        print("{0}通道的RefreshThread已经打开！".format(self.channelID))
        time.sleep(3)
        start = None
        end = None

        try:
            last_time = time.time()
            while True:

                # 等待唤醒
                self.channelDict[self.channelID]["RefreshThreadEvent"].wait()
                cur_time = time.time()
                print("距离上次唤醒时间：{0}".format(cur_time-last_time))
                last_time = cur_time

                start = time.time()
                self.org2Image()
                # 添加水印 -》有的话
                # 延时
                time.sleep(0.01)
                # 发送信号
                self.signal.emit()
                end = time.time()
                print("本次图像处理共耗时{0}".format(end - start))
                self.channelDict[self.channelID]["RefreshThreadEvent"].clear()


        except:
            error = traceback.fromat_exc()
            print(error)
            return error


    def org2Image(self):


        # 获得原图
        org = self.channelDict[self.channelID]["frame"][0]

        # 图片转换

        shrink = cv2.resize(org, self.labelSize, interpolation=cv2.INTER_AREA)

        # 更改编码
        shrink = cv2.cvtColor(shrink, cv2.COLOR_BGR2RGB)

        self.label.image = QImage(shrink.data,
                                                 shrink.shape[1],
                                                 shrink.shape[0],
                                                 shrink.shape[1] * 3,
                                                 QImage.Format_RGB888)

        # 添加水印...



def handle_error(error):
    print(error)
    sys.stdout.flush()

# 初始化所有通道(系统运行初期)
def createAllChannel(channelDict,PROCESS_POOL,MANAGE,labelAndChannelDict,ChannelRefreshThreadDict):

    CDL = ChannelDaoImpl()
    # 先从数据库获取信息
    allChannel = CDL.getAllChannel()

    for channel in allChannel:
        # 获取功能列表
        featuresList = CDL.getFeaturesByChannelID(channel[0])

        # 创建字典
        channelDict[channel[0]] = MANAGE.dict()
        channelDict[channel[0]] = {
            # 基本信息
            "info":MANAGE.list(),
            # frame信息
            "frame":MANAGE.list(),
            # 运行信息
            "RefreshThreadEvent":MANAGE.Event(),
            "ChannelCtrThreadEvent":MANAGE.Event(),
            "ChannelCtrThreadContent":MANAGE.list(),
            "watermark":MANAGE.list()
            #"RefreshThread":refreshThread
            #"ChannelCtrQueue":MANAGE.Queue()
            #"watermark_service":[],
            #"watermark_check":[]
            #"org":None,
            #"image":None,
            #"labelsize":None
            }

        # 初始化数据
        # 初始化基本信息
        channelDict[channel[0]]["info"].append(channel[1])# name
        channelDict[channel[0]]["info"].append(channel[2])# area
        channelDict[channel[0]]["info"].append(channel[3])# device
        channelDict[channel[0]]["info"].append(channel[4])# device_arg
        channelDict[channel[0]]["info"].append(channel[5])# mode
        channelDict[channel[0]]["info"].append(featuresList) # features

        # 初始化frame信息
        channelDict[channel[0]]["frame"].append(0) # org

        # 初始化watermark
        print("创建时候的全部字典{0}".format(channelDict))
        print("创建时候的通道字典{0}".format(channelDict[channel[0]]))

        # 初始化所有线程控制
        channelDict[channel[0]]["ChannelCtrThreadContent"].append(0)  # 通道控制命令

        # 创建一个线程
        refreshThread = RefreshThread(channel[0], channelDict, labelAndChannelDict,ChannelRefreshThreadDict)
        refreshThread.start()

        # 创建通道进程
        PROCESS_POOL.apply_async(createChannel,args=(channel,featuresList,channel[0],channelDict),error_callback=handle_error)



def createChannel(channel,featuresList,channelID,channelDict):
    Channel(channel,featuresList,channelID,channelDict)

# 打开通道
def openChannel(channelID=None):
    if channelID is None:
        # 打开所有通道
        pass
    else:
        # 打开指定通道
        # 找到通道字典
        pass


if __name__ == '__main__':

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    # 实例化窗口
    form = TestWin()
    # 创建服务
    print("创建进程服务")
    MANAGE = multiprocessing.Manager()
    print("创建数据库实例")
    CDI = ChannelDaoImpl()

    print("全局Label字典创建")
    LabelDict = dict()
    # 用于绑定Label和通道
    LabelDict["C_label"] = dict()
    LabelDict["A_label"] = dict()
    # 记录label分类的通道ID
    LabelDict["labelClass"] = dict()
    # 初始化字典
    LabelDict["labelClass"]["all"] = CDI.getAllChannelIDByClass()
    LabelDict["labelClass"]["monitor"] = CDI.getAllChannelIDByClass(1)
    LabelDict["labelClass"]["class"] = CDI.getAllChannelIDByClass(2)
    LabelDict["labelClass"]["dormin"] = CDI.getAllChannelIDByClass(3)
    LabelDict["labelClass"]["dormout"] = CDI.getAllChannelIDByClass(4)

    print("创建通道字典")
    CHANNEL_DICT = MANAGE.dict()
    print("创建通道刷新线程字典")
    ChannelRefreshThreadDict = dict()
    # 加载所有页面
    # 实例化窗口
    mainWin = MyMainForm(LabelDict,CHANNEL_DICT,ChannelRefreshThreadDict)
    # 将窗口控件显示在屏幕上
    # 第二次初始化
    mainWin.show()

    # 开始加载通道
    print("正在初始化...")



    print("创建进程池")
    # 获取所需进程数量
    processCount = len(LabelDict["labelClass"]["all"])
    PROCESS_POOL = MANAGE.Pool(processes=processCount)



    print("初始化所有通道")
    createAllChannel(CHANNEL_DICT,PROCESS_POOL,MANAGE,LabelDict,ChannelRefreshThreadDict)
    print(LabelDict)

    # 再次更新界面
    mainWin.setChannel()

    # 总label
    # 绑定mylabel

    # 创建所有页面

    # 窗口显示
    #form.show()


    print("初始化完成")

    time.sleep(10)

    # 打开通道
    # 获得所有通道的ID
    channelIDlist = LabelDict["labelClass"]["all"]
    print("所有通道ID为{0}".format(channelIDlist))
    for channelID in channelIDlist:
        # 设置命令
        CHANNEL_DICT[channelID]["ChannelCtrThreadContent"][0] = "open"
        # 发送命令
        CHANNEL_DICT[channelID]["ChannelCtrThreadEvent"].set()

    print("所有通道初始化完毕")

    sys.exit(app.exec_())