class SparseTable():
    '''
    更新がないかつ冪等性が成り立つ場合
    '''
    def __init__(self, arr: list, op: callable=min) -> None:
        n = len(arr)
        h = n.bit_length()
        self.op = op
        self.table = [[0] * n for _ in range(h)]
        self.table[0] = arr[::]
        for k in range(1, h):
            t, p = self.table[k], self.table[k - 1]
            l = 1 << (k - 1)
            for i in range(n - l * 2 + 1): t[i] = op(p[i], p[i + l])

    def query(self, l: int, r: int) -> int:
        k = (r - l).bit_length() - 1
        return self.op(self.table[k][l], self.table[k][r - (1 << k)])
