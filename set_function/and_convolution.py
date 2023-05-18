# https://nyaannyaan.github.io/library/set-function/and-convolution.hpp
# my module
from set_function.zeta_mobius_transform import *
# my module
def and_convolution(a, b, mod=0):
    'destructive'
    superset_zeta_transform(a)
    superset_zeta_transform(b)
    if mod:
        for i, x in enumerate(b): a[i] = a[i] * x % mod
    else:
        for i, x in enumerate(b): a[i] = a[i] * x
    superset_mobius_transform(a)
    return [x % mod for x in a] if mod else a
