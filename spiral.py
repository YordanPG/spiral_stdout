from math import sin, cos, pi
from typing import NamedTuple
from os import get_terminal_size

GRANULARITY = 0.2
TERMINAL_WIDTH, _ = get_terminal_size()
DEBUG = False
# DEBUG = True


class Point(NamedTuple):
    x: int | float
    y: int | float


def spiral_coordinates(circulation_factor: int | float = 1) -> list[Point]:

    radius = (TERMINAL_WIDTH / 2) / circulation_factor

    if DEBUG:
        radius -= 5
        print(
            f"Generating spiral points for{TERMINAL_WIDTH=}, {circulation_factor=} and "
            f"{GRANULARITY=}:\n  {radius=}"
        )

    points: list[Point] = []
    range_stop = int(360 * circulation_factor / GRANULARITY)

    for angle in range(0, range_stop + 1):
        phi = angle * GRANULARITY  # angle in degrees
        r = (
            circulation_factor * radius * angle / range_stop
        )  # r growing proportionaly to angle

        x = r * cos(phi * pi / 180)
        y = r * sin(phi * pi / 180)

        x = round(x)
        y = round(y)

        point = Point(x, y)

        # skip duplicates
        if point not in points:
            points.append(Point(x, y))

    return points


def translate_point(
    point: Point, delta_x: int | float, delta_y: int | float
) -> Point:
    return Point(point.x + delta_x, point.y + delta_y)


def group_points_by_y_coord(points: list[Point]) -> dict[int, list[int]]:
    """
    Assumes points list is ordered by the y-component of the points.
    Returns dict with keys the y-coordinates and values tuples withthe x-coordinates in ascending order.
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


def char_filled_print(line: list[int], char="O", prefix="") -> None:
    to_print = prefix + ""

    if len(line) == 0:
        print(to_print)
        return None

    for i in range(line[-1] + 1):
        if i in line:
            to_print += char
        else:
            to_print += " "

    print(to_print)


if __name__ == "__main__":

    # generate spiral points
    points = spiral_coordinates(circulation_factor=3)

    # sort points by y-coordinates
    points.sort(key=lambda p: p.y)

    # translate points
    left_most_point = min(points, key=lambda p: p.x)
    dx = abs(left_most_point.x)
    if DEBUG:
        dx += 2
    dy = abs(points[0].y)
    points = [translate_point(p, dx, dy) for p in points]

    # group x-coordinates by y, to represent a pritable line
    lines = group_points_by_y_coord(points)
    if DEBUG:
        print([y for y in lines.keys()])

    # print spiral
    for i in range(points[-1].y + 1):
        # pass
        if DEBUG:
            char_filled_print(lines.get(i, []), "*", prefix=str(i).zfill(3))
        else:
            char_filled_print(lines.get(i, []), char="*")
