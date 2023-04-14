class SegmentTreeBeats():
    pINF = 1<<60
    nINF = -1<<60
    def __init__(self, n, arr=None):
        size = 1 << (n - 1).bit_length()
        self.size = size
        size2 = size<<1
        self.fmax = [self.nINF] * (size2)
        self.fmin = [self.pINF] * (size2)
        self.smax = [self.nINF] * (size2)
        self.smin = [self.pINF] * (size2)
        self.maxc = [0] * (size2)
        self.minc = [0] * (size2)
        self.sum = [0] * (size2)
        self.add = [0] * (size2)
        self.upd = [self.pINF] * (size2)
        self.up = []
        self.down = []
        self.lt = [0] * (size2)
        self.rt = [0] * (size2)
        for i in range(size):
            self.lt[size + i] = i
            self.rt[size + i] = i + 1
        for i in range(size)[::-1]:
            self.lt[i] = self.lt[i << 1]
            self.rt[i] = self.rt[i<<1|1]
        if arr:
            for i, a in enumerate(arr):
                self.fmax[size + i] = a
                self.fmin[size + i] = a
                self.maxc[size + i] = 1
                self.minc[size + i] = 1
                self.sum[size + i] = a
            for i in range(1, size)[::-1]: #self.merge(i)
                self.sum[i] = self.sum[i<<1] + self.sum[i<<1|1]
                a, b = self.fmax[i<<1], self.fmax[i<<1|1]
                if a < b:
                    self.fmax[i] = b
                    self.maxc[i] = self.maxc[i<<1|1]
                    self.smax[i] = max(a, self.smax[i<<1|1])
                elif a > b:
                    self.fmax[i] = a
                    self.maxc[i] = self.maxc[i<<1]
                    self.smax[i] = max(self.smax[i<<1], b)
                else:
                    self.fmax[i] = a
                    self.maxc[i] = self.maxc[i<<1] + self.maxc[i<<1|1]
                    self.smax[i] = max(self.smax[i<<1], self.smax[i<<1|1])

                a, b = self.fmin[i<<1], self.fmin[i<<1|1]
                if a > b:
                    self.fmin[i] = b
                    self.minc[i] = self.minc[i<<1|1]
                    self.smin[i] = min(a, self.smin[i<<1|1])
                elif a < b:
                    self.fmin[i] = a
                    self.minc[i] = self.minc[i<<1]
                    self.smin[i] = min(self.smin[i<<1], b)
                else:
                    self.fmin[i] = a
                    self.minc[i] = self.minc[i<<1] + self.minc[i<<1|1]
                    self.smin[i] = min(self.smin[i<<1], self.smin[i<<1|1])

    def _up_merge(self):
        while self.up: #self.merge(self.up.pop())
            k = self.up.pop()
            self.sum[k] = self.sum[k<<1] + self.sum[k<<1|1]
            a, b = self.fmax[k<<1], self.fmax[k<<1|1]
            if a < b:
                self.fmax[k] = b
                self.maxc[k] = self.maxc[k<<1|1]
                self.smax[k] = max(a, self.smax[k<<1|1])
            elif a > b:
                self.fmax[k] = a
                self.maxc[k] = self.maxc[k<<1]
                self.smax[k] = max(self.smax[k<<1], b)
            else:
                self.fmax[k] = a
                self.maxc[k] = self.maxc[k<<1] + self.maxc[k<<1|1]
                self.smax[k] = max(self.smax[k<<1], self.smax[k<<1|1])

            a, b = self.fmin[k<<1], self.fmin[k<<1|1]
            if a > b:
                self.fmin[k] = b
                self.minc[k] = self.minc[k<<1|1]
                self.smin[k] = min(a, self.smin[k<<1|1])
            elif a < b:
                self.fmin[k] = a
                self.minc[k] = self.minc[k<<1]
                self.smin[k] = min(self.smin[k<<1], b)
            else:
                self.fmin[k] = a
                self.minc[k] = self.minc[k<<1] + self.minc[k<<1|1]
                self.smin[k] = min(self.smin[k<<1], self.smin[k<<1|1])

    def _down_propagate(self, k):
        if self.size <= k: pass #?
        else:
            a = self.upd[k]
            if a != self.pINF:
                self._update(k<<1, a)
                self._update(k<<1|1, a)
                self.upd[k] = self.pINF
            else:
                a = self.add[k]
                if a:
                    self._add(k<<1, a)
                    self._add(k<<1|1, a)
                    self.add[k] = 0
                a, b = self.fmax[k], self.fmin[k]
                if a < self.fmax[k<<1]: self._chmax(k<<1, a)
                if self.fmin[k<<1] < b: self._chmin(k<<1, b)
                if a < self.fmax[k<<1|1]: self._chmax(k<<1|1, a)
                if self.fmin[k<<1|1] < b: self._chmin(k<<1|1, b)
        self.down.append(k<<1)
        self.down.append(k<<1|1)

    def _update(self, k, x):
        a, b = self.lt[k], self.rt[k]
        self.fmax[k] = x
        self.smax[k] = self.nINF
        self.fmin[k] = x
        self.smin[k] = self.pINF
        self.maxc[k] = b - a
        self.minc[k] = b - a
        self.sum[k] = x * (b - a)
        self.add[k] = 0
        self.upd[k] = x

    def _add(self, k, x):
        self.fmax[k] += x
        if self.smax[k] != self.nINF: self.smax[k] += x
        self.fmin[k] += x
        if self.smin[k] != self.pINF: self.smin[k] += x
        self.sum[k] += x * (self.rt[k] - self.lt[k])
        if self.upd[k] != self.pINF: self.upd[k] += x
        else: self.add[k] += x

    def _chmax(self, k, x):
        a = self.fmax[k]
        self.sum[k] += (x - a) * self.maxc[k]
        if a == self.fmin[k]:
            self.fmax[k] = x
            self.fmin[k] = x
        elif a == self.smin[k]:
            self.fmax[k] = x
            self.smin[k] = x
        else: self.fmax[k] = x
        a = self.upd[k]
        if a != self.pINF and x < a: self.upd[k] = x

    def _chmin(self, k, x):
        a = self.fmin[k]
        self.sum[k] += (x - a) * self.minc[k]
        if a == self.fmax[k]:
            self.fmin[k] = x
            self.fmax[k] = x
        elif a == self.smax[k]:
            self.fmin[k] = x
            self.smax[k] = x
        else: self.fmin[k] = x
        a = self.upd[k]
        if a != self.pINF and a < x: self.upd[k] = x

    def range_chmax(self, l, r, x):
        self.down.append(1)
        while self.down:
            k = self.down.pop()
            if r <= self.lt[k] or self.rt[k] <= l or x <= self.fmin[k]: continue
            if l <= self.lt[k] and self.rt[k] <= r and x < self.smin[k]:
                self._chmin(k, x)
                continue
            self._down_propagate(k)
            self.up.append(k)
        self._up_merge()

    def range_chmin(self, l, r, x):
        self.down.append(1)
        while self.down:
            k = self.down.pop()
            if r <= self.lt[k] or self.rt[k] <= l or self.fmax[k] <= x: continue
            if l <= self.lt[k] and self.rt[k] <= r and self.smax[k] < x:
                self._chmax(k, x)
                continue
            self._down_propagate(k)
            self.up.append(k)
        self._up_merge()

    def range_add(self, l, r, x):
        self.down.append(1)
        while self.down:
            k = self.down.pop()
            if r <= self.lt[k] or self.rt[k] <= l: continue
            if l <= self.lt[k] and self.rt[k] <= r:
                self._add(k, x)
                continue
            self._down_propagate(k)
            self.up.append(k)
        self._up_merge()

    def range_update(self, l, r, x):
        self.down.append(1)
        while self.down:
            k = self.down.pop()
            if r <= self.lt[k] or self.rt[k] <= l: continue
            if l <= self.lt[k] and self.rt[k] <= r:
                self._update(k, x)
                continue
            self._down_propagate(k)
            self.up.append(k)
        self._up_merge()

    def get_max(self, l, r):
        self.down.append(1)
        v = self.nINF
        while self.down:
            k = self.down.pop()
            if r <= self.lt[k] or self.rt[k] <= l: continue
            if l <= self.lt[k] and self.rt[k] <= r:
                v = max(v, self.fmax[k])
                continue
            self._down_propagate(k)
        return v

    def get_min(self, l, r):
        self.down.append(1)
        v = self.pINF
        while self.down:
            k = self.down.pop()
            if r <= self.lt[k] or self.rt[k] <= l: continue
            if l <= self.lt[k] and self.rt[k] <= r:
                v = min(v, self.fmin[k])
                continue
            self._down_propagate(k)
        return v

    def get_sum(self, l, r):
        self.down.append(1)
        v = 0
        while self.down:
            k = self.down.pop()
            if r <= self.lt[k] or self.rt[k] <= l: continue
            if l <= self.lt[k] and self.rt[k] <= r:
                v += self.sum[k]
                continue
            self._down_propagate(k)
        return v

    def get(self, k): return self.get_sum(k, k+1)
    def add(self, k, x): self.range_add(k, k+1, x)
    def update(self, k, x): self.range_update(k, k+1, x)
    def chmin(self, k, x): self.range_chmin(k, k+1, x)
    def chmax(self, k, x): self.range_chmax(k, k+1, x)
