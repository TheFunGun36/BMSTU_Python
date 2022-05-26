from math import sqrt, floor


def get_type(element):
    a, b, e = '0', '0', '0'
    found_e = element.find('e')

    if found_e >= 0:
        a = element[:found_e]
        e = element[found_e + 1:]
    else:
        a = element

    found_dot = a.find('.')
    if found_dot >= 0:
        b = a[found_dot + 1:]
        a = a[:found_dot]

    if len(a) > 0 and a[0] == '-':
        a = a[1:]

    is_neg_e = False

    if len(e) > 0 and e[0] == '-':
        e = e[1:]
        is_neg_e = True

    if len(a) <= 0 or len(b) <= 0 or len(e) <= 0:
        return str

    if not (a.isdigit() and b.isdigit() and e.isdigit()):
        return str

    if e != '0':
        if is_neg_e:
            if int(a) == 0:
                return float

            b = b.replace('0', '')
            if len(b) > 0:
                return float

            zeros = 0
            while len(a) > 0 and a[-1] == '0':
                zeros += 1
                a = a[:-1]
            if zeros >= abs(int(e)):
                return int
            else:
                return float
        else:
            while len(b) > 0 and b[-1] == '0':
                b = b[:-1]

            if len(b) <= int(e):
                return int
            else:
                return float
    else:
        b = b.replace('0', '')

        if len(b) > 0:
            return float
        else:
            return int


# Возвращает array, min_val, max_val
def initialize_array(size):
    array = [0] * size
    a = 1
    t = a
    array[0] = t

    for i in range(2, size + 1):
        t *= a * a * (2 * (i - 1) - 1) ** 2
        t /= 2 * (i - 1)
        t /= 2 * i - 1
        array[i - 1] = t

    if a > 0:
        min_val = size - 1
        max_val = 0
    else:
        min_val = 0
        max_val = size - 1
    return array, min_val, max_val


def get_int_from_user(string, lower_bound=0, upper_bound=1e10):
    print(string)
    number = input('>')
    while not number.isdigit() or not (lower_bound <= int(number) <= upper_bound):
        print('Некорректный ввод. Попробуйте ещё раз')
        number = input('>')
    return int(number)


def print_array(array):
    cc = 0
    if len(array) > 0:
        for el in array:
            if isinstance(el, str):
                print('\'', el, '\', ', end='', sep='')
            else:
                print('{:g}, '.format(el), end='')

            if cc >= 10:
                print()
                cc = 0
            else:
                cc += 1
        print()
    else:
        print('\t<Список пуст>')


def find_ext_val_index(array, find_max=True):
    idx = 'n'
    if find_max:
        for i, el in enumerate(array):
            if not isinstance(el, str) and (idx == 'n' or el > array[idx]):
                idx = i
    else:
        for i, el in enumerate(array):
            if not isinstance(el, str) and (idx == 'n' or el < array[idx]):
                idx = i
    return idx


def get_primes_under(value):
    primes = []
    for i in range(2, value + 1):
        is_prime = True
        # for j, el in enumerate(primes):
        #     if i % el == 0:
        #         is_prime = False
        #         break
        # ИЛИ
        for j in range(2, floor(sqrt(i)) + 1):
            if i % j == 0:
                is_prime = False
                break
        # понятия не имею, что проще на дальней дистанции. Вроде как простых чисел
        # позже становиться мало, при больших числах, так что первый вариант выглядит весело.
        # С другой стороны, корень из 500-го простого числа равен 59 (окр. вниз), так что такие вот дела

        if is_prime:
            primes.append(i)

    return primes


arr = []
minValIndex = 'n'
maxValIndex = 'n'
amountOfStrings = 0

inpt = ''
while True:  # inpt != '0':
    print('''Выберите команду:
0 - выход из программы
1 - инициализация списка элементами ряда
2 - добавление элемента в список
3 - удалить элемент из списка
4 - очистить список
5 - поиск k-го экстремума
6 - поиск последовательности отрицательных чисел, модуль которых - простое число
7 - поиск последовательности, включающую наибольшее кол-во слов, состоящих из символов предыдущего слова
8 - вывести текущий список
>''', end='')

    inpt = input()

    if inpt == '0':
        break
    elif inpt == '1':
        n = get_int_from_user('Введите число элементов', lower_bound=1)
        arr, minValIndex, maxValIndex = initialize_array(n)
        if len(arr) < 10:
            print('Получившийся список:')
            print_array(arr)
    elif inpt == '2':
        inpt = input('Введите вставляемый элемент\n>')

        typ = get_type(inpt)
        if typ == int:
            inpt = int(inpt)
        elif typ == float:
            inpt = float(inpt)
        else:
            inpt = str(inpt)
            amountOfStrings += 1

        index = get_int_from_user(
            'Введите номер, под которым будет находиться элемент',
            lower_bound=1, upper_bound=len(arr) + 1)
        index -= 1

        if not isinstance(inpt, str):
            if maxValIndex == 'n' or inpt > arr[maxValIndex]:
                maxValIndex = index
            elif maxValIndex >= index:
                maxValIndex += 1

            if minValIndex == 'n' or inpt < arr[minValIndex]:
                minValIndex = index
            elif minValIndex >= index:
                minValIndex += 1
        else:
            if maxValIndex >= index:
                maxValIndex += 1
            if minValIndex >= index:
                minValIndex += 1

        arr.insert(index, inpt)

        if len(arr) < 10:
            print('Получившийся список:')
            print_array(arr)
    elif inpt == '3':

        if len(arr) == 1:
            arr = []
            minValIndex = 'n'
            maxValIndex = 'n'
        elif len(arr) > 0:
            n = get_int_from_user('Введите номер удаляемого элемента', 1, len(arr) + 1)
            n -= 1

            if isinstance(arr[n], str):
                amountOfStrings -= 1

            arr.pop(n)

            if n == minValIndex:
                minValIndex = find_ext_val_index(arr, False)
            if n == maxValIndex:
                maxValIndex = find_ext_val_index(arr, True)

            print('Элемент успешно удалён')
            if len(arr) < 10:
                print('Получившийся список:')
                print_array(arr)
        else:
            print('Невозможно удалить элементы из пустого списка')
    elif inpt == '4':
        arr = []
        minValIndex = 'n'
        maxValIndex = 'n'
        amountOfStrings = 0
        print('Список очищен')
    elif inpt == '5':
        if amountOfStrings > 0:
            print('Нельзя выполнить операцию со списком, в котором есть строка')
        if len(arr) > 0:
            k = get_int_from_user('Введите номер экстремума, который вы хотите найти', 1, len(arr))
            i = 0

            for i, el in enumerate(arr):
                # if isinstance(el, str):
                #     continue

                if el == arr[maxValIndex]\
                        or el == arr[minValIndex]:
                    k -= 1

                if k <= 0:
                    break

            if k > 0:
                print('Заданное число превышает количество экстремумов в списке')
            else:
                print('Искомый экстремум находится под номером {:d}, и равен {:g}'.format(i + 1, arr[i]))
        else:
            print('Невозможно выполнить операцию с пустым списком')
    elif inpt == '6':
        bestIndex = 0
        bestList = []
        currentIndex = 0
        currentList = []
        primeList = get_primes_under(1500)
        primeIndex = 0
        for i, el in enumerate(arr):
            if not isinstance(el, int) or el > -2:
                if len(currentList) > len(bestList):
                    bestList = currentList
                    bestIndex = currentIndex
                currentList = []
                currentIndex = i + 1
                primeIndex = 0
                continue

            el = -el

            while primeIndex < len(primeList):
                if el < primeList[primeIndex]:
                    if len(currentList) > len(bestList):
                        bestList = currentList
                        bestIndex = currentIndex
                    currentList = []
                    currentIndex = i + 1
                    primeIndex = 0
                    break
                elif el == primeList[primeIndex]:
                    primeIndex += 1
                    currentList.append(-el)
                    break
                else:
                    primeIndex += 1

        if len(currentList) > len(bestList):
            bestList = currentList
            bestIndex = currentIndex

        print('Найденная последовательность:')
        print_array(bestList)
        print('она начинается с {:d}-го элемента'.format(bestIndex + 1))
    elif inpt == '7':
        bestIndex = 0
        bestList = []
        currentIndex = 0
        currentList = []
        symbolList = []
        for i, word in enumerate(arr):
            if not isinstance(word, str):
                if len(currentList) > len(bestList):
                    bestIndex = currentIndex
                    bestList = currentList
                currentIndex = 0
                currentList = []
                symbolList = []

                if i + 1 < len(arr) and isinstance(arr[i + 1], str):
                    symbolList = [sym for sym in arr[i + 1]]
                continue

            for sym in word:
                if not (sym in symbolList):
                    if len(currentList) > len(bestList):
                        bestIndex = currentIndex
                        bestList = currentList
                    currentIndex = 0
                    currentList = []
                    symbolList = []
                    if i + 1 < len(arr) and isinstance(arr[i + 1], str):
                        symbolList = [s for s in arr[i + 1]]
                    break

            currentList.append(word)
            symbolList = [sym for sym in word]

        if len(currentList) > len(bestList):
            bestList = currentList
            bestIndex = currentIndex

        print('Найденная последовательность:')
        print_array(bestList)
        print('она начинается с {:d}-го элемента'.format(bestIndex + 1))
    elif inpt == '8':
        print('Текущий список:')
        print_array(arr)
    else:
        print('Ошибка ввода')

    input('Для продолжения, введите enter...')
    print('\n////////////////////////////////////////////////////////////\n')
