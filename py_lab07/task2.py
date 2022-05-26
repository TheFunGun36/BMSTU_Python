# -*- coding: cp1251 -*-

# Функция, принимающая от пользователя натуральное число
def getPositiveIntFromUser(text, lowerBound=0):
    print(text)

    number = input('>')

    while True:
        if not number.isdigit() or int(number) == 0:
            print('Число должно быть натуральным')
        elif int(number) < lowerBound:
            print(f'Число должно быть не меньше {lowerBound}')
        else:
            break
        number = input('>')

    return int(number)


# Функция, принимающая от пользователя действительное число
def getFloatFromUser(text):
    print(text)
    number = float(input('>'))

    #while True:
    #    isOk = True
    #    try:
    #        number = float(number)
    #    except:
    #        print('Число должно быть действительным')
    #        number = input('>')
    #    else:
    #        break;

    return number


# Функция, получающая матрицу от пользователя
def getAArrFromUser(szX, szY):
    A = [[0]*szX]*szY]

    print('Введите через пробел элементы массива A')

    for i in range(szY):
        while True:
            A[i] = list(map(float, input('>').split()))
            if len(A[i]) != szX:
                print('Количество элементов в массиве должно быть равно количеству столбцов\n')
            else: break

    return A


# Функция, печатающая список
def printList(list):
    for el in list:
        print('{:6g}'.format(el), end=' ')
    print()


# Функция, печатающая матрицу    
def printMatrix(arr):
    for st in arr:
        for el in st:
            print('{:6g}'.format(el), end=' ')
        print()


# САМ АЛГОРИТМ

# Инициализируем размеры матрицы
while True:
    szX = getPositiveIntFromUser('Введите число столбцов', 2)
    szY = getPositiveIntFromUser('Введите число строк')
    
    if szX < szY:
        print('Данный алгоритм не может провести операцию над матрицей')
        print('у которой число строк больше числа столбцов')
        print('(если она вычеркнет элементы главной диагонали,')
        print('то у получившейся матрицы в последних строках')
        print('элементов будет больше, чем в первых)')
        print('\nПопробуйте ещё раз:')
    else:
        break

# Получаем матрицу
A = getAArrFromUser(szX, szY)

# Инициализируем доп. матрицу (по заданию)
B = [[i]*(szX - 1) for i in range(szY)]

# Проходимся по каждой строке...
for iy in range(szY):

    # В каждую строку матрицы B записываем все элементы A, кроме элемента главной диагонали матрицы A
    for ix in range(iy):
        B[iy][ix] = A[iy][ix]

    for ix in range(iy, szX - 1):
        B[iy][ix] = A[iy][ix + 1]

# Выводим матрицу
print('Полученная матрица B:')
printMatrix(B)

# Теперь ищем столбец с наибольшим количеством положительных элементов

# Сохраняем лучший результат
maxPosAmount = 0
colIndex = 0

# Проходимся по каждому столбцу...
for ix in range(szX - 1):

    # Счётчик количества положительных элементов
    curPosAmount = 0

    # Просто проходимся по каждому элементу столбца
    for iy in range(szY):
        if B[iy][ix] > 0:
            curPosAmount += 1

    # Если количество положительных чисел больше, чем лучший результат
    if curPosAmount > maxPosAmount:

        # То лучший результат переписываем
        colIndex = ix
        maxPosAmount = curPosAmount

# Проверяем, есть ли вообще у нас положительные элементы
if maxPosAmount == 0:
    print('В матрице нет положительных элементов')
else:
    print(f'В столбце с индексом {colIndex} наибольшее число положительных элементов ({maxPosAmount})')

