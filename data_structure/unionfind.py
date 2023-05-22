class UnionFind():
    def __init__(self, n: int) -> None:
        self.n = n
        self.parents = [-1] * n

    def leader(self, x: int) -> int:
        'Root of the tree include x'
        y = x
        while self.parents[x] >= 0: x = self.parents[x]
        while self.parents[y] >= 0:
            self.parents[y] = x
            y = x
        return x

    def union(self, x: int, y: int) -> int:
        'False if same(x, y), else True'
        x = self.leader(x)
        y = self.leader(y)
        if x == y: return 0
        px = self.parents[x]
        py = self.parents[y]
        if px < py:
            self.parents[x] += py
            self.parents[y] = x
        else:
            self.parents[y] += px
            self.parents[x] = y
        return 1

    def size(self, x: int) -> int:
        'Size of the tree include x'
        return -self.parents[self.leader(x)]

    def same(self, x: int, y: int) -> bool:
        'True if x and y belong to same tree, else False'
        return self.leader(x) == self.leader(y)

    def members(self, x: int) -> 'List[int]':
        'All nodes of the tree x belong to'
        leader = self.leader(x)
        return [i for i in range(self.n) if self.leader(i) == leader]

    def leaders(self) -> 'List[int]':
        'All roots of trees'
        return [i for i, x in enumerate(self.parents) if x < 0]

    def group_count(self) -> int:
        'Count of trees'
        return len(self.leaders())

    def groups(self) -> 'List[List[int]]':
        'nodes grouped by tree'
        res = [[] for _ in range(self.n)]
        for v in range(self.n): res[self.leader(v)].append(v)
        return [r for r in res if r]

    def __str__(self) -> str:
        return '\n'.join(f'{m}' for m in self.groups())
