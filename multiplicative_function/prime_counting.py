# https://judge.yosupo.jp/submission/126093
def prime_counting(n: int) -> int:
    'O(N**0.75 / logN)'
    if n <= 3:
        if n <= 1: return 0
        return 2
    v = int(n ** 0.5) - 1
    while v * v <= n: v += 1
    v -= 1
    smalls = [i + 1 >> 1 for i in range(v + 1)]
    s = v + 1 >> 1
    roughs = [i << 1 | 1 for i in range(s)]
    larges = [int(n / (i << 1 | 1) + 1) >> 1 for i in range(s)]
    skip = bytearray([0] * (v + 1))
    pc = 0
    for p in range(3, v + 1, 2):
        if skip[p]: continue
        q = p * p
        pc += 1
        if q * q > n: break
        skip[p] = 1
        for i in range(q, v + 1, p << 1): skip[i] = 1
        ns = 0
        for k in range(s):
            i = roughs[k]
            if skip[i]:
                continue
            d = i * p
            if d <= v:
                x = larges[smalls[d] - pc]
            else:
                x = smalls[int(n / d)]
            larges[ns] = larges[k] + pc - x
            roughs[ns] = i
            ns += 1
        s = ns
        i = v
        for j in range(int(v / p), p - 1, -1):
            c = smalls[j] - pc
            e = j * p
            while i >= e:
                smalls[i] -= c
                i -= 1
    ret = larges[0] + ((s + (pc - 1 << 1)) * (s - 1) >> 1) - sum(larges[1:s])

    for l in range(1, s):
        q = roughs[l]
        m = int(n / q)
        e = smalls[int(m / q)] - pc
        if e <= l: break
        t = 0
        for r in roughs[l + 1:e + 1]: t += smalls[int(m / r)]
        ret += t - (e - l) * (pc + l - 1)
    return ret
