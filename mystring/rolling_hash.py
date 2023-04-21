from random import randint
from math import gcd

def _get_base(R=37):
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
    def mul(cls, a, b):
        au = a >> 31
        ad = a & cls.MASK31
        bu = b >> 31
        bd = b & cls.MASK31
        mid = ad * bu + au * bd
        midu = mid >> 30
        midd = mid & cls.MASK30
        return cls.calc_mod(au*bu*2 + midu + (midd << 31) + ad * bd)

    @classmethod
    def calc_mod(cls, x):
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

    #get hash of s[l:r]
    def get(self, l, r):
        res = self.hash[r] - self.mul(self.hash[l], self.power[r-l])
        if res < 0: res += self.MOD
        return res

    #connect S(hash : h1) and T(hash : h2, length : h2len)
    def connect(self, h1, h2, h2len):
        res = self.calc_mod(self.mul(h1, self.power[h2len]) + h2)
        return res

    #get longest common prefix self.s[l1:r2] and rh2.s[l2:r2] O(log(length))
    def lcp(self, rh, l1, r1, l2, r2):
        length = min(r1-l1, r2-l2)
        low = -1
        high = length + 1
        while high - low > 1:
            mid = (low+high) >> 1
            if self.get(l1, l1+mid) == rh.get(l2, l2+mid): low = mid
            else: high = mid
        return low
