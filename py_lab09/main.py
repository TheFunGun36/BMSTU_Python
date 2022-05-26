# Лабораторная работа №9
# Написать программу, реализующую меню:
# 1. Ввод строки.
# 2. Настройка шифрующего алгоритма.
# 3. Шифрование строки, используя шифр Виженера.
# 4. Расшифровывание строки.

# Чепрасов Кирилл Михайлович ИУ7-16Б

#1040 - 1071 больш‬ и 1072 - 1103 мал

def getStringFromUser(allowSpaces=False):
	print('Введите строку:')
	string = ''
	isError = True

	while isError:
		isError = False
		string = input('>')

		for symbol in string:
			symbolCode = ord(symbol)
			if not (65 <= symbolCode <= 90
				or 97 <= symbolCode <= 122
				or allowSpaces and symbolCode == 32
				or 1040 <= symbolCode <= 1103):
				isError = True
				break

		if isError:
			print('Вы ввели недопустимые символы.')
			print('Вводить можно только буквы латинского алфавита')
			print('Попробуйте ещё раз:')

	return string


def getKeyFromUser():
	strKey = getStringFromUser()

	key = [0] * len(strKey)

	for i, symbol in enumerate(strKey):
		symbolCode = ord(symbol)

		if symbolCode >= 1072:
			key[i] = -(symbolCode - 1072)
		elif symbolCode >= 1040:
			key[i] = -(symbolCode - 1040)
		elif symbolCode >= 97:
			key[i] = symbolCode - 97
		else:
			key[i] = symbolCode - 65

	return key


def getKeycodeArrayFromString(string):
	keycodeArray = [0] * len(string)
	for i, symbol in enumerate(string):
		keycodeArray[i] = ord(symbol)

	return keycodeArray


def getStringFromKeycodeArray(keycodeArray):
	string = [0] * len(keycodeArray)
	for i, keycode in enumerate(keycodeArray):
		string[i] = chr(keycode)

	string = ''.join(string)

	return string


def encryptString(string, key):
	strLength = len(string)
	stringKeycodes = getKeycodeArrayFromString(string)

	iForKey = 0
	for i in range(strLength):
		if stringKeycodes[i] == 32:
			continue

		isRus = stringKeycodes[i] >= 1040
		isSmall = stringKeycodes[i] >= 97 if not isRus else stringKeycodes[i] >= 1072
		stringKeycodes[i] += abs(key[iForKey % len(key)])

		if isRus:
			while isSmall and stringKeycodes[i] > 1103\
				or not isSmall and stringKeycodes[i] > 1071:
				stringKeycodes[i] -= 32
		else:
			while isSmall and stringKeycodes[i] > 122\
				or not isSmall and stringKeycodes[i] > 90:
				stringKeycodes[i] -= 26

		iForKey += 1

	resultString = getStringFromKeycodeArray(stringKeycodes)

	return resultString


def decryptString(string, key):
	strLength = len(string)
	stringKeycodes = getKeycodeArrayFromString(string)

	iForKey = 0
	for i in range(strLength):
		if stringKeycodes[i] == 32:
			continue

		isRus = stringKeycodes[i] >= 1040
		isSmall = stringKeycodes[i] >= 97 if not isRus else stringKeycodes[i] >= 1072
		stringKeycodes[i] -= abs(key[iForKey % len(key)])

		if isRus:
			while isSmall and stringKeycodes[i] < 1072\
				or not isSmall and stringKeycodes[i] < 1040:
				stringKeycodes[i] += 32
		else:
			while isSmall and stringKeycodes[i] < 97\
				or not isSmall and stringKeycodes[i] < 65:
				stringKeycodes[i] += 26

		iForKey += 1

	resultString = getStringFromKeycodeArray(stringKeycodes)

	return resultString


def isGoodInput(string, key):
	isGood = True
	if string == '':
		print('Не задана строка для совершения операции')
		isGood = False
	if key == []:
		print('Не задан ключ для совершения операции')
		isGood = False

	return isGood


def keyToString(key):
	string = [0] * len(key)
	for i, keycode in enumerate(key):
		if key[i] > 0:
			string[i] = chr(key[i] + 65)
		else:
			string[i] = chr(-key[i] + 1040)

	string = ''.join(string)

	return string


string = ''
key = []

userInput = ''
while userInput != '0':
	print('''Введите номер команд, которую требуется выполнить:
1. Ввести строку
2. Ввести шифровальный ключ
3. Раcшифровать введённую строки
4. Зашифровать введённую строки
0. Выход из программы
''')

	userInput = input('>')

	if userInput == '0':
		break
	elif userInput == '1':
		string = getStringFromUser(allowSpaces=True)
	elif userInput == '2':
		key = getKeyFromUser()
	elif userInput == '3' or userInput == '4':
		if isGoodInput(string, key):
			print('Исходная строка:       ' + string)

			print('Ключ:                  ' + keyToString(key))

			if userInput == '3':
				stringDecrypted = decryptString(string, key)
				print('Расшифрованная строка: ' + stringDecrypted)
			else:
				stringEncrypted = encryptString(string, key)
				print('Зашифрованная строка:  ' + stringEncrypted)

		print('Для продолжения нажмите enter... ')
		input()
	else:
		pass

	print('---------------------------------------')