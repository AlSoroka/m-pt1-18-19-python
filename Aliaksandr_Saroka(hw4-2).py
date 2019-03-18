# Вариант 2 Двойные декораторы
''' В декораторы вынесены проверки правильности ввода:
1. Имени нового пользователя decorateForAppend

2. Правильности введения цифры удаляемого пользователя decorateForDelete

3. Прверка верификации  при добавлении или удалении пользователя
   decorateOtherFunc - общий декоратор для функций добавления и удаления

4. Отдельный декоратор decorateForMenu проверки верификации при выборе
   пункта меню. Он другой, посокльку меню возвращает имя выбранного
   пользователя. Остальные функции модифицируют список.

5. Сам калькулятор вынес за скобки, чтобы не загромаждал код. На выходе
   просто имя выбранного пользователя.

6. Поскольку, функции удаления и добавления вызываются изнутри меню,
   для них логично применение синтаксического сахара @...
   Точка запуска меню известна и логично было бы применить
   имя=декоратор(меню) или в моих переменных
   name=decorateForMenu(showMenu), но у меня не получилось

   Может Вы подскажите почему?
'''


import os
import re


def clear():  # Очистка консоли
    os.system('cls')


def decorateForMenu(Menu):
    global authorization

    def verifyAuthorization():
        global authorization
        name = Menu()
        if not authorization:
            print("Требуется верификация")
            verUser = verifyUser(password)
            if verUser:
                input('Все отлично! Работаем. Нажмите Enter')
                authorization = True
                return name
            else:
                print('Наверно Вы чужой. Станьте своим')
                authorization = False
                return ''

    return verifyAuthorization


@decorateForMenu
def showMenu():
    iter = 0

    mess = '     Можно вводить только цифры (в пределах количества \
    \n     пользователей) или большие латинские D и N '

    while True:
        clear()
        lenList = len(users)
        possibleKeys = ''  # Переменная для возможных вариантов ответа
        for i in range(0, lenList):
            print(str(i+1)+'. '+users[i])
            possibleKeys += (str(i+1)+' ')

        possibleKeys += ' N D'
        possibleKeys = possibleKeys.split()

        print('Выбрать пользователя: (1, 2, 3...)')
        print('Новый пользователь - N;     удалить пользователя - D')
        if iter > 0:  # Если в первый раз ввод с ошибкой, выводится mess
            print(mess)
        key = input()

        iter += 1
        if key in possibleKeys:
            if key.isdigit():  # Если введен номер, выбираем пользователя
                name = users[int(key)-1]
                break  # Выход из цикла ввода данных и запуск калькулятора

# *********************** Блок удаление пользователя

            elif key == "D":
                checkNumber = 1
                while checkNumber == 1:
                    numUser = input('Номер удаляемого пользователя: ')
                    if numUser.isdigit():
                        checkNumber = deleteUser(int(numUser))


#  ******** Блок вставки нового пользователя

            else:
                checkName = 1
                while checkName == 1:
                    newName = input('Введите имя нового пользователя ')
                    checkName = insertUser(newName)

    return (name)


def verifyUser(password):
    global authorization
    print('\nДорогой друг, введите пароль')
    passw = input('(нужно ввести "'+password+'") ')
    if passw == password:
        authorization = True
        return (True)


''' Декоратор функций добавления пользлвателя и удаления.
Поскольку функции вызываются внутри меню, проверку верификации нужно
выпонять непосредственно при их определении '''


def decorateOtherFunc(OtherFunc):  # Декоратор верификация? кроме меню
    global authorization

    def verifyAuthorization(*args):
        global authorization
        if not authorization:
            print("Требуется верификация")
            verUser = verifyUser(password)  # Вызов процедуры ввода пароля
            if verUser:
                input('Все отлично! Работаем. Нажмите Enter')
                OtherFunc(*args)
            else:
                input('Наверно, Вы чужой. Станьте своим. Нажмите Enter')
        else:
            OtherFunc(*args)
    return verifyAuthorization


def decorateForDelete(deleteFromList):  # Декоратор функции удаления

    def verifyChoice(checkNum):
        ''' Получаемый параметр - номер удаляемого пользователя
            users - список пользователей (глобальный объект) '''
        if len(users) < 2:
            print('Хоть один должен остаться! Нажмите Enter')
            input()
            return (1)
        if (checkNum < 1) or (checkNum > len(users)):
            input('Неверный выбор! Нажмите Enter')
            return (1)
        else:
            deleteFromList(checkNum)
    return verifyChoice


def decorateForAppend(appendIntoList):  # Декоратор функции добавления

    def verifyName(name):
        ''' Получаемый параметр - имя нового пользователя
            Проверяем имя: кирилица, Строчными буквами с большой, не длинее 20
            Нужно же что-то проверять '''
        pattern = re.compile('''
                    ([А-Я]) # Кирилица с большой буквы
                    ([а-я]{1,19}) # Кирилица всего не более 20 символов
                    ''', re.VERBOSE)
        if not re.search(pattern, name):
            input('Неверный ввод. Для продолжения, нажмите Enter')
            return(1)
        else:
            appendIntoList(name)
    return verifyName


@decorateForDelete
@decorateOtherFunc
def deleteUser(delUser):
    ''' Локальные переменные  answer,
        получаемый параметр - номер удаляемого пользователя
        изменяемый объект (глобальный) - users - список пользователей
    '''

    answer = input('Удалить пользователя ' + users[int(delUser) - 1] + '?\
                    \nДа-Y/Нет - любое значение: ')
    if answer.strip() == 'Y':
        users.pop(int(delUser)-1)
    return (0)


@decorateForAppend
@decorateOtherFunc
def insertUser(newName):
    answer = input('Добавить пользователя ' + newName + '?\
                    \nДа-Y/Нет - любое значение: ')
    if answer.strip() == 'Y':
        users.append(newName)
    return (0)


# main
users = ['Петр', 'Андрей', 'Иоан', ]
password = 'Я свой'
name = ''
authorization = False

while name == '':
    print('\nПользователь авторизован - ', authorization, '\n')
    input()
#    name=decorateForMenu(showMenu())
#    name=decorateForMenu(showMenu)
    name = showMenu()
print(name)
