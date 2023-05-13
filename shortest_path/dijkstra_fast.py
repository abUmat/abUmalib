# my module
from data_structure.radix_heap import *
# my module
def dijkstra(g, s):
    mask = (1 << 30) - 1
    n = len(g)
    INF = (1 << 60) - 1
    dist = [INF] * n
    heap = RadixHeap()
    heap.push(0, s)
    dist[s] = 0
    while heap:
        d, v = heap.pop()
        if d > dist[v]: continue
        for tmp in g[v]:
            vv, w = tmp >> 30, tmp & mask
            if dist[vv] > d + w:
                dist[vv] = d + w
                heap.push(d + w ,vv)
    return dist