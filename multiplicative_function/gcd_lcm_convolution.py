# my module
from multiplicative_function.divisor_multiple_transform import *
# my module
def gcd_convolution(a: list, b: list, mod: int) -> list:
    s, t = a[::], b[::]
    MultipleTransform.zeta_transform_list(s, mod)
    MultipleTransform.zeta_transform_list(t, mod)
    for i, x in enumerate(t): s[i] = s[i] * x % mod
    MultipleTransform.mobius_transform_list(s, mod)
    return s

def lcm_convolution(a: list, b: list, mod: int) -> list:
    s, t = a[::], b[::]
    DivisorTransform.zeta_transform_list(s, mod)
    DivisorTransform.zeta_transform_list(t, mod)
    for i, x in enumerate(t): s[i] = s[i] * x % mod
    DivisorTransform.mobius_transform_list(s, mod)
    return s
