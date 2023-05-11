# my module
from ntt.ntt import *
# my module
class ArbitraryNTT: # namespace
    __m0 = 0xa000001 # 167772161
    __m1 = 0x1c000001 # 469762049
    __m2 = 0x2d000001 # 754974721
    __r01 = pow(__m0, __m1 - 2, __m1)
    __r02 = pow(__m0, __m2 - 2, __m2)
    __r12 = pow(__m1, __m2 - 2, __m2)
    __r02r12 = __r02 * __r12 % __m2
    __w1 = __m0
    __w2 = __m0 * __m1

    @staticmethod
    def mul(a: List[int], b: List[int], mod: int) -> List[int]:
        ntt = NTT(mod)
        s, t = [0] * len(a), [0] * len(b)
        for i in range(len(a)): s[i] = a[i] % mod
        for i in range(len(b)): t[i] = b[i] % mod
        return ntt.multiply(s, t)

    @classmethod
    def _multiply(cls, s: List[int], t: List[int], mod: int=0) -> List[int]:
        d0 = cls.mul(s, t, cls.__m0)
        d1 = cls.mul(s, t, cls.__m1)
        d2 = cls.mul(s, t, cls.__m2)
        n = len(d0)
        ret = [0] * n
        if mod: W1, W2 = cls.__w1 % mod, cls.__w2 % mod
        else: W1, W2 = cls.__w1, cls.__w2
        for i in range(n):
            n1, n2, a = d1[i], d2[i], d0[i]
            b = (n1 + cls.__m1 - a) * cls.__r01 % cls.__m1
            c = ((n2 + cls.__m2 - a) * cls.__r02r12 + (cls.__m2 - b) * cls.__r12) % cls.__m2
            ret[i] = a + b * W1 + c * W2
        return [x % mod for x in ret] if mod else ret

    @classmethod
    def multiply(cls, a: List[int], b: List[int], mod: int=0) -> List[int]:
        if not a and not b: return []
        if min(len(a), len(b)) < 128:
            ret = [0] * (len(a) + len(b) - 1)
            for i, x in enumerate(a):
                for j, y in enumerate(b):
                    ret[i + j] += x * y
            return [x % mod for x in ret] if mod else ret
        return cls._multiply(a, b, mod)

    @classmethod
    def multiply_u128(cls, s: List[int], t: List[int]) -> List[int]:
        if not s and not t: return []
        if min(len(s), len(t)) < 128:
            ret = [0] * (len(s) + len(t) - 1)
            for i, x in enumerate(s):
                for j, y in enumerate(t):
                    ret[i + j] += x * y
            return ret
        return cls._multiply(s, t)
