import sys
sys.setrecursionlimit = 10**8
from typing import TypeVar, Tuple, Iterable, Callable
T = TypeVar("T")
class SplayTreeBase:
    def __init__(self, Node) -> None:
        self.Node = Node

    def new(self, val: int) -> T:
        return self.Node(val)

    @staticmethod
    def _delete(t: T) -> None:
        if t.l: t.l.p = None
        if t.r: t.r.p = None
        if t.p:
            if t.p.l == t: t.p.l = None
            if t.p.r == t: t.p.r = None

    @staticmethod
    def _is_root(t: T) -> bool:
        return (t.p is None) or (t.p.l != t and t.p.r != t)

    @staticmethod
    def _count(t: T) -> int:
        return t.cnt if t else 0

    @staticmethod
    def _pos(t: T) -> int:
        if t.p:
            if t.p.l == t: return -1
            if t.p.r == t: return 1
        return 0

    def _rot(self, t: T) -> None:
        x = t.p; y = x.p
        if x.l == t:
            z = t.r; x.l = z
            if z: z.p = x
            t.r = x
            x.p = t
        else:
            z = t.l; x.r = z
            if z: z.p = x
            t.l = x
            x.p = t
        self._update(x)
        self._update(t)
        t.p = y
        if y:
            if y.l == x: y.l = t
            if y.r == x: y.r = t

    def _splay(self, t: T) -> None:
        self._push(t)
        q = t.p
        while not ((q is None) or (q.l != t and q.r != t)):
            r = q.p
            if (r is None) or (r.l != t and r.r != t):
                self._push(q); self._push(t); self._rot(t)
            else:
                self._push(r); self._push(q); self._push(t)
                if self._pos(q) == self._pos(t): self._rot(q); self._rot(t)
                else: self._rot(t); self._rot(t)
            q = t.p

    def _get_left(self, t: T) -> T:
        while t.l:
            self._push(t)
            t = t.l
        return t

    def _get_right(self, t: T) -> T:
        while t.r:
            self._push(t)
            t = t.r
        return t

    def _split(self, t: T, k: int) -> Tuple[T, T]:
        L, R = [], []
        while t:
            self._push(t)
            t.p = None
            if k <= self._count(t.l):
                R.append(t)
                t = t.l
            else:
                k -= self._count(t.l) + 1
                L.append(t)
                t = t.r
        l = None
        while L:
            tmp = L.pop()
            tmp.r = l
            if l: l.p = tmp
            self._update(tmp)
            l = tmp
        r = None
        while R:
            tmp = R.pop()
            tmp.l = r
            if r: r.p = tmp
            self._update(tmp)
            r = tmp
        return self._update(l), self._update(r)

    def _merge(self, l: T, r: T) -> T:
        if not l and not r: return None
        if not l:
            self._splay(r)
            return r
        if not r:
            self._splay(l)
            return l
        self._splay(l); self._splay(r)
        l = self._get_right(l)
        self._splay(l)
        l.r = r
        r.p = l
        self._update(l)
        return l

    def _build(self, v: Iterable[int], l: int, r: int) -> T:
        if not v: return None
        if l + 1 >= r: return self.new(v[l])
        return self._merge(self._build(v, l, l + r >> 1), self._build(v, l + r >> 1, r))

    def build(self, v: Iterable[int]) -> None:
        self.root = self._build(v, 0, len(v))

    def insert(self, t: T, k: int, val: int) -> None:
        '''
        insert new node to kth_index of t
        t: reference node
        k: index
        val: value
        '''
        self._splay(t)
        x1, x2 = self._split(t, k)
        self.root = self._merge(self._merge(x1, self.new(val)), x2)

    def erase(self, t: T, k: int) -> None:
        '''
        erase kth_indexed_node of t
        t: reference node
        k: index
        '''
        self._splay(t)
        x1, x2 = self._split(t, k)
        y1, y2 = self._split(x2, 1)
        self._delete(y1)
        self.root = self._merge(x1, y2)
