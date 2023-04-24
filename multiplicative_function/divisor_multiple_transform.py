# my module
from prime.prime_enumerate import *
# my module
class DivisorTransform:
    @staticmethod
    def zeta_transform_list(a, mod=0):
        N = len(a) - 1
        sieve = prime_enumerate(N)
        for p in sieve:
            for k in range(1, N // p + 1): a[k * p] += a[k]
        if mod:
            for i in range(len(a)): a[i] %= mod

    @staticmethod
    def mobius_transform_list(a, mod=0):
        N = len(a) - 1
        sieve = prime_enumerate(N)
        for p in sieve:
            for k in range(N // p, 0, -1): a[k * p] -= a[k]
        if mod:
            for i in range(len(a)): a[i] %= mod

    @staticmethod
    def zeta_transform_pair(a, mod=0):
        for i in range(len(a))[::-1]:
            for j in range(len(a)):
                if a[i][0] == a[j][0]: break
                if a[j][0] % a[i][0] == 0:  a[j][1] += a[i][1]
        if mod:
            for i in range(len(a)): a[i][1] %= mod

    @staticmethod
    def mobius_transform_pair(a, mod=0):
        for i in range(len(a)):
            for j in range(len(a))[::-1]:
                if a[i][0] == a[j][0]: break
                if a[j][0] % a[i][0] == 0:  a[j][1] -= a[i][1]
        if mod:
            for i in range(len(a)): a[i][1] %= mod

class MultipleTransform:
    @staticmethod
    def zeta_transform_list(a, mod=0):
        N = len(a) - 1
        sieve = prime_enumerate(N)
        for p in sieve:
            for k in range(N // p, 0, -1): a[k] += a[k * p]
        if mod:
            for i in range(len(a)): a[i] %= mod

    @staticmethod
    def mobius_transform_list(a, mod=0):
        N = len(a) - 1
        sieve = prime_enumerate(N)
        for p in sieve:
            for k in range(1, N // p + 1): a[k] -= a[k * p]
        if mod:
            for i in range(len(a)): a[i] %= mod

    @staticmethod
    def zeta_transform_pair(a, mod=0):
        for i in range(len(a)):
            for j in range(len(a))[::-1]:
                if a[i][0] == a[j][0]: break
                if a[j][0] % a[i][0] == 0: a[i][1] += a[j][1]
        if mod:
            for i in range(len(a)): a[i][1] %= mod

    @staticmethod
    def mobius_transform_pair(a, mod=0):
        for i in range(len(a))[::-1]:
            for j in range(len(a))[::-1]:
                if i == j: break
                if a[j][0] % a[i][0] == 0: a[i][1] -= a[j][1]
        if mod:
            for i in range(len(a)): a[i][1] %= mod
