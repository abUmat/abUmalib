# https://judge.yosupo.jp/problem/suffixarray
# my module
from mystring.suffix_array import *
# my module
s = input()
sa = sa_is(s)
print(*sa[1:])