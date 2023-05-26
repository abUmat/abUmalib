# https://judge.yosupo.jp/problem/number_of_substrings
# my module
from mystring.suffix_array import *
# my module
s = input()
sa = sa_is(s)
lcp, _ = lcp_array(s, sa)
ans = len(s) * (len(s) + 1) >> 1
for x in lcp: ans -= x
print(ans)