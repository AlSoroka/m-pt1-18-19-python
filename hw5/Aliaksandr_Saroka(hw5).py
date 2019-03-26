import os

def separateField (line):
    ''' Разбиваем файл на поля, заменяем  разрывы строк внутри полей
        на пробелы. Символы-разделители:  ";" и [Tab]  '''
    #sepSymbols={',', ';', chr(9)}
    sepSymbols={';', chr(9)}
    firstCommas=False
    # Если firstCommas=True, то это значит, что   уже открыты кавычки
    # и разделительный символ или разрыв строки - это просто часть поля

    field=''

    for c in line:
        firstCommas = not firstCommas if c=='"' else firstCommas

        if (c in sepSymbols) and firstCommas:
            field+=c
        elif (c in sepSymbols) and not firstCommas or ord(c)==1:

            fieldValue.append(field)
            field=''

        elif ord(c)==10 and firstCommas:
            field+=' ' # Если разрыв внутри поля, заменяем на пробел

        elif ord(c)==10 and not firstCommas:
            fieldValue.append(field)
            field=''
            break
            return
        else:
            field+=c
    return # Функция возвращает строку разбитую на поля в списке fieldValue


path = ''
fileIn = 'Книга5.csv'
fileOut = fileIn[:fileIn.find('.')+1]+'json'

lineNum=1 # Предполагаем, что первая строка содержит имена полей

with open(os.path.join(path, fileIn), 'r') as fi:

    for line in fi:
        fieldValue=[]
        separateField(line) # Функция возвращает строку разбитую на поля в списке fieldValue
#******************************************************************************
        # Проверяем совпадает ли число столбцов данных с заголовком.
        if lineNum>1 and fieldCount:
            if len(fieldValue) != fieldCount:
                print('В файле не совпадает количество столбцов данных с заголовками')
                if not fo.closed:
                    fo.seek(0)
                    fo.write ('Файл не сформирован или сформирован с ошибками')
                    fo.close()
                    exit(1)

#******************************************************************************
        for i  in range(len(fieldValue)):
            ''' Удаляем концевые пробелы, кавычки, заменяем сдвоенные
                кавычки одинарными и экранируем их'''
            fieldValue[i] = fieldValue[i].replace('""', '"').strip('"'). \
                replace('"', '\\"').strip().strip(',').strip()

            if lineNum==1: # Все имена полей помещаем в кавычки
                fieldValue[i]='"'+fieldValue[i]+'"'
            else: # Значения полей помещаем в кавычки, если они не цифровые

                if not fieldValue[i].isdigit():
                    fieldValue[i]='"'+fieldValue[i]+'"'

#******************************************************************************
        if lineNum==1:
            fieldName = fieldValue[:]  # Формируем список имен полей
            fieldCount=len(fieldName)
            fo = open(os.path.join(path, fileOut), 'w')
            fo.write('[')
        else:
            jsonString='{'
            for i  in range(len(fieldValue)):

                jsonString+=fieldName[i]+':'+fieldValue[i]
                if i<len(fieldValue)-1:
                    jsonString+=','
                else:
                    jsonString+='},'
            fo.write(jsonString)

        lineNum+=1
    fo.seek(fo.tell()-1) # Удаляем последнюю запятую
    fo.write(']')
    fo.close()










