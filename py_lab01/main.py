import tkinter as tk
from tkinter import messagebox as mb

SHOULD_INPUT_MULTIPLE_NUMBERS = True

def add_two_numbers(val1, val2):
    if len(val1) > 8 or len(val2) > 8:
        raise ValueError("too much digits in a number")

    while len(val1) < 8:
        val1 = '0' + val1
    while len(val2) < 8:
        val2 = '0' + val2

    result_val = [symbol for symbol in val1]

    takeover = 0

    for i in range(7, -1, -1):
        sum = takeover + int(val1[i]) + int(val2[i])
        if sum == 3:
            takeover = 1
            result_val[i] = '1'
        elif sum == 2:
            takeover = 1
            result_val[i] = '0'
        elif sum == 1:
            takeover = 0
            result_val[i] = '1'
        elif sum == 0:
            takeover = 0
            result_val[i] = '0'
        else:
            raise ValueError("non binary number")

    return ''.join(result_val)


def normalize(value):
    if len(value) < 1:
        raise ValueError('empty value')
    result = value
    if value[0] == '-':
        result = [symbol for symbol in value[1:]]

        if len(result) > 8:
            raise ValueError('too much digits in a number')

        while len(result) < 8:
            result.insert(0, '0')

        # negate
        for i in range(len(result)):
            result[i] = '0' if result[i] == '1' else '1'

        # plus1
        result = add_two_numbers(''.join(result), '1')
    else:
        if len(value) > 8:
            raise ValueError('too much digits in a number')
        while len(result) < 8:
            result = '0' + result

    return result


def bin_to_dec(value):
    if len(value) != 8:
        raise ValueError('wrong length')

    result = 0
    k = 1

    for i in range(8):
        if value[i] == '1':
            result += k
        elif value[i] != '0':
            raise ValueError('wrong symbol')

        k *= 2

    return result


def dec_to_bin(value):
    value %= 256
    result = ''
    p = int(pow(2, 7))

    for i in range(7, -1, -1):
        if value >= p:
            result += '1'
            value -= p
        else:
            result += '0'
        p //= 2

    return result


def parse_into_tokens(string):
    result_array = ['']

    if string[0] == '-':
        result_array[-1] = '-'
        string = string[1:]

    for symbol in string:
        if symbol.isdigit():
            result_array[-1] += symbol
        else:
            if len(result_array[-1]) <= 0:
                raise ValueError("unknown token")

            if result_array[-1] == '' or result_array[-1] == '-':
                raise ValueError('unknown token')

            if symbol == '+':
                result_array.append('')
            elif symbol == '-':
                result_array.append('-')
            else:
                raise ValueError("unknown token")

    return result_array


def process_input():
    string = entry_input.get()

    global output_text

    if len(string) <= 0:
        output_text.set('--------')
        return

    try:
        result = parse_into_tokens(string)

        if SHOULD_INPUT_MULTIPLE_NUMBERS:
            for i, el in enumerate(result):
                result[i] = dec_to_bin(int(result[i]))
        else:
            for i, el in enumerate(result):
                result[i] = normalize(el)

    except ValueError:
        output_text.set('--------')
        return

    while len(result) > 1:
        try:
            result[1] = add_two_numbers(result[0], result[1])
        except ValueError:
            output_text.set('--------')
            return
        result.pop(0)

    output_text.set(normalize(result[0]))


def input_filter(event):
    # event.state & 4 - Ctrl,
    if event.state & 4 and event.keysym == 'v':
        return 'break'
    if event.state & 4 and event.keysym == 'c':
        return

    possible_symbols = {'0', '1', 'minus', 'plus', 'BackSpace', 'Left', 'Right', 'Delete'}

    if SHOULD_INPUT_MULTIPLE_NUMBERS:
        for i in range(2, 10):
            possible_symbols.add(str(i))

    if event.keysym not in possible_symbols:
        print(event.keysym)
        return 'break'


def create_stylish_button(tk, window, text, command):
    return tk.Button(window,
                     text=text,
                     command=command,
                     background='#777',
                     foreground='#ddd',
                     font='24',
                     height=1,
                     width=1,
                     bd=0)


window = tk.Tk()
window.title('восьмеричный сумматор')
window.option_add('*Dialog.msg.font', 'Calibri 12')

label_input = tk.Label(window, text='Выражение:', font=('Calibri', 10))

input_text = tk.StringVar()
input_text.trace_add('write', lambda a, b, c: process_input())
entry_input = tk.Entry(window, width=40, textvariable=input_text)
entry_input.bind('<Key>', input_filter)

label_output = tk.Label(window, text='Результат:', font=('Calibri', 10))

# btn_0 = 0
# btn_1 = 1

if SHOULD_INPUT_MULTIPLE_NUMBERS:
    btn = []
    btn.append(create_stylish_button(tk, window, '0', lambda: input_text.set(input_text.get() + '0')))
    btn.append(create_stylish_button(tk, window, '1', lambda: input_text.set(input_text.get() + '1')))
    btn.append(create_stylish_button(tk, window, '2', lambda: input_text.set(input_text.get() + '2')))
    btn.append(create_stylish_button(tk, window, '3', lambda: input_text.set(input_text.get() + '3')))
    btn.append(create_stylish_button(tk, window, '4', lambda: input_text.set(input_text.get() + '4')))
    btn.append(create_stylish_button(tk, window, '5', lambda: input_text.set(input_text.get() + '5')))
    btn.append(create_stylish_button(tk, window, '6', lambda: input_text.set(input_text.get() + '6')))
    btn.append(create_stylish_button(tk, window, '7', lambda: input_text.set(input_text.get() + '7')))
    btn.append(create_stylish_button(tk, window, '8', lambda: input_text.set(input_text.get() + '8')))
    btn.append(create_stylish_button(tk, window, '9', lambda: input_text.set(input_text.get() + '9')))
    for i in range(10):
        if i == 0:
            i = 11
            x = ((i - 1) % 3 + 1) * 35 + 75
            y = ((i - 1) // 3) * 30 + 85
            i = 0
        else:
            x = ((i - 1) % 3 + 1) * 35 + 75
            y = ((i - 1) // 3) * 30 + 85

        btn[i].place(x=x, y=y)
else:
    btn_1 = create_stylish_button(tk, window, '1', lambda: input_text.set(input_text.get() + '1'))
    btn_0 = create_stylish_button(tk, window, '0', lambda: input_text.set(input_text.get() + '0'))
btn_plus = create_stylish_button(tk, window, '+', lambda: input_text.set(input_text.get() + '+'))
btn_minus = create_stylish_button(tk, window, '-', lambda: input_text.set(input_text.get() + '-'))
# btn_1 = tk.Button(window, text='1', command=lambda: input_text.set(input_text.get() + '1'))
# btn_0 = tk.Button(window, text='0', command=lambda: input_text.set(input_text.get() + '0'))
# btn_plus = tk.Button(window, text='+', command=lambda: input_text.set(input_text.get() + '+'))
# btn_minus = tk.Button(window, text='-', command=lambda: input_text.set(input_text.get() + '-'))

output_text = tk.StringVar()
output_text.set('--------')
entry_output = tk.Entry(window, width=8, state='readonly', textvariable=output_text, font=('Consolas', '10'))

label_input.place(x=10, y=0)
entry_input.place(x=10, y=20)

c = 40
cy = 5
if SHOULD_INPUT_MULTIPLE_NUMBERS:
    pass
else:
    btn_0.place(x=0 + c, y=70 + cy)
    btn_1.place(x=35 + c, y=70 + cy)
btn_minus.place(x=0 + c, y=40 + cy)
btn_plus.place(x=35 + c, y=40 + cy)
c1 = -40
label_output.place(x=170 + c1, y=40 + cy)
entry_output.place(x=255 + c1, y=40 + cy)
# label_input.grid(column=0, row=0, columnspan=4)
# entry_input.grid(column=0, row=1, columnspan=4)
# btn_0.grid(column=0, row=2)
# btn_1.grid(column=1, row=2)
# btn_minus.grid(column=2, row=2)
# btn_plus.grid(column=3, row=2)
# label_output.grid(column=4, row=0)
# entry_output.grid(column=4, row=1)

main_menu = tk.Menu(window)
window.config(menu=main_menu)

op_menu = tk.Menu(main_menu)

if SHOULD_INPUT_MULTIPLE_NUMBERS:
    op_menu.add_command(label='0', command=lambda: input_text.set(input_text.get() + '0'))
    op_menu.add_command(label='1', command=lambda: input_text.set(input_text.get() + '1'))
    op_menu.add_command(label='2', command=lambda: input_text.set(input_text.get() + '2'))
    op_menu.add_command(label='3', command=lambda: input_text.set(input_text.get() + '3'))
    op_menu.add_command(label='4', command=lambda: input_text.set(input_text.get() + '4'))
    op_menu.add_command(label='5', command=lambda: input_text.set(input_text.get() + '5'))
    op_menu.add_command(label='6', command=lambda: input_text.set(input_text.get() + '6'))
    op_menu.add_command(label='7', command=lambda: input_text.set(input_text.get() + '7'))
    op_menu.add_command(label='8', command=lambda: input_text.set(input_text.get() + '8'))
    op_menu.add_command(label='9', command=lambda: input_text.set(input_text.get() + '9'))
else:
    op_menu.add_command(label='0', command=lambda: input_text.set(input_text.get() + '0'))
    op_menu.add_command(label='1', command=lambda: input_text.set(input_text.get() + '1'))
op_menu.add_command(label='+ (прибавить)', command=lambda: input_text.set(input_text.get() + '+'))
op_menu.add_command(label='- (вычесть)', command=lambda: input_text.set(input_text.get() + '-'))

main_menu.add_cascade(label='Операция...', menu=op_menu)
main_menu.add_command(label='Очистить', command=lambda: input_text.set(''))
main_menu.add_command(label='О программе',
                      command=lambda: mb.showinfo(
                          title='Информация',
                          message='Данная программа моделирует работу восьмиразрядного сумматора\n\n' +
                                  'Автор: Чепрасов Кирилл Михайлович\n\n' +
                                  'Copyright ©: Poel Pospal Inc, 2002-2021. Ничьи права не защищены. Прав нет.'
                      ))

if SHOULD_INPUT_MULTIPLE_NUMBERS:
    window.geometry('345x220')
else:
    window.geometry('345x115')
window.mainloop()
