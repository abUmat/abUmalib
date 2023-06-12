# https://judge.yosupo.jp/problem/predecessor_problem
# my module
from data_structure.tatyam_sortedset import *
# my module
import sys
input = sys.stdin.buffer.readline
N, Q = map(int,input().split())
T = input()
arr = [i for i, c in enumerate(T) if c == 49]
s = SortedSetInt(arr)
ans = []
for _ in range(Q):
    c, k = map(int,input().split())
    if c == 0:
        s.add(k)
    elif c == 1:
        s.discard(k)
    elif c == 2:
        ans.append(int(k in s))
    elif c == 3:
        res = s.ge(k)
        if res is None: res = -1
        ans.append(res)
    else:
        res = s.le(k)
        if res is None: res = -1
        ans.append(res)
print('\n'.join(map(str, ans)))