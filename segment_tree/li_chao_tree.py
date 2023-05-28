from bisect import bisect_left as lower_bound, bisect_right as upper_bound
# my module
from misc.typing_template import *
# my module
# https://nyaannyaan.github.io/library/segment-tree/li-chao-tree.hpp
def _get(line: Tuple[int, int], x: int) -> int:
    return line[0] *  x + line[1]

def _over(l: Tuple[int, int], r: Tuple[int, int], x: int) -> bool:
    return _get(l, x) < _get(r, x)

class LiChaoTree:
    def __init__(self, xset: List[int], INF: int=(1 << 60) - 1) -> None:
        self.xset = sorted(set(xset))
        self.size = size = 1 << len(self.xset).bit_length()
        while len(self.xset) < size:
            self.xset.append(self.xset[-1] + 1)
        self.seg = [(0, INF) for _ in range(size << 1)]

    def _update(self, a: int, b: int, seg_idx: int, left: int=0, right: int=0) -> None:
        if not right:
            upper_bit = seg_idx.bit_length() - 1
            tmp = self.size >> upper_bit
            left = tmp *  (seg_idx ^ (1 << upper_bit))
            right = left + tmp
        line = (a, b)
        while 1:
            mid = left+right >> 1
            tmp = self.seg[seg_idx]
            l_over = _over(line, tmp, self.xset[left])
            r_over = _over(line, tmp, self.xset[right - 1])
            if l_over and r_over:
                self.seg[seg_idx] = line
                return
            if not l_over and not r_over: return
            m_over = _over(line, tmp, self.xset[mid])
            if m_over: self.seg[seg_idx], line = line, tmp
            if l_over != m_over: seg_idx, right = seg_idx << 1, mid
            else: seg_idx, left = seg_idx << 1 | 1, mid

    def update(self, a: int, b: int) -> None:
        '''add line y = ax + b'''
        self._update(a, b, 1, 0, self.size)

    def update_segment(self, a: int, b: int, low: int, high: int) -> None:
        '''add segment y = ax + b (x in [low, high])'''
        left = lower_bound(self.xset, low) + self.size
        tmp = upper_bound(self.xset, high)
        if tmp: right = tmp + self.size
        else: right = self.size + 1

        while left < right:
            if left & 1:
                self._update(a, b, left)
                left += 1
            if right & 1:
                right ^= 1
                self._update(a, b, right)
            left >>= 1
            right >>= 1

    def _query(self, x: int, seg_idx: int) -> int:
        res = _get(self.seg[seg_idx], x)
        while seg_idx > 1:
            seg_idx >>= 1
            tmp = _get(self.seg[seg_idx], x)
            if tmp < res: res = tmp
        return res

    def query_idx(self, k: int) -> int:
        '''minimun y in x = xset[k]'''
        x = self.xset[k]
        k += self.size
        return self._query(x, k)

    def query(self, x: int) -> int:
        '''minimun y in x'''
        k = lower_bound(self.xset, x)
        x = self.xset[k]
        k += self.size
        return self._query(x, k)
