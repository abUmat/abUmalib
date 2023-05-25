# https://nyaannyaan.github.io/library/set-function/xor-convolution.hpp
# my module
from mymath.modinv import *
from set_function.walsh_hadamard_transform import *
# my module
def xor_convolution(a, b, mod=0):
    'destructive'
    walsh_hadamard_transform(a)
    walsh_hadamard_transform(b)
    if mod:
        for i, x in enumerate(b): a[i] = a[i] * x % mod
    else:
        for i, x in enumerate(b): a[i] = a[i] * x
    if mod:
        walsh_hadamard_transform(a, 1, modinv(len(a), mod))
        return [x % mod for x in a]
    else: # ???
        walsh_hadamard_transform(a, 1, 1 / len(a))
        return a