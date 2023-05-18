# my module
from fps.fps998244353 import *
# my module
N, c = map(int,input().split())
A = list(map(int,input().split()))
print(*taylor_shift(A, c, Binomial(MOD, N)))