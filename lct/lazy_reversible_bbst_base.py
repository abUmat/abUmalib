# my module
from lct.splay_tree_base import *
# my module
class LazyReversibleBBST(SplayTreeBase):
    def __init__(self, Node, e, id_, op, mapping, composition, ts):
        super().__init__(Node, e, id_)
        self.op = op
        self.mapping = mapping
        self.composition = composition
        self.ts = ts

    def fold(self, t, a, b):
        x1, x2 = self.split(t, a)
        y1, y2 = self.split(x2, b-a)
        return self._sum(y1), self.merge(x1, self.merge(y1, y2))

    def reverse(self, t, a, b):
        x1, x2 = self.split(t, a)
        y1, y2 = self.split(x2, b-a)
        self.toggle(y1)
        return self.merge(x1, self.merge(y1, y2))

    def apply(self, t, a, b, F):
        x1, x2 = self.split(t, a)
        y1, y2 = self.split(x2, b-a)
        self.propagate(y1, F)
        return self.merge(x1, self.merge(y1, y2))

    def toggle(self, t):
        if not t: return
        t.l, t.r = t.r, t.l
        t.sum = self.ts(t.sum)
        t.rev ^= 1

    def _sum(self, t): return t.sum if t else self.e

    #override
    def update(self, t):
        if not t: return
        t.cnt = 1
        t.sum = t.key
        if t.l:
            t.cnt += t.l.cnt
            t.sum = self.op(t.l.sum, t.sum)
        if t.r:
            t.cnt += t.r.cnt
            t.sum = self.op(t.sum, t.r.sum)

    #override
    def push(self, t):
        if not t: return
        if t.rev:
            self.toggle(t.l); self.toggle(t.r)
            t.rev = 0
        if t.lazy != self.id:
            self.propagate(t.l, t.lazy); self.propagate(t.r, t.lazy)
            t.lazy = self.id

    def propagate(self, t, F):
        if not t: return
        t.lazy = self.composition(t.lazy, F)
        t.key = self.mapping(t.key, F)
        t.sum = self.mapping(t.sum, F)
