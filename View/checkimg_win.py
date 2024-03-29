# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'checkimg_win.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys
import time

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox

import person_dao_impl
from face import getFaceLocations, getFaceEncode, getFaceOf
from tools import saveRGB2JPG, getCurDateTime


class Ui_checkimg_win(object):
    def setupUi(self, checkimg_win):
        checkimg_win.setObjectName("checkimg_win")
        checkimg_win.resize(445, 358)
        self.verticalLayoutWidget = QtWidgets.QWidget(checkimg_win)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 20, 342, 330))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(150, 150))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(checkimg_win)
        QtCore.QMetaObject.connectSlotsByName(checkimg_win)

    def retranslateUi(self, checkimg_win):
        _translate = QtCore.QCoreApplication.translate
        checkimg_win.setWindowTitle(_translate("checkimg_win", "Form"))
        self.label.setText(_translate("checkimg_win", "请点击下方按钮选择图片"))
        self.pushButton.setText(_translate("checkimg_win", "图片"))
        self.pushButton_2.setText(_translate("checkimg_win", "摄像头"))
        self.pushButton_3.setText(_translate("checkimg_win", "确定"))
        self.pushButton_4.setText(_translate("checkimg_win", "取消"))

        self.pushButton_3.setEnabled(False)

class CheckImg(QMainWindow, Ui_checkimg_win):
    def __init__(self,channelDict,widgetDict,parent=None):
        super(CheckImg, self).__init__(parent)
        self.channelDict = channelDict
        self.widgetDict = widgetDict
        self.setupUi(self)
        self.frame = None
        self.faceEncode = None
        self.labelSize = (int(self.label.width()), int(self.label.height()))
        self.img = None
        self.connect()
    def connect(self):
        self.pushButton.clicked.connect(self.getFileFace)
        self.pushButton_2.clicked.connect(self.getFaceInCamera)
        self.pushButton_3.clicked.connect(self.OK)
        self.pushButton_4.clicked.connect(self.Cancel)

    def OK(self):

        # 判断人脸是否存在
        faceid = getFaceOf(self.faceEncode, self.channelDict["faceLib"])
        if faceid == 0:
            QMessageBox.warning(self, '警告', '该人脸与原来的不相符！', QMessageBox.Yes)
            return
        elif faceid != 0:
            # 保存图片
            file_path = saveRGB2JPG(self.img, "person/{0}_{1}".format(self.widgetDict["person_id_lineEdit"].text(), getCurDateTime()))
            self.widgetDict["imageChange"] = True
            self.widgetDict["imageEncode"] = self.faceEncode
            self.widgetDict["imagePath"] = file_path
            QMessageBox.information(self, '成功', '修改成功！', QMessageBox.Yes)
            self.close()

    #
    def getFaceInCamera(self):
        # 打开人脸识别框
        cap = cv2.VideoCapture(2)
        faceLocation = None
        img = None
        flag = False
        while (1):
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # get a frame
            ret, frame = cap.read()
            # 转码
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faceLocation = getFaceLocations(img)

            # show a frame
            if len(faceLocation) == 0:
                cv2.imshow("show", frame)
                continue
            else:
                # 设置图片
                self.frame = frame
                # 遍历人脸位置信息
                for top, right, bottom, left in faceLocation:
                    # 对人脸画框
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.imshow("show", frame)
                # 获取编码
                self.faceEncode = getFaceEncode(img, faceLocation)[0]

                time.sleep(2)
                flag = True
                break

        cap.release()
        cv2.destroyAllWindows()

        # 是否获取
        if flag == False:
            return False

        # 图片转换
        shrink = cv2.resize(self.frame, self.labelSize, interpolation=cv2.INTER_AREA)

        # 更改编码
        shrink = cv2.cvtColor(shrink, cv2.COLOR_BGR2RGB)

        image = QImage(shrink.data,
                       shrink.shape[1],
                       shrink.shape[0],
                       shrink.shape[1] * 3,
                       QImage.Format_RGB888)
        self.label.setPixmap(QPixmap().fromImage(image))
        self.img = img
        # 收获到人脸判断是否存在
        # 获取人脸后退出
        # 将人脸写到label
        # 打开输入选项
        self.pushButton_3.setEnabled(True)

        # 图片输入

    def getFileFace(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        if imgName == "":
            return
        else:
            imgName = imgName.replace('\\', '/')

        cv2Image = cv2.imread(imgName)
        img = cv2.cvtColor(cv2Image, cv2.COLOR_BGR2RGB)
        faceLocation = getFaceLocations(img)
        if len(faceLocation) == 0:
            QMessageBox.warning(self, '警告', '没有识别到人脸！', QMessageBox.Yes)
            self.pushButton_3.setEnabled(False)
            return
        else:
            self.faceEncode = getFaceEncode(img, faceLocation)[0]
            # 图片转换
            shrink = cv2.resize(cv2Image, self.labelSize, interpolation=cv2.INTER_AREA)
            # 更改编码
            shrink = cv2.cvtColor(shrink, cv2.COLOR_BGR2RGB)
            image = QImage(shrink.data,
                           shrink.shape[1],
                           shrink.shape[0],
                           shrink.shape[1] * 3,
                           QImage.Format_RGB888)
            self.label.setPixmap(QPixmap().fromImage(image))
            self.img = img

        self.pushButton_3.setEnabled(True)

    def Cancel(self):
        self.close()



if __name__ == '__main__':
    # 每一个pyqt程序中都需要有一个QApplication对象，sys.argv是一个命令行参数列表
    app = QApplication(sys.argv)
    # 实例化窗口
    form = CheckImg(None,None)
    # 将窗口控件显示在屏幕上
    form.show()
    # 进入程序的主循环，遇到退出情况，终止程序
    sys.exit(app.exec_())