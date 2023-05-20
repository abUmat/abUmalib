# https://judge.yosupo.jp/problem/division_of_polynomials
# my module
from misc.fastio import *
from fps.arbitrary_fps import *
# my module
mod = 998244353
fps = FPS(mod)
N, M = rd(), rd()
A = rdl(N)
B = rdl(M)
q, r = fps.divmod(A, B)
wt(len(q)); wt(' '); wtn(len(r))
wtnl(q)
wtnl(r)