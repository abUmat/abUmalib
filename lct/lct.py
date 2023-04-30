from typing import TypeVar, Tuple, Iterable, Callable
T = TypeVar("T")
class ReversibleSplayTreeNode:
    def __init__(self, e: int):
        self.l = None
        self.r = None
        self.p = None
        self.key = e
        self.sum = e
        self.cnt = 1
        self.rev = 0
Node = ReversibleSplayTreeNode

class LinkCutTree:
    def __init__(self, e: int, op: Callable[[int, int], int], ts: Callable[[int], int]):
        self.e = e
        self.op = op
        self.ts = ts

    def new(self, val: int) -> T:
        return Node(val)

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
        if x: self._update(x)
        if t: self._update(t)
        t.p = y
        if y:
            if y.l == x: y.l = t
            if y.r == x: y.r = t

    def _splay(self, t: T) -> None:
        self._push(t)
        q = t.p
        while not ((q is None) or (q.l != t and q.r != t)):
            r = q.p
            if ((r is None) or (r.l != t and r.r != t)):
                self._push(q); self._push(t); self._rot(t)
            else:
                self._push(r); self._push(q); self._push(t)
                if self._pos(q) == self._pos(t): self._rot(q); self._rot(t)
                else: self._rot(t); self._rot(t)
            q = t.p

    def _update(self, t: T) -> T:
        cnt = 1
        sm = t.key
        l, r = t.l, t.r
        if l:
            cnt += l.cnt
            sm = self.op(l.sum, sm)
        if r:
            cnt += r.cnt
            sm = self.op(sm, r.sum)
        t.cnt = cnt; t.sum = sm
        return t

    def _push(self, t: T) -> None:
        if t.rev:
            if t.l: self._toggle(t.l)
            if t.r: self._toggle(t.r)
            t.rev = 0

    def _toggle(self, t: T) -> None:
        t.l, t.r = t.r, t.l
        t.sum = self.ts(t.sum)
        t.rev ^= 1

    def _expose(self, t: T) -> T:
        rp = None
        cur = t
        while cur:
            self._splay(cur)
            cur.r = rp
            self._update(cur)
            rp = cur
            cur = cur.p
        self._splay(t)
        return rp

    def _evert(self, t: T) -> None:
        self._expose(t)
        self._toggle(t)
        self._push(t)

    def link(self, u: T, v: T) -> None:
        self._evert(u)
        # self.expose(v)
        u.p = v

    def cut(self, u: T, v: T) -> None:
        self._evert(u)
        self._expose(v)
        v.l = None; u.p = None
        self._update(v)

    def lca(self, u: T, v: T) -> T:
        if self.get_root(u) != self.get_root(v): return None
        self._expose(u)
        return self._expose(v)

    def get_kth(self, x: T, k: int) -> T:
        self._expose(x)
        while x:
            self._push(x)
            if x.r and x.r.cnt > k:
                x = x.r
            else:
                if x.r: k -= x.r.cnt
                if k == 0: return x
                k -= 1
                x = x.l
        return None

    def get_root(self, x: T) -> T:
        self._expose(x)
        while x.l:
            self._push(x)
            x = x.l
        return x

    def get_parent(self, x: T) -> T:
        self._expose(x)
        p = x.l
        if not p: return None
        while 1:
            self._push(p)
            if not p.r: return p
            p = p.r

    def set_key(self, t: T, key: int) -> None:
        self._splay(t)
        t.key = key
        self._update(t)

    def get_key(self, t: T) -> int:
        return t.key

    def fold(self, u: T, v: T) -> int:
        self._evert(u)
        self._expose(v)
        return v.sum
