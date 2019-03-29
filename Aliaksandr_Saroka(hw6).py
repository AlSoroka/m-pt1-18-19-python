#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' В декартовых координатах:
С точки зрения геметрии класс "отрезок" не является наследником класса
"точка", а является композицией двух объектов такого класса.

Для реализации полиморфизма и наследовани, в классе "точка" созданы два
метода: getPerimeter - вычисление периметра фигуры и getSquare -
вычисление площади. В дочернем классе "отрезок" один из них (периметр)
переопределяется.

В полярных координатах - "отрезок" может быть прямым наследником точки,
которая будет выступать его началом и приобретает ("отрезок") два
собственных свойства: длину и угол.

'''

#  В декартовых координатах


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def distance_from_origin(self):
        return (self.x**2 + self.y**2)**.5

    def getperimeter(self):
        return 0

    def getsquare(self):
        return 0


class LineSegment(Point):
    def __init__(self, point1, point2):

        self.x_beg = point1.x
        self.y_beg = point1.y
        self.x_end = point2.x
        self.y_end = point2.y

    def getperimeter(self):
        return ((self.x_beg-self.x_end)**2+(self.y_beg-self.y_end)**2)**.5


if __name__ == '__main__':
    import os
    import random
    from time import sleep

    def clear():
        os.system('cls')

    for i in range(5):
        x1 = random.randint(1, 78)
        y1 = random.randint(1, 23)
        x2 = random.randint(1, 78)
        y2 = random.randint(1, 23)

        a = Point(x1, y1)
        b = Point(x2, y2)

        line = LineSegment(a, b)

        for i in range(5):
            print('')
        print('     Декартовы координаты:')
        print('     Первая точка: ({}, {}). Вторая точка: ({}, {})'
              .format(a.x, a.y, b.x, b.y))
        print('     Периметр (переопределенный метод метод): {:.5}'
              .format(line.getperimeter()))
        print('     Площадь (наследуемый метод): {}'
              .format(line.getsquare()))
        sleep(3)
        clear()
        sleep(.5)
