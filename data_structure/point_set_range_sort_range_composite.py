def _rng():
    rngx = 2463534242
    while 1:
        rngx ^= rngx<<13&0xFFFFFFFF
        rngx ^= rngx>>17&0xFFFFFFFF
        rngx ^= rngx<<5&0xFFFFFFFF
        yield rngx&0xFFFFFFFF
_rand = _rng()

class Node:
    def __init__(self, key: int, val: int, p: int) -> None:
        self.key = self.kmin = self.kmax = key
        self.val = self.sum = val
        self.flip = 0
        self.size_all = self.size_inner = 1
        self.p = p
        self.inner_l = self.inner_r = self.outer_l = self.outer_r = None

from typing import Tuple
class SegmentTreeRangeSortRangeComposite:
    def __init__(self, e, op, ts, v) -> None:
        self.e = e
        self.op = op
        self.ts = ts
        self.root = self.build(0, len(v), v) if v else None

    def _update(self, v: Node):
        v.size_inner = 1
        v.sum = self.e
        if v.outer_l:
            v.sum = v.outer_l.sum
        if v.inner_l:
            v.size_inner += v.inner_l.size_inner
            v.sum = self.op(v.sum, v.inner_l.sum)
            v.kmin = min(v.kmin, v.inner_l.kmin)
            v.kmax = max(v.kmax, v.inner_l.kmax)
        v.sum = self.op(v.sum, v.val)
        if v.inner_r:
            v.size_inner += v.inner_r.size_inner
            v.sum = self.op(v.sum, v.inner_r.sum)
            v.kmin = min(v.kmin, v.inner_r.kmin)
            v.kmax = max(v.kmax, v.inner_r.kmax)
        if v.outer_r:
            v.sum = self.op(v.sum, v.outer_r.sum)
        v.size_all = v.size_inner + (v.outer_l.size_all if v.outer_l else 0) + (v.outer_r.size_all if v.outer_r else 0)

    def update_range_inner(self, v: Node, l: int, r: int, f) -> None:
        return

    def update_range_outer(self, v: Node, l: int, r: int, f) -> None:
        return

    @staticmethod
    def size(v: Node) -> int:
        return v.size_all if v else 0

    @staticmethod
    def new(key: int, val: int) -> Node:
        return Node(key, val, next(_rand))

    def _flip(self, v: Node) -> None:
        v.inner_l, v.inner_r = v.inner_r, v.inner_l
        v.outer_l, v.outer_r = v.outer_r, v.outer_l
        v.sum = self.ts(v.sum)
        v.flip ^= 1

    def push_down(self, v: Node) -> None:
        if not v.flip: return
        if v.inner_l: self._flip(v.inner_l)
        if v.inner_r: self._flip(v.inner_r)
        if v.outer_l: self._flip(v.outer_l)
        if v.outer_r: self._flip(v.outer_r)
        v.flip = 0

    def _insert(self, v: Node, n: Node, k: int) -> Node:
        if not v: return n
        self.push_down(v)
        szl = self.size(v.outer_l)
        if v.p < n.p:
            s1, s2 = self.split_outer(v, k)
            n.outer_l = s1; n.outer_r = s2
            self._update(n)
            return n
        elif szl <= k and k < szl + v.size_inner:
            s1, s2 = self.split_outer(v, k)
            s1 = self._insert(s1, n, k)
            self._update(s1)
            return self.merge_outer(s1, s2)
        elif k < szl:
            v.outer_l = self._insert(v.outer_l, n, k)
        else:
            v.outer_r = self._insert(v.outer_r, n, k - szl - v.size_inner)
        self._update(v)
        return v

    def merge_inner(self, a: Node, b: Node) -> Node:
        if not a or not b: return a if a else b
        self.push_down(a); self.push_down(b)
        if a.p > b.p:
            a.inner_r = self.merge_inner(a.inner_r, b)
            self._update(a)
            return a
        else:
            b.inner_l = self.merge_inner(a, b.inner_l)
            self._update(b)
            return b

    def merge_outer(self, a: Node, b: Node) -> Node:
        if not a or not b: return a if a else b
        self.push_down(a); self.push_down(b)
        if a.p > b.p:
            a.outer_r = self.merge_outer(a.outer_r, b)
            self._update(a)
            return a
        else:
            b.outer_l = self.merge_outer(a, b.outer_l)
            self._update(b)
            return b

    def merge_compress(self, a: Node, b: Node) -> Node:
        if not a or not b: return a if a else b
        self.push_down(a); self.push_down(b)
        if a.p < b.p: a, b = b, a
        if a.key < b.kmin: a.inner_r = self.merge_compress(a.inner_r, b)
        elif b.kmax < a.key: a.inner_l = self.merge_compress(a.inner_l, b)
        else:
            bl, br = self.split_key(b, a.key)
            a.inner_l = self.merge_compress(a.inner_l, bl)
            a.inner_r = self.merge_compress(a.inner_r, br)
        self._update(a)
        return a

    def cut_inner(self, v: Node, k: int) -> Tuple[Node, Node, Node]:
        if not v: return None, None, None
        self.push_down(v)
        szl = self.size(v.inner_l)
        if k < szl:
            a, b, c = self.cut_inner(v.inner_l, k)
            v.inner_l = c
            self._update(v)
            return a, b, v
        elif k == szl:
            res = v.inner_l, v, v.inner_r
            v.inner_l = v.inner_r = None
            self._update(v)
            return res
        else:
            a, b, c = self.cut_inner(v.inner_r, k - szl - 1)
            v.inner_r = a
            self._update(v)
            return v, b, c

    def cut_outer(self, v: Node, k: int) -> Tuple[Node, Node, Node]:
        if not v: return None, None, None
        self.push_down(v)
        szl = self.size(v.outer_l)
        szr = szl + v.size_inner
        if k < szl:
            a, b, c = self.cut_outer(v.outer_l, k)
            v.outer_l = c
            self._update(v)
            return a, b, v
        elif szr <= k:
            a, b, c = self.cut_outer(v.outer_r, k - szr)
            v.outer_r = a
            self._update(v)
            return v, b, c
        else:
            tmp_l, tmp_r = v.outer_l, v.outer_r
            v.outer_l = v.outer_r = None
            a, b, c = self.cut_inner(v, k - szl)
            a = self.merge_outer(tmp_l, a)
            c = self.merge_outer(c, tmp_r)
            return a, b, c

    def split_inner(self, v: Node, k: int) -> Tuple[Node, Node]:
        if not v: return None, None
        self.push_down(v)
        szl = self.size(v.inner_l)
        if k <= szl:
            s1, s2 = self.split_inner(v.inner_l, k)
            v.inner_l = s2
            self._update(v)
            return s1, v
        else:
            s1, s2 = self.split_inner(v.inner_r, k - szl - 1)
            v.inner_r = s1
            self._update(v)
            return v, s2

    def split_outer(self, v: Node, k: int) -> Tuple[Node, Node]:
        if not v: return None, None
        self.push_down(v)
        szl = self.size(v.outer_l)
        szr = szl + v.size_inner
        if k < szl:
            s1, s2 = self.split_outer(v.outer_l, k)
            v.outer_l = s2
            self._update(v)
            return s1, v
        elif szr <= k:
            s1, s2 = self.split_outer(v.outer_r, k - szr)
            v.outer_r = s1
            self._update(v)
            return v, s2
        else:
            tmp_l, tmp_r = v.outer_l, v.outer_r
            v.outer_l = v.outer_r = None
            s1, s2 =self.split_inner(v, k - szl)
            s1 = self.merge_outer(tmp_l, s1)
            s2 = self.merge_outer(s2, tmp_r)
            return s1, s2

    def split_range_outer(self, v: Node, l: int, r: int) -> Tuple[Node, Node, Node]:
        a, b = self.split_outer(v, l)
        bb, c = self.split_outer(b, r - l)
        return a, bb, c

    def split_key(self, v: Node, key: int) -> Tuple[Node, Node]:
        if not v: return None, None
        if key < v.kmin: return None, v
        if v.kmax <= key: return v, None
        self.push_down(v)
        if key < v.key:
            s1, s2 = self.split_key(v.inner_l, key)
            v.inner_l = s2
            self._update(v)
            return s1, v
        else:
            s1, s2 = self.split_key(v.inner_r, key)
            v.inner_r = s1
            self._update(v)
            return v, s2

    def query_range_inner(self, v: Node, l: int, r: int) -> int:
        if not v: return self.e
        if l == 0 and r == v.size_all: return v.sum
        self.push_down(v)
        szl = self.size(v.inner_l)
        szr = szl + 1
        left_q = right_q = self.e
        if l < szl:
            if r <= szl: return self.query_range_inner(v.inner_l, l, r)
            left_q = self.query_range_inner(v.inner_l, l, szl)
            l = szl
        if szr < r:
            if szr <= l: return self.query_range_inner(v.inner_r, l - szr, r - szr)
            right_q = self.query_range_inner(v.inner_r, 0, r - szr)
            r = szr
        res = self.e if l == r else v.val
        res = self.op(left_q, res)
        res = self.op(res, right_q)
        return res

    def query_range_outer(self, v: Node, l: int, r: int) -> int:
        if not v: return self.e
        if l == 0 and r == v.size_all: return v.sum
        self.push_down(v)
        szl = self.size(v.outer_l)
        szr = szl + 1
        left_q = right_q = self.e
        if l < szl:
            if r <= szl: return self.query_range_outer(v.outer_l, l, r)
            left_q = self.query_range_outer(v.outer_l, l, szl)
            l = szl
        if szr < r:
            if szr <= l: return self.query_range_outer(v.outer_r, l - szr, r - szr)
            right_q = self.query_range_outer(v.outer_r, 0, r - szr)
            r = szr
        res = self.e if l == r else self.query_range_inner(v, l - szl, r - szl)
        res = self.op(left_q, res)
        res = self.op(res, right_q)
        return res

    def sort_inner(self, v: Node) -> Node:
        if not v: return None
        tmp_l, tmp_r = v.outer_l, v.outer_r
        res = self.sort_inner(tmp_l)
        v.outer_l = v.outer_r = None
        self.push_down(v)
        if (v.inner_l and v.key < v.inner_l.kmax) or (v.inner_r and v.inner_r.kmin < v.key): self._flip(v)
        res = self.merge_compress(res, v)
        res = self.merge_compress(res, self.sort_inner(tmp_r))
        return res

    def enumerate_inner(self, v: Node, res) -> None:
        if not v: return
        self.push_down(v)
        if v.inner_l: self.enumerate_inner(v.inner_l, res)
        res.append((v.key, v.val))
        if v.inner_r: self.enumerate_inner(v.inner_r, res)

    def enumerate_outer(self, v: Node, res) -> None:
        if not v: return
        self.push_down(v)
        if v.outer_l: self.enumerate_outer(v.outer_l, res)
        self.enumerate_inner(v, res)
        if v.outer_r: self.enumerate_outer(v.outer_r, res)

    def p_satisfy(self, v: Node) -> None:
        if not v.outer_l:
            if not v.outer_r or v.p > v.outer_r.p: return
            v.p, v.outer_r.p = v.outer_r.p, v.p
            self.p_satisfy(v.outer_r)
        elif not v.outer_r:
            if v.p > v.outer_l.p: return
            v.p, v.outer_l.p = v.outer_l.p, v.p
            self.p_satisfy(v.outer_l)
        else:
            if v.outer_l.p > v.outer_r.p:
                if v.p > v.outer_l.p: return
                v.p, v.outer_l.p = v.outer_l.p, v.p
                self.p_satisfy(v.outer_l)
            else:
                if not v.outer_r or v.p > v.outer_r.p: return
                v.p, v.outer_r.p = v.outer_r.p, v.p
                self.p_satisfy(v.outer_r)

    def build(self, l: int, r: int, v) -> Node:
        mid = l + r >> 1
        u = self.new(*v[mid])
        if l < mid:
            u.outer_l = self.build(l, mid, v)
        else:
            u.outer_l = None
        if mid + 1 < r:
            u.outer_r = self.build(mid + 1, r, v)
        else:
            u.outer_r = None
        self.p_satisfy(u)
        self._update(u)
        return u

    def insert(self, k: int, key: int, val: int) -> None:
        self.root = self._insert(self.root, self.new(key, val), k)

    def erase(self, k: int) -> None:
        a, b, c = self.cut_outer(self.root, k)
        self.root = self.merge_outer(a, c)

    def set(self, k: int, key: int, val: int) -> None:
        a, b, c = self.cut_outer(self.root, k)
        b.key = key
        b.val = val
        self._update(b)
        self.root = self.merge_outer(a, self.merge_outer(b, c))

    def update(self, k: int, val: int) -> None:
        a, b, c = self.cut_outer(self.root, k)
        b.val = self.op(b.val, val)
        self._update(b)
        self.root = self.merge_outer(a, self.merge_outer(b, c))

    def query(self, l: int, r: int) -> int:
        if l == r: return self.e
        return self.query_range_outer(self.root, l, r)

    def query_all(self, l: int, r: int) -> int:
        return self.root.sum

    def reverse(self, l: int, r: int) -> None:
        if l == r: return
        a, b, c = self.split_range_outer(self.root, l, r)
        self._flip(b)
        self.root = self.merge_outer(a, self.merge_outer(b, c))

    def sort_ascending(self, l: int, r: int) -> None:
        if l == r: return
        a, b, c = self.split_range_outer(self.root, l, r)
        b = self.sort_inner(b)
        res = []
        for i in range(N):
            q = seg.query(i, i + 1)
            x, y = q >> 60, q >> 30 & ((1<<30)-1)
            res.append([x, y])
        print('f', res)

        self.root = self.merge_outer(a, self.merge_outer(b, c))

    def sort_descending(self, l: int, r: int) -> None:
        if l == r: return
        a, b, c = self.split_range_outer(self.root, l, r)
        b = self.sort_inner(b)
        self._flip(b)
        self.root = self.merge_outer(a, self.merge_outer(b, c))

    def to_list(self):
        res = []
        self.enumerate_outer(self.root, res)
        return res

mod = 998244353
mask = (1 << 30) - 1
N, Q = map(int,input().split())
v = []
for _ in range(N):
    p, a, b = map(int,input().split())
    v.append((p, a << 60 | b << 30 | b))

def op(x: int, y: int) -> int:
    a, b, c = x >> 60, x >> 30 & mask, x & mask
    e, f, g = y >> 60, y >> 30 & mask, y & mask
    p, q, r = a * e, b * e + f, g * a + c
    p %= mod; q %= mod; r %= mod
    return p << 60 | q << 30 | r
def ts(x: int) -> int:
    a, b, c = x >> 60, x >> 30 & mask, x & mask
    return a << 60 | c << 30 | b

def printseg():
    tmp = seg.to_list()
    res = [[x, y >> 60, y >> 30 & mask, y & mask] for x, y in tmp]
    print(res)
    res = []
    for i in range(N):
        q = seg.query(i, i + 1)
        a, b= q >> 60, q >> 30 & mask
        res.append([a, b])
    print(res)

def printnode(v: Node, end='\n'):
    key, val = v.key, v.val
    print(key, val >> 60, val >> 30 & mask, val & mask, 'l', v.outer_l.key if v.outer_l else None, 'r', v.outer_r.key if v.outer_r else None, end=end)

seg = SegmentTreeRangeSortRangeComposite(1 << 60, op, ts, v)
printseg()

for _ in range(Q):
    cmd, *arg = map(int,input().split())
    print(cmd, *arg)
    if cmd == 0:
        i, p, a, b = arg
        seg.set(i, p, a << 60 | b << 30 | b)
    elif cmd == 1:
        l, r, x = arg
        q = seg.query(l, r)
        print(((q >> 60) * x + (q >> 30 & mask)) % mod)
    elif cmd == 2:
        l, r = arg
        seg.sort_ascending(l, r)
    else:
        l, r = arg
        seg.sort_descending(l, r)
    printseg()
