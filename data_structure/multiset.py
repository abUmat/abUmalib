import bisect
class Multiset:
    # n: サイズ、compress: 座圧対象list-likeを指定(nは無効)
    # multi: マルチセットか通常のOrderedSetか
    def __init__(self, n=0, *, compress=[], multi=1):
        self.multi = multi
        self.inv_compress = sorted(set(compress)) if compress else [i for i in range(n)]
        self.compress = {k: v for v, k in enumerate(self.inv_compress)}
        self.counter_all = 0
        self.counter = [0] * len(self.inv_compress)
        self.n = len(self.inv_compress)
        self.size = 1<<self.n.bit_length()
        self.arr = [0] * (self.size+1)

    def build(self, nums):
        from collections import Counter
        c = Counter(nums)
        for k, v in c.items():
            self.add(k, v)

    def add(self, x, n=1): # O(log n)
        if not self.multi and n != 1: raise KeyError(n)
        x = self.compress[x]
        count = self.counter[x]
        if count == 0 or self.multi:  # multiなら複数カウントできる
            self.counter_all += n
            self.counter[x] += n
            #bit add
            x += 1
            while x <= self.size:
                self.arr[x] += n
                x += x & -x

    def discard(self, x, n=1): # O(log n)
        if not self.multi and n != 1: raise KeyError(n)
        x = self.compress[x]
        count = self.sum(x, x+1)
        if count < n: raise KeyError(x)
        self.counter_all -= n
        self.counter[x] -= n
        #bit add
        x += 1
        while x <= self.size:
            self.arr[x] -= n
            x += x & -x

    def sum(self, l, r):
        sl = 0
        while l >= 1:
            sl += self.arr[l]
            l -= l & -l
        sr = 0
        while r >= 1:
            sr += self.arr[r]
            r -= r & -r
        return sr-sl

    def lower_bound(self, w):
        if w <= 0: return 0
        x, r = 0, self.size
        while r > 0:
            if x+r <= self.size and self.arr[x+r] < w:
                w -= self.arr[x+r]
                x += r
            r >>= 1
        return x

    def bisect_left(self, x): return self.sum(bisect.bisect_left(self.inv_compress, x)) # O(log n)
    def bisect_right(self, x): return self.sum(bisect.bisect_right(self.inv_compress, x)) # O(log n)
    def count(self, x): return self.counter[self.compress[x]] if x in self.compress else 0 # O(1)
    def __contains__(self, x): return self.count(x) > 0 # operator in: O(1)
    def __repr__(self): return f'MultiSet {{{(", ".join(map(str, list(self))))}}}'
    def __len__(self): return self.counter_all # oprator len: O(1)
    def __getitem__(self, i):  # operator []: O(log n)
        if i < 0: i += len(self)
        x = self.lower_bound(i+1)
        if x > self.n: raise IndexError('list index out of range')
        return self.inv_compress[x]
