# Programacion_dinamica_Caminos_en_una_reticula.py
# Caminos en una retícula (con programación dinámica)
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 9-octubre-2023
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Se considera una retícula con sus posiciones numeradas, desde el
# vértice superior izquierdo, hacia la derecha y hacia abajo. Por
# ejemplo, la retícula de dimensión 3x4 se numera como sigue:
#    |-------+-------+-------+-------|
#    | (1,1) | (1,2) | (1,3) | (1,4) |
#    | (2,1) | (2,2) | (2,3) | (2,4) |
#    | (3,1) | (3,2) | (3,3) | (3,4) |
#    |-------+-------+-------+-------|
#
# Definir la función
#    caminos : (tuple[int, int]) -> list[list[tuple[int, int]]]
# tal que caminos((m,n)) es la lista de los caminos en la retícula de
# dimensión mxn desde (1,1) hasta (m,n). Por ejemplo,
#    >>> caminos((2,3))
#    [[(1, 1), (1, 2), (1, 3), (2, 3)],
#     [(1, 1), (1, 2), (2, 2), (2, 3)],
#     [(1, 1), (2, 1), (2, 2), (2, 3)]]
#    >>> for c in caminos1((3,4)):
#    ...     print(c)
#    ...
#    [(1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4)]
#    [(1, 1), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
#    [(1, 1), (1, 2), (2, 2), (2, 3), (2, 4), (3, 4)]
#    [(1, 1), (2, 1), (2, 2), (2, 3), (2, 4), (3, 4)]
#    [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4)]
#    [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (3, 4)]
#    [(1, 1), (2, 1), (2, 2), (2, 3), (3, 3), (3, 4)]
#    [(1, 1), (1, 2), (2, 2), (3, 2), (3, 3), (3, 4)]
#    [(1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (3, 4)]
#    [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (3, 4)]
# ---------------------------------------------------------------------

from collections import defaultdict
from sys import setrecursionlimit
from timeit import Timer, default_timer

setrecursionlimit(10**6)

# 1ª solución (por recursión)
# ===========================

def caminos1(p: tuple[int, int]) -> list[list[tuple[int, int]]]:
    def aux(p: tuple[int, int]) -> list[list[tuple[int, int]]]:
        (x, y) = p
        if x == 1:
            return [[(1,z) for z in range(y, 0, -1)]]
        if y == 1:
            return [[(z,1) for z in range(x, 0, -1)]]
        return [[(x,y)] + cs for cs in aux((x-1,y)) + aux((x,y-1))]

    return [list(reversed(ps)) for ps in aux(p)]

# 2ª solución (con programación dinámica)
# =======================================

def caminos2(p: tuple[int, int]) -> list[list[tuple[int, int]]]:
    return [list(reversed(ps)) for ps in diccionarioCaminos(p)[p]]

# diccionarioCaminos((m,n)) es el diccionario cuyas claves son los
# puntos de la retícula mxn y sus valores son los caminos a dichos
# puntos. Por ejemplo,
#    >>> diccionarioCaminos((2,3))
#    defaultdict(<class 'list'>,
#                {(1,1): [[(1,1)]],
#                 (1,2): [[(1,2),(1,1)]],
#                 (1,3): [[(1,3),(1,2),(1,1)]],
#                 (2,1): [[(2,1),(1,1)]],
#                 (2,2): [[(2,2),(1,2),(1,1)],
#                         [(2,2),(2,1),(1,1)]],
#                 (2,3): [[(2,3),(1,3),(1,2),(1,1)],
#                         [(2,3),(2,2),(1,2),(1,1)],
#                         [(2,3),(2,2),(2,1),(1,1)]]})
def diccionarioCaminos(p: tuple[int, int]) -> dict[tuple[int, int], list[list[tuple[int, int]]]]:
    m, n = p
    q = defaultdict(list)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if i == 1:
                q[(i, j)] = [[(1, z) for z in range(j, 0, -1)]]
            elif j == 1:
                q[(i, j)] = [[(z, 1) for z in range(i, 0, -1)]]
            else:
                q[(i, j)] = [[(i, j)] + cs for cs in q[(i-1, j)] + q[(i, j-1)]]
    return q

# Comparación de eficiencia
# =========================

def tiempo(e: str) -> None:
    """Tiempo (en segundos) de evaluar la expresión e."""
    t = Timer(e, "", default_timer, globals()).timeit(1)
    print(f"{t:0.2f} segundos")

# La comparación es
#    >>> tiempo('max(caminos1((13,13))[0])')
#    26.75 segundos
#    >>> tiempo('max(caminos2((13,13))[0])')
#    7.40 segundos

# Verificación
# ============

def test_caminos() -> None:
    assert caminos1((2,3)) == \
        [[(1,1),(1,2),(1,3),(2,3)],
         [(1,1),(1,2),(2,2),(2,3)],
         [(1,1),(2,1),(2,2),(2,3)]]
    assert caminos2((2,3)) == \
        [[(1,1),(1,2),(1,3),(2,3)],
         [(1,1),(1,2),(2,2),(2,3)],
         [(1,1),(2,1),(2,2),(2,3)]]
    print("Verificado")

# La verificación es
#    >>> test_caminos()
#    Verificado
