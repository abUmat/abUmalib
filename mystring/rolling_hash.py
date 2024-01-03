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
    _MOD = 0x1fffffffffffffff # (1<<61)-1
    _MASK30 = 0x3fffffff # (1<<30)-1
    _MASK31 = 0x7fffffff # (1<<31)-1
    _MASK61 = _MOD
    _BASE = _get_base()

    @classmethod
    def _mul(cls, a: int, b: int) -> int:
        au = a >> 31
        ad = a & cls._MASK31
        bu = b >> 31
        bd = b & cls._MASK31
        mid = ad * bu + au * bd
        midu = mid >> 30
        midd = mid & cls._MASK30
        return cls._calc_mod(au*bu*2 + midu + (midd << 31) + ad * bd)

    @classmethod
    def _calc_mod(cls, x: int) -> int:
        xu = x >> 61
        xd = x & cls._MASK61
        res = xu + xd
        return res if res < cls._MOD else res - cls._MOD

    def __init__(self, s):
        self._n = len(s)
        self._hash = [0] * (self._n + 1)
        self._power = [0] * (self._n + 1)
        tmphash = 0
        self._power[0] = tmppower = 1
        for i, c in enumerate(s):
            self._hash[i + 1] = tmphash = self._calc_mod(self._mul(tmphash, self._BASE) + ord(c))
            self._power[i + 1] = tmppower = self._mul(tmppower, self._BASE)

    def get(self, l: int, r: int) -> int:
        'get hash of s[l, r)'
        res = self._hash[r] - self._mul(self._hash[l], self._power[r-l])
        return res + self._MOD if res < 0 else res

    def connect(self, h1: int, h2: int, h2len: int) -> int:
        'connect S(hash = h1) and T(hash = h2, length = h2len)'
        return self._calc_mod(self._mul(h1, self._power[h2len]) + h2)

    def lcp(self, rh, l1: int, r1: int, l2: int, r2: int) -> int:
        'longest common prefix of self.s[l1, r1) and rh2.s[l2, r2) O(log(length))'
        length = min(r1 - l1, r2 - l2)
        ok = 0
        ng = length + 1
        while ng - ok > 1:
            mid = (ok+ng) >> 1
            if self.get(l1, l1+mid) == rh.get(l2, l2+mid): ok = mid
            else: ng = mid
        return ok
