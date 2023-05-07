def sum_of_totient(N: int, mod: int) -> int:
    if N < 2: return N
    ns = [0]; p = []
    i = N
    while i > 0:
        ns.append(i)
        i = N // (N // i + 1)
    s = len(ns)
    sq = int(N ** 0.5)

    h0 = [x - 1 for x in ns]
    h1 = [(x * (x + 3) >> 1) % mod for x in h0]
    for x in range(2, sq + 1):
        if h0[-x] == h0[-x + 1]: continue
        p.append(x)
        x2 = x * x
        h0tmp, h1tmp = h0[-x + 1], h1[-x + 1]
        for i, n in enumerate(ns):
            if not i: continue
            if n < x2: break
            id = i * x if i * x <= sq else s - n // x
            h0[i] -= h0[id] - h0tmp
            h1[i] -= (h1[id] - h1tmp) * x
    buf = [y - x for x, y in zip(h0, h1)]
    ans = buf[1] + 1
    idx = lambda n: s - n if n <= sq else N // n

    q = [[i, x, x, N // x, 1] for i, x in enumerate(p)]
    while q:
        i, x, val, lim, v = q.pop()
        if lim >= x * x:
            q.append([i, x, x * val, lim // x, v])
        vv = v * (val // x) * (x - 1)
        ans += (vv * (buf[idx(lim)] - buf[idx(x)]) + v * (val * x - val))
        for j in range(i + 1, len(p)):
            x = p[j]
            if x * x > lim: break
            q.append([j, x, x, lim // x, vv])
    return ans % mod
