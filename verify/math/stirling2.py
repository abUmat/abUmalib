# my module
from fps.fps998244353 import *
# my module
N = int(input())
C = Binomial(MOD, N + 10)
s2 = stirling2(N, C)
print(*s2)