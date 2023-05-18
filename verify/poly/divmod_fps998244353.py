# my module
from fps.fps998244353 import *
# my module
N, M = map(int,input().split())
A = list(map(int,input().split()))
B = list(map(int,input().split()))
q, r = div_mod(A, B)
print(len(q), len(r))
print(*q)
print(*r)