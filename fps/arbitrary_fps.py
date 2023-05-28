# my module
from ntt.complex_fft import *
from fps.fps import *
# my module
# arbitrary_nttだとTLEするのでCooleyTukeyを使いたい
# 2倍くらい速いっぽい
# https://nyaannyaan.github.io/library/fps/arbitrary-fps.hpp
def set_fft(self: FPS) -> None:
    self.ntt = CooleyTukey()
FPS.set_fft = set_fft

def mul(self: FPS, l: Poly, r: Union[Poly, int]) -> Poly:
    '''
    if r is int: l *= r
    if r is Polynomial: convolve l and r
    '''
    mod = self.mod
    if type(r) is int: return [x * r % mod for x in l]
    if type(r) is list:
        if not l or not r: return []
        if self.ntt is None: self.set_fft()
        return self.ntt.karatsuba(l, r, mod)
    raise TypeError()
FPS.mul = mul

def mul2(self: FPS, l: Poly) -> Poly:
    '''
    convolve l and l
    '''
    mod = self.mod
    if self.ntt is None: self.set_fft()
    return self.ntt.karatsuba_pow2(l, mod)
FPS.mul2 = mul2

def inv(self: FPS, a: Poly, deg: int=-1) -> Poly:
    '''return: g s.t. a*g == 1 (mod x**deg)'''
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

def exp(self: FPS, f: Poly, deg: int=-1) -> Poly:
    '''return: g s.t. log(g) == f (mod x ** deg)'''
    # assert(not self or self[0] == 0)
    if deg == -1: deg = len(f)
    ret = [1]
    i = 1
    while i < deg:
        i <<= 1
        ret = self.mul(ret, self.sub(self.add(f[:i], 1), self.log(ret, i)))[:i]
    return ret[:deg]
FPS.exp = exp
