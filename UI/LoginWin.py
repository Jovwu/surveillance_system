import os
import sys
import traceback

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon


class UserDaoImpl(object):
    @classmethod
    def selectUserByIDAndPwd(cls, param, param1):
        return ""


class MainWin(object):
    def show(self,dwadwa):
        pass


def curTime2String():
    return ""


def curUser2String():
    return ""


class Table2CSV(object,os):
    pass


class ChannelManage(object):
    @classmethod
    def GetChannelInfo(cls, channelID):
        pass

    @classmethod
    def GetChannelStatu(cls, channelID):
        pass




    class LoginWin(QMainWindow):
        def __init__(self, parent=None):
            # 初始化继承的父类（Qmainwindow）
            super(LoginWin, self).__init__(parent)
            # 设置窗口的大小
            self.resize(400, 200)
            # 实例化创建状态栏
            self.status = self.statusBar()
            # 将提示信息显示在状态栏中showMessage（‘提示信息'，显示时间（单位毫秒））
            self.status.showMessage('这是状态栏提示', 4000)
            # 创建窗口标题
            self.setWindowTitle('PyQt MainWindow例子')

            self.loginState = QLabel("信息")

            self.userIDEdit = QLineEdit("")

            self.userPwdEdit = QLineEdit("")

            # reply = QMessageBox.question(self, '导出成功', '是否打开文件所在目录？', QMessageBox.Yes | QMessageBox.No,
            #                              QMessageBox.Yes)
    def login(self):
        # 判断登录类型
        # 口令登录
        if self.loginState.text() == "info":

            # 判断信息输入为空
            if self.userIDEdit.text() == "" or self.userPwdEdit.text() == "":
                MyMessage("用户名和密码不得为空！")
                return
            # 数据库查询
            result = UserDaoImpl.selectUserByIDAndPwd(
                self.userIDEdit.text(),
                self.userPwdEdit.text())
            # 结果判断
            # 如果正确
            if result is True:
                MyMessage("登录成功！正在跳转...")
                # 创建主页面并显示
                mainWin = MainWin(self.userIDEdit.text())
                mainWin.show()
                self.hide()
                return
            # 结果错误
            else:
                MyMessage("用户名或密码错误！")
                # 清空密码
                self.userPwdEdit.setText("")
                return

        # 人脸登录
        else:
            # 判断是否有登录摄像头
            if self.myCamera is 0:
                MyMessage("找不到摄像设备！")
                return
            # 等待人脸输入，限时五秒
            if self.myCamera.waitFace() is True:
                # 数据库查询
                result = UserDaoImpl.selectUserByFaceID(self.myCamera.getFace())
                # 验证成功
                if result is True:
                    MyMessage("登录成功！正在跳转...")
                    mainWin = MainWin(self.userIDEdit.text())
                    mainWin.show()
                    self.hide()
                    return
                # 验证失败
                else:
                    MyMessage("人脸识别失败！")
                    return
            # 识别不到人脸
            else:
                MyMessage("未识别到人脸！")
                return

    def DataExport(self):

        # 获取保存文件夹的路径
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        # 如果没有选择文件目录，退出
        if directory == "":
            return

        # 拼接文件名:文件格式为当前时间加当前用户
        fileName = directory + curTime2String() + curUser2String()

        # 输入tableWidget和文件名
        result = Table2CSV(self.dataTable, fileName)

        # 判断结果
        if result is True:
            # 询问是否打开文件所在目录
            reply = QMessageBox.question(self, '导出成功', '是否打开文件所在目录？',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                         QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                os.startfile(directory)
            return
        else:
            MyMessage("导出失败！")
            return

    def ChannelChange(self, channelID):

        # 先判断选定通道是否处于运行状态
        # 如果处于运行状态
        if ChannelManage.GetChannelStatu(channelID):
            try:
                # 获取新的通道信息
                newInfoDict = ChannelManage.GetChannelInfo(channelID)
                # 将新的信息加载到页面上
                self.Refresh(newInfoDict)
            except Exception as e:
                traceback.print_exc()
                return False
            else:
                # 更新通道ID
                self.curChannelID = channelID
                return True
        # 如果不处于运行状态
        else:
            return False

    def DeletePerson(self, personID):

        # 先从业务表中删除相关信息
        # 直接从宿舍人员表中删除人员
        DormDaoImpl.deletePersonByID(personID)

        # 先找到人员所在教室
        gradeList = GradeDaoImpl.getGradeByPersonID(personID)
        # 从教室人员表中删除
        GradeDaoImpl.deletePersonByID(personID)
        # 去掉所有教室打卡人数
        for i in gradeList:
            GradeClockDaoImpl.deleteTotalByAddrID(i)

        # 删除人员表
        PersonDaoImpl.deletePersonByID(personID)


if __name__ == '__main__':
    # 每一个pyqt程序中都需要有一个QApplication对象，sys.argv是一个命令行参数列表
    app = QApplication(sys.argv)
    # 实例化窗口
    form = LoginWin()
    # 窗口显示
    form.show()
    # 进入程序的主循环，遇到退出情况，终止程序
    sys.exit(app.exec_())


def selectUserByIDAndPwd(id, pwd):
    return bool


def selectUserByFaceID(faceid):
    return bool


def MyMessage(dw):
    pass
