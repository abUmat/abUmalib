# https://judge.yosupo.jp/problem/zalgorithm
# my module
from mystring.suffix_array import *
# my module
s = input()
sa = sa_is(s)
lcp, rank = lcp_array(s, sa)
search = StringSearch(s, sa, lcp, rank)
print(*[search.arbitrary_lcp(0, i) for i in range(len(s))])