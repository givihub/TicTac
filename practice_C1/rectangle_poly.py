class Rectangle:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_area(self):
        return self.a * self.b


class Square:
    def __init__(self, a):
        self.a = a

    def get_area_square(self):
        return self.a ** 2

    # возведение в степень **2 (в квадрат)

     # далее создаём два прямоугольника

    rect_1 = Rectangle(3, 4)
    rect_2 = Rectangle(12, 5)
    # вывод площади наших двух прямоугольников
    print(rect_1.get_area())
    print(rect_2.get_area())


