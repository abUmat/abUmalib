# my module
from fps.fps998244353 import *
# my module
N = int(input())
C = Binomial(MOD, N)
s1 = stirling1(N, C)
for i in range(N)[::-2]: s1[i] = -s1[i] % MOD
print(*s1)