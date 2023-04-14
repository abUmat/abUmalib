class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n

    def leader(self, x):
        y = x
        while self.parents[x] >= 0: x = self.parents[x]
        while self.parents[y] >= 0:
            self.parents[y] = x
            y = x
        return x

    def union(self, x, y):
        x = self.leader(x)
        y = self.leader(y)
        if x == y: return 1
        px = self.parents[x]
        py = self.parents[y]
        if px < py:
            self.parents[x] += py
            self.parents[y] = x
        else:
            self.parents[y] += px
            self.parents[x] = y
        return 0

    def size(self, x): return -self.parents[self.leader(x)]

    def same(self, x, y): return self.leader(x) == self.leader(y)

    def members(self, x):
        leader = self.leader(x)
        return [i for i in range(self.n) if self.leader(i) == leader]

    def leaders(self): return [i for i, x in enumerate(self.parents) if x < 0]

    def group_count(self): return len(self.leaders())

    def groups(self):
        res = [[] for _ in range(self.n)]
        for v in range(self.n): res[self.leader(v)].append(v)
        return [r for r in res if r]

    def __str__(self): return '\n'.join(f'{m}' for m in self.groups())
