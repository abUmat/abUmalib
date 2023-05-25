# my module
from ntt.ntt import *
# my module
# https://nyaannyaan.github.io/library/ntt/arbitrary-ntt.hpp
class ArbitraryNTT: # namespace
    _m0 = 0xa000001 # 167772161
    _m1 = 0x1c000001 # 469762049
    _m2 = 0x2d000001 # 754974721
    _r01 = modinv(_m0, _m1)
    _r02 = modinv(_m0, _m2)
    _r12 = modinv(_m1, _m2)
    _r02r12 = _r02 * _r12 % _m2
    _w1 = _m0
    _w2 = _m0 * _m1
    _nttm0 = NTT(_m0)
    _nttm1 = NTT(_m1)
    _nttm2 = NTT(_m2)

    @classmethod
    def _multiply(cls, s: list, t: list, mod: int=0) -> list:
        d0 = cls._nttm0.multiply(s, t)
        d1 = cls._nttm1.multiply(s, t)
        d2 = cls._nttm2.multiply(s, t)
        n = len(d0)
        ret = [0] * n
        if mod: W1, W2 = cls._w1 % mod, cls._w2 % mod
        else: W1, W2 = cls._w1, cls._w2
        for i in range(n):
            n1, n2, a = d1[i], d2[i], d0[i]
            b = (n1 - a) * cls._r01 % cls._m1
            c = ((n2 - a) * cls._r02r12 - b * cls._r12) % cls._m2
            ret[i] = (a + b * W1 + c * W2) % mod if mod else a + b * W1 + c * W2
        return ret

    @classmethod
    def _pow2(cls, s: list, mod: int=0) -> list:
        d0 = cls._nttm0.pow2(s)
        d1 = cls._nttm1.pow2(s)
        d2 = cls._nttm2.pow2(s)
        n = len(d0)
        ret = [0] * n
        if mod: W1, W2 = cls._w1 % mod, cls._w2 % mod
        else: W1, W2 = cls._w1, cls._w2
        for i in range(n):
            n1, n2, a = d1[i], d2[i], d0[i]
            b = (n1 - a) * cls._r01 % cls._m1
            c = ((n2 - a) * cls._r02r12 - b * cls._r12) % cls._m2
            ret[i] = (a + b * W1 + c * W2) % mod if mod else a + b * W1 + c * W2
        return ret

    @classmethod
    def multiply(cls, a: list, b: list, mod: int=0) -> list:
        if not a and not b: return []
        if min(len(a), len(b)) < 128:
            ret = [0] * (len(a) + len(b) - 1)
            for i, x in enumerate(a):
                for j, y in enumerate(b):
                    ret[i + j] += x * y
            return [x % mod for x in ret] if mod else ret
        return cls._multiply(a, b, mod)

    @classmethod
    def pow2(cls, a: list, mod: int=0) -> list:
        if not a: return []
        if len(a) < 128:
            ret = [0] * ((len(a) << 1) - 1)
            for i, x in enumerate(a):
                for j, y in enumerate(a):
                    ret[i + j] += x * y
            return [x % mod for x in ret] if mod else ret
        return cls._pow2(a, mod)
