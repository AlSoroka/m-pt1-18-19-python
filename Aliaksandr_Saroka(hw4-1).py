# Вариант 1
''' В декораторы вынесены проверки правильности ввода:

1. Прверка верификации  при добавлении или удалении пользователя
   decorateOtherFunc - общий декоратор для функций добавления и удаления
   Проверка правильности ввода имени и выбора номера удаляемого
   пользователя включены в соответствующие фукции удаления и добавления.

2. Отдельный декоратор decorateForMenu проверки верификации при выборе
   пункта меню. Он другой, посокльку меню возвращает имя выбранного
   пользователя. Остальные функции модифицируют список.

3. Сам калькулятор вынес за скобки, чтобы не загромаждал код.

4. Поскольку, функции удаления и добавления вызываются изнутри меню,
   для них логично применение синтаксического сахара @...
   Точка запуска меню известна и логично было бы применить конструкцию
   имя=декоратор(меню) или в моих переменных
   name=decorateForMenu(showMenu), но у меня не получилось.

   Может Вы подскажите?



Если я правильно понял задание, нужно:
1.  Все испоняемые блоки, включая меню должны быть оформлены в def

2.  При входе пользователь может выбрать себя из списка.

3.  С помощью декоратора фукции меню должна осуществляться проверка,
    прошел ли пользователь процедуру верефикации, если да - доступ
    к дополнительным функциям меню, если нет - запрос пароля. '''


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


def decorateForDelete(deleteFromList):  # Декоратор функции удаления
    def verifyChoice(checkNum):
        '''   Получаемый параметр - номер удаляемого пользователя
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


def verifyUser(password):
    global authorization
    print('\nДорогой друг, введите пароль')
    passw = input('(нужно ввести "'+password+'") ')
    if passw == password:
        authorization = True
        return (True)


''' Декоратор функций добавления пользолвателя и его удаления.
Поскольку функции вызываются внутри меню, проверку верификации нужно
выпонять непосредственно при их определении '''


def decorateOtherFunc(OtherFunc):
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
            OtherFunc()
    return verifyAuthorization


@decorateOtherFunc
def deleteUser(delUser):
    ''' Локальные переменные  answer,
        получаемый параметр - номер удаляемого пользователя
        изменяемый объект (глобальный) - users - список пользователей
    '''
    if len(users) < 2:
        input('Хоть один должен остаться! Нажмите Enter')
        if (delUser < 1) or (delUser > len(users)):
            input('Неверный выбор! Нажмите Enter')
    else:
        answer = input('Удалить пользователя ' + users[int(delUser) - 1]
                       + '?\nДа-Y/Нет - любое значение: ')
    if answer.strip() == 'Y':
        users.pop(int(delUser)-1)
    return (0)


@decorateOtherFunc
def insertUser(newName):
    pattern = re.compile('''
    ([А-Я]) # Кирилица с большой буквы
    ([а-я]{1,19}) # Кирилица всего не более 20 символов
     ''', re.VERBOSE)
    if not re.search(pattern, newName):
        input('Неверный ввод. Для продолжения, нажмите Enter')
        return(1)
    else:
        answer = input('Добавить пользователя ' + newName + '?\
                    \nДа-Y/Нет - любое значение: ')
        if answer.strip() == 'Y':
            users.append(newName)
            return (0)


users = ['Петр', 'Андрей', 'Иоан', ]
password = 'Я свой'
name = ''
authorization = False

while name == '':
    # print('Пользователь авторизован - ',authorization)
    # input()
    name = showMenu()
print(name)
