# -*- coding: cp1251 -*-

# �������, ����������� �� ������������ ����������� �����
def getPositiveIntFromUser(text, lowerBound=0):
    print(text)

    number = input('>')

    while True:
        if not number.isdigit() or int(number) == 0:
            print('����� ������ ���� �����������')
        elif int(number) < lowerBound:
            print(f'����� ������ ���� �� ������ {lowerBound}')
        else:
            break
        number = input('>')

    return int(number)


# �������, ����������� �� ������������ �������������� �����
def getFloatFromUser(text):
    print(text)
    number = float(input('>'))

    #while True:
    #    isOk = True
    #    try:
    #        number = float(number)
    #    except:
    #        print('����� ������ ���� ��������������')
    #        number = input('>')
    #    else:
    #        break;

    return number


# �������, ���������� ������� �� ������������
def getAArrFromUser(szX, szY):
    A = [[0]*szX]*szY]

    print('������� ����� ������ �������� ������� A')

    for i in range(szY):
        while True:
            A[i] = list(map(float, input('>').split()))
            if len(A[i]) != szX:
                print('���������� ��������� � ������� ������ ���� ����� ���������� ��������\n')
            else: break

    return A


# �������, ���������� ������
def printList(list):
    for el in list:
        print('{:6g}'.format(el), end=' ')
    print()


# �������, ���������� �������    
def printMatrix(arr):
    for st in arr:
        for el in st:
            print('{:6g}'.format(el), end=' ')
        print()


# ��� ��������

# �������������� ������� �������
while True:
    szX = getPositiveIntFromUser('������� ����� ��������', 2)
    szY = getPositiveIntFromUser('������� ����� �����')
    
    if szX < szY:
        print('������ �������� �� ����� �������� �������� ��� ��������')
        print('� ������� ����� ����� ������ ����� ��������')
        print('(���� ��� ��������� �������� ������� ���������,')
        print('�� � ������������ ������� � ��������� �������')
        print('��������� ����� ������, ��� � ������)')
        print('\n���������� ��� ���:')
    else:
        break

# �������� �������
A = getAArrFromUser(szX, szY)

# �������������� ���. ������� (�� �������)
B = [[i]*(szX - 1) for i in range(szY)]

# ���������� �� ������ ������...
for iy in range(szY):

    # � ������ ������ ������� B ���������� ��� �������� A, ����� �������� ������� ��������� ������� A
    for ix in range(iy):
        B[iy][ix] = A[iy][ix]

    for ix in range(iy, szX - 1):
        B[iy][ix] = A[iy][ix + 1]

# ������� �������
print('���������� ������� B:')
printMatrix(B)

# ������ ���� ������� � ���������� ����������� ������������� ���������

# ��������� ������ ���������
maxPosAmount = 0
colIndex = 0

# ���������� �� ������� �������...
for ix in range(szX - 1):

    # ������� ���������� ������������� ���������
    curPosAmount = 0

    # ������ ���������� �� ������� �������� �������
    for iy in range(szY):
        if B[iy][ix] > 0:
            curPosAmount += 1

    # ���� ���������� ������������� ����� ������, ��� ������ ���������
    if curPosAmount > maxPosAmount:

        # �� ������ ��������� ������������
        colIndex = ix
        maxPosAmount = curPosAmount

# ���������, ���� �� ������ � ��� ������������� ��������
if maxPosAmount == 0:
    print('� ������� ��� ������������� ���������')
else:
    print(f'� ������� � �������� {colIndex} ���������� ����� ������������� ��������� ({maxPosAmount})')

