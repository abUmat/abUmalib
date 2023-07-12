from functools import cmp_to_key
# https://nyaannyaan.github.io/library/geometry/integer-geometry.hpp
class Point:
    def __init__(self, x: int=0, y: int=0) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return str((self.x, self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int):
        return Point(self.x * scalar, self.y * scalar)

    def __matmul__(self, other):
        return self.x * other.x + self.y * other.y

    def __or__(self, other):
        return self.x * other.y - self.y * other.x

    def __pos__(self):
        return Point(self.x, self.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __lt__(self, other):
        return self.y < other.y if self.x == other.x else self.x < other.x

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return self.y > other.y if self.x == other.x else self.x > other.x

    def __ge__(self, other):
        return not self > other or self == other

    def pos(self) -> int:
        if self.y < 0: return -1
        if self.y == 0 and 0 <= self.x: return 0
        return 1

def ccw(a: Point, b: Point, c: Point) -> int:
    'return: a->b->c is ... anti-clockwise 1 / straight 0 / clockwise -1'
    t = (b - a) | (c - a)
    if t < 0: return -1
    if t == 0: return 0
    return 1

def lower_hull(ps: list) -> list:
    N = len(ps)
    ps.sort()
    if N <= 2: return ps
    convex = [None] * N
    k = 0
    for i in range(N):
        while k >= 2 and ccw(convex[k-2], convex[k-1], ps[i]) <= 0: k -= 1
        convex[k] = ps[i]
        k += 1
    return convex[:k]

def upper_hull(ps: list) -> list:
    N = len(ps)
    ps.sort()
    if N <= 2: return ps
    convex = [None] * N
    k = 0
    for i in range(N):
        while k >= 2 and ccw(convex[k-2], convex[k-1], ps[i]) >= 0: k -= 1
        convex[k] = ps[i]
        k += 1
    return convex[:k]

def convex_hull(ps: list) -> list:
    N = len(ps)
    ps.sort()
    if N <= 2: return ps
    convex = [None] * (N<<1)
    k = 0
    for i in range(N):
        while k >= 2 and ccw(convex[k-2], convex[k-1], ps[i]) <= 0: k -= 1
        convex[k] = ps[i]
        k += 1
    t = k + 1
    for i in range(N-1)[::-1]:
        while k >= t and ccw(convex[k-2], convex[k-1], ps[i]) <= 0: k -= 1
        convex[k] = ps[i]
        k += 1
    return convex[:k-1]

def argument_sort(v: list) -> None:
    'sort v by argument -Pi to Pi'
    def compare(a, b):
        apos, bpos = a.pos(), b.pos()
        cross = a | b
        if apos == bpos: return -cross
        return apos - bpos
    v.sort(key=cmp_to_key(compare))
