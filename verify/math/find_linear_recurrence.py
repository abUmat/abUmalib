# https://judge.yosupo.jp/problem/find_linear_recurrence
# my module
from misc.fastio import *
from fps.berlekamp_massey import *
# my module
mod = 998244353
N = rd()
A = rdl(N)
c = berlekamp_massey(A, mod)
c = [mod - x if x else x for i, x in enumerate(c) if i]
wtn(len(c))
wtnl(c)