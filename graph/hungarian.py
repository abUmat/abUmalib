# my module
from misc.typing_template import *
# my module
# https://judge.yosupo.jp/submission/106182
def hungarian(cost: Matrix) -> Tuple[int, List[int]]:
    inf = 1 << 60
    V = len(cost)

    row_mate = [-1] * V
    col_mate = [-1] * V
    pi = [0] * V
    residual: Func21= lambda r, c: cost[r][c] - pi[c]
    transferrable = bytearray(V)
    for col in range(V):
        row = min(range(V), key=lambda r: cost[r][col])
        pi[col] = cost[row][col]
        if row_mate[row] == -1:
            row_mate[row] = col
            col_mate[col] = row
            transferrable[row] = 1
        else:
            transferrable[row] = 0

    for row, col in enumerate(row_mate):
        if not transferrable[row]: continue
        c = -1
        for v in range(V):
            if v != col and (c == -1 or residual(row, c) > residual(row, v)):
                c = v
        pi[col] -= residual(row, c)

    for _ in range(2):
        for row in range(V):
            if row_mate[row] != -1: continue
            u1 = residual(row, 0)
            u2 = inf
            c1 = 0
            for c in range(V):
                u = residual(row, c)
                if u < u1 or (u == u1 and col_mate[c1] != -1):
                    u2 = u1
                    u1 = u
                    c1 = c
                elif u < u2:
                    u2 = u
            if u1 < u2: pi[c1] -= u2 - u1
            if col_mate[c1] != -1: row_mate[col_mate[c1]] = col_mate[c1] = -1
            row_mate[row] = c1
            col_mate[c1] = row

    cols = list(range(V))
    for row in range(V):
        if row_mate[row] != -1: continue
        dist = [residual(row, c) for c in range(V)]
        pred = [row] * V
        def func():
            scanned = 0
            labeled = 0
            last = 0
            while 1:
                if scanned == labeled:
                    last = scanned
                    mn = dist[cols[scanned]]
                    for j in range(scanned, V):
                        c = cols[j]
                        if dist[c] <= mn:
                            if dist[c] < mn:
                                mn = dist[c]
                                labeled = scanned
                            cols[j], cols[labeled] = cols[labeled], cols[j]
                            labeled += 1
                    for j in range(scanned, labeled):
                        if col_mate[cols[j]] == -1:
                            return cols[j], last
                assert(scanned < labeled)
                c1 = cols[scanned]
                scanned += 1
                r1 = col_mate[c1]
                for j in range(labeled, V):
                    c2 = cols[j]
                    ln = residual(r1, c2) - residual(r1, c1)
                    assert(ln >= 0)
                    if dist[c2] > dist[c1] + ln:
                        dist[c2] = dist[c1] + ln
                        pred[c2] = r1
                        if ln == 0:
                            if col_mate[c2] == -1:
                                return c2, last
                            cols[j], cols[labeled] = cols[labeled], cols[j]
                            labeled += 1

        col, last = func()
        for i, c in enumerate(cols):
            if i == last: break
            pi[c] += dist[c] - dist[col]

        t = col
        while t != -1:
            col = t
            r = pred[col]
            col_mate[col] = r
            row_mate[r], t = t, row_mate[r]

    total = sum(cost[u][r] for u, r in enumerate(row_mate))

    return total, row_mate
