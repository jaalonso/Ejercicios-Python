# Longitud_SCM.py
# Longitud de la subsecuencia común máxima.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 24-septiembre-2023
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
# Se desea encontrar la longitud de las subsecuencias comunes más
# largas de dos secuencias de caracteres dadas.
#
# Definir la función
#    longitudSCM : (str, str) -> int
# tal que longitudSCM(xs, ys) es la longitud de la subsecuencia máxima
# de xs e ys. Por ejemplo,
#    longitudSCM("amapola", "matamoscas") == 4
#    longitudSCM("atamos", "matamoscas")  == 6
#    longitudSCM("aaa", "bbbb")           == 0
# ---------------------------------------------------------------------

from timeit import Timer, default_timer

# 1ª definición (por recursión)
# =============================

def longitudSCM1(xs: str, ys: str) -> int:
    if not xs:
        return 0
    if not ys:
        return 0
    if xs[0] == ys[0]:
        return 1 + longitudSCM1(xs[1:], ys[1:])
    return max(longitudSCM1(xs, ys[1:]), longitudSCM1(xs[1:], ys))

# 2ª definición (con programación dinámica)
# =========================================

# matrizLongitudSCM2(xs, ys) es la matriz de orden (n+1)x(m+1) (donde n
# y m son los números de elementos de xs e ys, respectivamente) tal que
# el valor en la posición (i,j) es la longitud de la SCM de los i
# primeros elementos de xs y los j primeros elementos de ys. Por ejemplo,
#    >>> matrizLongitudSCM2("amapola", "matamoscas")
#    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
#     [0, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3],
#     [0, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3],
#     [0, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3],
#     [0, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3],
#     [0, 1, 2, 2, 3, 3, 3, 3, 3, 4, 4]]
# Gráficamente,
#       m a t a m o s c a s
#    [0,0,0,0,0,0,0,0,0,0,0,
# a   0,0,1,1,1,1,1,1,1,1,1,
# m   0,1,1,1,1,2,2,2,2,2,2,
# a   0,1,2,2,2,2,2,2,2,3,3,
# p   0,1,2,2,2,2,2,2,2,3,3,
# o   0,1,2,2,2,2,3,3,3,3,3,
# l   0,1,2,2,2,2,3,3,3,3,3,
# a   0,1,2,2,3,3,3,3,3,4,4]
def matrizLongitudSCM2(xs: str, ys: str) -> list[list[int]]:
    n = len(xs)
    m = len(ys)
    q = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if xs[i - 1] == ys[j - 1]:
                q[i][j] = 1 + q[i - 1][j - 1]
            else:
                q[i][j] = max(q[i - 1][j], q[i][j - 1])
    return q

def longitudSCM2(xs: str, ys: str) -> int:
    n = len(xs)
    m = len(ys)
    return matrizLongitudSCM2(xs, ys)[n][m]

# Comparación de eficiencia
# =========================

def tiempo(e: str) -> None:
    """Tiempo (en segundos) de evaluar la expresión e."""
    t = Timer(e, "", default_timer, globals()).timeit(1)
    print(f"{t:0.2f} segundos")

# La comparación es
#    >>> tiempo('longitudSCM1([1,3]*9, [2,3]*9)')
#    8.04 segundos
#    >>> tiempo('longitudSCM2([1,3]*9, [2,3]*9)')
#    0.00 segundos

# Verificación
# ============

def test_longitudSCM() -> None:
    assert longitudSCM1("amapola", "matamoscas") == 4
    assert longitudSCM1("atamos", "matamoscas")  == 6
    assert longitudSCM1("aaa", "bbbb")           == 0
    assert longitudSCM2("amapola", "matamoscas") == 4
    assert longitudSCM2("atamos", "matamoscas")  == 6
    assert longitudSCM2("aaa", "bbbb")           == 0
    print("Verificado")

# La verificación es
#    >>> test_longitudSCM()
#    Verificado
