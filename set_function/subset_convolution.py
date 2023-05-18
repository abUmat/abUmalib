# https://nyaannyaan.github.io/library/set-function/subset-convolution.hpp
# my module
from gcc_builtins import *
# my module
class SubsetConvolution:
    def __init__(self, s: int, mod: int) -> None:
        self.s = s
        self.mod = mod
        self.pc = pc = [0] * (1 << s)
        for i in range(1, 1 << s): pc[i] = pc[i - (i & -i)] + 1

    def add(self, l: list, r: list, d: int) -> None:
        'destcuctive'
        for i in range(d): l[i] += r[i]

    def sub(self, l: list, r: list, d: int) -> None:
        'destructive'
        for i in range(d, self.s + 1): l[i] -= r[i]

    def zeta(self, A: list) -> None:
        n = len(A)
        w = 1
        while w < n:
            for k in range(0, n, w << 1):
                for i in range(w):
                    self.add(A[k + w + i], A[k + i], self.pc[k + w + i])
            w <<= 1

    def mobius(self, A: list) -> None:
        n = len(A)
        w = n >> 1
        while w:
            for k in range(0, n, w << 1):
                for i in range(w):
                    self.sub(A[k + w + i], A[k + i], self.pc[k + w + i])
            w >>= 1

    def lift(self, a: list) -> list:
        A = [[0] * (self.s + 1) for _ in range(len(a))]
        for i, x in enumerate(a): A[i][self.pc[i]] = x
        return A

    def unlift(self, A: list) -> list:
        mod = self.mod
        a = [0] * len(A)
        for i, arr in enumerate(A): a[i] = arr[self.pc[i]] % mod
        return a

    def prod(self, A: list, B: list) -> None:
        'destructive'
        mod = self.mod; s = self.s
        n = len(A)
        d = ctz(n)
        for i in range(n):
            c = [0] * (s + 1)
            a = [x % mod for x in A[i]]
            b = [x % mod for x in B[i]]
            for j in range(d + 1):
                for k in range(d - j + 1):
                    c[j + k] += a[j] * b[k]
            A[i] = [x % mod for x in c]


    def multiply(self, a: list, b: list) -> list:
        A = self.lift(a); B = self.lift(b)
        self.zeta(A); self.zeta(B)
        self.prod(A, B)
        self.mobius(A)
        return self.unlift(A)
