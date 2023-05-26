# my module
from data_structure.sparse_table import *
# my module
# https://nyaannyaan.github.io/library/string/suffix-array.hpp

def sa_is(s: str) -> list:
    a = bytearray(s.encode())
    for i in range(len(a)): a[i] -= 32
    a.append(0)
    k = max(a) + 1
    n = len(a)

    def induce_l(sa: list, a: bytearray, n: int, k: int, stype: bytearray) -> None:
        bucket = get_buckets(a, k, 1)
        for i in range(n):
            j = sa[i] - 1
            if j >= 0 and stype[j]:
                sa[bucket[a[j]]] = j
                bucket[a[j]] += 1

    def induce_s(sa: list, a: bytearray, n: int, k: int, stype: bytearray) -> None:
        bucket = get_buckets(a, k, 0)
        for i in range(n)[::-1]:
            j = sa[i] - 1
            if j >= 0 and not stype[j]:
                bucket[a[j]] -= 1
                sa[bucket[a[j]]] = j

    def get_buckets(a: bytearray, k: int, start: int=0) -> list:
        bucket = [0] * k
        for item in a: bucket[item] += 1
        s = 0
        for i, x in enumerate(bucket):
            s += x
            bucket[i] = s - (x if start else 0)
        return bucket

    def set_lms(a: bytearray, n: int, k: int, default_order: list) -> list:
        bucket = get_buckets(a, k)
        sa = [-1] * n
        for i in default_order[::-1]:
            bucket[a[i]] -= 1
            sa[bucket[a[i]]] = i
        return sa

    def induce(a: bytearray, n: int, k: int, stype: bytearray, default_order: list) -> list:
        sa = set_lms(a, n, k, default_order)
        induce_l(sa, a, n, k, stype)
        induce_s(sa, a, n, k, stype)
        return sa

    def rename_LMS_substring(sa: list, a: bytearray, n: int, stype: bytearray, LMS: bytearray, l: int) -> tuple:
        sa = [_s for _s in sa if LMS[_s]]
        tmp = [-1] * (n >> 1) + [0]
        dupl = 0
        for idx in range(1, l):
            i, j = sa[idx - 1], sa[idx]
            for k in range(n):
                if a[i + k] != a[j + k] or stype[i + k] != stype[j + k]: break
                if k and (LMS[i + k] or LMS[j + k]):
                    dupl += 1
                    break
            tmp[j >> 1] = idx - dupl
        return [t for t in tmp if t >= 0], dupl

    def calc(a, n: int, k: int) -> list:
        stype = bytearray(n)
        for i in range(n - 1)[::-1]:
            if a[i] > a[i + 1] or (a[i] == a[i + 1] and stype[i + 1]): stype[i] = 1

        LMS = bytearray([1 if not stype[i] and stype[i - 1] else 0 for i in range(n - 1)])
        LMS.append(1)
        l = sum(LMS)
        lms = [i for i in range(n) if LMS[i]]
        sa = induce(a, n, k, stype, lms)
        renamed_LMS, dupl = rename_LMS_substring(sa, a, n, stype, LMS, l)

        if dupl: sub_sa = calc(renamed_LMS, l, l - dupl)
        else:
            sub_sa = [0] * l
            for i in range(l): sub_sa[renamed_LMS[i]] = i

        sa = induce(a, n, k, stype, [lms[x] for x in sub_sa])
        return sa

    return calc(a, n, k)

def lcp_array(s: str, sa: list) -> tuple:
    rank = [0] * len(sa)
    for i, x in enumerate(sa): rank[x] = i
    lcp = [0] * len(sa)
    h = 0
    for i in range(len(sa) - 1):
        j = sa[rank[i] - 1]
        if h: h -= 1
        while (i if i > j else j) + h < len(sa) - 1 and s[i + h] == s[j + h]:
            h += 1
        lcp[rank[i] - 1] = h
    return lcp, rank

class StringSearch:
    def __init__(self, s: str, sa: list, lcp: list, rank: list) -> None:
        self.s = s
        self.sa = sa
        self.sparse = SparseTable(lcp)
        self.rank = rank

    def comp(self, t: str, length: int, si: int, ti: int=0) -> tuple:
        sn = len(self.s); tn = len(t)
        si += length; ti += length
        while si < sn and ti < tn:
            if self.s[si] != t[ti]: return self.s[si] < t[ti], ti
            si += 1; ti += 1
        return (si >= sn and ti < tn), ti

    def find_range(self, left: int, med: int, right: int, length: int) -> tuple:
        ng = left - 1; ok = med
        while ok - ng > 1:
            cur = ng + ok >> 1
            if self.sparse.query(cur, med) >= length:
                ok = cur
            else:
                ng = cur
        left = ok
        ok = med; ng = right + 1
        while ng - ok > 1:
            cur = ng + ok >> 1
            if self.sparse.query(med, cur) >= length:
                ok = cur
            else:
                ng = cur
        right = ok
        return left, right

    def arbitrary_lcp(self, i: int, j: int) -> int:
        if i == j: return len(self.s) - i
        return self.sparse.query(min(self.rank[i], self.rank[j]), max(self.rank[i], self.rank[j]))

    def find(self, t: str) -> tuple:
        left = 1; right = len(self.sa) - 1; med = left
        leftlen = 0; rightlen = 0; tlen = len(t)
        while right - left > 1:
            med = left + right >> 1
            corres_len = max(min(leftlen, self.sparse.query(left, med)), min(rightlen, self.sparse.query(med, right)))
            if corres_len < max(leftlen, rightlen):
                if leftlen < rightlen:
                    left = med; leftlen = corres_len
                else:
                    right = med; rightlen = corres_len
                continue
            ret = self.comp(t, corres_len, self.sa[med])
            if ret[1] == tlen: return self.find_range(left, med, right, tlen)
            if ret[0] == 0:
                right = med; rightlen = ret[1]
            else:
                left = med; leftlen = ret[1]
        if len(self.sa) <= 3:
            if self.comp(t, 0, self.sa[left])[1] == tlen:
                return self.find_range(left, left, right, tlen)
            if self.comp(t, 0, self.sa[right])[1] == tlen:
                return self.find_range(left, right, right, tlen)
            return -1, -1
        med = left + right - med
        ret = self.comp(t, min(leftlen, rightlen), self.sa[med])
        if ret[1] == tlen: return self.find_range(left, med, right, tlen)
        return -1, -1
