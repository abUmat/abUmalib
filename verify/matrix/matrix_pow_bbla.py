# https://yukicoder.me/problems/no/1112
# my module
from misc.fastio import *
from matrix.black_box_linear_algebra import *
from fps.arbitrary_fps import *
# my module
mod = 1_000_000_007
K, M, N = rd(), rd(), rd()
m = ModMatrix(K * K, mod)
for i in range(M):
    p, q, r = rd() - 1, rd() - 1, rd() - 1
    m.add(p * K + q, q * K + r, 1)
b = [0] * (K * K)
for i in range(K): b[i * K] = 1
res = fast_pow(m, b, N - 2)
wtn(sum(res[:K]) % mod)