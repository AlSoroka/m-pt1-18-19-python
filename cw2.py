a, b, c = input('Введите 3 значения через пробел: ').split()
a, b, c = int(a), int(b), int(c)

if a and b and c:
    print("Нет ни оного нуля")
d = int(a or b or c)
if d:
    print(d)
else:
    print("Не нулевых значений нет")
if d > (b+c):
    print(a-b-c)
else:
    print(b+c-a)
if d > 50 and (b > d or c > d):
    print("Вася")
if d > 5 or (b == c == 7):
    print("Петя")
