# https://judge.yosupo.jp/problem/inv_of_polynomials
# my module
from misc.fastio import *
from fps.ntt_friendly_fps import *
from fps.polynomial_gcd import *
# my module
mod = 998244353
N, M = rd(), rd()
A = rdl(N)
B = rdl(M)
flg, h = poly_inv(A, B, mod)
if flg:
    wtn(len(h))
    wtnl(h)
else:
    wtn(-1)