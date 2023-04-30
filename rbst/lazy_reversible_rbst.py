from typing import Callable, Tuple, Iterable
def _rng():
    rngx = 2463534242
    while 1:
        rngx ^= rngx<<13&0xFFFFFFFF
        rngx ^= rngx>>17&0xFFFFFFFF
        rngx ^= rngx<<5&0xFFFFFFFF
        yield rngx&0xFFFFFFFF

class LazyReversibleRBSTNode:
    def __init__(self, val, lazy):
        self.l = None
        self.r = None
        self.key = val
        self.sum = val
        self.lazy = lazy
        self.cnt = 1
        self.rev = 0

class LazyReversibleRBST:
    def __init__(self, e: int, id_: int, op: Callable[[int, int], int], mapping: Callable[[int, int], int], composition: Callable[[int, int], int], ts: Callable[[int], int]) -> None:
        '''
        e: identity element of op
        id_: identity mapping s.t. id(x) == x
        op: S*S -> S
        mapping: mapping(f, x) := f(x)
        composition: composition(f, g) := fog
        '''
        self.e = e
        self.id = id_
        self.op = op
        self.mapping = mapping
        self.composition = composition
        self.ts = ts
        self.rand = _rng()

    def _toggle(self, t: LazyReversibleRBSTNode) -> None:
        if not t: return
        t.l, t.r = t.r, t.l
        t.sum = self.ts(t.sum)
        t.rev ^= 1

    def _propagate(self, t: LazyReversibleRBSTNode, F: int) -> None:
        if not t: return
        t.lazy = self.composition(t.lazy, F)
        t.key = self.mapping(t.key, F)
        t.sum = self.mapping(t.sum, F)

    def _update(self, t: LazyReversibleRBSTNode) -> LazyReversibleRBSTNode:
        if not t: return
        self._push(t)
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

    def _push(self, t: LazyReversibleRBSTNode) -> None:
        if t.rev:
            self._toggle(t.l); self._toggle(t.r)
            t.rev = 0
        if t.lazy != self.id:
            self._propagate(t.l, t.lazy); self._propagate(t.r, t.lazy)
            t.lazy = self.id

    def _merge(self, l: LazyReversibleRBSTNode, r: LazyReversibleRBSTNode) -> LazyReversibleRBSTNode:
        if not l or not r: return l if l else r
        root = None
        leaf = None
        pos = -1
        q = []
        while l and r:
            if (next(self.rand) * (l.cnt + r.cnt)) >> 32 < l.cnt:
                self._push(l)
                if not pos: leaf.r = l
                elif pos == 1: leaf.l = l
                else: root = l
                leaf = l
                l = l.r
                pos = 0
            else:
                self._push(r)
                if not pos: leaf.r = r
                elif pos == 1: leaf.l = r
                else: root = r
                leaf = r
                r = r.l
                pos = 1
            q.append(leaf)
        if r: leaf.r = r
        if l: leaf.l = l
        update = self._update
        while q: update(q.pop())
        return update(root)

    def _split(self, t: LazyReversibleRBSTNode, k: int) -> Tuple[LazyReversibleRBSTNode, LazyReversibleRBSTNode]:
        L, R = [], []
        while t:
            self._push(t)
            cnt = t.l.cnt if t.l else 0
            if k <= cnt:
                R.append(t)
                t = t.l
            else:
                k -= cnt + 1
                L.append(t)
                t = t.r
        l = None
        while L:
            tmp = L.pop()
            tmp.r = l
            self._update(tmp)
            l = tmp
        r = None
        while R:
            tmp = R.pop()
            tmp.l = r
            self._update(tmp)
            r = tmp
        return self._update(l), self._update(r)

    def _build(self, v: Iterable[int], l: int, r: int) -> LazyReversibleRBSTNode:
        if l + 1 == r: return LazyReversibleRBSTNode(v[l], self.id)
        m = l + r>>1
        pm = LazyReversibleRBSTNode(v[m], self.id)
        if l < m: pm.l = self._build(v, l, m)
        if m + 1 < r: pm.r = self._build(v, m + 1, r)
        return self._update(pm)

    def build(self, v: Iterable[int]) -> None:
        self.root = self._build(v, 0, len(v))

    def insert(self, k: int, e: int) -> None:
        '''
        insert new node to kth_index
        k: index
        e: value
        '''
        x1, x2 = self._split(self.root, k)
        self.root = self._merge(self._merge(x1, LazyReversibleRBSTNode(e, self.id)), x2)

    def erase(self, k: int) -> None:
        '''
        erase kth_indexed_node
        k: index
        '''
        x1, x2 = self._split(self.root, k)
        self.root = self._merge(x1, self._split(x2, 1)[1])

    def reverse(self, l: int, r: int) -> None:
        '''
        reverse [l, r)
        l: left
        r: right
        '''
        x1, x2 = self._split(self.root, l)
        y1, y2 = self._split(x2, r-l)
        self._toggle(y1)
        self.root = self._merge(x1, self._merge(y1, y2))

    def apply(self, l: int, r: int, F: int) -> None:
        '''
        apply F to [l, r)
        l: left
        r: right
        F: operator
        '''
        x1, x2 = self._split(self.root, l)
        y1, y2 = self._split(x2, r-l)
        self._propagate(y1, F)
        self.root = self._merge(x1, self._merge(y1, y2))

    def fold(self, l: int, r: int) -> int:
        '''
        product [l, r)
        l: left
        r: right
        return: sum
        '''
        x1, x2 = self._split(self.root, l)
        y1, y2 = self._split(x2, r-l)
        res = y1.sum if y1 else self.e
        self.root = self._merge(x1, self._merge(y1, y2))
        return res
