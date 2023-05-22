# my module
from multiplicative_function.divisor_multiple_transform import *
# my module
def gcd_convolution(a, b, mod):
    s, t = a[::], b[::]
    MultipleTransform.zeta_transform_list(s, mod)
    MultipleTransform.zeta_transform_list(t, mod)
    for i in range(len(a)): s[i] = s[i] * t[i] % mod
    MultipleTransform.mobius_transform_list(s, mod)
    return s
