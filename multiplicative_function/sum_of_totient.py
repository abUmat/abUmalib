def sum_of_totient(N: int, mod: int) -> int:
    if N < 2: return N
    f = lambda v, p, c: v // p * (p - 1)
    ns = [0]; p = []
    i = N
    while i > 0:
        ns.append(i)
        i = N // (N // i + 1)
    s = len(ns)
    sq = int(N ** 0.5)
    idx = lambda n: s - n if n <= sq else N // n

    h0 = [(x - 1) % mod for x in ns]
    h1 = [((x * (x + 1) >> 1) - 1) % mod for x in ns]

    for x in range(2, sq + 1):
        if h0[s - x] == h0[s - x + 1]: continue
        p.append(x)
        x2 = x * x
        for i in range(1, s):
            n = ns[i]
            if n < x2: break
            id = i * x if i * x <= sq else s - n // x
            h0[i] -= h0[id] - h0[s - x + 1]
            h1[i] -= (h1[id] - h1[s - x + 1]) * x % mod
    buf = [(y - x) % mod for x, y in zip(h0, h1)]
    ans = buf[idx(N)] + 1

    def dfs(i: int, c: int, v: int, lim: int, cur: int) -> None:
        nonlocal ans
        ans += cur * f(p[i] * v, p[i], c + 1) % mod
        if lim >= p[i] * p[i]:
            dfs(i, c + 1, p[i] * v, lim // p[i], cur)
        cur *= f(v, p[i], c)
        ans += cur * (buf[idx(lim)] - buf[idx(p[i])]) % mod
        for j in range(i + 1, len(p)):
            if p[j] * p[j] > lim: break
            dfs(j, 1, p[j], lim // p[j], cur)

    for i in range(len(p)):
        dfs(i, 1, p[i], N // p[i], 1)

    return ans % mod
