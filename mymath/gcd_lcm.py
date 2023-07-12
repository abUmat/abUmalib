from functools import reduce
# my module
from misc.typing_template import *
# my module
def gcd2(a: int, b: int) -> int:
    while a: a, b = b % a, a
    return b

def gcd(*numbers) -> int:
    return reduce(gcd2, numbers)

def lcm2(x: int, y: int) -> int:
    return (x * y) // gcd2(x, y)

def lcm(*integers) -> int:
    return reduce(lcm2, integers)

def extgcd(a: int, b: int) -> Tuple[int, int, int]:
    'Tuple[gcd(a, b), x, y] s.t. ax + by = gcd(a, b) (Extended Euclidean algorithm)'
    if b:
        d, y, x = extgcd(b, a % b)
        y -= (a // b) * x
        return d, x, y
    return a, 1, 0

def crt(V: List[Pair]) -> Pair:
    '''
    V: [(x_i, y_i), ...]: x_i (mod y_i)
    return: x, r s.t. x == r (mod lcm(y))'''
    x = 0; d = 1
    for X, Y in V:
        g, a, b = extgcd(d, Y)
        x, d = (Y*b*x + d*a*X) // g, d*(Y // g)
        x %= d
    return x, d
