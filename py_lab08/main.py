def f(x):
	return x*x - 4


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


def getFloatFromUser(text):
    print(text)
    number = input('>')

    while True:
        isOk = True
        try:
            number = float(number)
        except ValueError:
            print('Число должно быть действительным')
            number = input('>')
        else:
            break;

    return number


def countByRectangles(amountOfDivisions, lowerBound, upperBound):
    area = 0
    divisionSize = (upperBound - lowerBound) / amountOfDivisions
    xValue = lowerBound
    
    for i in range(amountOfDivisions):
        area += f(xValue + divisionSize)
        xValue += divisionSize

    return area * divisionSize


def countByUeddle(amountOfDivisions, lowerBound, upperBound):
    area = 0

    amountOfDivisions += 6 - amountOfDivisions % 6

    divisionSize = (upperBound - lowerBound) / amountOfDivisions
    xValue = lowerBound

    for i in range(0, amountOfDivisions, 6):
        area += f(xValue)
        xValue += divisionSize 
        area += 5*f(xValue)
        xValue += divisionSize
        area += f(xValue)
        xValue += divisionSize
        area += 6*f(xValue)
        xValue += divisionSize
        area += f(xValue)
        xValue += divisionSize
        area += 5*f(xValue)
        xValue += divisionSize
        area += f(xValue)

    return 0.3*divisionSize*area


def printTableHead():
    print('В 2-м и 3-м столбцах будет считаться площадь посчитанная')
    print('соответствующими методами.\n')
    print('+-------------+-------------+-------------+')
    print('|Кол-во отрезк|прав прямоуг.|метод Уэддля |')
    print('+-------------+-------------+-------------+')


def printTableElement(i, a1, a2):
    i = '{:g}'.format(i).center(13)
    a1 = '{:g}'.format(a1).center(13)
    a2 = '{:g}'.format(a2).center(13)

    print('|' + i + '|' + a1 + '|' + a2 + '|')


def printTableEnd():
    print('+-------------+-------------+-------------+')


# Возвращает: количество итерация, нижний предел, верхний предел
def provideInput():
    lowerBound = getFloatFromUser('Введите нижний предел интегрирования')
    upperBound = getFloatFromUser('Введите верхний предел интегрирования')

    amountOfDivisions1 = getPositiveIntFromUser('Введите количество делений кривой')

    amountOfDivisions2 = getPositiveIntFromUser('Введите количество делений кривой ещё раз')

    if lowerBound > upperBound:
        print('В вводе нижний предел больше верхнего. При вычислении, они будут поменяны местами')
        lowerBound, upperBound = upperBound, lowerBound

    return amountOfDivisions1, amountOfDivisions2, lowerBound, upperBound


def getRectMethodAmountOfDivisions(accuracity, lowerBound, upperBound):
    prevVal = -1
    currentVal = 0

    #iterationsNum = 1
    iterationsNum = 0

    while abs(currentVal - prevVal) > accuracity:
        #iterationsNum *= 2
        iterationsNum += 1

        prevVal = currentVal
        currentVal = countByRectangles(iterationsNum, lowerBound, upperBound)

    return iterationsNum, currentVal


def getUedMethodAmountOfDivisions(accuracity, lowerBound, upperBound):
    prevVal = -1
    currentVal = 0

    iterationsNum = 0

    while abs(currentVal - prevVal) > accuracity:
        iterationsNum += 6
        prevVal = currentVal
        currentVal = countByUeddle(iterationsNum, lowerBound, upperBound)

    return iterationsNum, currentVal


amountOfDivisions1, amountOfDivisions2, lowerBound, upperBound = provideInput()

printTableHead()

areaRect1 = countByRectangles(amountOfDivisions1, lowerBound, upperBound)
areaUed1 = countByUeddle(amountOfDivisions1, lowerBound, upperBound)

printTableElement(amountOfDivisions1, areaRect1, areaUed1)

areaRect2 = countByRectangles(amountOfDivisions2, lowerBound, upperBound)
areaUed2 = countByUeddle(amountOfDivisions2, lowerBound, upperBound)

printTableElement(amountOfDivisions2, areaRect2, areaUed2)

printTableEnd()

avgVal = (areaRect1 + areaRect2 + areaUed1 + areaUed2) / 4

rectDeviation = max(abs(avgVal - areaRect1), abs(avgVal - areaRect2))
uedDeviation = max(abs(avgVal - areaUed1), abs(avgVal - areaUed2))

if rectDeviation > uedDeviation:
    print('Метод правых прямоугольников показал большее отклонение, чем метод Уэддля.')
else:
    print('Метод Уэддля показал большее отклонение, чем метод правых прямоугольников.')

accuracity = getFloatFromUser('Введите наибольшую допустимую погрешность')

area = 0

if rectDeviation > uedDeviation:
    maxAmountOfIterations, area = getRectMethodAmountOfDivisions(accuracity, lowerBound, upperBound)
else:
    maxAmountOfIterations, area = getUedMethodAmountOfDivisions(accuracity, lowerBound, upperBound)

print('Допустимый результат для введённой погрешности достигается после введения')
print(f'{maxAmountOfIterations} отрезков. Площадь при этом равна {area}')