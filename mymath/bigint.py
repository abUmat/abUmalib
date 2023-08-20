# my module
from ntt.arbitrary_ntt import *
# my module
# https://nyaannyaan.github.io/library/math/bigint.hpp
_bigint_D = 1_000_000_000
_bigint_logD = 9
class MultiPrecisionInteger:
    def __init__(self, s: str) -> None:
        if type(s) is not str:
            raise TypeError('bigint() argument must be a string')
        if s == '':
            raise ValueError('bigint() argument must not be a empty-string')
        self.neg: bool = 0
        self.dat: List[int] = []
        if len(s) == 1 and s[0] == '0':
            return
        l = 0
        if s[0] == '-':
            l += 1
            self.neg = 1
        for ie in range(len(s), l, -_bigint_logD):
            is_ = max(l, ie - _bigint_logD)
            x = 0
            for i in range(is_, ie):
                x = x * 10 + int(s[i])
            self.dat.append(x)

    @staticmethod
    def _new(n: bool, d: List[int]):
        ret = MultiPrecisionInteger('0')
        ret.neg = n
        ret.dat = d[:]
        return ret

    @staticmethod
    def _shrink(a: List[int]) -> None:
        while a and not a[-1]:
            a.pop()

    def shrink(self) -> None:
        while self and not self.dat[-1]:
            self.dat.pop()

    @staticmethod
    def _is_zero(a: List[int]) -> bool:
        '''a == 0'''
        return not a

    def is_zero(self) -> bool:
        return self._is_zero(self.dat)

    @staticmethod
    def _is_one(a: List[int]) -> bool:
        return len(a) == 1 and a[0] == 1

    @staticmethod
    def _eq(a: List[int], b: List[int]) -> bool:
        '''a == b'''
        return a == b

    @staticmethod
    def _lt(a: List[int], b: List[int]) -> bool:
        '''a < b'''
        if len(a) != len(b):
            return len(a) < len(b)
        for i in range(len(a))[::-1]:
            if a[i] != b[i]:
                return a[i] < b[i]
        return 0

    @classmethod
    def _leq(cls, a: List[int], b: List[int]) -> bool:
        '''a <= b'''
        return cls._eq(a, b) or cls._lt(a, b)

    @classmethod
    def _neq_lt(cls, lhs, rhs) -> bool:
        assert(lhs != rhs)
        if lhs.neg != rhs.neg:
            return lhs.neg
        f = cls._lt(lhs.dat, rhs.dat)
        return f ^ lhs.neg

    @classmethod
    def _add(cls, a: List[int], b: List[int]) -> List[int]:
        c: List[int] = [0] * (max(len(a), len(b)) + 1)
        for i, x in enumerate(a):
            c[i] += x
        for i, x in enumerate(b):
            c[i] += x
        for i in range(len(c) - 1):
            if c[i] >= _bigint_D:
                c[i] -= _bigint_D
                c[i + 1] += 1
        cls._shrink(c)
        return c

    @classmethod
    def _sub(cls, a: List[int], b: List[int]) -> List[int]:
        assert(cls._leq(b, a))
        c = a[:]
        borrow = 0
        for i in range(len(a)):
            if i < len(b):
                borrow += b[i]
            c[i] -= borrow
            borrow = 0
            if c[i] < 0:
                c[i] += _bigint_D
                borrow = 1
        assert(not borrow)
        cls._shrink(c)
        return c

    @classmethod
    def _mul(cls, a: List[int], b: List[int]) -> List[int]:
        if cls._is_zero(a) or cls._is_zero(b):
            return []
        if cls._is_one(a):
            return b[:]
        if cls._is_one(b):
            return a[:]
        if min(len(a), len(b)) <= 128:
            if len(a) < len(b):
                return cls._mul_naive(b, a)
            else:
                return cls._mul_naive(a, b)
        return cls._mul_fft(a, b)

    @classmethod
    def _mul_naive(cls, a: List[int], b: List[int]) -> List[int]:
        if not a or not b:
            return []
        prod: List[int] = [0] * (len(a) + len(b))
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                prod[i + j] += x * y
                if prod[i + j] >= 4 * _bigint_D * _bigint_D:
                    prod[i + j] -= 4 * _bigint_D * _bigint_D
                    prod[i + j + 1] += 4 * _bigint_D

        c: List[int] = [0] * (len(prod) + 1)
        x = 0
        for i, p in enumerate(prod):
            x += p
            x, c[i] = divmod(x, _bigint_D)
        while x:
            x, c[i] = divmod(x, _bigint_D)
            i += 1
        cls._shrink(c)
        return c

    @classmethod
    def _mul_fft(cls, a: List[int], b: List[int]) -> List[int]:
        '''mが多倍長整数の配列になっているので改善の余地あり?'''
        if not a or not b:
            return []
        m = ArbitraryNTT.multiply(a, b)
        c: List[int] = []
        x = 0
        i = 0
        while 1:
            if i > len(m) and not x:
                break
            if i < len(m):
                x += m[i]
            x, rem = divmod(x, _bigint_D)
            c.append(rem)
            i += 1
        cls._shrink(c)
        return c

    @classmethod
    def _divmod_newton(cls, a: List[int], b: List[int]) -> Tuple[List[int], List[int]]:
        if cls._is_zero(b):
            raise ZeroDivisionError('division by zero')
        if len(b) <= 64:
            return cls._divmod_naive(a, b)
        if len(a) - len(b) <= 64:
            return cls._divmod_naive(a, b)
        add, sub = cls._add, cls._sub
        lt, leq = cls._lt, cls._leq
        norm = _bigint_D // (b[-1] + 1)
        x = cls._mul(a, [norm])
        y = cls._mul(b, [norm])
        deg = len(x) - len(y) + 2
        z = cls._calc_inv(y, deg)
        q = cls._mul(x, z)
        q[:len(y) + deg] = []
        yq = cls._mul(y, q)
        while lt(x, yq):
            q = sub(q, [1])
            yq = sub(yq, y)
        r = sub(x, yq)
        while leq(y, r):
            q = add(q, [1])
            r = sub(r, y)
        cls._shrink(q)
        cls._shrink(r)
        q2, r2 = cls._divmod_1e9(r, [norm])
        assert(cls._is_zero(r2))
        return q, q2

    @classmethod
    def _divmod_naive(cls, a: List[int], b: List[int]) -> Tuple[List[int], List[int]]:
        if cls._is_zero(b):
            raise ZeroDivisionError('division by zero')
        assert(1 <= len(b))
        if len(b) == 1:
            return cls._divmod_1e9(a, b)
        if len(a) <= 2 and len(b) <= 2:
            return cls._divmod_ll(a, b)
        if cls._lt(a, b):
            return [], a
        # b >= 1e9 and a >= b
        sub, mul = cls._sub, cls._mul
        lt, leq = cls._lt, cls._leq
        norm = _bigint_D // (b[-1] + 1)
        x = mul(a, [norm])
        y = mul(b, [norm])
        yb = y[-1]
        quo = [0] * (len(x) - len(y) + 1)
        rem = x[-len(y):]
        for i in range(len(quo))[::-1]:
            if len(rem) < len(y):
                pass
            elif len(rem) == len(y):
                if leq(y, rem):
                    quo[i] = 1
                    rem = sub(rem, y)
            else:
                assert(len(y) + 1 == len(rem))
                rb = rem[-1] * _bigint_D + rem[-2]
                q = rb // yb
                yq = mul(y, [q])
                # 真の商は q-2 以上 q+1 以下だが自信が無いので念のため while を回す by Nyaan's Library
                while lt(rem, yq):
                    q -= 1
                    yq = sub(yq, y)
                rem = sub(rem, yq)
                while leq(y, rem):
                    q += 1
                    rem = sub(rem, y)
                quo[i] = q
            if i:
                rem[:0] = [x[i - 1]]
        cls._shrink(quo)
        cls._shrink(rem)
        q2, r2 = cls._divmod_1e9(rem, [norm])
        assert(cls._is_zero(r2))
        return quo, q2

    @classmethod
    def _divmod_1e9(cls, a: List[int], b: List[int]) -> Tuple[List[int], List[int]]:
        assert(len(b) == 1)
        if b[0] == 1:
            return a, []
        if len(a) <= 2:
            return cls._divmod_li(a, b)
        quo = [0] * len(a)
        d = 0
        b0 = b[0]
        for i in range(len(a))[::-1]:
            d = d * _bigint_D + a[i]
            assert(d < _bigint_D * b0)
            quo[i], d = divmod(d, b0)
        cls._shrink(quo)
        return quo, [d] if d else []

    @classmethod
    def _divmod_li(cls, a: List[int], b: List[int]) -> Tuple[List[int], List[int]]:
        assert(len(a) <= 2)
        assert(len(b) == 1)
        va = cls._to_ll(a)
        vb = b[0]
        quo, rem = divmod(va, vb)
        return cls._int_to_vec(quo), cls._int_to_vec(rem)

    @classmethod
    def _divmod_ll(cls, a: List[int], b: List[int]) -> Tuple[List[int], List[int]]:
        assert(len(a) <= 2)
        assert(len(b) == 1 or len(b) == 2)
        va = cls._to_ll(a)
        vb = cls._to_ll(b)
        quo, rem = divmod(va, vb)
        return cls._int_to_vec(quo), cls._int_to_vec(rem)

    @classmethod
    def _calc_inv(cls, a: List[int], deg: int) -> List[int]:
        assert(a and _bigint_D >> 1 <= a[-1] and a[-1] < _bigint_D)
        add, sub, mul = cls._add, cls._sub, cls._mul
        k = deg
        c = len(a)
        while k > 64:
            k = (k + 1) >> 1
        z = [0] * (c + k + 1)
        z[-1] = 1
        z = cls._divmod_naive(z, a)[0]
        while k < deg:
            s = [0] + mul(z, z)
            d = min(c, k << 1 | 1)
            t = a[-d:]
            u = mul(s, t)[d:]
            w = [0] * (k + 1)
            w += add(z, z)
            z = sub(w, u)[1:]
            k <<= 1
        return z[k - deg:]

    @staticmethod
    def _itos(x: int, zero_padding: bool) -> str:
        assert(0 <= x and x < _bigint_D)
        res: List[int] = []
        for _ in range(_bigint_logD):
            x, rem = divmod(x, 10)
            res.append(rem)
        if not zero_padding:
            while res and not res[-1]:
                res.pop()
            assert(res)
        return ''.join(map(str, res[::-1]))

    @staticmethod
    def _int_to_vec(x: int) -> List[int]:
        res: List[int] = []
        while x:
            x, rem = divmod(x, _bigint_D)
            res.append(rem)
        return res

    @staticmethod
    def _to_ll(a: List[int]) -> int:
        res = 0
        for i in range(len(a))[::-1]:
            res = res * _bigint_D + a[i]
        return res

    def __str__(self) -> str:
        if self.is_zero():
            return '0'
        ret: List[str] = []
        if self.neg:
            ret.append('-')
        for i in range(len(self))[::-1]:
            ret.append(self._itos(self.dat[i], i != len(self) - 1))
        return ''.join(ret)

    def __len__(self) -> int:
        return len(self.dat)

    def __neg__(self):
        if self.is_zero():
            return self._new(0, [])
        return self._new(not self.neg, self.dat)

    def __add__(self, other: object):
        if type(other) is not MultiPrecisionInteger:
            raise TypeError(f"unsupported operand type(s) for +: 'bigint' and '{type(other)}'")
        if self.neg == other.neg:
            return self._new(self.neg, self._add(self.dat, other.dat))
        if self._leq(self.dat, other.dat):
            #|self| <= |other|
            c = self._sub(other.dat, self.dat)
            n = 0 if self._is_zero(c) else other.neg
            return self._new(n, c)
        c = self._sub(self.dat, other.dat)
        n = 0 if self._is_zero(c) else self.neg
        return self._new(n, c)

    def __sub__(self, other: object):
        if type(other) is not MultiPrecisionInteger:
            raise TypeError(f"unsupported operand type(s) for -: 'bigint' and '{type(other)}'")
        return self + (-other)

    def __mul__(self, other: object):
        if type(other) is not MultiPrecisionInteger:
            raise TypeError(f"unsupported operand type(s) for *: 'bigint' and '{type(other)}'")
        c = self._mul(self.dat, other.dat)
        n = 0 if self._is_zero(c) else (self.neg ^ other.neg)
        return self._new(n, c)

    def __floordiv__(self, other: object):
        if type(other) is not MultiPrecisionInteger:
            raise TypeError(f"unsupported operand type(s) for //: 'bigint' and '{type(other)}'")
        return divmod(self, other)[0]

    def __mod__(self, other: object):
        if type(other) is not MultiPrecisionInteger:
            raise TypeError(f"unsupported operand type(s) for %: 'bigint' and '{type(other)}'")
        return divmod(self, other)[1]

    def __divmod__(self, other: object):
        if type(other) is not MultiPrecisionInteger:
            raise TypeError(f"unsupported operand type(s) for divmod(): 'bigint' and '{type(other)}'")
        dm = self._divmod_newton(self.dat, other.dat)
        dn = 0 if self._is_zero(dm[0]) else (self.neg != other.neg)
        mn = 0 if self._is_zero(dm[1]) else self.neg
        return self._new(dn, dm[0]), self._new(mn, dm[1])

    def __abs__(self):
        return self._new(0, self.dat)

    def __eq__(self, other: object) -> bool:
        if type(other) is not MultiPrecisionInteger:
            raise TypeError(f"unsupported operand type(s) for ==: 'bigint' and '{type(other)}'")
        return self.neg == other.neg and self.dat == other.dat

    def __ne__(self, other: object) -> bool:
        if type(other) is not MultiPrecisionInteger:
            raise TypeError(f"unsupported operand type(s) for !=: 'bigint' and '{type(other)}'")
        return self.neg != other.neg or self.dat != other.dat

    def __lt__(self, other: object) -> bool:
        if type(other) is not MultiPrecisionInteger:
            raise TypeError(f"unsupported operand type(s) for <: 'bigint' and '{type(other)}'")
        if self == other: return 0
        return self._neq_lt(self, other)

    def __le__(self, other: object) -> bool:
        if type(other) is not MultiPrecisionInteger:
            raise TypeError(f"unsupported operand type(s) for <=: 'bigint' and '{type(other)}'")
        if self == other: return 1
        return self._neq_lt(self, other)

    def __gt__(self, other: object) -> bool:
        if type(other) is not MultiPrecisionInteger:
            raise TypeError(f"unsupported operand type(s) for >: 'bigint' and '{type(other)}'")
        if self == other: return 0
        return self._neq_lt(other, self)

    def __ge__(self, other: object) -> bool:
        if type(other) is not MultiPrecisionInteger:
            raise TypeError(f"unsupported operand type(s) for >=: 'bigint' and '{type(other)}'")
        if self == other: return 1
        return self._neq_lt(other, self)

bigint = MultiPrecisionInteger
