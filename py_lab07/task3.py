def getArrFromUser(szX, szY):
    A = [[0]*szX for i in range(szY)]

    print('Введите через пробел элементы массива')

    for i in range(szY):
        while True:
            A[i] = list(map(float, input('>').split()))
            if len(A[i]) != szX:
                print('Количество элементов в массиве должно быть равно количеству столбцов\n')
            else: break

    return A


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


# Функция, печатающая матрицу
def printMatrix(arr):
    for st in arr:
        for el in st:
            print('{:6g}'.format(el), end=' ')
        print()


def getMaxAmountOfZeros(arr, szX, szY):
    bestIndex = 0
    bestAmount = 0
    for ix in range(szX):
        counter = 0
        for iy in range(szY):
            if arr[iy][ix] == 0:
                counter += 1
        if counter > bestAmount:
            bestIndex = ix
            bestAmount = counter

    return bestIndex, bestAmount


def putColumnToTheEnd(arr, index, szX, szY):
    column = [arr[i][index] for i in range(szY)]

    for ix in range(index, szX - 1):
        for iy in range(szY):
            arr[iy][ix] = arr[iy][ix + 1]

    for i in range(szY):
        arr[i][-1] = column[i]

    return arr


szX = getPositiveIntFromUser('Введите ширину матрицы (количество столбцов)')
szY = getPositiveIntFromUser('Введите высоту матрицы (количество строк)')
arr = getArrFromUser(szX, szY)

index, zeros = getMaxAmountOfZeros(arr, szX, szY)

if zeros == 0:
    print('В матрице нет нулей')
else:
    print(f'Наибольшее количество нулей было найдено под индексом {index}.')
    print(f'Количество нулей в этом столбце {zeros}')

    arr = putColumnToTheEnd(arr, index, szX, szY)

    print(f'Столбец {index} был перенесён в конец. Получившаяся матрица')
    printMatrix(arr)
