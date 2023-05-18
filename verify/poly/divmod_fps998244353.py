# https://judge.yosupo.jp/problem/division_of_polynomials
# my module
from misc.fastio import *
from fps.fps998244353 import *
# my module
N, M = rd(), rd()
A = rdl(N)
B = rdl(M)
q, r = div_mod(A, B)
wt(len(q)); wt(' '); wtn(len(r))
wtnl(q)
wtnl(r)