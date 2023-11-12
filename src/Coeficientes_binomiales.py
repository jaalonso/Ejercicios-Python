# Coeficientes_binomiales.py
# Coeficientes binomiales.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 19-septiembre-2023
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# El coeficiente binomial n sobre k es el número de subconjuntos de k
# elementos escogidos de un conjunto con n elementos.
#
# Definir la función
#    binomial : (int, int) -> int
# tal que binomial(n, k) es el coeficiente binomial n sobre k. Por
# ejemplo,
#    binomial(6, 3) == 20
#    binomial(5, 2) == 10
#    binomial(5, 3) == 10
# ---------------------------------------------------------------------

from sys import setrecursionlimit
from timeit import Timer, default_timer

import numpy as np
import numpy.typing as npt

setrecursionlimit(10**6)

# 1ª definición (por recursión)
# =============================

def binomial1(n: int, k: int) -> int:
    if k == 0:
        return 1
    if n == k:
        return 1
    return binomial1(n-1, k-1) + binomial1(n-1, k)

# 2ª definición (con programación dinámica)
# =========================================

def binomial2(n: int, k: int) -> int:
    return matrizBinomial2(n, k)[n][k]

# (matrizBinomial2 n k) es la matriz de orden (n+1)x(k+1) tal que el
# valor en la posición (i,j) (con j <= i) es el coeficiente binomial i
# sobre j. Por ejemplo,
#    >>> matrizBinomial2(3, 3)
#    [[1, 0, 0, 0], [1, 1, 0, 0], [1, 2, 1, 0], [1, 3, 3, 1]]
def matrizBinomial2(n: int, k: int) -> list[list[int]]:
    q = [[0 for i in range(k + 1)] for j in range(n + 1)]

    for i in range(n + 1):
        for j in range(min(i, k) + 1):
            if j == 0:
                q[i][j] = 1
            elif i == j:
                q[i][j] = 1
            else:
                q[i][j] = q[i - 1][j - 1] + q[i - 1][j]

    return q

# 3ª definición (con programación dinámica y numpy)
# ================================================

def binomial3(n: int, k: int) -> int:
    return matrizBinomial3(n, k)[n][k]

# (matrizBinomial3 n k) es la matriz de orden (n+1)x(k+1) tal que el
# valor en la posición (i,j) (con j <= i) es el coeficiente binomial i
# sobre j. Por ejemplo,
#    >>> matrizBinomial3(3, 3)
#    array([[1, 0, 0, 0],
#           [1, 1, 0, 0],
#           [1, 2, 1, 0],
#           [1, 3, 3, 1]])
def matrizBinomial3(n: int, k: int) -> npt.NDArray[np.int_]:
    q = np.zeros((n + 1, k + 1), dtype=object)

    for i in range(n + 1):
        for j in range(min(i, k) + 1):
            if j == 0:
                q[i, j] = 1
            elif i == j:
                q[i, j] = 1
            else:
                q[i, j] = q[i - 1, j - 1] + q[i - 1, j]

    return q

# Comparación de eficiencia
# =========================

def tiempo(e: str) -> None:
    """Tiempo (en segundos) de evaluar la expresión e."""
    t = Timer(e, "", default_timer, globals()).timeit(1)
    print(f"{t:0.2f} segundos")

# La comparación es
#    >>> tiempo('binomial1(27, 12)')
#    4.26 segundos
#    >>> tiempo('binomial2(27, 12)')
#    0.00 segundos
#    >>> tiempo('binomial3(27, 12)')
#    0.00 segundos
#
# >>> tiempo('binomial2(50000, 12)')
# 0.18 segundos
# >>> tiempo('binomial3(50000, 12)')
# 0.26 segundos

# Verificación
# ============

def test_binomial() -> None:
    assert binomial1(6, 3) == 20
    assert binomial1(5, 2) == 10
    assert binomial1(5, 3) == 10
    assert binomial2(6, 3) == 20
    assert binomial2(5, 2) == 10
    assert binomial2(5, 3) == 10
    assert binomial3(6, 3) == 20
    assert binomial3(5, 2) == 10
    assert binomial3(5, 3) == 10
    print("Verificado")

# La verificación es
#    >>> test_binomial()
#    Verificado
