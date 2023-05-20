# https://judge.yosupo.jp/problem/division_of_polynomials
# my module
from misc.fastio import *
from math998244353.fps import *
# my module
N, M = rd(), rd()
A = rdl(N)
B = rdl(M)
q, r = FPS.divmod(A, B)
wt(len(q)); wt(' '); wtn(len(r))
wtnl(q)
wtnl(r)