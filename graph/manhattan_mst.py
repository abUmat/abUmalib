# my module
from data_structure.tatyam_sortedset import *
from data_structure.unionfind import *
# my module
class Map:
    '''I want to use dict like c++ map while transrating c++ library...'''
    def __init__(self) -> None:
        self.keys = SortedSetInt()
        self.dic: Dict[int, int] = {}

    def lower_bound(self, k: int) -> int:
        '''O(N**0.5)'''
        it = self.keys.index(k)
        return it

    def erase(self, it: int) -> None:
        '''O(N**0.5)'''
        key = self.keys[it]
        self.keys.discard(key)
        self.dic.pop(key)

    def end(self) -> int:
        '''O(1)'''
        return len(self.keys)

    def __getitem__(self, k: int) -> int:
        '''O(1)'''
        return self.dic[k]

    def __setitem__(self, k: int, v: int) -> int:
        '''O(N**0.5)'''
        self.keys.add(k)
        self.dic[k] = v

    def get_by_iter(self, it: int) -> Tuple[int, int]:
        '''O(abs(it) / (N ** 0.5))'''
        key = self.keys[it]
        val = self.dic[key]
        return key, val

    def get(self, k: int, default: int) -> int:
        '''O(1)'''
        return self.dic.get(k, default)


def manhattan_mst(X: List[int], Y: List[int]) -> Dict[int, int]:
    '''
    X, Y: Points
    return: dict(key = i << 30 | j, value = cost)'''
    assert(len(X) == len(Y))
    N = len(X)
    dat: List[Tuple[int, int]]= []
    idx = list(range(N))
    mX = [-x for x in X]
    for _ in range(2):
        X, mX = mX, X
        for _ in range(2):
            X, Y = Y, X
            idx.sort(key=lambda i: X[i] + Y[i])
            mp = Map()
            for i in idx:
                x, y = X[i], Y[i]
                it = mp.lower_bound(-y)
                while it != mp.end():
                    _, j = mp.get_by_iter(it)
                    xj, yj = X[j], Y[j]
                    dx = x - xj
                    dy = y - yj
                    if dy > dx: break
                    dat.append((dx + dy, i << 30 | j))
                    mp.erase(it)
                mp[-y] = i
    dat.sort()
    G: Dict[int, int] = {}
    uf = UnionFind(N)
    mask = (1 << 30) - 1
    for cost, ij in dat:
        i, j = ij >> 30, ij & mask
        if uf.union(i, j):
            if i > j: i, j = j, i
            G[i << 30 | j] = cost
    return G
