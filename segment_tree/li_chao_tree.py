from bisect import bisect_left as lower_bound, bisect_right as upper_bound
class Line:
    def __init__(self, slope, intercept):
        self.slope = slope
        self.intercept = intercept
    def get(self, x): return self.slope * x + self.intercept
    def over(self, other, x): return self.get(x) < other.get(x)

class LiChaoTree:
    def __init__(self, xset, INF=1<<61):
        self.xset = sorted(set(xset))
        size = 1<<len(self.xset).bit_length()
        while len(self.xset) < size: self.xset.append(self.xset[-1]+1)
        self.seg = [Line(0, INF) for _ in range(size<<1)]
        self.size = size

    def _update(self, a, b, seg_idx, left=0, right=0):
        if not right:
            upper_bit = seg_idx.bit_length() - 1
            tmp = self.size>>upper_bit
            left = tmp *  (seg_idx^(1<<upper_bit))
            right = left + tmp
        line = Line(a, b)
        while 1:
            mid = left+right>>1
            tmp = self.seg[seg_idx]
            l_over = line.over(tmp, self.xset[left])
            r_over = line.over(tmp, self.xset[right-1])
            if l_over and r_over:
                self.seg[seg_idx] = line
                return
            if not l_over and not r_over: return
            m_over = line.over(tmp, self.xset[mid])
            if m_over: self.seg[seg_idx], line = line, tmp
            if l_over != m_over: seg_idx, right = seg_idx<<1, mid
            else: seg_idx, left = seg_idx<<1|1, mid

    def update(self, a, b): self._update(a, b, 1, 0, self.size)

    def update_segment(self, a, b, low, high):
        left = lower_bound(self.xset, low) + self.size
        tmp = upper_bound(self.xset, high)
        if tmp: right = tmp + self.size
        else: right = self.size + 1

        while left < right:
            if left&1:
                self._update(a, b, left)
                left += 1
            if right&1:
                right ^= 1
                self._update(a, b, right)
            left >>= 1
            right >>= 1

    def _query(self, x, seg_idx):
        res = self.seg[seg_idx].get(x)
        while seg_idx > 1:
            seg_idx >>= 1
            tmp = self.seg[seg_idx].get(x)
            if tmp < res: res = tmp
        return res

    def query_idx(self, k):
        x = self.xset[k]
        k += self.size
        return self._query(x, k)

    def query(self, x):
        k = lower_bound(self.xset, x)
        x = self.xset[k]
        k += self.size
        return self._query(x, k)
