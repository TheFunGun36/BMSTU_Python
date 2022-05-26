from math import sqrt

text = ['Я помню чудное мгновенье:',
		'Передо мной. явилась ты,',
		'Как мимолетное виденье,',
		'Как гений. чистой красоты',
		'В томленьях грусти безнадежной,',
		'В тревогах шумной. суеты,',
		'Звучал мне долго голос нежный',
		'И снились милые. черты',
		'Шли годы. Бурь. порыв мятежный',
		'Рассеял прежние. мечты,',
		'И я забыл твой голос нежный,',
		'Твои небесные. черты',
		'В глуши, во. мраке заточенья',
		'Тянулись тихо. дни мои',
		'Без. божества, без вдохновенья,',
		'Без. слез, без жизни, без любви',
		'Душе настало. пробужденье:',
		'И вот опять явилась. ты,',
		'Как мимолетное. виденье,',
		'Как гений чистой. красоты',
		'И сердце бьется. в упоенье,',
		'И для него. воскресли вновь',
		'И божество, и. вдохновенье,',
		'И жизнь, и. слезы, и любовь.']


def isfloat(value):
	try:
		value = float(value)
	except ValueError:
		return False
	else:
		return True


def OLDparseMathExpression(expression):
	pointer = 0
	expressionParsed = []
	
	closingBracketExpected = False
	while pointer < len(expression):
		
		if expression[pointer].isdigit():
			number = 0.0
			
			while pointer < len(expression) and expression[pointer].isdigit():
				number *= 10
				number += int(expression[pointer])
				pointer += 1
			
			if pointer < len(expression) and expression[pointer] == '.':
				pointer += 1
				division = 10
			
				while pointer < len(expression) and expression[pointer].isdigit():
					number += float(expression[pointer]) / division
					pointer += 1
					division *= 10
				
			expressionParsed.append(number)
			
		else:
			if closingBracketExpected:
				if expression[pointer] != ')':
					return ['error', f'На позиции {pointer} нет закрывающей скобки']
				
				closingBracketExpected = False
				pointer += 1
				continue
			
			token = []
			
			while pointer < len(expression) and not expression[pointer].isdigit():
				token.append(expression[pointer])
				pointer += 1
			
			token = ''.join(token)
			
			if len(token) != 5 and token.find('sqrt(') != -1:
				token = token[:-5]
				pointer -= 5
			
			if (token == '+' or token == '-' or token == '*' or token == '/' or token == '%' or token == '**'):
				expressionParsed.append(token)
			elif (token == 'sqrt('):
				closingBracketExpected = True
				expressionParsed.append(token[:-1])
			else:
				pointer -= len(token)
				return ['error', f'Неизвестная операция "{token}" на позиции {pointer}']
	
	
	return expressionParsed


def parseMathExpression(expression):
	# if (token == '+' or token == '-' or token == '*' or token == '/' or token == '%' or token == '**'):
	pointer = 0
	expressionParsed = []

	while pointer < len(expression):
		
		if expression[pointer].isdigit():
			number = 0.0
			
			while pointer < len(expression) and expression[pointer].isdigit():
				number *= 10
				number += int(expression[pointer])
				pointer += 1
			
			if pointer < len(expression) and expression[pointer] == '.':
				pointer += 1
				division = 10
			
				while pointer < len(expression) and expression[pointer].isdigit():
					number += float(expression[pointer]) / division
					pointer += 1
					division *= 10
				
			expressionParsed.append(number)
		else:
			token = ''
			while pointer < len(expression) and not expression[pointer].isdigit():
				if expression[pointer] == ' ':
					pointer += 1
					continue
				token = token + expression[pointer]
				if (token == '(' or
					token == ')' or
					token == '+' or
					token == '-' or
					token == '*' or
					token == '/' or
					token == '%' or
					token == '^' or
					token == 'sqrt'):
					expressionParsed.append(token)
					token = ''
				pointer += 1
			if token != '':
				return ['error', f'Неизвестная операция: {token}']

	return expressionParsed


def calculate(expression):
	if len(expression) == 0:
		return ['error', 'Обнаружено пустое выражение']

	i = 0
	while i < len(expression):
		if expression[i] == '(':
			notClosed = 1
			startIndex = i + 1  # на первом элементе внутри скобки
			endIndex = i + 1  # на закрывающей скобке

			while notClosed > 0:
				if endIndex >= len(expression):
					return ['error', f'Обнаружена незакрытая скобка на позиции {i}']

				if expression[endIndex] == '(':
					notClosed += 1
				elif expression[endIndex] == ')':
					notClosed -= 1

				endIndex += 1
			endIndex -= 1

			calculatedElement = calculate(expression[startIndex:endIndex])
			if calculatedElement[0] == 'error':
				return calculatedElement
			else:
			   calculatedElement = calculatedElement[0]

			expression = expression[:startIndex] + expression[endIndex + 1:]

			expression[startIndex-1] = calculatedElement
		i += 1

	try:
		while True:
			i = expression.index('sqrt')
			expression[i + 1] = sqrt(expression[i + 1])
			expression.pop(i)
	except ValueError:
		pass
	
	if expression[0] == '+':
		expression.pop(0)
	elif expression[0] == '-':
		expression.pop(0)
		expression[0] *= -1
	
	i = 1
	while i < len(expression) - 1:
		if expression[i] == '^':
			expression[i - 1] **= expression[i + 1]
			expression.pop(i)
			expression.pop(i)
		else:
			i += 1
	
	i = 1
	while i < len(expression):
		if expression[i] == '*':
			expression[i - 1] *= expression[i + 1]
			expression.pop(i)
			expression.pop(i)
		elif isfloat(expression[i]) and isfloat(expression[i - 1]):
			expression[i] *= expression[i - 1]
			expression.pop(i - 1)
		elif expression[i] == '/':
			try:
				expression[i - 1] /= expression[i + 1]
			except ZeroDivisionError:
				return ['error', 'Была совершена попытка деления на ноль']
			expression.pop(i)
			expression.pop(i)
		elif expression[i] == '%':
			try:
				expression[i - 1] %= expression[i + 1]
			except ZeroDivisionError:
				return ['error', 'Была совершена попытка деления на ноль']
			expression.pop(i)
			expression.pop(i)
		else:
			i += 1
	
	i = 1
	while i < len(expression) - 1:
		if expression[i] == '+':
			expression[i - 1] += expression[i + 1]
			expression.pop(i)
			expression.pop(i)
		elif expression[i] == '-':
			expression[i - 1] -= expression[i + 1]
			expression.pop(i)
			expression.pop(i)
		else:
			i += 2  # С умножением разобрались, теперь операции чередуются с числами
	
	return expression
	

def calculateMathExpression(expression):
	expression = parseMathExpression(expression)
	
	if len(expression) == 0:
		expression = ['error', 'Введено пустое выражение']

	if expression[0] == 'error':
		return expression[-1]
	
	expression = calculate(expression)

	if len(expression) > 1:
		expression = ['error', 'Обнаружена лишняя закрывающая скобка']


	return expression[-1]


def findLargestStrLen(text):
	mx = 0
	for el in text:
		if len(el) > mx:
			mx = len(el)
	return mx


def removeMultipleSpaces(text):
	for i in range(len(text)):
		text[i] = text[i].split(' ')

		while '' in text[i]:
			text[i].remove('')

		text[i] = ' '.join(text[i])
	return text


def alignLeft(text, maxStrLen):
	text = removeMultipleSpaces(text)

	for i in range(len(text)):
		text[i] = text[i] + ' ' * (maxStrLen - len(text[i]))
	
	return text


def alignRight(text, maxStrLen):
	text = removeMultipleSpaces(text)

	for i in range(len(text)):
		text[i] = ' ' * (maxStrLen - len(text[i])) + text[i]
	
	return text


def alignWidth(text, maxStrLen):
	text = alignLeft(text, maxStrLen)

	for i, string in enumerate(text):
		if i == len(text) - 1:
			break
		
		wordList = string.split()
		
		if len(wordList) == 1:
			text[i] = wordList[0] + ' ' * (maxStrLen - len(wordList[0]))
			continue
		elif len(wordList) == 2:
			text[i] = wordList[0] + ' ' * (maxStrLen - len(wordList[0]) - len(wordList[1])) + wordList[1]
			continue

		spacesAmount = string.count(' ')
		newWordList = []
		
		spacesBetweenWords = int(spacesAmount / (len(wordList) - 1))
		spacesNotUsed = spacesAmount % (len(wordList) - 1) + 1
		
		for j in range(len(wordList) - spacesNotUsed):
			newWordList.append(wordList[j] + ' ' * spacesBetweenWords)
		
		for j in range(len(wordList) - spacesNotUsed, len(wordList)):
			newWordList.append(wordList[j] + ' ' * (spacesBetweenWords + 1))
		
		string = ''.join(newWordList)
		text[i] = string[:maxStrLen]
	
	return text


def isLetter(symbol):
	code = ord(symbol)
	
	return (0x0041 <= code <= 0x005A or
		0x0061 <= code <= 0x007A or
		0x0410 <= code <= 0x044F)


def replaceWord(replaceWhat, replaceBy, text):
	for i, string in enumerate(text):
		wordList = string.split()
		
		for j, word in enumerate(wordList):

			nonWordSymbol = ''

			k = 0
			while k < len(word) and not isLetter(word[-(k + 1)]):
				k += 1

			if k > 0:
				nonWordSymbol = word[-k:]
				word = word[:-k]

			if word == replaceWhat:
				word = replaceBy
				word = word + nonWordSymbol
				wordList[j] = word

				if replaceBy == '':
					if j > 0:
						wordList[j - 1] = wordList[j - 1] + nonWordSymbol
						wordList.pop(j)
					else:
						wordList.pop(j)
						
						if i > 0 and nonWordSymbol != '.' and isLetter(text[i - 1][-1]):
							text[i - 1] = text[i - 1] + nonWordSymbol
		
		if len(wordList) > 0:
			text[i] = ' '.join(wordList)
		else:
			text.pop(i)
	
	text = removeMultipleSpaces(text)

	return text


def printText(text):
	print('+' + '-' * len(text[0]) + '+')
	
	for i, string in enumerate(text):
		print('|' + string + '|')
		
	print('+' + '-' * len(text[0]) + '+')


def sortByFirstElementValue(inputArray):
	return inputArray[0]


def findSentencesWithSameWordsAmount(text):
	text = [text[i] for i in range(len(text))]
	text = ' '.join(text)
	text = text.split('.')
	
	removeMultipleSpaces(text)

	matches = []
	
	for i, sentence in enumerate(text):
		val = len(sentence.split())

		isFound = False
		for j in range(len(matches)):
			if matches[j][0] == val:
				matches[j].append(sentence)
				isFound = True
				break
		
		if not isFound:
			matches.append([val, sentence])

	#for sentences in text:
	#	for i, sentence in enumerate(sentences):
	#		if i == len(sentences) - 1:
	#			break
	#		
	#		sentence = saved + ' ' + sentence
	#		saved = ''
	#		val = len(sentence.split())
	#		
	#		isFound = False
	#		for j in range(len(matches)):
	#			if matches[j][0] == val:
	#				matches[j].append(sentence)
	#				isFound = True
	#				break
	#		
	#		if not isFound:
	#			matches.append([val, sentence])
	#	
	#	saved = sentences[-1]

	i = 0
	while i < len(matches):
		if len(matches[i]) <= 2:
			matches.pop(i)
		else:
			i += 1
	
	for i in range(len(text)):
		text[i] = ''.join(text[i])

	
	for i in range(len(matches)):
		j = 1
		while j in range(len(matches[i])):
			matches[i][j] = matches[i][j].split(' ')

			while '' in matches[i][j]:
				matches[i][j].remove('')

			matches[i][j] = ' '.join(matches[i][j])
			j += 1
	
	matches.sort(key=sortByFirstElementValue)

	return matches

text = removeMultipleSpaces(text)
maxStrLen = findLargestStrLen(text)
lastAlignment = 0  # 0 - left, 1 - width, 2 - right
text = alignLeft(text, maxStrLen)

while True:
	printText(text)
	print('''Выберите действие:
1. Выровнять текст по левому краю
2. Выровнять текст по ширине
3. Выровнять текст по правому краю
4. Удалить слово
5. Заменить слово во всём тексте
6. Вычислить арифметическое выражение
7. Найти предложения, с одинаковым количеством слов
0. Выход из программы
''')
	npt = input('>')

	if npt == '1':
		text = alignLeft(text, maxStrLen)
		lastAlignment = 0
	if npt == '2':
		text = alignWidth(text, maxStrLen)
		lastAlignment = 1
	if npt == '3':
		text = alignRight(text, maxStrLen)
		lastAlignment = 2
	if npt == '4':
		replaceWhat = input('Введите слово, которое хотите удалить\n>')
		text = replaceWord(replaceWhat, '', text)
		
		maxStrLen = findLargestStrLen(text)
		
		if lastAlignment == 0:
			text = alignLeft(text, maxStrLen)
		elif lastAlignment == 1:
			text = alignWidth(text, maxStrLen)
		elif lastAlignment == 2:
			text = alignRight(text, maxStrLen)
	if npt == '5':
		replaceWhat = input('Введите слово, которое хотите заменить\n>')
		replaceBy = input('Введите слово, которое будет заменой предыдущему\n>')
		text = replaceWord(replaceWhat, replaceBy, text)
		
		maxStrLen = findLargestStrLen(text)
		
		if lastAlignment == 0:
			text = alignLeft(text, maxStrLen)
		elif lastAlignment == 1:
			text = alignWidth(text, maxStrLen)
		elif lastAlignment == 2:
			text = alignRight(text, maxStrLen)
	if npt == '6':
		expression = input('Введите арифметическое выражение\n>')
		result = calculateMathExpression(expression)
		if not isinstance(result, str):
			print('Результат: {:g}'.format(result))
		else:
			print('При вычислении возникла ошибка:')
			print(result)

		input('Для продолжения нажмите enter... ')
	if npt == '7':
		result = findSentencesWithSameWordsAmount(text)
		print('Были найдены следующие совпадения:')
		for el in result:
			print(f'С {el[0]} количеством слов:')
			for i in range(1, len(el)):
				print('\t', el[i], sep='')

		if lastAlignment == 0:
			text = alignLeft(text, maxStrLen)
		elif lastAlignment == 1:
			text = alignWidth(text, maxStrLen)
		elif lastAlignment == 2:
			text = alignRight(text, maxStrLen)

		input('Для продолжения нажмите enter... ')
	if npt == '0':
		break

