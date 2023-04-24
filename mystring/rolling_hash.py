def _get_base(R: int=37) -> int:
    from math import gcd
    from random import randint
    while 1:
        k = randint(1, 0x1ffffffffffffffd)
        if gcd(k, 0x1ffffffffffffffe) != 1: continue
        rh_base = pow(R, k, 0x1fffffffffffffff)
        if rh_base >> 8: break
    return rh_base

class RollingHash:
    MOD = 0x1fffffffffffffff # (1<<61)-1
    MASK30 = 0x3fffffff # (1<<30)-1
    MASK31 = 0x7fffffff # (1<<31)-1
    MASK61 = MOD
    BASE = _get_base()

    @classmethod
    def mul(cls, a: int, b: int) -> int:
        au = a >> 31
        ad = a & cls.MASK31
        bu = b >> 31
        bd = b & cls.MASK31
        mid = ad * bu + au * bd
        midu = mid >> 30
        midd = mid & cls.MASK30
        return cls.calc_mod(au*bu*2 + midu + (midd << 31) + ad * bd)

    @classmethod
    def calc_mod(cls, x: int) -> int:
        xu = x >> 61
        xd = x & cls.MASK61
        res = xu + xd
        if res >= cls.MOD: res -= cls.MOD
        return res

    def __init__(self, s):
        self.n = len(s)
        self.hash = [0] * (self.n+1)
        self.power = [0] * (self.n+1)
        self.power[0] = 1
        for i in range(self.n):
            self.hash[i+1] = self.calc_mod(self.mul(self.hash[i], self.BASE) + ord(s[i]))
            self.power[i+1] = self.mul(self.power[i], self.BASE)

    def get(self, l: int, r: int) -> int:
        'get hash of s[l, r)'
        res = self.hash[r] - self.mul(self.hash[l], self.power[r-l])
        if res < 0: res += self.MOD
        return res

    def connect(self, h1: int, h2: int, h2len: int) -> int:
        'connect S(hash = h1) and T(hash = h2, length = h2len)'
        res = self.calc_mod(self.mul(h1, self.power[h2len]) + h2)
        return res

    def lcp(self, rh, l1: int, r1: int, l2: int, r2: int) -> int:
        'longetst common prefix of self.s[l1, r1) and rh2.s[l2, r2) O(log(length))'
        length = min(r1-l1, r2-l2)
        low = -1
        high = length + 1
        while high - low > 1:
            mid = (low+high) >> 1
            if self.get(l1, l1+mid) == rh.get(l2, l2+mid): low = mid
            else: high = mid
        return low
