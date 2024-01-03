# https://judge.yosupo.jp/problem/longest_common_substring
# my module
from misc.fastio import *
from mystring.rolling_hash import *
# my module
# RollingHash Bisect
S = rds()
T = rds()
ls, lt = len(S), len(T)
rhs = RollingHash(S)
rht = RollingHash(T)
ok = 0
ng = min(ls, lt) + 1
a, b, c, d, length = 0, 0, 0, 0, 0
while ng - ok > 1:
    mid = ok + ng >> 1
    dic = {}
    for r in range(mid, ls+1):
        dic[rhs.get(r - mid, r)] = r
    for r in range(mid, lt+1):
        h = rht.get(r - mid, r)
        if h in dic.keys():
            contain = 1
            if length < mid:
                a, b, c, d, length = dic[h]-mid, dic[h], r-mid, r, mid
            break
    if contain:
        ok = mid
    else:
        ng = mid
print(a, b, c, d)
