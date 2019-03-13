# Александр Сорока
''' Исходные данные для расчета, дигноза и рекомендаций
взяты https://hudeyko.ru/raschet-imt.html
'''
name = input("Введите Ваше имя: ")
while True:
    age = input("Введите Ваш возраст (число лет): ").strip()
    if age.replace('.', '', 1).isdigit() or age.replace(',', '', 1).\
       isdigit():
        break
''' Проверяем, похожи ли введенные данные на десятичное (содержит
не более одной точки или одной запятой) или целое число.
'''
if float(age) < 18.0:
    print('Только для взрослых! \n        18+')
    exit(0)

while True:
    gender = input("Введите Ваш пол (только одна буква 'м' или 'ж': ").strip()
    if gender.lower() in ['м', 'ж']:
        break

while True:
    height = input("Введите Ваш рост в сантиметрах (число в интервале\
    от 100 до 250): ").strip()
    # Если случайно ввели см
    height = height.replace('см.', '').strip()
    height = height.replace('см', '').strip()
    if (height.replace('.', '', 1).isdigit() or height.replace
       (',', '', 1).isdigit()) and float(height) > 100.0 and \
       float(height) < 250.0:
        height = float(height) / 100
        break

while True:
    weight = input("Введите Ваш вес в кг (число в интервале от \
    10 до 250): ").strip()
    # или кг
    weight = weight.replace('кг.', '').strip()
    weight = weight.replace('кг', '').strip()
    if (weight.replace('.', '', 1).isdigit() or weight.replace(',', '', 1).
       isdigit()) and float(weight) > 10.0 and float(weight) < 250.0:
        weight = float(weight)
        break

'''
Для проверки без ввода данных

name=  'aa'
weight=  80.0
age=  48.1
height=  1.75
gender=  'м'
'''
imt = weight / height / height

if imt < 16.0:
    diagnosis = 'Выраженный дефицит массы тела, истощение'
    advice = 'Срочно к врачу!'
elif imt < 18.5:
    diagnosis = 'Недостаточная масса тела'
    advice = 'Усиленное питание, занятия ЛФК, сон не менее 8 часов,\
избегать \nстрессов и тяжелых физических нагрузок. Регулярный контроль веса'
elif imt < 24.9:
    diagnosis = 'Нормальный индекс массы'
    advice = 'Сбалансированное питание, занятия спортом, сон не менее\
8 часов, \nизбегать стрессов'
elif imt < 29.9:
    diagnosis = 'Лишний вес, предожирение'
    advice = 'Сбалансированное питание, больше двигаться, сон не менее\
8 часов, \nизбегать стрессов. Регулярный контроль веса'
elif imt < 34.9:
    diagnosis = 'Ожирение I степени'
    advice = 'Сбалансированное питание, больше двигаться, сон не менее\
8 часов, \nизбегать стрессов. Обязательно обратится к врачу'
elif imt < 39.9:
    diagnosis = 'Ожирение II степени'
    advice = 'Строго соблюдать и выполнять все назначения врача'
else:
    diagnosis = 'Ожирение III степени'
    advice = 'Срочно к врачу!'
answer = '\nУважаемый ' if gender.lower() == 'м' else '\nУважаемая '
print(answer + name + "!")
print("Ваш возраст: {} лет.". format(age))
print("Ваш рост: {:4.2f} м.". format(height))
print("Ваш вес: {:3.1f} кг.". format(weight))
print("Ваш ИМТ: {:3.1f} кг/м2.". format(imt))
print("Ваш диагноз: {}.". format(diagnosis))
print("Рекомендации: {}.\n\n". format(advice))


''' Дипазон значений для диаграммы: от 12 до 44
Дефолтная ширина консоли 80 символов
'''
parts = [12.0, 16.0, 18.5, 24.9, 29.9, 34.9, 39.9, 44.0]

symbs = ['!', '▒', '█', '▒', '!', '‼', '†']

div_val = (80)/(parts[len(parts)-1]-parts[0])
j = 0
graph = '+'
dig_scl = str(parts[0])
len_prev = len(dig_scl)

for i in range(1, len(parts)):
    dl = int((parts[i] - parts[i-1])*div_val) - 1
    # -1 так как в ключевых точках ставим плюсы

    ''' Для заполнения разными симовлами : graph += symbs[j]*dl + '+'
    Но получается криво. По-этому заполняем '-'
    '''
    graph += '-'*dl + '+'
    plus_pos = len(graph)  # Получаем позицию '+'
    len_curr = len(str(parts[i]))  # Получаем длину текущего значения

    ''' Рассчитываем позицию первого знака числа:
        Если это второе значение, то позиция '+' минус длина первого
        значения, если последующие, то позиция '+' минус половина длины
        предыдущего и последующего  значений
    '''
    dig_pos = plus_pos-len_prev + 1 if i == 1 else plus_pos - len_prev//2\
        - len_curr//2 + 1
    dig_scl += (dig_pos-len(dig_scl))*' ' + str(parts[i])
    len_prev = len_curr
    j += 1

pos_imt = int((imt-parts[0])*div_val) # рассчитываем экранную позицию ИМТ

your = 'Ваше значение ИМТ в норме' if (imt >= 18.5 and imt <= 24.9) \
    else 'Ваше значение ИМТ в зоне риска'
metka = ' '*(pos_imt-1) + '♥' + ' '
res = ''
res += (pos_imt-len(your)//2)*' ' + your
print(res)
print("{}({:3.1f})".format(metka, imt))
graph = graph[:pos_imt-1] + '▲' + graph[pos_imt+1:]
print(graph)
print(dig_scl)
