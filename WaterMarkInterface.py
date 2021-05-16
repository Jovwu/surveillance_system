from PyQt5 import Qt
from PyQt5.QtGui import QPainter, QColor, QFont


class WaterMark:

    def __init__(self):
        pass

    # 指定位置添加水印
    def draw(self,x,y,text,frame):

        print("设置水印开始")
        self.qpainter = QPainter(frame)
        print("设置颜色")
        # 设置颜色
        self.qpainter.setPen(QColor(3, 20, 160))
        # 设置字体
        self.qpainter.setFont(QFont('SimSun', 20))
        print("beg")
        self.qpainter.begin()
        print("开始绘制")
        self.qpainter.drawText(x,y,text)
        self.qpainter.end()