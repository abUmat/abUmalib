def euler_tour(root, G):
    N = len(G)
    ete = []
    etv = []
    parents = [None] * N
    in_ = [0] * N
    out = [0] * N
    depth = [None]*N
    q = [~root, root]
    depth[root] = 0
    i = 0
    while q:
        v = q.pop()
        if v >= 0:
            ete.append(v)
            etv.append(v)
            in_[v] = i
            for vv in G[v]:
                if depth[vv] is not None: continue
                depth[vv] = depth[v] + 1
                parents[vv] = v
                q.append(~vv)
                q.append(vv)
        else:
            ete.append(~v)
            etv.append(parents[~v])
            out[~v] = i
        i += 1
    etv.pop()
    return ete, etv, in_, out, depth
