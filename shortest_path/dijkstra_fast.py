# my module
from data_structure.radix_heap import *
# my module
def dijkstra(g, s: int) -> list:
    INF = (1 << 60) - 1
    MASK = (1 << 30) - 1
    dist = [INF] * len(g)
    heap = RadixHeap()
    heap.push(0, s)
    dist[s] = 0
    while heap.s:
        d, v = heap.pop()
        if d > dist[v]: continue
        for tmp in g[v]:
            vv, w = tmp >> 30, tmp & MASK
            if dist[vv] > d + w:
                dist[vv] = d + w
                heap.push(d + w, vv)
    return dist

def dijkstra_point(g, start: int, goal: int) -> int:
    INF = (1 << 60) - 1
    MASK = (1 << 30) - 1
    dist = [INF] * len(g)
    heap = RadixHeap()
    dist[start] = 0
    heap.push(0, start)
    while heap.s:
        d, v = heap.pop()
        if v == goal: return dist[v]
        if d > dist[v]: continue
        for tmp in g[v]:
            vv, w = tmp >> 30, tmp & MASK
            if dist[vv] > d + w:
                dist[vv] = d + w
                heap.push(d + w, vv)
    return -1

def dijkstra_restore(g, start: int=0):
    INF = (1 << 60) - 1
    MASK = (1 << 30) - 1
    dist = [(INF, -1) for _ in range(len(g))]
    heap = RadixHeap()
    dist[start] = 0, -1
    heap.push(0, start)
    while heap.s:
        d, v = heap.pop()
        if d > dist[v][0]: continue
        for tmp in g[v]:
            vv, w = tmp >> 30, tmp & MASK
            if dist[vv][0] > d + w:
                dist[vv] = d + w, v
                heap.push(d + w, vv)
    return dist
