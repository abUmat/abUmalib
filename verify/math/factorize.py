# https://judge.yosupo.jp/problem/factorize
# my module
from misc.fastio import *
from prime.fast_factorize import *
# my module
Q = rd()
for _ in range(Q):
    a = rd()
    f = factorize(a)
    ans = [i for i,j in sorted(f.items()) for _ in range(j)]
    wt(len(ans)); wt(' '); wtnl(ans)