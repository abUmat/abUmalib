# my module
from misc.typing_template import *
# my module
def euler_tour(g: Graph, root: int=0) -> Tuple[List, List, List, List, List]:
    '''
    隣接リストと根を与えると
    通る辺, 通る頂点, 頂点に到達した時刻, 頂点を最後に通った時刻, 頂点の深さ
    のタプルを返す
    g: 隣接リスト
    root: root
    '''
    N = len(g)
    ete = []
    etv = []
    parents = [0] * N
    in_ = [0] * N
    out = [0] * N
    depth = [-1] * N
    stack = [root]
    depth[root] = 0
    i = 0
    while stack:
        v = stack.pop()
        if v >= 0:
            stack.append(~v)
            ete.append(v)
            etv.append(v)
            in_[v] = i
            for vv in g[v]:
                if depth[vv] != -1: continue
                depth[vv] = depth[v] + 1
                parents[vv] = v
                stack.append(vv)
        else:
            ete.append(~v)
            etv.append(parents[~v])
            out[~v] = i
        i += 1
    etv.pop()
    return ete, etv, in_, out, depth
