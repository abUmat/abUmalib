# my module
from misc.typing_template import *
# my module
from heapq import heappush, heappop
class DoubleEndedPriorityQueue:
    def __init__(self, arr: List[int]=None) -> None:
        if not arr: arr = []
        self.used = bytearray(len(arr))
        self.idx = len(arr)
        self.hq1: List[int] = []
        self.hq2: List[int] = []
        for i, x in enumerate(arr):
            tmp = x << 20 | i
            heappush(self.hq1, tmp)
            heappush(self.hq2, ~tmp)

    def pop_min(self) -> int:
        while 1:
            tmp = heappop(self.hq1)
            x, i = tmp >> 20, tmp & 0xfffff
            if self.used[i]: continue
            self.used[i] = 1
            return x

    def pop_max(self) -> int:
        while 1:
            tmp = ~heappop(self.hq2)
            x, i = tmp >> 20, tmp & 0xfffff
            if self.used[i]: continue
            self.used[i] = 1
            return x

    def push(self, x: int) -> None:
        tmp = x << 20 | self.idx
        heappush(self.hq1, tmp)
        heappush(self.hq2, ~tmp)
        self.used.append(0)
        self.idx += 1
