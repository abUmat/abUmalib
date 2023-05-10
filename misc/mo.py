class Mo:
    def __init__(self, Q, add_left, add_right, remove_left, remove_right, get):
        self._q = Q
        self._query = [0] * Q
        self._data = [0] * Q
        self._add_left = add_left
        self._add_right = add_right
        self._remove_left = remove_left
        self._remove_right = remove_right
        self._get = get

    def add_query(self, l, r, i, W):
        self._data[i] = l << 20 | r
        self._query[i] = (int(l / W) << 40) + ((-r if int(l / W) & 1 else r) << 20) + i

    def solve(self):
        add_left = self._add_left
        add_right = self._add_right
        remove_left = self._remove_left
        remove_right = self._remove_right
        get = self._get
        self._query.sort()
        pop = self._query.pop
        L, R = 0, 0
        res = [0] * self._q
        for _ in range(self._q):
            i = pop() & 0xfffff
            lr = self._data[i]
            l, r = lr >> 20, lr & 0xfffff
            while L > l:
                L -= 1
                add_left(L)
            while R < r:
                add_right(R)
                R += 1
            while L < l:
                remove_left(L)
                L += 1
            while R > r:
                R -= 1
                remove_right(R)
            res[i] = get()
        return res
