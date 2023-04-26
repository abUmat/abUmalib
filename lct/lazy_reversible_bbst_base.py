# my module
from lct.splay_tree_base import *
# my module
class LazyReversibleBBST(SplayTreeBase):
    def __init__(self, Node, e: int, id_: int, op: Callable[[int, int], int], mapping: Callable[[int, int], int], composition: Callable[[int, int], int], ts: Callable[[int], int]) -> None:
        super().__init__(Node, e, id_)
        self.op = op
        self.mapping = mapping
        self.composition = composition
        self.ts = ts

    def _toggle(self, t: T) -> None:
        if not t: return
        t.l, t.r = t.r, t.l
        t.sum = self.ts(t.sum)
        t.rev ^= 1

    def _sum(self, t: T) -> None:
        return t.sum if t else self.e

    def _propagate(self, t: T, F: int) -> None:
        if not t: return
        t.lazy = self.composition(t.lazy, F)
        t.key = self.mapping(t.key, F)
        t.sum = self.mapping(t.sum, F)

    def _update(self, t: T) -> T:
        if not t: return
        l, r = t.l, t.r
        cnt = 1
        s = t.key
        if l:
            cnt += l.cnt
            s = self.op(l.sum, s)
        if r:
            cnt += r.cnt
            s = self.op(s, r.sum)
        t.cnt = cnt; t.sum = s
        return t

    def _push(self, t: T) -> None:
        if not t: return
        if t.rev:
            self._toggle(t.l); self._toggle(t.r)
            t.rev = 0
        if t.lazy != self.id:
            self._propagate(t.l, t.lazy); self._propagate(t.r, t.lazy)
            t.lazy = self.id

    def reverse(self, t: T, l: int, r: int) -> None:
        '''
        reverse [l, r) of t
        t: reference node
        l: left
        r: right
        '''
        x1, x2 = self._split(t, l)
        y1, y2 = self._split(x2, r-l)
        self._toggle(y1)
        self.root = self._merge(x1, self._merge(y1, y2))

    def apply(self, t: T, l: int, r: int, F: int) -> None:
        '''
        apply F to [l, r) of t
        t: reference node
        l: left
        r: right
        F: operator
        '''
        x1, x2 = self._split(t, l)
        y1, y2 = self._split(x2, r-l)
        self._propagate(y1, F)
        self.root = self._merge(x1, self._merge(y1, y2))

    def fold(self, t: T, l: int, r: int) -> int:
        '''
        product [l, r) of t
        t: reference node
        l: left
        r: right
        return: sum
        '''
        x1, x2 = self._split(t, l)
        y1, y2 = self._split(x2, r-l)
        res = self._sum(y1)
        self.root = self._merge(x1, self._merge(y1, y2))
        return res
