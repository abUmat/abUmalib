def berlekamp_massey(s, mod):
    N = len(s)
    b = [1]
    c = [1]
    y = 1
    for ed in range(1, N + 1):
        l = len(c)
        m = len(b)
        x = 0
        for i in range(l): x += c[i] * s[ed - l + i] % mod
        x %= mod
        b.append(0)
        m += 1
        if x == 0: continue
        freq = x * pow(y, mod - 2, mod)
        if l < m:
            tmp = c[:]
            c[:0] = [0] * (m - l)
            for i in range(m): c[m - 1 - i] = (c[m - 1 - i] - freq * b[m - 1 - i]) % mod
            b = tmp
            y = x
        else:
            for i in range(m): c[l - 1 - i] = (c[l - 1 - i] - freq * b[m - 1 - i]) % mod
    c.reverse()
    return c