import traceback

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class MyQLabel(QLabel):

    # label点击
    click_signal = pyqtSignal()

    def __init__(self,parent,channelID=None,channelDict=None):
        QLabel.__init__(self, parent)

        self.channelID = channelID
        self.channelDict = channelDict
        # 设置label点击事件
        self.click_signal.connect(self.clickEvent)

        self.image = None


    # 使用普通图片刷新刷新label
    def refreshCommon(self):
        print("label已被触发")
        try:

            self.setPixmap(QPixmap().fromImage(self.image))
        except:
            error = traceback.fromat_exc()
            print(error)
            return error


    def mouseReleaseEvent(self, QMouseEvent):
        self.click_signal.emit()

    # 点击事件
    def clickEvent(self):
        print("click")

    # 使用帧处理过的图片刷新label

    # 设置通道
    def setChannel(self,channelID):

        self.channelID = channelID