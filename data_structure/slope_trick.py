# my module
from misc.typing_template import *
# my module
# https://nyaannyaan.github.io/library/data-structure/slope-trick.hpp
from heapq import heappop, heappush
class SlopeTrick:
    def _pushL(self, x: int, c: int=1) -> None:
        heappush(self._L, (-x + self._addL, -c))

    def _pushR(self, x: int, c: int=1) -> None:
        heappush(self._R, (x - self._addR, c))

    def _getL(self) -> Tuple[int, int]:
        lx, lc = heappop(self._L)
        heappush(self._L, (lx, lc))
        return -lx + self._addL, -lc

    def _getR(self) -> Tuple[int, int]:
        rx, rc = heappop(self._R)
        heappush(self._R, (rx, rc))
        return rx + self._addR, rc

    def _popL(self) -> Tuple[int, int]:
        lx, lc = heappop(self._L)
        return -lx + self._addL, -lc

    def _popR(self) -> Tuple[int, int]:
        rx, rc = heappop(self._R)
        return rx + self._addR, rc

    def __init__(self) -> None:
        self._addL = 0
        self._addR = 0
        self._min_y = 0
        self._L = []
        self._R = []

    def get_min(self) -> Tuple[int, int]:
        '''
        return: (x, y) s.t. (argmin, min)
        '''
        if not self._L:
            if not self._R:
                x = 0
            else:
                x = self._getR()[0]
        else:
            x = self._getL()[0]
        return x, self._min_y

    def shift_L(self, a: int) -> None:
        self._addL += a

    def shift_R(self, a: int) -> None:
        self._addR += a

    def shift_x(self, a: int) -> None:
        self._addL += a
        self._addR += a

    def shift_y(self, a: int) -> None:
        self._min_y += a

    def add_xma(self, a: int, c: int=1) -> None:
        '''add max(0, x - a) ____/'''
        used = 0
        while used < c and self._L:
            X, C = self._getL()
            if X < a: break
            self._popL()
            tmp = min(c - used, C)
            self._pushR(X, tmp)
            if C != tmp: self._pushL(X, C - tmp)
            self._min_y += (X - a) * tmp
            used += tmp
        if used: self._pushL(a, used)
        if c - used: self._pushR(a, c - used)

    def add_amx(self, a: int, c: int=1) -> None:
        '''add max(0, a - x) \____'''
        used = 0
        while used < c and self._R:
            X, C = self._getR()
            if X >= a: break
            self._popR()
            tmp = min(c - used, C)
            self._pushL(X, tmp)
            if C != tmp: self._pushR(X, C - tmp)
            self._min_y += (a - X) * tmp
            used += tmp
        if used: self._pushR(a, used)
        if c - used: self._pushL(a, c - used)

    def add_abs_xma(self, a: int, c: int=1) -> None:
        '''add |x - a| \/'''
        self.add_xma(a, c)
        self.add_amx(a, c)

    def chmin_right(self):
        '''chmin right side \_/ -> \__'''
        self._R = []

    def chmin_left(self):
        '''chmin left side \_/ -> __/'''
        self._L = []

    def merge(self, r):
        '''destructive merge'''
        if len(self._L) + len(self._R) < len(r.L) + len(r.R):
            self, r = r, self
        while r._L:
            x, c = r._popL()
            self.add_amx(x, c)
        while r._R:
            x, c = r._popR()
            self.add_xma(x, c)
        self.shift_y(r._min_y)
