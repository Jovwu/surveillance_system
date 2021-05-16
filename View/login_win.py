import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon


class LoginWin(QMainWindow):
    def __init__(self, parent=None):
        # 初始化继承的父类（Qmainwindow）
        super(LoginWin, self).__init__(parent)
        # 设置窗口的大小
        self.resize(1300, 768)
        # 创建窗口标题
        self.setWindowTitle('PyQt MainWindow例子')





if __name__ == '__main__':
    # 每一个pyqt程序中都需要有一个QApplication对象，sys.argv是一个命令行参数列表
    app = QApplication(sys.argv)
    # 实例化窗口
    form = LoginWin()
    # 窗口显示
    form.show()
    # 进入程序的主循环，遇到退出情况，终止程序
    sys.exit(app.exec_())

