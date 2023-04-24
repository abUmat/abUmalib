def walsh_hadamard_transform(f, inverse=0, invn=0):
    'destructive'
    n = len(f)
    i = 1
    while i < n:
        for j in range(n):
            if not j & i:
                x = f[j]; y = f[j | i]
                f[j] = x + y; f[j | i] = x - y
        i <<= 1
    if inverse:
        for i in range(n): f[i] *= invn