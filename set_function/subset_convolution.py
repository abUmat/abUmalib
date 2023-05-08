from typing import List
# my module
from gcc_builtins import *
# my module
from typing import List
class SubsetConvolution:
    def __init__(self, s: int, mod: int) -> None:
        self.s = s
        self.mod = mod
        self.pc = pc = [0] * (1 << s)
        for i in range(1, 1 << s): pc[i] = pc[i - (i & -i)] + 1

    @staticmethod
    def add(l: List[int], r: List[int], d: int) -> None:
        'destcuctive'
        for i in range(d): l[i] += r[i]

    def sub(self, l: List[int], r: List[int], d: int) -> None:
        'destructive'
        for i in range(d, self.s + 1): l[i] -= r[i]

    def zeta(self, a: List[List[int]]) -> None:
        mod = self.mod; s = self.s
        n = len(a)
        w = 1
        while w < n:
            for k in range(0, n, w << 1):
                for i in range(w):
                    self.add(a[k + w + i], a[k + i], self.pc[k + w + i])
            w <<= 1
        for i in range(n):
            for j in range(s + 1):
                a[i][j] %= mod

    def mobius(self, a: List[List[int]]) -> None:
        n = len(a)
        w = n >> 1
        while w:
            for k in range(0, n, w << 1):
                for i in range(w):
                    self.sub(a[k + w + i], a[k + i], self.pc[k + w + i])
            w >>= 1

    def lift(self, a: List[int]) -> List[List[int]]:
        A = [[0] * (self.s + 1) for _ in range(len(a))]
        for i, (x, j) in enumerate(zip(a, self.pc)): A[i][j] = x
        return A

    def unlift(self, A: List[List[int]]) -> List[int]:
        a = [0] * len(A)
        for i, (arr, j) in enumerate(zip(A, self.pc)): a[i] = arr[j]
        return a

    def prod(self, A: List[List[int]], B: List[List[int]]) -> None:
        'destructive'
        mod = self.mod; s = self.s
        n = len(A)
        d = ctz(n)
        for i in range(n):
            c = [0] * (s + 1)
            a, b = A[i], B[i]
            for j in range(d + 1):
                for k in range(d - j + 1):
                    c[j + k] += a[j] * b[k] % mod
            A[i] = c


    def multiply(self, a: List[int], b: List[int]) -> List[int]:
        A = self.lift(a); B = self.lift(b)
        self.zeta(A); self.zeta(B)
        self.prod(A, B)
        self.mobius(A)
        return self.unlift(A)
