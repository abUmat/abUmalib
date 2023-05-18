# https://nyaannyaan.github.io/library/set-function/or-convolution.hpp
# my module
from set_function.zeta_mobius_transform import *
# my module
def or_convolution(a, b, mod=0):
    'destructive'
    subset_zeta_transform(a)
    subset_zeta_transform(b)
    if mod:
        for i, x in enumerate(b): a[i] = a[i] * x % mod
    else:
        for i, x in enumerate(b): a[i] = a[i] * x
    subset_mobius_transform(a)
    return [x % mod for x in a] if mod else a