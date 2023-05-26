# my module
from prime.prime_enumerate import *
# my module
# https://nyaannyaan.github.io/library/modulo/tetration.hpp
__ps = prime_enumerate(int(1_000_000_000 ** 0.5) + 1)
def tetration(a: int, b: int, m: int) -> int:
    def totient(n: int) -> int:
        res = n
        for p in __ps:
            if p * p > n: break
            if not n % p:
                res -= res // p
                while not n % p: n //= p
        if n != 1: res -= res // n
        return res

    def mpow(a: int, p: int, m: int):
        ret = 1 % m
        flg = 1
        while p:
            if p & 1:
                ret *= a
                if ret >= m:
                    flg = 0
                    ret %= m
            if p == 1: break
            a *= a
            if a >= m:
                flg = 0
                a %= m
            p >>= 1
        return ret, flg

    def calc(a: int, b: int, m: int):
        if a == 0: return int(not b & 1), 1
        if a == 1: return 1, 1
        if m == 1: return 0, 0
        if b == 0: return 1, 1
        if b == 1: return a % m, int(a < m)
        phi_m = totient(m)
        pre, flg1 = calc(a, b - 1, phi_m)
        res, flg2 = mpow(a % m, pre + (0 if flg1 else phi_m), m)
        return res, flg1 & flg2

    return calc(a, b, m)[0] % m
