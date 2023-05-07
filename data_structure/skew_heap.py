# https://nyaannyaan.github.io/library/data-structure/skew-heap.hpp
class SkewHeapNode:
    def __init__(self, k: int, i: int=-1):
        self.key = k
        self.laz = 0
        self.l = self.r = None
        self.idx = i

class SkewHeap:
    def __init__(self, is_min: bool=True) -> None:
        self.is_min = is_min

    @staticmethod
    def propagate(x: SkewHeapNode) -> None:
        if x.laz == 0: return
        if x.l: x.l.laz += x.laz
        if x.r: x.r.laz += x.laz
        x.key += x.laz
        x.laz = 0

    def meld(self, x: SkewHeapNode, y: SkewHeapNode) -> SkewHeapNode:
        if not x or not y: return x if x else y
        if not self._comp(x, y): x, y = y, x
        self.propagate(x)
        x.r = self.meld(x.r, y)
        x.l, x.r = x.r, x.l
        return x

    @staticmethod
    def alloc(key: int, idx: int=-1) -> SkewHeapNode:
        return SkewHeapNode(key, idx)

    def pop(self, x: SkewHeapNode) -> SkewHeapNode:
        self.propagate(x)
        return self.meld(x.l, x.r)

    def append(self, x: SkewHeapNode ,key: int, idx: int=-1):
        return self.meld(x, self.alloc(key, idx))

    @classmethod
    def apply(cls, x: SkewHeapNode, laz: int) -> None:
        x.laz += laz
        cls.propagate(x)

    def _comp(self, x: SkewHeapNode, y: SkewHeapNode) -> bool:
        if self.is_min:
            return x.key + x.laz < y.key + y.laz
        else:
            return x.key + x.laz > y.key + y.laz