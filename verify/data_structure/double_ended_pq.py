# https://judge.yosupo.jp/problem/double_ended_priority_queue
# my module
from misc.fastio import *
from data_structure.double_ended_priority_queue import *
# my module
N, Q = rd(), rd()
S = rdl(N)
depq = DoubleEndedPriorityQueue(S)
for i in range(Q):
    cmd = rd()
    if cmd == 0:
        x = rd()
        depq.push(x)
    elif cmd == 1:
        wtn(depq.pop_min())
    else:
        wtn(depq.pop_max())