# my module
from misc.typing_template import *
from modulo.modinv import *
# my module
def determinant(mat: Matrix, mod: int) -> int:
    mat = [arr[:] for arr in mat]
    n = len(mat)
    cnt = 0
    for i, arr_i in enumerate(mat):
        if not arr_i[i]:
            for j in range(i + 1, n):
                if mat[j][i]: break
            else: return 0
            cnt ^= 1
            mat[i], mat[j] = mat[j], mat[i]
            arr_i = mat[i]
        if not arr_i[i]: return 0
        inv = modinv(arr_i[i], mod)
        for j in range(i + 1, n):
            arr_j = mat[j]
            a = arr_j[i] * inv % mod
            if not a: continue
            for k in range(i + 1, n):
                arr_j[k] -= arr_i[k] * a
                arr_j[k] %= mod
    ret = -1 if cnt else 1
    for i, arr_i in enumerate(mat):
        ret *= arr_i[i]
        if i & 1: ret %= mod
    return ret % mod
