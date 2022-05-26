# Функция, принимающая от пользователя натуральное число
def getPositiveIntFromUser(text):
    print(text)

    number = input('>')

    while not number.isdigit() or int(number) == 0:
        print('Число должно быть натуральным')
        number = input('>')

    return int(number)


# Функция, принимающая от пользователя действительное число
def getFloatFromUser(text):
    print(text)
    number = float(input('>'))

    return number


# Функция, принимающая от пользователя список Z
def getZArrFromUser(sz):
    Z = [0]*sz

    print('Введите через пробел элементы массива Z')

    while True:
        Z = list(map(float, input('>').split()))
        if len(Z) != sz:
            print('Количество элементов в массиве должно быть равно количеству столбцов')
        else:
            break

    return Z


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
szX = getPositiveIntFromUser('Введите число столбцов')
szY = getPositiveIntFromUser('Введите число строк')

# Принимаем от пользователя список Z (по заданию)
Z = getZArrFromUser(szX)

# Инициализируем матрицу F
F = [[0]*szX for i in range(szY)]

# Задаём шаг и нач. знач для y
yFirst = getFloatFromUser('Введите начальное значение для y')
yStep = getFloatFromUser('Введите шаг для y')
y = yFirst

# Создаём два списка: для минимальной и строки матрицы F
Wmin = F[0]
Wmax = F[0]

# Кроме того, инициализируем значения мин и макс сумм для соотв. списков
maxSum = 'n'
minSum = 'n'

# Проходимся по каждой строке матрицы
for iy in range(szY):

    # Считаем текущ. сумму...
    currentSum = 0
    for ix in range(szX):
        F[iy][ix] = Z[ix]*(iy + 1)*y
        currentSum += F[iy][ix]

    # Сразу определяем строку матрици с максимальной...
    if maxSum == 'n' or currentSum > maxSum:
        maxSum = currentSum
        Wmax = F[iy]

    # ... и минимальной суммой элементов
    if minSum == 'n' or currentSum < minSum:
        minSum = currentSum
        Wmin = F[iy]
    y += yStep


print('Получившаяся матрица F:')
printMatrix(F)

W = Wmin + Wmax

print('Сформированный список W:')
printList(W)