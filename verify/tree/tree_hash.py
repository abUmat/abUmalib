# https://judge.yosupo.jp/problem/rooted_tree_isomorphism_classification
# my module
from misc.fastio import *
from tree.tree_hash import *
# my module
N = rd()
G = [[] for _ in range(N)]
for i in range(N - 1):
    G[rd()].append(i + 1)
tree = TreeHash(G)
h = tree.hash
compress = {a: i for i, a in enumerate(sorted(set(h)))}
wtn(len(set(h)))
wtnl([compress[a] for a in h])