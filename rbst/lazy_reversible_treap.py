from typing import Callable, Tuple, Iterable
def _rng():
    rngx = 2463534242
    while 1:
        rngx ^= rngx<<13&0xFFFFFFFF
        rngx ^= rngx>>17&0xFFFFFFFF
        rngx ^= rngx<<5&0xFFFFFFFF
        yield rngx&0xFFFFFFFF
rand_generator = _rng()

class LazyReversibleTreapNode:
    def __init__(self, val, lazy):
        self.l = None
        self.r = None
        self.key = val
        self.sum = val
        self.lazy = lazy
        self.cnt = 1
        self.rev = 0
        self.pr = next(rand_generator)

class LazyReversibleTreap:
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

    def _toggle(self, t: LazyReversibleTreapNode) -> None:
        if not t: return
        t.l, t.r = t.r, t.l
        t.sum = self.ts(t.sum)
        t.rev ^= 1

    def _propagate(self, t: LazyReversibleTreapNode, F: int) -> None:
        if not t: return
        t.lazy = self.composition(t.lazy, F)
        t.key = self.mapping(t.key, F)
        t.sum = self.mapping(t.sum, F)

    def _update(self, t: LazyReversibleTreapNode) -> LazyReversibleTreapNode:
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

    def _push(self, t: LazyReversibleTreapNode) -> None:
        if t.rev:
            self._toggle(t.l); self._toggle(t.r)
            t.rev = 0
        if t.lazy != self.id:
            self._propagate(t.l, t.lazy); self._propagate(t.r, t.lazy)
            t.lazy = self.id

    def _merge(self, l: LazyReversibleTreapNode, r: LazyReversibleTreapNode) -> LazyReversibleTreapNode:
        if not l or not r: return l if l else r
        root = None
        leaf = None
        pos = 0
        q = []
        while l and r:
            if l.pr >= r.pr:
                self._push(l)
                if pos == 0: root = l
                elif pos == 1: leaf.r = l
                else: leaf.l = l
                leaf = l
                l = l.r
                pos = 1
            else:
                self._push(r)
                if pos == 0: root = r
                elif pos == 1: leaf.r = r
                else: leaf.l = r
                leaf = r
                r = r.l
                pos = -1
            q.append(leaf)
        if r: leaf.r = r
        if l: leaf.l = l
        while q: self._update(q.pop())
        return self._update(root)

    def _split(self, t: LazyReversibleTreapNode, k: int) -> Tuple[LazyReversibleTreapNode, LazyReversibleTreapNode]:
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

    def _dfs(self, t: LazyReversibleTreapNode) -> None:
        from collections import defaultdict
        q = [t]
        route = []
        used = defaultdict(int)
        while q:
            node = q.pop()
            if used[node]: continue
            used[node] = 1
            route.append(node)
            if node.l: q.append(node.l)
            if node.r: q.append(node.r)
        while route: self._update(route.pop())

    def build(self, arr: Iterable[int]) -> None:
        n = len(arr)
        ps = [LazyReversibleTreapNode(x, self.id) for x in arr]
        p = [-1] * n
        st = []
        for i in range(n):
            prv = -1
            while st and ps[i].pr > ps[st[-1]].pr: prv = st.pop()
            if prv != -1: p[prv] = i
            if st: p[i] = st[-1]
            st.append(i)
        root = -1
        for i in range(n):
            if p[i] != -1:
                if i < p[i]: ps[p[i]].l = ps[i]
                else: ps[p[i]].r = ps[i]
            else:
                root = i
        self._dfs(ps[root])
        self.root = ps[root]

    def insert(self, k: int, val: int) -> None:
        '''
        insert new node to kth_index
        k: index
        val: value
        '''
        x1, x2 = self._split(self.root, k)
        self.root = self._merge(self._merge(x1, LazyReversibleTreapNode(val, self.id)), x2)

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
