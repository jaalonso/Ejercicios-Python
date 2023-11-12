# Subsecuencia_comun_maxima.py
# Subsecuencia común_máxima
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 29-septiembre-2023
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Si a una secuencia X de elementos (pongamos por ejemplo, caracteres)
# le quitamos algunos de ellos y dejamos los que quedan en el orden en
# el que aparecían originalmente tenemos lo que se llama una
# subsecuencia de X. Por ejemplo, "aaoa" es una subsecuencia de la
# secuencia "amapola".
#
# El término también se aplica cuando quitamos todos los elementos (es
# decir, la secuencia vacía es siempre subsecuencia de cualquier
# secuencia) o cuando no quitamos ninguno (lo que significa que
# cualquier secuencia es siempre subsecuencia de sí misma).
#
# Dadas dos secuencias X e Y, decimos que Z es una subsecuencia común
# de X e Y si Z es subsecuencia de X y de Y. Por ejemplo, si X =
# "amapola" e Y = "matamoscas", la secuencia "aaoa" es una de las
# subsecuencias comunes de X e Y más larga, con longitud 4, ya que no
# hay ninguna subsecuencia común a X e Y de longitud mayor que
# 4. También son subsecuencias comunes de longitud 4 "maoa" o "amoa".
#
# Definir la función
#    scm : (str, str) -> str
# tal que scm(xs, ys) es una de las subsecuencias comunes de longitud
# máxima de xs e ys. Por ejemplo,
#    scm("amapola", "matamoscas") == "amoa"
#    scm("atamos", "matamoscas")  == "atamos"
#    scm("aaa", "bbbb")           == ""
# ---------------------------------------------------------------------

from sys import setrecursionlimit
from timeit import Timer, default_timer

setrecursionlimit(10**6)

# 1ª definición (por recursión)
# =============================

# (mayor xs ys) es la cadena más larga de xs e ys.
#    mayor "hola" "buenas"  ==  "buenas"
#    mayor "hola" "pera"    ==  "hola"
def mayor(xs: str, ys: str) -> str:
    if len(xs) >= len(ys):
        return xs
    return ys

def scm1(xs: str, ys: str) -> str:
    if not xs:
        return ""
    if not ys:
        return ""
    if xs[0] == ys[0]:
        return xs[0] + scm1(xs[1:], ys[1:])
    return mayor(scm1(xs, ys[1:]), scm1(xs[1:], ys))

# 2ª definición (con programación dinámica)
# =========================================

def scm2(xs: str, ys: str) -> str:
    n = len(xs)
    m = len(ys)
    return (matrizSCM2(xs, ys)[n][m])[::-1]

# matrizSCM2(xs, ys) es la matriz de orden (n+1)x(m+1) (donde n
# y m son los números de elementos de xs e ys, respectivamente) tal que
# el valor en la posición (i,j) es una SCM de los i primeros
# elementos de xs y los j primeros elementos de ys. Por ejemplo,
#    >>> matrizSCM2("amapola", "matamoscas")
#    [['', '', '', '', '', '', '', '', '', '', ''],
#     ['', '', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
#     ['', 'm', 'a', 'a', 'a', 'ma', 'ma', 'ma', 'ma', 'ma', 'ma'],
#     ['', 'm', 'am', 'am', 'aa', 'ma', 'ma', 'ma', 'ma', 'ama', 'ama'],
#     ['', 'm', 'am', 'am', 'aa', 'ma', 'ma', 'ma', 'ma', 'ama', 'ama'],
#     ['', 'm', 'am', 'am', 'aa', 'ma', 'oma', 'oma', 'oma', 'ama', 'ama'],
#     ['', 'm', 'am', 'am', 'aa', 'ma', 'oma', 'oma', 'oma', 'ama', 'ama'],
#     ['', 'm', 'am', 'am', 'aam', 'aam', 'oma', 'oma', 'oma', 'aoma', 'aoma']]
# Gráficamente,
#        m   a    t    a     m     o     s     c     a      s
#    ["","" ,""  ,""  ,""   ,""   ,""   ,""   ,""   ,""    ,"",
# a   "","" ,"a" ,"a" ,"a"  ,"a"  ,"a"  ,"a"  ,"a"  ,"a"   ,"a",
# m   "","m","a" ,"a" ,"a"  ,"ma" ,"ma" ,"ma" ,"ma" ,"ma"  ,"ma",
# a   "","m","am","am","aa" ,"ma" ,"ma" ,"ma" ,"ma" ,"ama" ,"ama",
# p   "","m","am","am","aa" ,"ma" ,"ma" ,"ma" ,"ma" ,"ama" ,"ama",
# o   "","m","am","am","aa" ,"ma" ,"oma","oma","oma","ama" ,"ama",
# l   "","m","am","am","aa" ,"ma" ,"oma","oma","oma","ama" ,"ama",
# a   "","m","am","am","aam","aam","oma","oma","oma","aoma","aoma"]
def matrizSCM2(xs: str, ys: str) -> list[list[str]]:
    n = len(xs)
    m = len(ys)
    q = [["" for _ in range(m + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if xs[i - 1] == ys[j - 1]:
                q[i][j] = xs[i - 1] + q[i - 1][j - 1]
            else:
                q[i][j] = mayor(q[i - 1][j], q[i][j - 1])
    return q

# # Comparación de eficiencia
# # =========================

def tiempo(e: str) -> None:
    """Tiempo (en segundos) de evaluar la expresión e."""
    t = Timer(e, "", default_timer, globals()).timeit(1)
    print(f"{t:0.2f} segundos")

# La comparación es
#    >>> tiempo('scm1(["1","3"]*9, ["2","3"]*9)')
#    8.44 segundos
#    >>> tiempo('scm2(["1","3"]*9, ["2","3"]*9)')
#    0.00 segundos

# Verificación
# ============

def test_scm() -> None:
    assert scm1("amapola", "matamoscas") == "amoa"
    assert scm1("atamos", "matamoscas")  == "atamos"
    assert scm1("aaa", "bbbb")           == ""
    assert scm2("amapola", "matamoscas") == "amoa"
    assert scm2("atamos", "matamoscas")  == "atamos"
    assert scm2("aaa", "bbbb")           == ""
    print("Verificado")

# La verificación es
#    >>> test_scm()
#    Verificado
