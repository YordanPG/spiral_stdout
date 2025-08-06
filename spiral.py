from math import sin, cos, pi
from typing import NamedTuple
from os import get_terminal_size

GRANULARITY = 1
terminal_width, terminal_height = get_terminal_size()


class Point(NamedTuple):
    x: int | float
    y: int | float


def spiral_coordinates(circulation_factor: int | float = 1) -> list[Point]:

    radius = (terminal_width / 2) / circulation_factor

    points: list[Point] = []
    range_stop = int(360 * circulation_factor / GRANULARITY)

    for angle in range(0, range_stop + 1):
        phi = angle * GRANULARITY  # angle in degrees
        r = radius * angle / range_stop  # r growing proportionaly to angle

        x = r * cos(phi * pi / 180)
        y = r * sin(phi * pi / 180)

        x = round(x)
        y = round(y)

        point = Point(x, y)

        # skip duplicates
        if point not in points:
            points.append(Point(x, y))

    return points


def translate_point(point: Point, delta_x: int | float, delta_y: int | float):
    return Point(point.x + delta_x, point.y + delta_y)


def group_points_by_y_coord(points: list[Point]) -> dict[int, list[int]]:
    """
    Assumes points list is ordered by the y-component of the points.
    Returns dict with keys the y-coordinates and values tuples with the x-coordinates in ascending order.
    """
    lines = {}  # e.g.: {y1: [x11, x12], y2: [x21]}

    for p in points:
        y = p.y
        if y in lines:
            lines[y].append(p.x)
        else:
            lines[y] = [p.x]

    for line in lines.values():
        line.sort()

    return lines


def char_filled_print(line: list[int], char="O") -> None:
    if len(line) == 0:
        print()
        return None

    to_print = ""
    for i in range(line[-1] + 1):
        if i in line:
            to_print += char
        else:
            to_print += " "

    print(to_print)


# print(spiral_coordinates())
points = spiral_coordinates(circulation_factor=1)
points.sort(key=lambda p: p.y)

left_most_point = min(points, key=lambda p: p.x)
dx = abs(left_most_point.x)
dy = abs(points[0].y)
points = [translate_point(p, dx, dy) for p in points]

lines = group_points_by_y_coord(points)
print(lines)

for line in lines.values():
    char_filled_print(line)
