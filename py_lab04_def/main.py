import sys
import math
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(800, 600)
        self.installEventFilter(self)
        self.pointList = []

    def mousePressEvent(self, event):
        if len(self.pointList) >= 3:
            self.pointList.clear()
        self.pointList.append(event.position())
        self.update()

    def getCircle(self):
        x1, x2, x3 = self.pointList[0].x(), self.pointList[1].x(), self.pointList[2].x()
        y1, y2, y3 = self.pointList[0].y(), self.pointList[1].y(), self.pointList[2].y()
        try:
            x0 = -(1/2)*(y1*(x2**2-x3**2+y2**2-y3**2)+y2*(-x1**2+x3**2-y1**2+y3**2)+y3*(x1**2-x2**2+y1**2-y2**2))/(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2))
            y0 = (1/2)*(x1*(x2**2-x3**2+y2**2-y3**2)+x2*(-x1**2+x3**2-y1**2+y3**2)+x3*(x1**2-x2**2+y1**2-y2**2))/(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2))
        except ZeroDivisionError:
            return None
        return x0, y0, math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

    def paintEvent(self, event):
        painter = QPainter(self)

        if len(self.pointList) == 3:
            res = self.getCircle()

            if res:
                brush = QBrush(QColor(0, 0, 0, 0))
                pen = QPen(QColor(50, 50, 200), 4)
                painter.setBrush(brush)
                painter.setPen(pen)
                painter.drawEllipse(QPointF(res[0], res[1]), res[2], res[2])


        brush = QBrush(QColor(0, 50, 0))
        pen = QPen(QColor(0, 50, 0))
        painter.setBrush(brush)
        painter.setPen(pen)

        for point in self.pointList:
            painter.drawEllipse(point, 3, 3)
        painter.end()


if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
