import tkinter as tk
import time
import random


def comb_sort(array):
    shrink_factor = 4/5
    current_gap = int(len(array) * shrink_factor)

    while current_gap > 0:
        for i in range(len(array) - current_gap):
            if array[i] > array[i + current_gap]:
                array[i], array[i + current_gap] = array[i + current_gap], array[i]

        current_gap = int(current_gap * shrink_factor)

    return array


def is_number(value):
    try:
        value = float(value)
    except ValueError:
        return False
    return True


def parse_array(array_str: str):
    array = array_str.split(' ')

    while True:
        try:
            array.remove('')
        except ValueError:
            break

    for i, el in enumerate(array):
        if not is_number(el):
            raise ValueError('Ошибка: должны быть введены числа')
        else:
            array[i] = float(el)

    if len(array) <= 1:
        raise ValueError('Ошибка: слишком мало элементов')

    return array


def represent_array(array):
    array = [str(el) for el in array]
    return ' '.join(array)


def sort_button_command(array_str, output_string: tk.StringVar, output_time_string: tk.StringVar):
    array = list()

    try:
        array = parse_array(array_str)
    except ValueError as c:
        output_string.set(c)
        return

    time_stamp_begin = time.time()
    array = comb_sort(array)
    time_stamp_end = time.time()

    array = represent_array(array)
    time_str = '{:g}'.format(1e3 * (time_stamp_end - time_stamp_begin))  # '{:.6f}'.format((time_stamp_end - time_stamp_begin) * 1000000)
    output_time_string.set(time_str)
    output_string.set(array)


def test(array):
    time_stamp_begin = time.time()
    comb_sort(array)
    time_stamp_end = time.time()
    return time_stamp_end - time_stamp_begin


def generate_random_array(size: int):
    array = [0] * size

    for i in range(size):
        array[i] = random.randint(0, size)

    return array


def generate_ascending_array(size: int):
    array = [0] * size

    for i in range(1, size):
        array[i] = random.randint(array[i - 1], array[i - 1] + 10)

    return array


def generate_descending_array(size: int):
    array = [size * 10] * size

    for i in range(1, size):
        array[i] = random.randint(array[i - 1] - 10, array[i - 1])

    return array


def only_int_filter(e, string_var: tk.StringVar):
    if e.char.isdigit() and len(string_var.get()) < 6\
            or e.keysym == 'Delete'\
            or e.keysym == 'BackSpace'\
            or e.keysym == 'Left'\
            or e.keysym == 'Right'\
            or e.keysym == 'Tab':
        return
    return 'break'


def get_time_measures(sizes_str):
    result = [0.0 for i in range(9)]

    for i in range(3):
        if len(sizes_str[i]) <= 0:
            continue

        size = int(sizes_str[i])

        test_array = generate_random_array(size)
        result[i] = test(test_array)

        test_array = generate_ascending_array(size)
        result[i + 3] = test(test_array)

        test_array = generate_descending_array(size)
        result[i + 6] = test(test_array)

    return result


def normalize_number(val):
    return '{:g} мс'.format(val * 1e3)
    # if val > 1e-1:
    #     return '{:.6f} с'.format(val)
    # elif val > 1e-4:
    #     return '{:.6f} мс'.format(val * 1e3)
    # else:
    #     return '{:.6f} нс'.format(val)


def measure_button_click(string_vars, sizes_str):
    time_measures = get_time_measures(sizes_str)

    for i, string_var in enumerate(string_vars):
        string_var.set(normalize_number(time_measures[i]))


def sort_capability(window: tk.Tk):
    array_input_label = tk.Label(text='Введите через пробел элементы массива:')
    array_input_label.place(x=0, y=0)

    array_input_string = tk.StringVar()
    time_output_string = tk.StringVar()

    array_input_entry = tk.Entry(width=35, textvariable=array_input_string)
    array_input_entry.place(x=0, y=20)
    array_input_entry.bind('<Return>', lambda e: sort_button_command(array_input_string.get(),
                                                                     array_output_string,
                                                                     time_output_string))

    array_output_string = tk.StringVar()
    array_output_entry = tk.Entry(width=35, state='readonly', textvariable=array_output_string)
    array_output_entry.place(x=0, y=41)

    clean_button = tk.Button(text='Очистить', command=lambda: array_input_string.set(''))
    clean_button.place(x=290, y=3)

    sort_button = tk.Button(text='Отсортировать', command=lambda:
                            sort_button_command(array_input_string.get(),
                                                array_output_string,
                                                time_output_string))

    sort_button.place(x=290, y=33)

    time_label = tk.Label(text='Затраченное время:')
    time_label.place(x=0, y=62)

    time_output_entry = tk.Entry(width=10, state='readonly', textvariable=time_output_string)
    time_output_entry.place(x=133, y=62)

    nanoseconds_label = tk.Label(text='миллисекунд (1e-3)')
    nanoseconds_label.place(x=222, y=62)


def time_table(window: tk.Tk):
    array_size_strings = [tk.StringVar() for i in range(3)]

    array_size_label = tk.Label(text='Размерности массивов:')
    array_size_label.place(x=140, y=100)

    array_size_entrys = [tk.Entry(width=6, textvariable=array_size_strings[i]) for i in range(3)]

    array_size_entrys[0].bind('<Key>', lambda e: only_int_filter(e, array_size_strings[0]))
    array_size_entrys[1].bind('<Key>', lambda e: only_int_filter(e, array_size_strings[1]))
    array_size_entrys[2].bind('<Key>', lambda e: only_int_filter(e, array_size_strings[2]))
    for i in range(3):
        array_size_entrys[i].place(x=(105 + 86 * i), y=120)

    random_array_label = tk.Label(text='Случайный:')
    ascending_array_label = tk.Label(text='Восходящий:')
    descending_array_label = tk.Label(text='Нисходящий:')

    random_array_label.place(x=0, y=141)
    ascending_array_label.place(x=0, y=161)
    descending_array_label.place(x=0, y=181)

    time_out_table_string = [tk.StringVar() for i in range(9)]  # i = x + y * size_x

    measure_button = tk.Button(text='Замерить', command=lambda:
                               measure_button_click(time_out_table_string,
                                                    [array_size_strings[i].get() for i in range(3)]))
    measure_button.place(x=173, y=205)

    time_out_table_entry = [tk.Entry(width=10, state='readonly', textvariable=time_out_table_string[i]) for i in
                            range(9)]

    for i, el in enumerate(time_out_table_entry):
        x = (i % 3) * 86 + 88
        y = (i // 3) * 21 + 141

        el.place(x=x, y=y)


def main():
    window = tk.Tk()
    window.title('Сортировка расчёской')

    sort_capability(window)

    time_table(window)

    window.geometry("420x240")
    window.mainloop()


if __name__ == '__main__':
    main()
