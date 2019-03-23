''' Простейший парсинг scsv-файла.
По умолчанию использует:
в качестве символа-разделителя ";" semi-colon
Не реализованы:
1. Обработка разрыва строки внутри поля
2. Обработка экранированных разделительных символов и кавычек'''

import os


def GetSeparatePointWithCommas(sepLine):
    '''
    Формируем массив координат разделителей в строках с кавычками
    символы-разделители, находящиеся внутри кавычек как разделители
    не обрабатываются.

    Возвращает список положений разделителя ";" в принимаемой строке
    '''

    commasNum = sepLine.count('"')  # Находим количество вхождений кавычек

    if commasNum % 2 > 0:
        print('Присутствуют не закрытые кавычки. Не парсится')
        exit


#  Находим координаты кавычек в строке
    commasCoord = []
    for i in range(0, len(sepLine)-1):
        if line[i] == '"':
            commasCoord.append(i)

#  Находим координаты точек-с-запятой в строке
    semiColonCoord = []
    for i in range(0, len(sepLine)-1):
        if line[i] == ';':
            semiColonCoord.append(i)
# Список индексов точек-с-запятой, которые будут исключены
    forDel = []

    for i in range(0, len(semiColonCoord)-1):
        k = 0
        while k <= len(commasCoord)-2:
            if semiColonCoord[i] > commasCoord[k] and \
             semiColonCoord[i] < commasCoord[k+1]:
                forDel.append(i)  # Если точка-с-запятой между кавычек
            k += 2

    for i in forDel:
        semiColonCoord.pop(i)

    # Т. к. Последнее поле не закрывается разделителем
    semiColonCoord.append(len(sepLine)-1)
    return semiColonCoord


def GetSeparatePointWithoutCommas(sepLine):
    # Формируем массив координат разделителей в строках кавычек

    #  Находим координаты точек-с-запятой в строке
    semiColonCoord = []
    for i in range(0, len(sepLine)-1):
        if line[i] == ';':
            semiColonCoord.append(i)
    # Т. к. Последнее поле не закрывается разделителем
    semiColonCoord.append(len(sepLine)-1)
    return semiColonCoord


path = ''
fileIn = r'Книга3.csv'
fileOut = r'Книга3.json'

with open(os.path.join(path, fileIn), 'r') as fp:
    lineNum = 1
    lineCount = sum(1 for line in fp)
    input(lineCount)
    fp.seek(0)

    for line in fp:
        if line.count('"') > 0:
            breakPoint = GetSeparatePointWithCommas(line)
        else:
            breakPoint = GetSeparatePointWithoutCommas(line)

        if lineNum == 1:
            fieldName = []  # Инициализируем массив имен полей
            numField = len(breakPoint)

        fieldValue = []  # Инициализируем массив значений

        print(breakPoint)
        for i in range(0, numField-1):
            if i == 0:
                fName = line[:breakPoint[i]]
            elif i == numField-1:
                fName = line[breakPoint[i]:]
            else:
                fName = line[breakPoint[i]+1:breakPoint[i+1]]
                ''' Удаляем концевые пробелы, кавычки, заменяем сдвоенные
                 кавычки одинарными и экранируем их
                 Проверяем и удаляем концевые запятые т. к.
                 будет экспорт в JSON '''
            fName = fName.replace('""', '"').strip('"'). \
                replace('"', '\\"').strip().strip(',').strip()
            if lineNum == 1:
                fieldName.append(fName)
            else:
                fieldValue.append(fName)
        if lineNum == 1:
            fo = open(os.path.join(path, fileOut), 'w')
            fo.write('[')
        else:
            fo.write('{')
            for i in range(0, numField-1):
                print('Номер поля ', i, '   Количество полей ', numField-1)

                if i == (numField-2):
                    print('Ура')
                    fo.write('"'+fieldName[i]+'":'+fieldValue[i])
                else:
                    fo.write('"'+fieldName[i]+'":'+fieldValue[i]+',')
        if lineNum == lineCount:
            fo.write('}')
        elif lineNum == 1:
            pass
        else:
            fo.write('},')
        lineNum += 1
    fo.write(']')
    fo.close()
