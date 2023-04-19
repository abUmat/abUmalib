# my module
from ntt.ntt import *
# my module
class ArbitraryNTT: # namespace
    m0 = 167772161
    m1 = 469762049
    m2 = 754974721
    r01 = pow(m0, m1 - 2, m1)
    r02 = pow(m0, m2 - 2, m2)
    r12 = pow(m1, m2 - 2, m2)
    r02r12 = r02 * r12 % m2
    w1 = m0
    w2 = m0 * m1

    @staticmethod
    def mul(a, b, mod):
        ntt = NTT(mod)
        s, t = [0] * len(a), [0] * len(b)
        for i in range(len(a)): s[i] = a[i] % mod
        for i in range(len(b)): t[i] = b[i] % mod
        return ntt.multiply(s, t)

    @classmethod
    def _multiply(cls, s, t, mod=0):
        d0 = cls.mul(s, t, cls.m0)
        d1 = cls.mul(s, t, cls.m1)
        d2 = cls.mul(s, t, cls.m2)
        n = len(d0)
        ret = [0] * n
        if mod: W1, W2 = cls.w1 % mod, cls.w2 % mod
        else: W1, W2 = cls.w1, cls.w2
        for i in range(n):
            n1, n2, a = d1[i], d2[i], d0[i]
            b = (n1 + cls.m1 - a) * cls.r01 % cls.m1
            c = ((n2 + cls.m2 - a) * cls.r02r12 + (cls.m2 - b) * cls.r12) % cls.m2
            ret[i] = a + b * W1 + c * W2
        return [x % mod for x in ret] if mod else ret

    @classmethod
    def multiply(cls, a, b, mod=0):
        if not a and not b: return []
        if min(len(a), len(b)) < 128:
            ret = [0] * (len(a) + len(b) - 1)
            for i, x in enumerate(a):
                for j, y in enumerate(b):
                    ret[i + j] += x * y
            return [x % mod for x in ret] if mod else ret
        return cls._multiply(a, b, mod)

    @classmethod
    def multiply_u128(cls, s, t):
        if not s and not t: return []
        if min(len(s), len(t)) < 128:
            ret = [0] * (len(s) + len(t) - 1)
            for i, x in enumerate(s):
                for j, y in enumerate(t):
                    ret[i + j] += x * y
            return ret
        return cls._multiply(s, t)