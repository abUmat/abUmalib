from functools import reduce

def _gcd(a, b):
    while a: a, b = b%a, a
    return b

def gcd(*numbers): return reduce(_gcd, numbers)

def _lcm(x, y): return (x * y) // _gcd(x, y)

def lcm(*integers): return reduce(_lcm, integers)

def extgcd(a, b):
    if b:
        d, y, x = extgcd(b, a % b)
        y -= (a // b) * x
        return d, x, y
    return a, 1, 0

# V = [(X_i, Y_i), ...]: X_i (mod Y_i)
def crt(V):
    x = 0; d = 1
    for X, Y in V:
        g, a, b = extgcd(d, Y)
        x, d = (Y*b*x + d*a*X) // g, d*(Y // g)
        x %= d
    return x, d
