def superset_zeta_transform(f):
    'destructive'
    n = len(f)
    i = 1
    while i < n:
        for j in range(n):
            if not j & i: f[j] += f[j | i]
        i <<= 1

def superset_mobius_transform(f):
    'destructive'
    n = len(f)
    i = 1
    while i < n:
        for j in range(n):
            if not j & i: f[j] -= f[j | i]
        i <<= 1

def subset_zeta_transform(f):
    'destructive'
    n = len(f)
    i = 1
    while i < n:
        for j in range(n):
            if not j & i: f[j | i] += f[j]
        i <<= 1

def subset_mobius_transform(f):
    'destructive'
    n = len(f)
    i = 1
    while i < n:
        for j in range(n):
            if not j & i: f[j | i] -= f[j]
        i <<= 1