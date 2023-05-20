# https://judge.yosupo.jp/problem/product_of_polynomial_sequence
# my module
from misc.fastio import *
from math998244353.fps import *
# my module
from collections import deque
N = rd()
q = deque()
for _ in range(N):
    d = rd()
    A = rdl(d + 1)
    q.append(A)
while len(q) >= 2:
    q.append(FPS.mul(q.popleft(), q.popleft()))
if N: wtnl(q.pop())
else: wtn(1)
