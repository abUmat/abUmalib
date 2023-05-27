# https://nyaannyaan.github.io/library/data-structure/radix-heap.hpp
class RadixHeap:
    s = 0
    last = 0
    MAX_BIT = 64
    def __init__(self) -> None:
        self.vs = [[] for _ in range(self.MAX_BIT + 1)]
    def __bool__(self) -> bool:
        return self.s != 0

    def __len__(self) -> int:
        return self.s

    def push(self, key: int, val: int) -> None:
        self.s += 1
        b = (key ^ self.last).bit_length()
        self.vs[b].append(key << 20 | val)

    def pop(self):
        if not self.vs[0]:
            idx = 1
            while not self.vs[idx]: idx += 1
            last = min(self.vs[idx]) >> 20
            for tmp in self.vs[idx]:
                b = ((tmp >> 20) ^ last).bit_length()
                self.vs[b].append(tmp)
            self.vs[idx] = []
            self.last = last
        self.s -= 1
        tmp = self.vs[0].pop()
        return tmp >> 20, tmp & 0xfffff
