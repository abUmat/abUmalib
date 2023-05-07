# https://nyaannyaan.github.io/library/data-structure/skew-heap.hpp
class SkewHeapNode:
    def __init__(self, k: int, i: int=-1) -> None:
        self.key = k
        self.laz = 0
        self.l = self.r = None
        self.idx = i

    def propagate(self) -> None:
        if self.laz == 0: return
        if self.l: self.l.laz += self.laz
        if self.r: self.r.laz += self.laz
        self.key += self.laz
        self.laz = 0

class SkewHeap:
    def __init__(self, is_min: bool=True) -> None:
        self.is_min = is_min

    def meld(self, x: SkewHeapNode, y: SkewHeapNode) -> SkewHeapNode:
        if not x: return y
        if not y: return x
        if not self._comp(x, y): x, y = y, x
        x.propagate()
        x.r = self.meld(x.r, y)
        x.l, x.r = x.r, x.l
        return x

    @staticmethod
    def alloc(key: int, idx: int=-1) -> SkewHeapNode:
        return SkewHeapNode(key, idx)

    def pop(self, x: SkewHeapNode) -> SkewHeapNode:
        x.propagate()
        return self.meld(x.l, x.r)

    def push(self, x: SkewHeapNode ,key: int, idx: int=-1):
        return self.meld(x, self.alloc(key, idx))

    @staticmethod
    def apply(x: SkewHeapNode, laz: int) -> None:
        x.laz += laz

    def _comp(self, x: SkewHeapNode, y: SkewHeapNode) -> bool:
        if self.is_min:
            return x.key + x.laz < y.key + y.laz
        else:
            return x.key + x.laz > y.key + y.laz