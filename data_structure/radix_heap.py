class RadixHeap:
    s = 0
    last = 0
    vs = [[] for _ in range(33)]
    def __bool__(self) -> bool:
        return self.s != 0

    def __len__(self) -> int:
        return self.s

    def push(self, key: int, val: int) -> None:
        self.s += 1
        b = (key ^ self.last).bit_length()
        self.vs[b].append(key << 32 | val)

    def pop(self):
        if not self.vs[0]:
            idx = 1
            while not self.vs[idx]: idx += 1
            last = min(self.vs[idx]) >> 32
            for tmp in self.vs[idx]:
                key, val = tmp >> 32, tmp & 0xffffffff
                b = (key ^ last).bit_length()
                self.vs[b].append(key << 32 | val)
            self.vs[idx] = []
            self.last = last
        self.s -= 1
        tmp = self.vs[0].pop()
        return tmp >> 32, tmp & 0xffffffff
