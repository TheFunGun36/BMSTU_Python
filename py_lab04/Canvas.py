from LineWorks import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QWidget
import numpy

class Canvas(QWidget):
    lineArray: list[Line] = []
    pointArray: list[Point] = []
    gridSize = 1.0
    canvasGridStep = 50

    def calculateBestScaleForPoints(self):
        result = 0

        for point in self.pointArray:
            if abs(point.x) > result:
                result = abs(point.x)
            if abs(point.y) > result:
                result = abs(point.y)

        return 2 * result

    def recalculateScale(self):
        self.canvasWidth = self.frameGeometry().width()
        self.canvasHeight = self.frameGeometry().height()

        self.canvasCenterX, self.canvasCenterY = self.canvasWidth / 2, self.canvasHeight / 2

        scalePoints = self.calculateBestScaleForPoints() / (self.canvasHeight - 100)
        scaleLines = self.calculateBestScaleForLines() / (self.canvasHeight - 100)
        self.scaleFactor = scalePoints if scalePoints > scaleLines else scaleLines

        if isEqual(self.scaleFactor, 0.0):
            self.scaleFactor = 1

        self.gridSize = self.canvasGridStep * self.scaleFactor

    def calculateBestScaleForLines(self):
        result = 0

        for line in self.lineArray:
            orth = line.getOrthogonal()
            point = orth.intercept(line)

            if abs(point.x) > result:
                result = abs(point.x)
            if abs(point.y) > result:
                result = abs(point.y)

        return 2 * result

    def paintEvent(self, event):
        painter = QPainter(self)
        whiteBrush = QBrush(QColor(50, 50, 50))
        painter.fillRect(self.geometry(), whiteBrush)

        penSimple = QPen(QColor(200, 200, 200))
        penHighlighted = QPen(QColor(20, 200, 200), 1)
        penHovered = QPen(QColor(20, 100, 200), 1)
        penChosen = QPen(QColor(20, 100, 200), 2)

        painter.setPen(QPen(QColor(120, 120, 120)))

        # ОСИ
        painter.drawLine(0, self.canvasCenterY, self.canvasWidth, self.canvasCenterY)
        painter.drawLine(self.canvasCenterX, 0, self.canvasCenterY, self.canvasHeight)

        # ОСНОВНАЯ СЕТКА
        painter.setPen(QPen(QColor(80, 80, 80)))

        for i in numpy.arange(self.canvasCenterX + self.canvasGridStep, self.canvasWidth, self.canvasGridStep):
            painter.drawLine(0, self.canvasHeight - i, self.canvasWidth, self.canvasHeight - i)
            painter.drawLine(0, i, self.canvasWidth, i)

        for i in numpy.arange(self.canvasCenterY + self.canvasGridStep, self.canvasHeight, self.canvasGridStep):
            painter.drawLine(self.canvasWidth - i, 0, self.canvasWidth - i, self.canvasHeight)
            painter.drawLine(i, 0, i, self.canvasHeight)

        # ВТОРИЧНАЯ СЕТКА
        painter.setPen(QPen(QColor(65, 65, 65)))

        for i in numpy.arange(self.canvasCenterX + self.canvasGridStep / 2, self.canvasWidth, self.canvasGridStep):
            painter.drawLine(0, self.canvasHeight - i, self.canvasWidth, self.canvasHeight - i)
            painter.drawLine(0, i, self.canvasWidth, i)

        for i in numpy.arange(self.canvasCenterY + self.canvasGridStep / 2, self.canvasHeight, self.canvasGridStep):
            painter.drawLine(self.canvasWidth - i, 0, self.canvasWidth - i, self.canvasHeight)
            painter.drawLine(i, 0, i, self.canvasHeight)

        # ПРЯМЫЕ
        for line in self.lineArray:
            interceptions = line.findRectInterceptions(
                (self.canvasCenterX - self.canvasWidth) * self.scaleFactor,
                (self.canvasCenterY - self.canvasHeight) * self.scaleFactor,
                (self.canvasCenterX + self.canvasWidth) * self.scaleFactor,
                (self.canvasCenterY + self.canvasHeight) * self.scaleFactor
            )

            if (len(interceptions) >= 2):
                if line.isChosen:
                    painter.setPen(penChosen)
                elif line.isHovered:
                    painter.setPen(penHovered)
                elif line.isHighlighted:
                    painter.setPen(penHighlighted)
                else:
                    painter.setPen(penSimple)

                painter.drawLine(
                    interceptions[0].x / self.scaleFactor + self.canvasCenterX,
                    self.canvasCenterY - interceptions[0].y / self.scaleFactor,
                    interceptions[1].x / self.scaleFactor + self.canvasWidth / 2,
                    self.canvasHeight / 2 - interceptions[1].y / self.scaleFactor
                )

        penSimple = QPen(QColor(200, 200, 200), 3)
        penHighlighted = QPen(QColor(20, 200, 200), 4)
        penHovered = QPen(QColor(20, 100, 200), 4)
        penChosen = QPen(QColor(20, 100, 200), 5)

        # ТОЧКИ
        for point in self.pointArray:
            if point.isChosen:
                painter.setPen(penChosen)
            elif point.isHovered:
                painter.setPen(penHovered)
            elif point.isHighlighted:
                painter.setPen(penHighlighted)
            else:
                painter.setPen(penSimple)

            painter.drawPoint(
                self.canvasCenterX + point.x / self.scaleFactor,
                self.canvasCenterY - point.y / self.scaleFactor
            )

        painter.end()
