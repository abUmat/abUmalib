# my module
from data_structure.skew_heap import *
from data_structure.unionfind import *
# my module
def minimum_cost_arborescence(N: int, root: int, es: List[int]) -> List[int]:
    '''
    Directed MST
    N: number of Vertex
    root: Root
    es: List of Edges. values is (cost << 40 | frm << 20 | to)
    '''
    mask = (1 << 20) - 1
    Heap = SkewHeap()
    uf = UnionFind(N)
    used = [-1] * N
    frm = [0] * N
    from_cost = [0] * N
    come: List[SkewHeapNode] = [None] * N
    used[root] = root
    par_e = [-1] * len(es)
    stem = [-1] * N
    idxs = []
    for i, e in enumerate(es):
        come[e & mask] = Heap.append(come[e & mask], e >> 40, i)

    costs = 0
    for start in range(N):
        if used[start] != -1: continue
        cur = start
        chi_e = []
        cycle = 0
        while used[cur] == -1 or used[cur] == start:
            used[cur] = start
            if come[cur] == None: return []
            src = uf.leader(es[come[cur].idx] >> 20 & mask)
            cost = come[cur].key + come[cur].laz
            idx = come[cur].idx
            come[cur] = Heap.pop(come[cur])
            if src == cur: continue

            frm[cur] = src
            from_cost[cur] = cost
            if stem[cur] == -1: stem[cur] = idx
            costs += cost
            idxs.append(idx)
            while cycle:
                par_e[chi_e.pop()] = idx
                cycle -= 1
            chi_e.append(idx)

            if used[src] == start:
                p = cur
                while 1:
                    if come[p]: Heap.apply(come[p], -from_cost[p])
                    if p != cur:
                        uf.union(p, cur)
                        newheap = Heap.meld(come[cur], come[p])
                        cur = uf.leader(cur)
                        come[cur] = newheap
                    p = uf.leader(frm[p])
                    cycle += 1
                    if p == cur: break
            else:
                cur = src

    used_e = [0] * len(es)
    res = []
    for _ in range(len(idxs))[::-1]:
        idx = idxs[_]
        if used_e[idx]: continue
        e = es[idx]
        res.append(e)
        x = stem[e & mask]
        while x != idx:
            used_e[x] = 1
            x = par_e[x]
    return res
