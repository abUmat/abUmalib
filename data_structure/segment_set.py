class SegmentSet:
    '''
    0以上u未満の整数が載る集合\n
    セグ木的な構造、各Nodeはその子孫のOR値を保持(ORではなくSUMならBITと同じ感じ)\n
    insert, delete, contains, predecessor, successorがO(logu)\n
    空間はO(u)\n
    k番目の値の取得、イテレートはO(u)(実装していない)
    #'''
    def __init__(self, u: int) -> None:
        self.log = (u-1).bit_length()
        self.size = 1 << self.log
        self.u = u
        self.data = bytearray(self.size << 1)

    def add(self, k: int) -> bool:
        k += self.size
        if self.data[k]: return False
        self.data[k] = 1
        while k > 1:
            k >>= 1
            if self.data[k]: break
            self.data[k] = 1
        return True

    def discard(self, k: int) -> bool:
        k += self.size
        if self.data[k] == 0: return False
        self.data[k] = 0
        while k > 1:
            if k & 1:
                if self.data[k - 1]: break
            else:
                if self.data[k + 1]: break
            k >>= 1
            self.data[k] = 0
        return True

    def __contains__(self, k: int) -> bool:
        return self.data[k + self.size] == 1

    def get_min(self) -> int:
        '''Find the minimam element, or -1 if it doesn't exist.'''
        if self.data[1] == 0: return -1
        k = 1
        while k < self.size:
            k <<= 1
            if self.data[k] == 0: k |= 1
        return k - self.size

    def get_max(self) -> int:
        '''Find the maximam element, or -1 if it doesn't exist.'''
        if self.data[1] == 0: return -1
        k = 1
        while k < self.size:
            k <<= 1
            if self.data[k | 1]: k |= 1
        return k - self.size

    def lt(self, k: int) -> int:
        '''Find the largest element < k, or -1 if it doesn't exist.'''
        if self.data[1] == 0: return -1
        x = k
        k += self.size
        while k > 1:
            if k & 1 and self.data[k ^ 1]:
                k >>= 1
                break
            k >>= 1
        k <<= 1
        if self.data[k] == 0: return -1
        while k < self.size:
            k <<= 1
            if self.data[k | 1]: k |= 1
        k -= self.size
        return k if k < x else -1

    def le(self, k: int) -> int:
        '''Find the largest element <= k, or -1 if it doesn't exist.'''
        if self.data[k + self.size]: return k
        return self.lt(k)

    def gt(self, k: int) -> int:
        '''Find the smallest element > k, or -1 if it doesn't exist.'''
        if self.data[1] == 0: return -1
        x = k
        k += self.size
        while k > 1:
            if k & 1 == 0 and self.data[k | 1]:
                k >>= 1
                break
            k >>= 1
        k = k << 1 | 1
        while k < self.size:
            k <<= 1
            if self.data[k] == 0: k |= 1
        k -= self.size
        return k if k > x and k < self.u else -1

    def ge(self, k: int) -> int:
        '''Find the smallest element >= k, or -1 if it doesn't exist.'''
        if self.data[k + self.size]: return k
        return self.gt(k)

    def __str__(self):
        return '{' + ', '.join(map(str, (i for i in range(self.u) if self.data[i + self.size]))) + '}'
