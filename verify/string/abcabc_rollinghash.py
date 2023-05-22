# https://atcoder.jp/contests/abc284/tasks/abc284_f
# my module
from mystring.rolling_hash import *
# my module
N = int(input())
T = input()
rh1, rh2 = RollingHash(T), RollingHash(T[::-1])
for i in range(N):
    h1 = rh1.get(0, i)
    h2 = rh1.get(N+i, N<<1)
    h = rh1.connect(h1, h2, N-i)
    h3 = rh2.get(N-i, N+N-i)
    if h == h3:
        print(T[:i]+T[N+i:])
        print(i)
        exit()
print(-1)