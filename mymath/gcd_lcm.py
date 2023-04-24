from functools import reduce

def _gcd(a: int, b: int) -> int:
    while a: a, b = b % a, a
    return b

def gcd(*numbers) -> int: return reduce(_gcd, numbers)

def _lcm(x: int, y: int) -> int: return (x * y) // _gcd(x, y)

def lcm(*integers) -> int: return reduce(_lcm, integers)

def extgcd(a: int, b: int):
    'Tuple[gcd(a, b), x, y] s.t. ax + by = gcd(a, b) (Extended Euclidean algorithm)'
    if b:
        d, y, x = extgcd(b, a % b)
        y -= (a // b) * x
        return d, x, y
    return a, 1, 0

def crt(V):
    'V: [(X_i, Y_i), ...]: X_i (mod Y_i)'
    x = 0; d = 1
    for X, Y in V:
        g, a, b = extgcd(d, Y)
        x, d = (Y*b*x + d*a*X) // g, d*(Y // g)
        x %= d
    return x, d
