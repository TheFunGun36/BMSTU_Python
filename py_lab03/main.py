# Кодировка UTF-8,
# Вариант 3, 1
# Метод Ньютона для уточнения корней
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import pyqtSlot
import MathModule
import UIMainWindow
from Graph import Graph
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

        self.window_ui.buildGraphButton.clicked.connect(
            self.show_graph_button
        )

    def set_table(self, table):
        for i in range(len(table) - 1, 0, -1):
            if table[i].error_code == 1:
                table.pop(i)

        for i in range(len(table) - 2, -1, -1):
            if fabs(table[i].root - table[i + 1].root) < 1e-5:
                table.pop(i)

        self.window_ui.outputTable.setRowCount(len(table))

        for index, table_element in enumerate(table):
            index_str = QTableWidgetItem(str(index))
            self.window_ui.outputTable.setItem(index, 0, index_str)

            interval_str = '[{:g}, '.format(table_element.interval_a)
            interval_str += '{:g}]'.format(table_element.interval_b)
            interval_str = QTableWidgetItem(interval_str)
            self.window_ui.outputTable.setItem(index, 1, interval_str)

            if table_element.root is not None:
                root_str = '{:g}'.format(table_element.root)
                root_str = QTableWidgetItem(root_str)
                func_val_str = '{:2.2e}'.format(table_element.function_value)
                func_val_str = QTableWidgetItem(func_val_str)
            else:
                root_str = QTableWidgetItem('-')
                func_val_str = QTableWidgetItem('-')

            self.window_ui.outputTable.setItem(index, 2, root_str)
            self.window_ui.outputTable.setItem(index, 3, func_val_str)

            iterations = QTableWidgetItem(str(table_element.iterations_amount))
            self.window_ui.outputTable.setItem(index, 4, iterations)

            error_code = QTableWidgetItem(str(table_element.error_code))
            self.window_ui.outputTable.setItem(index, 5, error_code)

    def calculate_values(self, interval_a, interval_b, step, accuracity):
        table = MathModule.get_root_table(
            MathModule.function,
            interval_a,
            interval_b,
            step,
            accuracity)

        self.root_list = []

        for el in table:
            if el.error_code == 0:
                self.root_list.append(el.root)

        self.set_table(table)

    @pyqtSlot()
    def calculate_button_click(self):
        interval_a = self.window_ui.inputIntervalLeft.text()
        interval_b = self.window_ui.inputIntervalRight.text()
        step = self.window_ui.inputStep.text()
        accuracity = self.window_ui.inputAccuracity.text()

        try:
            interval_a = float(interval_a)
            interval_b = float(interval_b)
            step = float(step)
            accuracity = float(accuracity)
        except ValueError:
            QMessageBox.about(
                self,
                'Ошибка',
                'Должны быть введены числа'
            )

        if step <= 0 or accuracity <= 0:
            QMessageBox.about(
                self,
                'Ошибка',
                'Шаг и точность должны быть положительными'
            )
            return

        if interval_a > interval_b:
            interval_a, interval_b = interval_b, interval_a

        self.calculate_values(
            interval_a,
            interval_b,
            step,
            accuracity
        )

        self.current_interval_a = interval_a
        self.current_interval_b = interval_b

    @pyqtSlot()
    def show_graph_button(self):
        if self.current_interval_a is None:
            QMessageBox.about(
                self,
                'Ошибка',
                'Не заданы пределы расчёта функции'
            )
        else:
            Graph.create_window(
                None,
                self.current_interval_a,
                self.current_interval_b,
                self.root_list
            )


if __name__ == "__main__":
    app = QApplication([])
    window = Main()

    window.show()
    sys.exit(app.exec_())
