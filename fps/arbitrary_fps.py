# my module
from ntt.complex_fft import *
from fps.fps import *
# my module
# arbitrary_nttだとTLEするのでCooleyTukeyを使う
# 2倍くらい速いっぽい
# https://nyaannyaan.github.io/library/fps/arbitrary-fps.hpp
def mul(self: FPS, l: list, r) -> list:
    mod = self.mod
    if type(r) is int: return [x * r % mod for x in l]
    if type(r) is list:
        if not l or not r: return []
        return CooleyTukey().karatsuba(l, r, mod)
    raise TypeError()
FPS.mul = mul

def mul2(self: FPS, l: list) -> list:
    mod = self.mod
    return CooleyTukey().karatsuba_pow2(l, mod)
FPS.mul2 = mul2

def inv(self: FPS, a: list, deg: int=-1):
    # assert(self[0] != 0)
    if deg == -1: deg = len(a)
    mod = self.mod
    res = [pow(a[0], mod - 2, mod)]
    i = 1
    while i < deg:
        i <<= 1
        res = self.add(res, self.sub(res, self.mul(self.mul2(res), a[:i])[:i]))
    return res[:deg]
FPS.inv = inv

def exp(self: FPS, a: list, deg: int=-1) -> list:
    # assert(not self or self[0] == 0)
    if deg == -1: deg = len(a)
    ret = [1]
    i = 1
    while i < deg:
        i <<= 1
        ret = self.mul(ret, self.sub(self.add(a[:i], 1), self.log(ret, i)))[:i]
    return ret[:deg]
FPS.exp = exp
