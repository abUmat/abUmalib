class Mo:
    def __init__(self, Q, add_left, add_right, remove_left, remove_right, get):
        self.q = Q
        self.query = [0] * Q
        self.data = [0] * Q
        self.add_left = add_left
        self.add_right = add_right
        self.remove_left = remove_left
        self.remove_right = remove_right
        self.get = get

    def add_query(self, l, r, i, W):
        self.data[i] = l<<20|r
        self.query[i] = ((l//W)<<40)+((-r if (l//W)&1 else r)<<20)+i

    def solve(self):
        self.query.sort()
        L, R = 0, 0
        res = [0] * self.q
        mask = (1<<20)-1
        add_left = self.add_left
        add_right = self.add_right
        remove_left = self.remove_left
        remove_right = self.remove_right
        get = self.get
        for lri  in self.query:
            i = lri&mask
            lr = self.data[i]
            l, r = lr>>20, lr&mask
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
