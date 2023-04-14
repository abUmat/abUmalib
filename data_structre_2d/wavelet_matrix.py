def bit_count(x):
    '''xの立っているビット数をカウントする関数
    (xは32bit整数)'''

    # 2bitごとの組に分け、立っているビット数を2bitで表現する
    x = x - ((x >> 1) & 0x55555555)
    # 4bit整数に 上位2bit + 下位2bit を計算した値を入れる
    x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
    x = (x + (x >> 4)) & 0x0f0f0f0f # 8bitごと
    x = x + (x >> 8) # 16bitごと
    x = x + (x >> 16) # 32bitごと = 全部の合計
    return x & 0x0000007f

class bit_vector:
    def get(self, i): return self.block[i>>5]>>(i&31)&1
    def set(self, i): self.block[i>>5] |= 1<<(i&31)
    def __init__(self, n):
        self.n = n
        self.zeros = n
        self.block = [0] * ((n>>5) + 1)
        self.count = [0] * ((n>>5) + 1)
    def build(self):
        for i in range(self.n>>5):
            # Python 3.10までお預け
            # self.count[i+1] = self.count[i] + self.block[i].bit_count()
            self.count[i+1] = self.count[i] + bit_count(self.block[i])
        self.zeros -= self.n - self.rank0(self.n)
    def rank0(self, i):
        # Python 3.10までお預け
        # return i - self.count[i>>6] - (self.block[i>>6]&((1<<(i&self.mask))-1)).bit_count()
        return i - self.count[i>>5] - bit_count(self.block[i>>5]&((1<<(i&31))-1))
    def rank1(self, i):
        # Python 3.10までお預け
        # return self.count[i>>6] + (self.block[i>>6]&((1<<(i&self.mask))-1)).bit_count()
        return self.count[i>>5] - bit_count(self.block[i>>5]&((1<<(i&31))-1))

class WaveletMatrix:
    def __init__(self, arr):
        n = len(arr)
        lg = max(max(arr), 1).bit_length()
        self.bv = [bit_vector(n) for _ in range(lg)]
        cur = arr[::]
        nxt = [0] * n
        for h in range(lg)[::-1]:
            for i in range(n):
                if cur[i]>>h&1: self.bv[h].set(i)
            self.bv[h].build()
            it = [0, self.bv[h].zeros]
            for i, a in enumerate(cur):
                tmp = self.bv[h].get(i)
                nxt[it[tmp]] = a
                it[tmp] += 1
            cur = nxt[::]
        self.lg = lg
        self.n = n
        self.arr = arr

    def set(self, i, x): self.arr[i] = x
    def succ0(self, l, r, h): return self.bv[h].rank0(l), self.bv[h].rank0(r)
    def succ1(self, l, r, h):
        l1 = l - self.bv[h].rank0(l)
        r1 = r - self.bv[h].rank0(r)
        zeros = self.bv[h].zeros
        return zeros+l1, zeros+r1

    def access(self, k):
        res = 0
        for h in range(self.lg)[::-1]:
            f = self.bv[h].get(k)
            res |= 1<<h if f else 0
            k = k - self.bv[h].rank0(k) + self.bv[h].zeros if f else self.bv[h].rank0(k)
        return res

    def kth_smallest(self, l, r, k):
        res = 0
        for h in range(self.lg)[::-1]:
            l0, r0 = self.bv[h].rank0(l), self.bv[h].rank0(r)
            if k < r0 - l0:
                l = l0
                r = r0
            else:
                k -= r0 - l0
                res |= 1<<h
                l += self.bv[h].zeros - l0
                r += self.bv[h].zeros - r0
        return res

    def kth_largest(self, l, r, k): return self.kth_smallest(l, r, r-l-k-1)

    def pref_freq(self, l, r, upper):
        if upper >= 1<<self.lg: return r-l
        res = 0
        for h in range(self.lg)[::-1]:
            f = upper>>h&1
            l0, r0 = self.bv[h].rank0(l), self.bv[h].rank0(r)
            if f:
                res += r0-l0
                l += self.bv[h].zeros - l0
                r += self.bv[h].zeros - r0
            else:
                l, r = l0, r0
        return res

    def range_freq(self, l, r, lower, upper): return self.pref_freq(l, r, upper) - self.pref_freq(l, r, lower)

    def prev_value(self, l, r, upper):
        cnt = self.pref_freq(l, r, upper)
        return self.kth_smallest(l, r, cnt-1) if cnt else -1

    def next_value(self, l, r, lower):
        cnt = self.pref_freq(l, r, lower)
        return -1 if cnt == r-l else self.kth_smallest(l, r, cnt)
