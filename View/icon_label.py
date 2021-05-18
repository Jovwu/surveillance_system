import traceback

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from View.checkimg_win import CheckImg


class ICON_label(QLabel):

    # label点击
    click_signal = pyqtSignal()

    def __init__(self,channelDict,widgetDict,parent):
        QLabel.__init__(self, parent)

        self.widgetDict = widgetDict
        self.channelDict = channelDict
        # 设置label点击事件
        self.click_signal.connect(self.clickEvent)


    def mouseReleaseEvent(self, QMouseEvent):
        self.click_signal.emit()

    # 点击事件
    def clickEvent(self):
        self.checkImg = CheckImg(self.channelDict,self.widgetDict)
        self.checkImg.show()

