# Caminos_en_una_matriz.py
# Caminos en una matriz (con programación dinámica)
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 14-octubre-2023
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Los caminos desde el extremo superior izquierdo (posición (1,1))
# hasta el extremo inferior derecho (posición (3,4)) en la matriz
#    (  1  6 11  2 )
#    (  7 12  3  8 )
#    (  3  8  4  9 )
# moviéndose en cada paso una casilla hacia la derecha o abajo, son los
# siguientes:
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
#
# Definir la función
#    caminos : (list[list[int]]) -> list[list[int]]
# tal que caminos (m) es la lista de los caminos en la matriz m desde
# el extremo superior izquierdo hasta el extremo inferior derecho,
# moviéndose en cada paso una casilla hacia abajo o hacia la
# derecha. Por ejemplo,
#    >>> caminos([[1,6,11,2],[7,12,3,8],[3,8,4,9]])
#    [[1, 6, 11, 2, 8, 9],
#     [1, 6, 11, 3, 8, 9],
#     [1, 6, 12, 3, 8, 9],
#     [1, 7, 12, 3, 8, 9],
#     [1, 6, 11, 3, 4, 9],
#     [1, 6, 12, 3, 4, 9],
#     [1, 7, 12, 3, 4, 9],
#     [1, 6, 12, 8, 4, 9],
#     [1, 7, 12, 8, 4, 9],
#     [1, 7,  3, 8, 4, 9]]
#    >>> len(caminos([list(range(12*n+1, 12*(n+1)+1)) for n in range(12)]))
#    705432
# ---------------------------------------------------------------------

from collections import defaultdict
from sys import setrecursionlimit
from timeit import Timer, default_timer

setrecursionlimit(10**6)

# 1ª definición (por recursión)
# =============================

def caminos1(m: list[list[int]]) -> list[list[int]]:
    nf = len(m)
    nc = len(m[0])
    return list(reversed([list(reversed(xs)) for xs in caminos1Aux(m, (nf,nc))]))

# caminos1Aux(m, p) es la lista de los caminos invertidos en la matriz m
# desde la posición (1,1) hasta la posición p. Por ejemplo,
def caminos1Aux(m: list[list[int]], p: tuple[int, int]) -> list[list[int]]:
    (i, j) = p
    if p == (1,1):
        return [[m[0][0]]]
    if i == 1:
        return [[m[0][k-1] for k in range(j, 0, -1)]]
    if j == 1:
        return [[m[k-1][0] for k in range(i, 0, -1)]]
    return [[m[i-1][j-1]] + xs
            for xs in caminos1Aux(m, (i,j-1)) + caminos1Aux(m, (i-1,j))]

# 2ª solución (mediante programación dinámica)
# ============================================

def caminos2(p: list[list[int]]) -> list[list[int]]:
    m = len(p)
    n = len(p[0])
    return [list(reversed(xs)) for xs in diccionarioCaminos(p)[(m, n)]]

# diccionarioCaminos(p) es el diccionario cuyas claves son los
# puntos de la matriz p y sus valores son los caminos a dichos
# puntos. Por ejemplo,
#    >>> diccionarioCaminos([[1,6,11,2],[7,12,3,8],[3,8,4,9]])
#    defaultdict(<class 'list'>,
#                {(1, 1): [[1]],
#                 (1, 2): [[6, 1]],
#                 (1, 3): [[11, 6, 1]],
#                 (1, 4): [[2, 11, 6, 1]],
#                 (2, 1): [[7, 1]],
#                 (2, 2): [[12, 6, 1], [12, 7, 1]],
#                 (2, 3): [[3, 11, 6, 1], [3, 12, 6, 1], [3, 12, 7, 1]],
#                 (2, 4): [[8, 2, 11, 6, 1], [8, 3, 11, 6, 1],
#                          [8, 3, 12, 6, 1], [8, 3, 12, 7, 1]],
#                 (3, 1): [[3, 7, 1]],
#                 (3, 2): [[8, 12, 6, 1], [8, 12, 7, 1], [8, 3, 7, 1]],
#                 (3, 3): [[4, 3, 11, 6, 1], [4, 3, 12, 6, 1],
#                          [4, 3, 12, 7, 1], [4, 8, 12, 6, 1],
#                          [4, 8, 12, 7, 1], [4, 8, 3, 7, 1]],
#                 (3, 4): [[9, 8, 2, 11, 6, 1], [9, 8, 3, 11, 6, 1],
#                          [9, 8, 3, 12, 6, 1], [9, 8, 3, 12, 7, 1],
#                          [9, 4, 3, 11, 6, 1], [9, 4, 3, 12, 6, 1],
#                          [9, 4, 3, 12, 7, 1], [9, 4, 8, 12, 6, 1],
#                          [9, 4, 8, 12, 7, 1], [9, 4, 8, 3, 7, 1]]})
def diccionarioCaminos(p: list[list[int]]) -> dict[tuple[int, int], list[list[int]]]:
    m = len(p)
    n = len(p[0])
    q = defaultdict(list)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if i == 1:
                q[(i, j)] = [[p[0][z-1] for z in range(j, 0, -1)]]
            elif j == 1:
                q[(i, j)] = [[p[z-1][0] for z in range(i, 0, -1)]]
            else:
                q[(i, j)] = [[p[i-1][j-1]] + cs for cs in q[(i-1, j)] + q[(i, j-1)]]
    return q

# Comparación de eficiencia
# =========================

def tiempo(e: str) -> None:
    """Tiempo (en segundos) de evaluar la expresión e."""
    t = Timer(e, "", default_timer, globals()).timeit(1)
    print(f"{t:0.2f} segundos")

# La comparación es
#    >>> tiempo('caminos1([list(range(11*n+1, 11*(n+1)+1)) for n in range(12)])')
#    2.20 segundos
#    >>> tiempo('caminos2([list(range(11*n+1, 11*(n+1)+1)) for n in range(12)])')
#    0.64 segundos

# Verificación
# ============

def test_caminos() -> None:
    r = [[1, 6, 11, 2, 8, 9],
         [1, 6, 11, 3, 8, 9],
         [1, 6, 12, 3, 8, 9],
         [1, 7, 12, 3, 8, 9],
         [1, 6, 11, 3, 4, 9],
         [1, 6, 12, 3, 4, 9],
         [1, 7, 12, 3, 4, 9],
         [1, 6, 12, 8, 4, 9],
         [1, 7, 12, 8, 4, 9],
         [1, 7,  3, 8, 4, 9]]
    assert caminos1([[1,6,11,2],[7,12,3,8],[3,8,4,9]]) == r
    assert caminos2([[1,6,11,2],[7,12,3,8],[3,8,4,9]]) == r
    print("Verificado")

# La verificación es
#    >>> test_caminos()
#    Verificado
