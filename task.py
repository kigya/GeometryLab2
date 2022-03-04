import matplotlib.pyplot as plt
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def init_points(xs: list, ys: list) -> list:
    points = []
    for i in range(len(xs)):
        x = Point(xs[i], ys[i])
        points.append(x)
    return points


def draw_polygon(points: list):
    for i in range(len(points) - 1):
        plt.plot([points[i].x, points[i + 1].x], [points[i].y, points[i + 1].y])


def draw_point(point: Point):
    plt.scatter(point.x, point.y)


def draw_line(p1: Point, p2: Point):
    plt.plot([p1.x, p2.x], [p1.y, p2.y])


# Определитель матрицы
def det(a, b, c, d):
    return a * d - b * c


# Пересекаются ли прямые P1P2 и P3P4
def are_intersected(p1: Point, p2: Point, p3: Point, p4: Point) -> bool:
    d1 = det(p4.x - p3.x, p4.y - p3.y, p1.x - p3.x, p1.y - p3.y)
    d2 = det(p4.x - p3.x, p4.y - p3.y, p2.x - p3.x, p2.y - p3.y)
    d3 = det(p2.x - p1.x, p2.y - p1.y, p3.x - p1.x, p3.y - p1.y)
    d4 = det(p2.x - p1.x, p2.y - p1.y, p4.x - p1.x, p4.y - p1.y)

    if d1 * d2 <= 0 and d3 * d4 <= 0:
        return True
    else:
        return False


# Положение точки Р0 к прямой Р1Р2
def get_point_position_to_line(p0: Point, p1: Point, p2: Point) -> str:
    d = det(p2.x - p1.x, p2.y - p1.y, p0.x - p1.x, p0.y - p1.y)
    if d > 0:
        return 'left'
    elif d < 0:
        return 'right'
    else:
        return 'on the line'


# Проходит ли прямая P0Q через сторону многоугольника
def ptest(p0: Point, points: list) -> bool:
    for i in range(len(points) - 1):
        if get_point_position_to_line(p0, points[i], points[i + 1]) == 'on the line':
            return True
    return False


# Минимальный Х
def get_min_x(points: list):
    min_x = points[0].x
    for i in range(len(points)):
        if points[i].x < min_x:
            min_x = points[i].x
    return min_x


# Положение точки относительно многоугольника
def check_point_position(initial_point: Point, points: list) -> bool:
    q = Point(get_min_x(points) - 1, initial_point.y)
    draw_point(q)
    draw_line(initial_point, q)
    plt.annotate("Q",(q.x + 0.1, q.y + 0.22))
    plt.annotate("P0",(initial_point.x + 0.1, initial_point.y + 0.22))

    s = 0

    for i in range(len(points) - 1):
        # пересекается ли с любой из сторон многоугольника
        if are_intersected(points[i], points[i + 1], q, initial_point):
            # если пересекается, то проверяем пересекается ли по вершине
            if (not get_point_position_to_line(points[i], q, initial_point) == 'on the line' and
                    not get_point_position_to_line(points[i + 1], q, initial_point) == 'on the line'):
                # если пересекается не по вершине, увеличиваем счетчик
                s += 1
                # иначе: если по вершине, то запускаем счетчик вершин на нашем отрезке
            elif get_point_position_to_line(points[i], q, initial_point) == 'on the line':
                k = 0
                while get_point_position_to_line(points[i + k], q, initial_point) == 'on the line':
                    k += 1
                if (not get_point_position_to_line(points[i - 1], q, initial_point) ==
                        get_point_position_to_line(points[i + k], q, initial_point) and
                        not get_point_position_to_line(points[i - 1], q, initial_point) == 'on the line' and
                        not get_point_position_to_line(points[i + k], q, initial_point) == 'on the line'):
                    s += 1

    if s % 2 == 0:
        return False
    else:
        return True


def init():
    plt.grid(True)  # линии вспомогательной сетки

    xs = [1, 3, 1, 5, 6, 7, 8, 9, 10, 8, 7, 6, 5, 4, 1]  # координаты вершин многоугольника
    ys = [1, 5, 9, 10, 8, 9, 8, 11, 6, 3, 4, 2, 4, 2, 1]
    points = init_points(xs, ys)
    initial_point = Point(random.random() * 12, random.random() * 12)  # получение случайных к-т в диапазоне от 0 до 12

    q = Point(get_min_x(points) - 1, initial_point.y)  # точка, лежащая слева от многоугольника

    draw_polygon(points)
    draw_point(initial_point)

    if not check_point_position(initial_point, points):
        plt.suptitle('Снаружи', fontsize=14)
    elif ptest(initial_point, points):
        plt.suptitle('Внутри', fontsize=14)
    elif check_point_position(initial_point, points):
        plt.suptitle('Внутри', fontsize=14)

    plt.show()


init()


