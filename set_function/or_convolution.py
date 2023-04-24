# my module
from set_function.zeta_mobius_transform import *
# my module
def or_convolution(a, b, mod=0):
    'destructive'
    subset_zeta_transform(a)
    subset_zeta_transform(b)
    if mod:
        a = [(x % mod) * (y % mod) % mod for x, y in zip(a, b)]
    else:
        a = [x * y for x, y in zip(a, b)]
    subset_mobius_transform(a)
    if mod: return [x % mod for x in a]
    return a
