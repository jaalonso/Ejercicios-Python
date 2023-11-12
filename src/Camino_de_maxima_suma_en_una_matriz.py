# Camino_de_maxima_suma_en_una_matriz.py
# Camino de máxima suma en una matriz.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 24-octubre-2023
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Los caminos desde el extremo superior izquierdo (posición (1,1))
# hasta el extremo inferior derecho (posición (3,4)) en la matriz
#    (  1  6 11  2 )
#    (  7 12  3  8 )
#    (  3  8  4  9 )
# moviéndose en cada paso una casilla hacia la derecha o hacia abajo,
# son los siguientes:
#    [1,6,11,2,8,9]
#    [1,6,11,3,8,9]
#    [1,6,12,3,8,9]
#    [1,7,12,3,8,9]
#    [1,6,11,3,4,9]
#    [1,6,12,3,4,9]
#    [1,7,12,3,4,9]
#    [1,6,12,8,4,9]
#    [1,7,12,8,4,9]
#    [1,7, 3,8,4,9]
# La suma de los caminos son 37, 38, 39, 40, 34, 35, 36, 40, 41 y 32,
# respectivamente. El camino de máxima suma es el penúltimo (1, 7, 12, 8,
# 4, 9) que tiene una suma de 41.
#
# Definir la función
#    caminoMaxSuma : (list[list[int]]) -> list[int]
# tal que caminoMaxSuma(m) es un camino de máxima suma en la matriz m
# desde el extremo superior izquierdo hasta el extremo inferior derecho,
# moviéndose en cada paso una casilla hacia abajo o hacia la
# derecha. Por ejemplo,
#    >>> caminoMaxSuma1([[1,6,11,2],[7,12,3,8],[3,8,4,9]])
#    [1, 7, 12, 8, 4, 9]
#    >>> sum(caminoMaxSuma3([list(range(500*n+1, 500*(n+1)+1)) for n in range(500)]))
#    187001249
# ---------------------------------------------------------------------

from collections import defaultdict
from sys import setrecursionlimit
from timeit import Timer, default_timer

from src.Caminos_en_una_matriz import caminos1, caminos2

setrecursionlimit(10**6)

# 1ª definición de caminoMaxSuma (con caminos1)
# =============================================

def caminoMaxSuma1(m: list[list[int]]) -> list[int]:
    cs = caminos1(m)
    k = max((sum(c) for c in cs))
    return [c for c in cs if sum(c) == k][0]

# Se usa la función caminos1 del ejercicio
# "Caminos en una matriz" que se encuentra en
# https://bit.ly/45bYoYE

# 2ª definición de caminoMaxSuma (con caminos2)
# =============================================

def caminoMaxSuma2(m: list[list[int]]) -> list[int]:
    cs = caminos2(m)
    k = max((sum(c) for c in cs))
    return [c for c in cs if sum(c) == k][0]

# Se usa la función caminos2 del ejercicio
# "Caminos en una matriz" que se encuentra en
# https://bit.ly/45bYoYE

# 3ª definición de caminoMaxSuma (con programación dinámica)
# ==========================================================

def caminoMaxSuma3(m: list[list[int]]) -> list[int]:
    nf = len(m)
    nc = len(m[0])
    return list(reversed(diccionarioCaminoMaxSuma(m)[(nf, nc)][1]))

# diccionarioCaminoMaxSuma(p) es el diccionario cuyas claves son los
# puntos de la matriz p y sus valores son los pares formados por la
# máxima suma de los caminos hasta dicho punto y uno de los caminos con
# esa suma. Por ejemplo,
#    >>> diccionarioCaminoMaxSuma([[1,6,11,2],[7,12,3,8],[3,8,4,9]])
#    {(1, 1): (1, [1]),
#     (1, 2): (7, [6, 1]),
#     (1, 3): (18, [11, 6, 1]),
#     (1, 4): (20, [2, 11, 6, 1]),
#     (2, 1): (8, [7, 1]),
#     (3, 1): (11, [3, 7, 1]),
#     (2, 2): (20, [12, 7, 1]),
#     (2, 3): (23, [3, 12, 7, 1]),
#     (2, 4): (31, [8, 3, 12, 7, 1]),
#     (3, 2): (28, [8, 12, 7, 1]),
#     (3, 3): (32, [4, 8, 12, 7, 1]),
#     (3, 4): (41, [9, 4, 8, 12, 7, 1])}
def diccionarioCaminoMaxSuma(p: list[list[int]]) -> dict[tuple[int, int], tuple[int, list[int]]]:
    m = len(p)
    n = len(p[0])
    q: dict[tuple[int, int], tuple[int, list[int]]] = {}
    q[(1, 1)] = (p[0][0], [p[0][0]])
    for j in range(2, n + 1):
        (k, xs) = q[(1, j-1)]
        q[(1, j)] = (k + p[0][j-1], [p[0][j-1]] + xs)
    for i in range(2, m + 1):
        (k,xs) = q[(i-1,1)]
        q[(i, 1)] =  (k + p[i-1][0], [p[i-1][0]] + xs)
    for i in range(2, m + 1):
        for j in range(2, n + 1):
            (k1,xs) = q[(i,j-1)]
            (k2,ys) = q[(i-1,j)]
            if k1 > k2:
                q[(i,j)] = (k1 + p[i-1][j-1], [p[i-1][j-1]] + xs)
            else:
                q[(i,j)] = (k2 + p[i-1][j-1], [p[i-1][j-1]] + ys)
    return q

# Comparación de eficiencia
# =========================

def tiempo(e: str) -> None:
    """Tiempo (en segundos) de evaluar la expresión e."""
    t = Timer(e, "", default_timer, globals()).timeit(1)
    print(f"{t:0.2f} segundos")

# La comparación es
#    >>> tiempo('caminoMaxSuma1([list(range(11*n+1, 11*(n+1)+1)) for n in range(12)])')
#    1.92 segundos
#    >>> tiempo('caminoMaxSuma2([list(range(11*n+1, 11*(n+1)+1)) for n in range(12)])')
#    0.65 segundos
#    >>> tiempo('caminoMaxSuma3([list(range(11*n+1, 11*(n+1)+1)) for n in range(12)])')
#    0.00 segundos

# Verificación
# ============

def test_caminoMaxSuma() -> None:
    assert caminoMaxSuma1([[1,6,11,2],[7,12,3,8],[3,8,4,9]]) == \
        [1, 7, 12, 8, 4, 9]
    assert caminoMaxSuma2([[1,6,11,2],[7,12,3,8],[3,8,4,9]]) == \
        [1, 7, 12, 8, 4, 9]
    assert caminoMaxSuma3([[1,6,11,2],[7,12,3,8],[3,8,4,9]]) == \
        [1, 7, 12, 8, 4, 9]
    print("Verificado")

# La verificación es
#    >>> test_caminoMaxSuma()
#    Verificado
