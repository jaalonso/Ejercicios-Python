# Levenshtein.py
# La distancia Levenshtein (con programación dinámica)
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 4-octubre-2023
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# La distancia de Levenshtein (o distancia de edición) es el número
# mínimo de operaciones requeridas para transformar una cadena de
# caracteres en otra. Las operaciones de edición que se pueden hacer
# son:
# + insertar un carácter (por ejemplo, de "abc" a "abca")
# + eliminar un carácter (por ejemplo, de "abc" a "ac")
# + sustituir un carácter (por ejemplo, de "abc" a "adc")
#
# Por ejemplo, la distancia de Levenshtein entre "casa" y "calle" es de
# 3 porque se necesitan al menos tres ediciones elementales para
# cambiar uno en el otro:
#    "casa"  --> "cala"  (sustitución de 's' por 'l')
#    "cala"  --> "calla" (inserción de 'l' entre 'l' y 'a')
#    "calla" --> "calle" (sustitución de 'a' por 'e')
#
# Definir la función
#    levenshtein : (str, str) -> int
# tal que levenshtein(xs, ys) es la distancia de Levenshtein entre xs e
# ys. Por ejemplo,
#    levenshtein("casa",  "calle")     ==  3
#    levenshtein("calle", "casa")      ==  3
#    levenshtein("casa",  "casa")      ==  0
#    levenshtein("ana",   "maria")     ==  3
#    levenshtein("agua",  "manantial") ==  7
# ---------------------------------------------------------------------

from sys import setrecursionlimit
from timeit import Timer, default_timer

setrecursionlimit(10**6)

# 1ª definición (por recursión)
# =============================

def levenshtein1(xs: str, ys: str) -> int:
    if not xs:
        return len(ys)
    if not ys:
        return len(xs)
    if xs[0] == ys[0]:
        return levenshtein1(xs[1:], ys[1:])
    return 1 + min([levenshtein1(xs[1:], ys),
                    levenshtein1(xs, ys[1:]),
                    levenshtein1(xs[1:], ys[1:])])


# 2ª definición (con programación dinámica)
# =========================================

# matrizLevenshtein(xs, ys) es la matriz cuyo número de filas es la
# longitud de xs, cuyo número de columnas es la longitud de ys y en
# valor en la posición (i,j) es la distancia de Levenshtein entre los
# primeros i caracteres de xs y los j primeros caracteres de ys. Por
# ejemplo,
#    >>> matrizLevenshtein("casa", "calle")
#    [[0, 1, 2, 3, 4, 5],
#     [1, 0, 1, 2, 3, 4],
#     [2, 1, 0, 1, 2, 3],
#     [3, 2, 1, 1, 2, 3],
#     [4, 3, 2, 2, 2, 3]]
# Gráficamente,
#       c a l l e
#     0,1,2,3,4,5,
#  c  1,0,1,2,3,4,
#  a  2,1,0,1,2,3,
#  s  3,2,1,1,2,3,
#  a  4,3,2,2,2,3
def matrizLevenshtein(xs: str, ys: str) -> list[list[int]]:
    n = len(xs)
    m = len(ys)
    q = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    for i in range(n + 1):
        q[i][0] = i
    for j in range(m + 1):
        q[0][j] = j
    for i in range(1,n + 1):
        for j in range(1, m + 1):
            if xs[i - 1] == ys[j - 1]:
                q[i][j] = q[i - 1][j - 1]
            else:
                q[i][j] = 1 + min([q[i-1][j],  q[i][j-1], q[i-1][j-1]])
    return q

def levenshtein2(xs: str, ys: str) -> int:
    m = len(xs)
    n = len(ys)
    return matrizLevenshtein(xs, ys)[m][n]

# Comparación de eficiencia
# =========================

def tiempo(e: str) -> None:
    """Tiempo (en segundos) de evaluar la expresión e."""
    t = Timer(e, "", default_timer, globals()).timeit(1)
    print(f"{t:0.2f} segundos")

# La comparación es
#    >>> tiempo('levenshtein1(str(2**33), str(3**33))')
#    13.78 segundos
#    >>> tiempo('levenshtein2(str(2**33), str(3**33))')
#    0.00 segundos

# Verificación
# ============

def test_levenshtein() -> None:
    assert levenshtein1("casa",  "calle")     ==  3
    assert levenshtein1("calle", "casa")      ==  3
    assert levenshtein1("casa",  "casa")      ==  0
    assert levenshtein1("ana",   "maria")     ==  3
    assert levenshtein1("agua",  "manantial") ==  7
    assert levenshtein2("casa",  "calle")     ==  3
    assert levenshtein2("calle", "casa")      ==  3
    assert levenshtein2("casa",  "casa")      ==  0
    assert levenshtein2("ana",   "maria")     ==  3
    assert levenshtein2("agua",  "manantial") ==  7
    print("Verificado")
