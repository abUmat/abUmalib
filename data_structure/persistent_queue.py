# my module
from gcc_builtins import *
# my module
# https://nyaannyaan.github.io/library/data-structure/persistent-queue.hpp
class _PersistentQueueNode:
    def __init__(self, d: int, val: int, n: list) -> None:
        self.d = d
        self.val = val
        self.par = n

class PersistentQueue:
    def __init__(self, e: int) -> None:
        root = _PersistentQueueNode(0, e, [])
        self.start = [root]
        self.end = [root]

    def append(self, val: int, id_: int=-1) -> int:
        s = self.start[id_]; e = self.end[id_]
        ne = _PersistentQueueNode(e.d + 1, val, [e])
        self.start.append(s); self.end.append(ne)
        for i in range(0x100000):
            if len(e.par) <= i: break
            e = e.par[i]
            ne.par.append(e)
        return len(self.start) - 1

    def popleft(self, id_: int=-1) -> tuple:
        s = self.start[id_]; e = self.end[id_]
        ns = e
        x = e.d - s.d - 1
        while x:
            d = ctz(x)
            ns = ns.par[d]
            x ^= 1 << d
        self.start.append(ns); self.end.append(e)
        return ns.val, len(self.start) - 1
