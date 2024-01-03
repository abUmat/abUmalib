# https://judge.yosupo.jp/problem/stern_brocot_tree
# my module
from misc.fastio import *
from mymath.stern_brocot_tree import *
# my module
T = rd()
for _ in range(T):
    cmd = rds()
    if cmd == "ENCODE_PATH":
        a, b = rd(), rd()
        f = SternBrocotTreeNode(a, b)
        wt(len(f.seq)); wt(' ')
        for s in f.seq:
            wt('R' if s > 0 else "L")
            wt(' ')
            wt(abs(s))
            wt(' ')
        wt('\n')
    elif cmd == "DECODE_PATH":
        k = rd()
        f = SternBrocotTreeNode()
        for _ in range(k):
            c = rds()
            n = rd()
            if c == 'R':
                f.go_right(n)
            if c == "L":
                f.go_left(n)
        print(f.x, f.y)
    elif cmd == "LCA":
        a, b, c, d = rd(), rd(), rd(), rd()
        f = SternBrocotTreeNode(a, b)
        g = SternBrocotTreeNode(c, d)
        h = SternBrocotTreeNode.lca(f, g)
        print(h.x, h.y)
    elif cmd == "ANCESTOR":
        k, a, b = rd(), rd(), rd()
        f = SternBrocotTreeNode(a, b)
        l = f.depth() - k
        if l < 0:
            wtn(-1)
        else:
            b = f.go_parent(l)
            assert(b)
            print(f.x, f.y)
    else:
        a, b = rd(), rd()
        f = SternBrocotTreeNode(a, b)
        print(*f.lower_bound(), *f.upper_bound())
