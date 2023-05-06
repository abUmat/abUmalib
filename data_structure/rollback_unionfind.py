class RollbackUnionFind:
    def __init__(self, size: int) -> None:
        self.data = [-1] * size
        self.history = []
        self.inner_snap = 0

    def union(self, x: int, y: int) -> bool:
        '''
        merge x and y O(logn)
        return False if same(x, y), else True
        '''
        x, y = self.find(x), self.find(y)
        self.history.append(x << 30 | (-self.data[x]))
        self.history.append(y << 30 | (-self.data[y]))
        if x == y: return False
        if self.data[x] > self.data[y]: x, y = y, x
        self.data[x] += self.data[y]
        self.data[y] = x
        return True

    def find(self, k: int) -> int:
        'Root of the tree include x O(logn)'
        tmp = self.data[k]
        while tmp >= 0: k, tmp = tmp, self.data[tmp]
        return k

    def same(self, x: int, y: int) -> bool:
        'True if x and y belong to same tree, else False O(logn)'
        return self.find(x) == self.find(y)

    def size(self, k: int) -> int:
        'Size of the tree include x O(logn)'
        return -self.data[self.find(k)]

    def undo(self) -> None:
        'Undo last union O(1)'
        self.data[self.history[-1] >> 30] = -(self.history[-1] & 0x3fffffff)
        self.history.pop()
        self.data[self.history[-1] >> 30] = -(self.history[-1] & 0x3fffffff)
        self.history.pop()

    def snapshot(self) -> None:
        'Save current state O(1)'
        self.inner_snap = len(self.history) >> 1

    def get_state(self) -> int:
        'return number of excution of union method'
        return len(self.history) >> 1

    def rollback(self, state: int=-1) -> None:
        '''
        Rollback
        if state == -1 then rollback to the state saved by snapshot method
        else rollback to the state s.t. number of excution of union method == state'''
        if state == -1: state = self.inner_snap
        state <<= 1
        while state < len(self.history): self.undo()
