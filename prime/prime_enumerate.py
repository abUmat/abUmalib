# https://judge.yosupo.jp/submission/100731
from bisect import bisect_right
from math import log
# my module
from misc.typing_template import *
# my module
def prime_enumerate(n: int) -> List[int]:
    K_MOD30 = [1, 7, 11, 13, 17, 19, 23, 29]
    C1 = [6, 4, 2, 4, 2, 4, 6, 2]
    C0 = [[0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 0, 1, 1, 1, 1],
          [2, 2, 0, 2, 0, 2, 2, 1], [3, 1, 1, 2, 1, 1, 3, 1],
          [3, 3, 1, 2, 1, 3, 3, 1], [4, 2, 2, 2, 2, 2, 4, 1],
          [5, 3, 1, 4, 1, 3, 5, 1], [6, 4, 2, 4, 2, 4, 6, 1]]
    k_mask = [[254, 253, 251, 247, 239, 223, 191, 127], [253, 223, 239, 254, 127, 247, 251, 191],
              [251, 239, 254, 191, 253, 127, 247, 223], [247, 254, 191, 223, 251, 253, 127, 239],
              [239, 127, 253, 251, 223, 191, 254, 247], [223, 247, 127, 253, 191, 254, 239, 251],
              [191, 251, 247, 127, 254, 239, 223, 253], [127, 191, 223, 239, 247, 251, 253, 254]]

    def __sieve(n: int):
        """素数列挙 O(N loglogN)"""
        A = [1, 7, 11, 13, 17, 19, 23, 29]
        bit_to_index = {1 << i: i for i in range(8)}
        N, r = (n + 29) // 30, n % 30
        flags = bytearray([0xff] * N)  # bytesarrayが高速
        if r != 0: flags[-1] = (1 << bisect_right(A, r)) - 1
        flags[0] &= 0xfe
        sqni = (int(n ** 0.5) + 1) // 30 + 1
        len_flags = len(flags)
        for i in range(sqni):
            flag = flags[i]
            while flag:
                lsb = flag & (-flag)
                ibit = bit_to_index[lsb]
                m = K_MOD30[ibit]
                pm = 30 * i + 2 * m
                j = i * pm + (m * m) // 30
                k = ibit
                while j < len_flags:
                    flags[j] &= k_mask[ibit][k]
                    j += i * C1[k] + C0[ibit][k]
                    k = (k + 1) & 7
                flag &= (flag - 1)
        return flags

    if n < 2: return []
    if n < 3: return [2]
    if n < 5: return [2, 3]
    res = __sieve(n)
    primes = [0] * int(1.2551 * n / log(n) + 10)
    primes[:3] = 2, 3, 5
    cnt = 3
    pat = [0,1,6,2,7,5,4,3]
    for i, bit in enumerate(res):
        while bit:
            t = bit & -bit
            t *= 0b11101
            t >>= 5
            j = pat[t & 0b111]
            primes[cnt] = 30 * i + K_MOD30[j]
            cnt += 1
            bit &= bit - 1
    return primes[:cnt]
