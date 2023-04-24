# my module
from set_function.walsh_hadamard_transform import *
# my module
def xor_convolution(a, b, mod=0):
    'destructive'
    walsh_hadamard_transform(a)
    walsh_hadamard_transform(b)
    if mod:
        a = [(x % mod) * (y % mod) % mod for x, y in zip(a, b)]
    else:
        a = [x * y for x, y in zip(a, b)]
    if mod:
        walsh_hadamard_transform(a, 1, pow(len(a), mod-2, mod))
        a = [x % mod for x in a]
    else:
        walsh_hadamard_transform(a, 1, 1 / len(a))
    return a