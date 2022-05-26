# Кодировка UTF-8,
# Вариант 3, 1
# Метод Ньютона для уточнения корней
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import pyqtSlot
import MathModule
import UIMainWindow
from math import fabs


class Main(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)

        self.current_interval_a = None
        self.current_interval_b = None
        self.root_list = []

        self.window_ui = UIMainWindow.Ui_MainWindow()
        self.window_ui.setupUi(self)
        self.window_ui.retranslateUi(self)

        self.window_ui.calculateButton.clicked.connect(
            self.calculate_button_click
        )

    @pyqtSlot()
    def calculate_button_click(self):
        interval_a = self.window_ui.inputIntervalLeft.text()
        interval_b = self.window_ui.inputIntervalRight.text()
        accuracity = self.window_ui.inputAccuracity.text()

        try:
            interval_a = float(interval_a)
            interval_b = float(interval_b)
            accuracity = float(accuracity)
        except ValueError:
            QMessageBox.about(
                self,
                'Ошибка',
                'Должны быть введены числа'
            )

        if accuracity <= 0:
            QMessageBox.about(
                self,
                'Ошибка',
                'Точность должна быть положительной'
            )
            return

        if interval_a > interval_b:
            interval_a, interval_b = interval_b, interval_a

        result = MathModule.TableElement()
        result.interval_a = interval_a
        result.interval_b = interval_b

        MathModule.find_root(MathModule.function, result, accuracity)

        self.window_ui.outputRoot.setText('{:g}'.format(result.root))
        self.window_ui.outputValue.setText('{:g}'.format(result.function_value))
        self.window_ui.outputIterations.setText(str(result.iterations_amount))
        self.window_ui.outputErrorCode.setText(str(result.error_code))

        self.current_interval_a = interval_a
        self.current_interval_b = interval_b


if __name__ == "__main__":
    app = QApplication([])
    window = Main()

    window.show()
    sys.exit(app.exec_())
