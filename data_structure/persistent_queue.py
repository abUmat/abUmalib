from typing import List, Tuple
# my module
from gcc_builtins import *
# my module
class _PersistentQueueNode:
    def __init__(self, d: int, val: int, n: List) -> None:
        self.d = d
        self.val = val
        self.par = n

class PersistentQueue:
    def __init__(self, e: int) -> None:
        self.root = _PersistentQueueNode(0, e, [])
        self.start = [self.root]
        self.end = [self.root]

    def push(self, val: int, id_: int=-1) -> int:
        s = self.start[id_]; e = self.end[id_]
        ne = _PersistentQueueNode(e.d + 1, val, [e])
        self.start.append(s); self.end.append(ne)
        for i in range(0x100000):
            if len(e.par) <= i: break
            e = e.par[i]
            ne.par.append(e)
        return len(self.start) - 1

    def pop(self, id_: int=-1) -> Tuple[int, int]:
        s = self.start[id_]; e = self.end[id_]
        ns = e
        x = e.d - s.d - 1
        while x:
            d = ctz(x)
            ns = ns.par[d]
            x ^= 1 << d
        self.start.append(ns); self.end.append(e)
        return ns.val, len(self.start) - 1
