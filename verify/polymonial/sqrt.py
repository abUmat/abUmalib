# my module
from fps.fps998244353 import *
# my module
N = int(input())
A = list(map(int,input().split()))
ans = sqrt(A)
print(*ans) if ans else print(-1)