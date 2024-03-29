# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_win.ui'
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
from model import Person
from tools import getKeyByValue, saveRGB2JPG, getCurDateTime


class Ui_add_win(object):
    def setupUi(self, add_win):
        add_win.setObjectName("add_win")
        add_win.resize(504, 409)
        self.verticalLayoutWidget = QtWidgets.QWidget(add_win)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 50, 342, 311))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ADD_frame_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ADD_frame_label.setObjectName("ADD_frame_label")
        self.verticalLayout.addWidget(self.ADD_frame_label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.ADD_name_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.ADD_name_edit.setEnabled(False)
        self.ADD_name_edit.setObjectName("ADD_name_edit")
        self.horizontalLayout_2.addWidget(self.ADD_name_edit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.ADD_comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.ADD_comboBox.setEnabled(False)
        self.ADD_comboBox.setObjectName("ADD_comboBox")
        self.horizontalLayout_3.addWidget(self.ADD_comboBox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ADD_imageface_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ADD_imageface_btn.setObjectName("ADD_imageface_btn")
        self.horizontalLayout.addWidget(self.ADD_imageface_btn)
        self.ADD_cameraface_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ADD_cameraface_btn.setObjectName("ADD_cameraface_btn")
        self.horizontalLayout.addWidget(self.ADD_cameraface_btn)
        self.ADD_OK = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ADD_OK.setEnabled(False)
        self.ADD_OK.setObjectName("ADD_OK")
        self.horizontalLayout.addWidget(self.ADD_OK)
        self.ADD_cancel = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ADD_cancel.setObjectName("ADD_cancel")
        self.horizontalLayout.addWidget(self.ADD_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 4)

        self.retranslateUi(add_win)
        QtCore.QMetaObject.connectSlotsByName(add_win)

    def retranslateUi(self, add_win):
        _translate = QtCore.QCoreApplication.translate
        add_win.setWindowTitle(_translate("add_win", "Form"))
        self.ADD_frame_label.setText(_translate("add_win", "请点击下方按钮获取人脸"))
        self.label.setText(_translate("add_win", "用户名称"))
        self.label_2.setText(_translate("add_win", "用户类型"))
        self.ADD_imageface_btn.setText(_translate("add_win", "从图片获取"))
        self.ADD_cameraface_btn.setText(_translate("add_win", "实时人脸"))
        self.ADD_OK.setText(_translate("add_win", "确定"))
        self.ADD_cancel.setText(_translate("add_win", "取消"))
        self.ADD_frame_label.setFixedSize(200,200)

class AddPersonForm(QMainWindow, Ui_add_win):
    def __init__(self, channelDict,parent=None):
        super(AddPersonForm, self).__init__(parent)
        self.setupUi(self)
        self.channelDict = channelDict

        self.labelSize = (int(self.ADD_frame_label.width()), int(self.ADD_frame_label.height()))

        self.PDI = person_dao_impl.PersonDaoImpl()


        self.frame = None
        self.faceEncode = None
        self.img = None

        self.init()

        self.connect()

    def init(self):
        # 更新combox
        for values in self.channelDict["personClass"].values():
            self.ADD_comboBox.addItem(values)
        self.ADD_comboBox.setCurrentIndex(0)

    def connect(self):
        self.ADD_cameraface_btn.clicked.connect(self.getCameraFace)
        self.ADD_imageface_btn.clicked.connect(self.getFileFace)
        self.ADD_OK.clicked.connect(self.OK_btn)
        self.ADD_cancel.clicked.connect(self.close)

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
            QMessageBox.warning(self, '警告', '没有识别到人脸！',QMessageBox.Yes)
            return
        else:
            self.faceEncode = getFaceEncode(img,faceLocation)[0]
            # 图片转换
            shrink = cv2.resize(cv2Image, self.labelSize, interpolation=cv2.INTER_AREA)
            # 更改编码
            shrink = cv2.cvtColor(shrink, cv2.COLOR_BGR2RGB)
            image = QImage(shrink.data,
                           shrink.shape[1],
                           shrink.shape[0],
                           shrink.shape[1] * 3,
                           QImage.Format_RGB888)
            self.ADD_frame_label.setPixmap(QPixmap().fromImage(image))
            self.img = img

        self.openAll()


    # 实时人脸监听事件
    def getCameraFace(self):
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
                self.faceEncode = getFaceEncode(img,faceLocation)[0]

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
        self.ADD_frame_label.setPixmap(QPixmap().fromImage(image))
        self.img = img
        # 收获到人脸判断是否存在
        # 获取人脸后退出
        # 将人脸写到label
        # 打开输入选项
        self.openAll()

    def OK_btn(self):
        # 判断人脸是否存在
        faceid = getFaceOf(self.faceEncode,self.channelDict["faceLib"])
        if faceid != 0:
            QMessageBox.warning(self, '警告', '该人脸已存在！', QMessageBox.Yes)
            return
        elif self.ADD_name_edit.text() == "":
            QMessageBox.warning(self, '警告', '请输入信息！', QMessageBox.Yes)
        elif faceid == 0:
            PDI = person_dao_impl.PersonDaoImpl()
            # 获得personClass的ID
            personClassID = getKeyByValue(self.channelDict["personClass"],self.ADD_comboBox.currentText())
            # 先添加人员
            PDI.addPerson(Person(self.faceEncode, self.ADD_name_edit.text(), int(personClassID), "null"))
            # 获得最后一条记录
            personID = int(self.PDI.getLastPersonID())
            # 保存图片 然后获得图片路径
            file_path = saveRGB2JPG(self.img,"person/{0}_{1}".format(personID,getCurDateTime()))
            # 再填充人员图片信息
            PDI.setPersonPicPath(personID,file_path)

            # 实时更新人脸库
            self.channelDict["DataGetThreadContent"].append("updateFaceLib")
            self.channelDict["DataGetThreadEvent"].set()

            QMessageBox.information(self, '恭喜', '注册成功！', QMessageBox.Yes)
            self.closeAll()



    def closeAll(self):
        self.ADD_frame_label.setText("请点击下方按钮获取人脸")
        self.ADD_name_edit.setText("")
        self.ADD_comboBox.setCurrentIndex(0)
        self.ADD_name_edit.setEnabled(False)
        self.ADD_comboBox.setEnabled(False)
        self.ADD_OK.setEnabled(False)
        self.frame = None
        self.faceEncode = None
        self.img = None



    def openAll(self):
        self.ADD_name_edit.setEnabled(True)
        self.ADD_comboBox.setEnabled(True)
        self.ADD_OK.setEnabled(True)


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    # 每一个pyqt程序中都需要有一个QApplication对象，sys.argv是一个命令行参数列表
    app = QApplication(sys.argv)
    # 实例化窗口
    form = AddPersonForm()
    # 将窗口控件显示在屏幕上
    form.show()
    # 进入程序的主循环，遇到退出情况，终止程序
    sys.exit(app.exec_())