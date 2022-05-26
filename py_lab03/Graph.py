import matplotlib.pyplot as mpl
import MathModule
from numpy import linspace


class Graph(object):
    def __init__(self):
        pass

    def create_window(self, interval_a, interval_b, root_list):
        mpl.title('График функции')
        mpl.axhline(0, color='black')
        mpl.axvline(0, color='black')

        x = [i for i in linspace(interval_a, interval_b, 300)]
        y = [MathModule.function(i) for i in x]
        # dy = [derivative(MathModule.function, i) for i in x]

        values_in_roots = [MathModule.function(i) for i in root_list]

        mpl.plot(x, y, 'b')
        mpl.plot(root_list, values_in_roots, 'ro')

        extremum_points = []
        extremum_values = []

        for i in range(1, len(y) - 1):
            if y[i - 1] <= y[i] > y[i + 1] or y[i - 1] >= y[i] < y[i + 1]:
                extremum_points.append(x[i])
                extremum_values.append(y[i])

        mpl.plot(extremum_points, extremum_values, 'go')

        mpl.grid()
        mpl.show()
