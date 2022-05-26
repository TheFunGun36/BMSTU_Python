from math import fabs, sin, cos
from scipy.misc import derivative

#def derivative(func, x):
#    dx = 1e-10
#    return (func(x + dx) - func(x)) / dx

# Let error codes be:
# 0 for OK
# 1 for ROOT NOT FOUND
# 2 for TOO MUCH ITERATIONS


class TableElement:
    def __init__(self):
        self.interval_a = None
        self.interval_b = None
        self.root = None
        self.function_value = None
        self.iterations_amount = None
        self.error_code = None


def function(value):
    return sin(value)  # value*value - 4#sin(value)
    # return 2 * value * value * value + 7 * value * value + 4 * value - 3


def function_derivative(value):
    return derivative(function, value)


def is_equal(value_left, value_right, accuracity):
    return fabs(value_left - value_right) < accuracity


def find_root_newton_method(func, base_value, accuracity, a, b):
    new_root = base_value
    root = 2 * new_root + 2 * accuracity

    iterations_amount = 0

    while fabs(new_root - root) > accuracity:
        iterations_amount += 1
        root = new_root
        # ddf = derivative(func, root)

        new_root = root - func(root) \
            / derivative(func, root)
        if not a <= new_root <= b:
            new_root = (new_root + root) / 2

        if iterations_amount >= 10000:
            return new_root, iterations_amount

    return new_root, iterations_amount


def find_root_chord_method(func, base_value, accuracity, a, b):
    iterations_amount = 1
    new_root = 0

    try:
        new_root = a - (b - a) * function(a) / (function(b) - function(a))

        while (fabs(new_root - a) > accuracity):
            a = b
            b = new_root
            new_root = a - (b - a) * function(a) / (function(b) - function(a))
            iterations_amount += 1

            if iterations_amount >= 10000:
                break
    finally:
        return new_root, iterations_amount


def find_root(func, table_element: TableElement, accuracity):
    root = (table_element.interval_b + table_element.interval_a) / 2

    if table_element.interval_a > 0 and table_element.interval_b > 0 \
        or table_element.interval_a > 0 and table_element.interval_b > 0:
            table_element.iterations_amount = 0
            table_element.error_code = 1

    try:
        root, iterations_amount = find_root_chord_method(
            func,
            root,
            accuracity,
            table_element.interval_a,
            table_element.interval_b
        )
    except ZeroDivisionError:
        table_element.root = root
        table_element.error_code = 3
        return

    if table_element.interval_a <= root <= table_element.interval_b:
        table_element.root = root
        table_element.function_value = func(root)
        table_element.iterations_amount = iterations_amount
        table_element.error_code = 0 if iterations_amount < 10000 else 2
    else:
        table_element.iterations_amount = iterations_amount
        table_element.error_code = 1


def get_root_table(func, interval_a, interval_b, step, accuracity):
    root_amount = int((interval_b - interval_a) / step)
    table = [TableElement() for i in range(root_amount)]

    for i in range(root_amount):
        table[i].interval_a = i * step + interval_a
        table[i].interval_b = (i + 1) * step + interval_a
        find_root(func, table[i], accuracity)

    return table


def find_extremum_points(interval_a, interval_b):
    table = get_root_table(
        function_derivative,
        interval_a,
        interval_b,
        (interval_b - interval_a) / 300, 1e-10
    )

    inflection_point_list = []

    for element in table:
        if element.error_code == 0:
            inflection_point_list.append(element.root)

    return inflection_point_list
