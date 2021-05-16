import _thread
import os
import sys
import time

import cv2
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QLineEdit, QMessageBox, QFileDialog

from View.MyQLabelImpl import MyQLabel
from View.dorm_diy import Ui_dorm_diy


class TestWin(QMainWindow):
    def __init__(self, parent=None):
        # 初始化继承的父类（Qmainwindow）
        super(TestWin, self).__init__(parent)
        # 设置窗口的大小
        self.resize(800, 800)
        # 创建窗口标题
        self.setWindowTitle('TestUI')

        # 显示图片
        self.qimage = None

        self.testQLabel = MyQLabel(self)
        self.testQLabel.setGeometry(0, 0, 800, 800)

        self.diy = Ui_dorm_diy()

        # _thread.start_new_thread(self.__run())
        # print("ok")

        # pix = QPixmap('C:\zhongshiyu\WorkSpace\PythonProjects\pythonProject\image\奥巴马1.png')
        # self.testQLabel.setPixmap(pix)
        # self.testQLabel.setScaledContents(True)




    # def __run(self):
    #
    #     time.sleep(2)
    #     cap = cv2.VideoCapture(0)
    #     self.__size = (int(self.testQLabel.width()), int(self.testQLabel.height()))
    #     while 1:
    #         time.sleep(0.3)
    #         # get a frame
    #         ret, frame = cap.read()
    #
    #         # 转换
    #         shrink = cv2.resize(frame, self.__size, interpolation=cv2.INTER_AREA)
    #         # 更改编码
    #         shrink = cv2.cvtColor(shrink, cv2.COLOR_BGR2RGB)
    #         # 创建qimage
    #         self.__qimage = QImage(shrink.data,
    #                                shrink.shape[1],
    #                                shrink.shape[0],
    #                                shrink.shape[1] * 3,
    #                                QImage.Format_RGB888)
    #         # 显示
    #         self.testQLabel.setPixmap(QPixmap.fromImage(self.__qimage))
    #
    #
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #
    #     cap.release()
    #     cv2.destroyAllWindows()

if __name__ == '__main__':
    # 创建QT窗口
    app = QApplication(sys.argv)
    # 实例化窗口
    form = TestWin()
    # 窗口显示
    form.show()

    # 进入程序的主循环，遇到退出情况，终止程序
    sys.exit(app.exec_())
