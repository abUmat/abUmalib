# https://nyaannyaan.github.io/library/modulo/mod-sqrt.hpp
def mod_sqrt(a: int, p: int) -> int:
    'x s.t. x**2 == a (mod p) if exist else -1'
    if a < 2: return a
    if pow(a, (p - 1) >> 1, p) != 1: return -1
    b = 1
    while pow(b, (p - 1) >> 1, p) == 1: b += 1
    m = p - 1; e = 0
    while not m & 1:
        m >>= 1
        e += 1
    x = pow(a, (m - 1) >> 1, p)
    y = (a * x % p) * x % p
    x = a * x % p
    z = pow(b, m, p)
    while y != 1:
        j = 0
        t = y
        while t != 1:
            j += 1
            t = t * t % p
        z = pow(z, 1 << (e - j - 1), p)
        x = x * z % p
        z = z * z % p
        y = y * z % p
        e = j
    return x
