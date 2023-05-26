# https://judge.yosupo.jp/problem/min_of_mod_of_linear
# my module
from misc.fastio import *
from mymath.sum_of_floor import *
# my module
T = rd()
for _ in range(T):
    n, m, a, b = rd(), rd(), rd(), rd()
    ng = -1; ok = m - 1
    while ok - ng > 1:
        mid = ok + ng >> 1
        if mod_affine_range_counting(a, b, m, n, mid + 1):
            ok = mid
        else:
            ng = mid
    wtn(ok)