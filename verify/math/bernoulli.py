# my module
from fps.fps998244353 import *
# my module
N = int(input())
C = Binomial(MOD, N + 10)
b = bernoulli(N, C)
print(*b)