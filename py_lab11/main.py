import pickle
from os import path

filename = ""


def addRecord(filename):
	tableElement = {}
	
	f = open(filename, 'rb')
	fields = pickle.load(f)
	f.close()

	for el in fields:
		print(f'Введите значение для поля "{el}":')
		tableElement[el] = input('>')


	f = open(filename, 'ab')
	pickle.dump(tableElement, f)
	f.close()


def printTableHead(fields):
	print('+', end='')
	for el in fields:
		print('---------------------+', end='')
	print()
	
	print('|', end='')
	for el in fields:
		print(el.center(21), end='|')
	print()

	print('+', end='')
	for el in fields:
		print('---------------------+', end='')
	print()


def printTableElement(dict, fields):
	print('|', end='')
	for el in fields:
		print(dict[el].center(21), end='|')
	print()


def printTableEnd(fields):
	print('+', end='')
	for el in fields:
		print('---------------------+', end='')
	print()

	
def printDatabase(filename):
	f = open(filename, 'rb')
	fields = pickle.load(f)

	printTableHead(fields)

	try:
		while True:
			tableElement = pickle.load(f)
			printTableElement(tableElement, fields)
	except EOFError:
		pass

	printTableEnd(fields)

	f.close()


def printNFindOneField(filename):
	fieldName = input('Введите название поля, по которому вы хотите совершить поиск:\n>')

	f = open(filename, 'rb')
	fields = pickle.load(f)

	if not fieldName in fields:
		print(f'Поля "{fieldName}" нет в базе данных')
		f.close()
		return

	searchFor = input('Введите значение, которое должно быть у элемента таблицы\n>')

	print('Найденные совпадения:')
	printTableHead(fields)

	try:
		while True:
			tableElement = pickle.load(f)

			if tableElement[fieldName] == searchFor:
				printTableElement(tableElement, fields)
	except EOFError:
		pass

	printTableEnd(fields)

	f.close()


def printNFindTwoFields(filename):
	f = open(filename, 'rb')
	fields = pickle.load(f)


	fieldName1 = input('Введите название поля, по которому вы хотите совершить поиск:\n>')

	if not fieldName1 in fields:
		print(f'Поля "{fieldName1}" нет в базе данных')
		f.close()
		return
	searchFor1 = input('Введите значение, которое должно быть у элемента таблицы\n>')

	fieldName2 = input('Введите название другого поля, по которому вы хотите совершить поиск:\n>')

	if not fieldName2 in fields:
		print(f'Поля "{fieldName2}" нет в базе данных')
		f.close()
		return
	searchFor2 = input('Введите значение для этого поля, которое должно быть у элемента таблицы\n>')


	print('Найденные совпадения:')
	printTableHead(fields)

	try:
		while True:
			tableElement = pickle.load(f)

			if (tableElement[fieldName1] == searchFor1 and
				tableElement[fieldName2] == searchFor2):
				printTableElement(tableElement, fields)
	except EOFError:
		pass

	printTableEnd(fields)

	f.close()


def createDatabase():
	filename = input("Введине название базы данных\n>") + '.pickle'
	
	if path.exists(filename):
		print('База данных уже существует. Будет использованы существующие в ней данные')
	else:
		fields = []

		print('Введите количество полей базы данных')

		fieldsNum = 'n'

		while True:
			try:
				fieldsNum = int(input('>'))
				assert fieldsNum > 0
				break
			except ValueError:
				print('Можно ввести только натуральное число')
			except AssertionError:
				print('В базе данных должно быть как минимум одно поле')
		
		print(f'Введите {fieldsNum} полей:')

		for i in range(fieldsNum):
			fields.append(input('>'))

		f = open(filename, 'wb')
		pickle.dump(fields, f)
		f.close()

		print(f'База данных {filename} успешно создана')

	return filename


print('Прежде чем начать работу программы, нужно создать базу данных.')
filename = createDatabase()

while True:
	print(f'''Текущая база данных: {filename}
Выберите команду:
1. Создать новую БД
2. Добавить запись в БД
3. Вывести БД.
4. Поиск записи по полю
5. Поиск записи по двум полям
0. Выход
''')
	inpt = input(">")

	if inpt == '1':
		filename = createDatabase()
	elif inpt == '2':
		addRecord(filename)
	elif inpt == '3':
		printDatabase(filename)
	elif inpt == '4':
		printNFindOneField(filename)
	elif inpt == '5':
		printNFindTwoFields(filename)
	elif inpt == '0':
		break

	