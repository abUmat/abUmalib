from typing import Tuple, TypeVar
T = TypeVar("T")
def _rng():
    rngx = 2463534242
    while 1:
        rngx ^= rngx<<13&0xFFFFFFFF
        rngx ^= rngx>>17&0xFFFFFFFF
        rngx ^= rngx<<5&0xFFFFFFFF
        yield rngx&0xFFFFFFFF
_rand = _rng()

class _Node:
    def __init__(self, key: int, val: T) -> None:
        self.key = self.kmin = self.kmax = key
        self.val = self.sum = val
        self.flip = 0
        self.size_all = self.size_inner = 1
        self.p = next(_rand)
        self.inner_l = self.inner_r = self.outer_l = self.outer_r = None

    def toggle(self) -> None:
        self.inner_l, self.inner_r = self.inner_r, self.inner_l
        self.outer_l, self.outer_r = self.outer_r, self.outer_l
        self.sum = ts(self.sum)
        self.flip ^= 1

    def push_down(self) -> None:
        if not self.flip: return
        if self.inner_l: self.inner_l.toggle()
        if self.inner_r: self.inner_r.toggle()
        if self.outer_l: self.outer_l.toggle()
        if self.outer_r: self.outer_r.toggle()
        self.flip = 0

    def update(self) -> None:
        self.size_inner = 1
        self.size_all = 0
        self.kmin = self.kmax = self.key
        self.sum = ide_ele
        if self.outer_l:
            self.sum = self.outer_l.sum
            self.size_all = self.outer_l.size_all
        if self.inner_l:
            self.size_inner += self.inner_l.size_inner
            self.sum = op(self.sum, self.inner_l.sum)
            self.kmin = min(self.kmin, self.inner_l.kmin)
            self.kmax = max(self.kmax, self.inner_l.kmax)
        self.sum = op(self.sum, self.val)
        if self.inner_r:
            self.size_inner += self.inner_r.size_inner
            self.sum = op(self.sum, self.inner_r.sum)
            self.kmin = min(self.kmin, self.inner_r.kmin)
            self.kmax = max(self.kmax, self.inner_r.kmax)
        if self.outer_r:
            self.sum = op(self.sum, self.outer_r.sum)
            self.size_all += self.outer_r.size_all
        self.size_all += self.size_inner

Node = _Node
class SegmentTreeRangeSortRangeComposite:
    def __init__(self, v) -> None:
        self.root = self._build(0, len(v), v) if v else None

    @staticmethod
    def _size(v: Node) -> int:
        return v.size_all if v else 0

    @classmethod
    def _update_range_inner(cls, v: Node, l: int, r: int, f) -> None:
        if not v: return
        if l == 0 and r == v.size_all:
            f(v)
            return
        v.push_down()
        szl = cls.size(v.inner_l)
        szr = szl + 1
        if l < szl:
            if r <= szl:
                cls._update_range_inner(v.inner_l, l, r, f)
                return
            cls._update_range_inner(v.inner_l, l, szl, f)
            l = szl
        if szr < r:
            if szr <= l:
                cls._update_range_inner(v.inner_r, l - szr, r - szr, f)
                return
            cls._update_range_inner(v.inner_r, 0, r - szr, f)
            r = szr
        if l != r: f(v)

    @classmethod
    def _update_range_outer(cls, v: Node, l: int, r: int, f) -> None:
        if not v: return
        if l == 0 and r == v.size_all:
            f(v)
            return
        v.push_down()
        szl = cls.size(v.outer_l)
        szr = szl + v.size_inner
        if l < szl:
            if r <= szl:
                cls._update_range_outer(v.outer_l, l, r, f)
                return
            cls._update_range_outer(v.outer_l, l, szl, f)
            l = szl
        if szr < r:
            if szr <= l:
                cls._update_range_outer(v.outer_r, l - szr, r - szr, f)
                return
            cls._update_range_outer(v.outer_r, 0, r - szr, f)
            r = szr
        if l != r: f(v)

    @classmethod
    def _merge_inner(cls, a: Node, b: Node) -> Node:
        if not a or not b: return b if not a else a
        a.push_down(); b.push_down()
        if a.p > b.p:
            a.inner_r = cls._merge_inner(a.inner_r, b)
            a.update()
            return a
        else:
            b.inner_l = cls._merge_inner(a, b.inner_l)
            b.update()
            return b

    @classmethod
    def _merge_outer(cls, a: Node, b: Node) -> Node:
        if not a or not b: return b if not a else a
        a.push_down(); b.push_down()
        if a.p > b.p:
            a.outer_r = cls._merge_outer(a.outer_r, b)
            a.update()
            return a
        else:
            b.outer_l = cls._merge_outer(a, b.outer_l)
            b.update()
            return b

    @classmethod
    def _merge_compress(cls, a: Node, b: Node) -> Node:
        if not a or not b: return b if not a else a
        a.push_down(); b.push_down()
        if a.p < b.p: a, b = b, a
        if a.key < b.kmin: a.inner_r = cls._merge_compress(a.inner_r, b)
        elif b.kmax < a.key: a.inner_l = cls._merge_compress(a.inner_l, b)
        else:
            bl, br = cls._split_key(b, a.key)
            a.inner_l = cls._merge_compress(a.inner_l, bl)
            a.inner_r = cls._merge_compress(a.inner_r, br)
        a.update()
        return a

    @classmethod
    def _split_inner(cls, v: Node, k: int) -> Tuple[Node, Node]:
        if not v: return None, None
        v.push_down()
        szl = cls._size(v.inner_l)
        if k <= szl:
            s1, v.inner_l = cls._split_inner(v.inner_l, k)
            v.update()
            return s1, v
        else:
            v.inner_r, s2 = cls._split_inner(v.inner_r, k - szl - 1)
            v.update()
            return v, s2

    @classmethod
    def _split_outer(cls, v: Node, k: int) -> Tuple[Node, Node]:
        if not v: return None, None
        v.push_down()
        szl = cls._size(v.outer_l)
        szr = szl + v.size_inner
        if k < szl:
            s1, v.outer_l = cls._split_outer(v.outer_l, k)
            v.update()
            return s1, v
        elif szr <= k:
            v.outer_r, s2 = cls._split_outer(v.outer_r, k - szr)
            v.update()
            return v, s2
        else:
            tmp_l, tmp_r = v.outer_l, v.outer_r
            v.outer_l = v.outer_r = None
            s1, s2 =cls._split_inner(v, k - szl)
            s1 = cls._merge_outer(tmp_l, s1)
            s2 = cls._merge_outer(s2, tmp_r)
            return s1, s2

    @classmethod
    def _split_range_outer(cls, v: Node, l: int, r: int) -> Tuple[Node, Node, Node]:
        a, b = cls._split_outer(v, l)
        bb, c = cls._split_outer(b, r - l)
        return a, bb, c

    @classmethod
    def _split_key(cls, v: Node, key: int) -> Tuple[Node, Node]:
        if not v: return None, None
        if key < v.kmin: return None, v
        if v.kmax <= key: return v, None
        v.push_down()
        if key < v.key:
            s1, v.inner_l = cls._split_key(v.inner_l, key)
            v.update()
            return s1, v
        else:
            v.inner_r, s2 = cls._split_key(v.inner_r, key)
            v.update()
            return v, s2

    @classmethod
    def _cut_inner(cls, v: Node, k: int) -> Tuple[Node, Node, Node]:
        if not v: return None, None, None
        v.push_down()
        szl = cls._size(v.inner_l)
        if k < szl:
            a, b, v.inner_l = cls._cut_inner(v.inner_l, k)
            v.update()
            return a, b, v
        elif k == szl:
            res = v.inner_l, v, v.inner_r
            v.inner_l = v.inner_r = None
            v.update()
            return res
        else:
            v.inner_r, b, c = cls._cut_inner(v.inner_r, k - szl - 1)
            v.update()
            return v, b, c

    @classmethod
    def _cut_outer(cls, v: Node, k: int) -> Tuple[Node, Node, Node]:
        if not v: return None, None, None
        v.push_down()
        szl = cls._size(v.outer_l)
        szr = szl + v.size_inner
        if k < szl:
            a, b, v.outer_l = cls._cut_outer(v.outer_l, k)
            v.update()
            return a, b, v
        elif szr <= k:
            v.outer_r, b, c = cls._cut_outer(v.outer_r, k - szr)
            v.update()
            return v, b, c
        else:
            tmp_l, tmp_r = v.outer_l, v.outer_r
            v.outer_l = v.outer_r = None
            a, b, c = cls._cut_inner(v, k - szl)
            a = cls._merge_outer(tmp_l, a)
            c = cls._merge_outer(c, tmp_r)
            return a, b, c

    @classmethod
    def _insert(cls, v: Node, n: Node, k: int) -> Node:
        if not v: return n
        v.push_down()
        szl = cls._size(v.outer_l)
        if v.p < n.p:
            n.outer_l, n.outer_r = cls._split_outer(v, k)
            n.update()
            return n
        elif k < szl:
            v.outer_l = cls._insert(v.outer_l, n, k)
        elif k < szl + v.size_inner:
            s1, s2 = cls._split_outer(v, k)
            s1 = cls._insert(s1, n, k)
            s1.update()
            return cls._merge_outer(s1, s2)
        else:
            v.outer_r = cls._insert(v.outer_r, n, k - szl - v.size_inner)
        v.update()
        return v

    @classmethod
    def _query_range_inner(cls, v: Node, l: int, r: int) -> T:
        if not v: return ide_ele
        if l == 0 and r == v.size_all: return v.sum
        v.push_down()
        szl = cls._size(v.inner_l)
        szr = szl + 1
        left_q = right_q = ide_ele
        if l < szl:
            if r <= szl: return cls._query_range_inner(v.inner_l, l, r)
            left_q = cls._query_range_inner(v.inner_l, l, szl)
            l = szl
        if szr < r:
            if szr <= l: return cls._query_range_inner(v.inner_r, l - szr, r - szr)
            right_q = cls._query_range_inner(v.inner_r, 0, r - szr)
            r = szr
        res = ide_ele if l == r else v.val
        res = op(left_q, res)
        res = op(res, right_q)
        return res

    @classmethod
    def _query_range_outer(cls, v: Node, l: int, r: int) -> T:
        if not v: return ide_ele
        if l == 0 and r == v.size_all: return v.sum
        v.push_down()
        szl = cls._size(v.outer_l)
        szr = szl + v.size_inner
        left_q = right_q = ide_ele
        if l < szl:
            if r <= szl: return cls._query_range_outer(v.outer_l, l, r)
            left_q = cls._query_range_outer(v.outer_l, l, szl)
            l = szl
        if szr < r:
            if szr <= l: return cls._query_range_outer(v.outer_r, l - szr, r - szr)
            right_q = cls._query_range_outer(v.outer_r, 0, r - szr)
            r = szr
        res = ide_ele if l == r else cls._query_range_inner(v, l - szl, r - szl)
        res = op(left_q, res)
        res = op(res, right_q)
        return res

    @classmethod
    def _sort_inner(cls, v: Node) -> Node:
        if not v: return None
        tmp_l, tmp_r = v.outer_l, v.outer_r
        v.outer_l = v.outer_r = None
        v.push_down()
        if (v.inner_l and v.key < v.inner_l.kmax) or (v.inner_r and v.inner_r.kmin < v.key): v.toggle()
        res = cls._merge_compress(cls._sort_inner(tmp_l), v)
        res = cls._merge_compress(res, cls._sort_inner(tmp_r))
        return res

    @classmethod
    def _enumerate_inner(cls, v: Node, res) -> None:
        if not v: return
        v.push_down()
        if v.inner_l: cls._enumerate_inner(v.inner_l, res)
        res.append((v.key, v.val))
        if v.inner_r: cls._enumerate_inner(v.inner_r, res)

    @classmethod
    def _enumerate_outer(cls, v: Node, res) -> None:
        if not v: return
        v.push_down()
        if v.outer_l: cls._enumerate_outer(v.outer_l, res)
        cls._enumerate_inner(v, res)
        if v.outer_r: cls._enumerate_outer(v.outer_r, res)

    @classmethod
    def _p_satisfy(cls, v: Node) -> None:
        if not v.outer_l:
            if not v.outer_r or v.p > v.outer_r.p: return
            v.p, v.outer_r.p = v.outer_r.p, v.p
            cls._p_satisfy(v.outer_r)
        elif not v.outer_r:
            if v.p > v.outer_l.p: return
            v.p, v.outer_l.p = v.outer_l.p, v.p
            cls._p_satisfy(v.outer_l)
        else:
            if v.outer_l.p > v.outer_r.p:
                if v.p > v.outer_l.p: return
                v.p, v.outer_l.p = v.outer_l.p, v.p
                cls._p_satisfy(v.outer_l)
            else:
                if v.p > v.outer_r.p: return
                v.p, v.outer_r.p = v.outer_r.p, v.p
                cls._p_satisfy(v.outer_r)

    @classmethod
    def _build(cls, l: int, r: int, v) -> Node:
        mid = l + r >> 1
        u = Node(*v[mid])
        if l < mid:
            u.outer_l = cls._build(l, mid, v)
        else:
            u.outer_l = None
        if mid + 1 < r:
            u.outer_r = cls._build(mid + 1, r, v)
        else:
            u.outer_r = None
        cls._p_satisfy(u)
        u.update()
        return u

    def insert(self, k: int, key: int, val: T) -> None:
        self.root = self._insert(self.root, Node(key, val), k)

    def erase(self, k: int) -> None:
        a, _, b = self._cut_outer(self.root, k)
        self.root = self._merge_outer(a, b)

    def set(self, k: int, key: int, val: T) -> None:
        a, b, c = self._cut_outer(self.root, k)
        b.key = key
        b.val = val
        b.update()
        self.root = self._merge_outer(a, self._merge_outer(b, c))

    def update(self, k: int, val: T) -> None:
        a, b, c = self._cut_outer(self.root, k)
        b.val = op(b.val, val)
        b.update()
        self.root = self._merge_outer(a, self._merge_outer(b, c))

    def reverse(self, l: int, r: int) -> None:
        if l == r: return
        a, b, c = self._split_range_outer(self.root, l, r)
        b.toggle()
        self.root = self._merge_outer(a, self._merge_outer(b, c))

    def query(self, l: int, r: int) -> T:
        if l == r: return ide_ele
        return self._query_range_outer(self.root, l, r)

    def query_all(self) -> T:
        return self.root.sum

    def sort_ascending(self, l: int, r: int) -> None:
        if l == r: return
        a, b, c = self._split_range_outer(self.root, l, r)
        b = self._sort_inner(b)
        self.root = self._merge_outer(a, self._merge_outer(b, c))

    def sort_descending(self, l: int, r: int) -> None:
        if l == r: return
        a, b, c = self._split_range_outer(self.root, l, r)
        b = self._sort_inner(b)
        b.toggle()
        self.root = self._merge_outer(a, self._merge_outer(b, c))

    def to_list(self):
        res = []
        self._enumerate_outer(self.root, res)
        return res
