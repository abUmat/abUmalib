# https://judge.yosupo.jp/problem/inv_of_polynomials
# my module
from misc.fastio import *
from math998244353.polynomial_gcd import *
# my module
N, M = rd(), rd()
A = rdl(N)
B = rdl(M)
flg, h = poly_inv(A, B)
if flg:
    wtn(len(h))
    wtnl(h)
else:
    wtn(-1)