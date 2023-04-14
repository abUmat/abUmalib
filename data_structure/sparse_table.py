class SparseTable():
    def __init__(self, op, arr):
        n = len(arr)
        h = n.bit_length()
        self.table = [[0] * n for _ in range(h)]
        self.table[0] = arr[::]
        for k in range(1, h):
            t, p = self.table[k], self.table[k - 1]
            l = 1 << (k - 1)
            for i in range(n - l * 2 + 1): t[i] = op(p[i], p[i + l])
        self.op = op

    def query(self, l, r):
        k = (r - l).bit_length() - 1
        return self.op(self.table[k][l], self.table[k][r - (1 << k)])
