from random import randrange
# my module
from misc.typing_template import *
from prime.is_prime import *
from mymath.gcd_lcm import *
# my module
# https://nyaannyaan.github.io/library/prime/fast-factorize.hpp
def pollard_rho(n: int) -> int:
    b = n.bit_length()-1
    b = (b >> 2) << 2
    m = int(2 ** (b / 8)) << 1
    while 1:
        c = randrange(1, n)
        f = lambda a: (a * a + c) % n
        y = 0
        g = q = r = 1
        while g == 1:
            x = y
            for _ in range(r): y = f(y)
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = f(y)
                    q = q * (x - y if x > y else y - x) % n
                g = gcd2(q, n)
                k += m
            r <<= 1
        if g == n:
            g = 1
            y = ys
            while g == 1:
                y = f(y)
                g = gcd2((x - y if x > y else y - x) , n)
        if g == n: continue
        if is_prime(g): return g
        elif is_prime(n // g): return n // g
        else: n = g

def factorize(n: int) -> Dict[int, int]:
    '''
    O(N**0.25) pollard rho algorithm
    return: dict s.t. n == PI(key^val for key, val in dict.items())
    '''
    res = {}
    for p in range(2,1000):
        if p * p > n: break
        if n % p: continue
        s = 0
        while n % p == 0:
            n //= p
            s += 1
        res[p] = s
    while not is_prime(n) and n > 1:
        p = pollard_rho(n)
        s = 0
        while n % p == 0:
            n //= p
            s += 1
        res[p] = s
    if n > 1: res[n] = 1
    return res
