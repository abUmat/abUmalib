# https://judge.yosupo.jp/problem/product_of_polynomial_sequence
# my module
from misc.fastio import *
from fps.ntt_friendly_fps import *
# my module
from collections import deque
mod = 998244353
fps = FPS(mod)
N = rd()
q = deque()
for _ in range(N):
    d = rd()
    A = rdl(d + 1)
    q.append(A)
while len(q) >= 2:
    q.append(fps.mul(q.popleft(), q.popleft()))
if N: wtnl(q.pop())
else: wtn(1)
