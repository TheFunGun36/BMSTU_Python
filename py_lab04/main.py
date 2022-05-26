import sys
from LineWorks import *
from Canvas import *

from PyQt6.QtGui import *
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import *


class LineWorker(QWidget):
    pointArray: list[Point] = []
    lineArray: list[Line] = []

    def __init__(self):
        super(LineWorker, self).__init__()

        canvasSize = 800

        self.setFixedSize(canvasSize + 210, canvasSize)
        self.canvas = Canvas(self)
        self.canvas.setGeometry(0, 0, canvasSize, canvasSize)

        self.lineArray = []
        self.PointArray = []

        self.canvas.lineArray = self.lineArray
        self.canvas.pointArray = self.pointArray

        # СОЗДАНИЕ ПРЯМОЙ
        label = QLabel("Создание прямой:", self)
        label.setGeometry(canvasSize + 20, 10, 200, 20)

        label = QLabel("Точка 1:", self)
        label.setGeometry(canvasSize + 10, 30, 50, 20)
        self.createLinePointAX = QLineEdit(self)
        self.createLinePointAX.setGeometry(canvasSize + 55, 31, 70, 20)
        self.createLinePointAY = QLineEdit(self)
        self.createLinePointAY.setGeometry(canvasSize + 127, 31, 70, 20)

        label = QLabel("Точка 2:", self)
        label.setGeometry(canvasSize + 10, 52, 50, 20)
        self.createLinePointBX = QLineEdit(self)
        self.createLinePointBX.setGeometry(canvasSize + 55, 53, 70, 20)
        self.createLinePointBY = QLineEdit(self)
        self.createLinePointBY.setGeometry(canvasSize + 127, 53, 70, 20)

        self.createLineButton = QPushButton("Создать прямую", self)
        self.createLineButton.setGeometry(canvasSize + 60, 74, 130, 23)
        self.createLineButton.clicked.connect(self.createLine)

        # СОЗДАНИЕ ТОЧКИ
        label = QLabel("Создание точки:", self)
        label.setGeometry(canvasSize + 20, 110, 200, 20)

        label = QLabel("Точка:", self)
        label.setGeometry(canvasSize + 10, 130, 50, 20)
        self.createPointX = QLineEdit(self)
        self.createPointX.setGeometry(canvasSize + 55, 131, 70, 20)
        self.createPointY = QLineEdit(self)
        self.createPointY.setGeometry(canvasSize + 127, 131, 70, 20)

        self.createPointButton = QPushButton("Создать точку", self)
        self.createPointButton.setGeometry(canvasSize + 60, 152, 130, 23)
        self.createPointButton.clicked.connect(self.createPoint)

        # ОЧИСТКА
        self.clearButton = QPushButton("Очистить поле", self)
        self.clearButton.setGeometry(canvasSize + 20, 200, 170, 30)
        self.clearButton.clicked.connect(self.clearField)

        # УДАЛЕНИЕ
#        self.deleteButton = QPushButton("Удалить\nвыбранный объект", self)
#        self.deleteButton.setGeometry(canvasSize + 20, 232, 170, 50)

        # РАЗМЕР СЕТКИ
        self.gridSizeLabel = QLabel("Масштаб не установлен", self)
        self.gridSizeLabel.setGeometry(canvasSize + 2, 280, 198, 50)

        # РЕЗУЛЬТАТ
        self.labelResult = QLabel("Чтобы задача имела смысл,\nнеобходимо наличие двух\nточек и прямой:", self)
        self.labelResult.setGeometry(canvasSize + 2, 320, 198, 80)

        self.onRepaint()

    def onRepaint(self):
        self.canvas.recalculateScale()
        self.gridSizeLabel.setText("Шаг сетки: {:.3f}".format(self.canvas.gridSize))
        self.repaint()

    @pyqtSlot()
    def clearField(self):
       self.lineArray.clear()
       self.pointArray.clear()
       self.onRepaint()

    def convertToFloat(self, value: str):
        result = None

        try:
            result = float(value)
        except ValueError:
            result = None

        return result

    @pyqtSlot()
    def createLine(self):
        pointA = Point()
        pointA.x = self.convertToFloat(self.createLinePointAX.text())
        pointA.y = self.convertToFloat(self.createLinePointAY.text())

        pointB = Point()
        pointB.x = self.convertToFloat(self.createLinePointBX.text())
        pointB.y = self.convertToFloat(self.createLinePointBY.text())

        if pointA.x is None or pointA.y is None or pointB.x is None or pointB.y is None:
            QMessageBox.information(self, "Создание прямой", "Чтобы создать прямую, необходимо ввести числовые координаты любых двух точек, через которые она проходит")
        else:
            if pointA == pointB:
                QMessageBox.information(self, "Создание прямой", "Нельзя провести прямую через две одинаковые точки")
            else:
                newLine = Line(pointA, pointB)

                if findSameLine(self.lineArray, newLine):
                    QMessageBox.information(self, "Создание прямой", "Такая прямая уже существует")
                else:
                    self.lineArray.append(newLine)
                    self.processTwoBestPoints()
                    self.onRepaint()

    @pyqtSlot()
    def createPoint(self):
        point = Point()
        point.x = self.convertToFloat(self.createPointX.text())
        point.y = self.convertToFloat(self.createPointY.text())

        if point.x is None or point.y is None:
            QMessageBox.information(self, "Создание точки", "Чтобы создать точку, нужно ввести её числовые координаты")
        else:
            if findSamePoint(self.pointArray, point):
                QMessageBox.information(self, "Создание точки", "Такая точка уже существует")
            else:
                self.pointArray.append(point)
                self.processTwoBestPoints()
                self.onRepaint()

    def processTwoBestPoints(self):
        bestPointA = None
        bestPointB = None
        bestLine = None
        bestParallelLinesAmount = -1

        for i, pointA in enumerate(self.pointArray):
            for pointB in self.pointArray[i + 1:]:
                linesBetweenPoints = findLinesBetweenPoints(pointA, pointB, self.lineArray)

                for line in linesBetweenPoints:
                    currentParallelLinesAmount = countParallelLines(self.lineArray, line)

                    if currentParallelLinesAmount > bestParallelLinesAmount:
                        bestParallelLinesAmount = currentParallelLinesAmount
                        bestPointA = pointA
                        bestPointB = pointB
                        bestLine = line

        for line in self.lineArray:
            line.isHighlighted = False

        parallelLines = []

        if bestLine:
            parallelLines = findParallelLines(self.lineArray, bestLine)

        if bestPointA and bestPointB:
            bestPointA.isHighlighted = True
            bestPointB.isHighlighted = True

            self.labelResult.setText(
                "Найденные точки имеют\nкоординаты:\n({:g}, {:g})\n({:g}, {:g})".format(
                    bestPointA.x, bestPointA.y,
                    bestPointB.x, bestPointB.y
                )
            )
        elif len(self.pointArray) >= 2 and len(self.lineArray) >= 1:
            self.labelResult.setText(
                "Не найдено подходящих точек"
            )
        else:
            self.labelResult.setText(
                "Чтобы задача имела смысл,\nнеобходимо наличие двух\nточек и прямой:"
            )

        for line in parallelLines:
            line.isHighlighted = True


if __name__ == "__main__":
    app = QApplication([])
    widget = LineWorker()
    widget.show()

    sys.exit(app.exec())
