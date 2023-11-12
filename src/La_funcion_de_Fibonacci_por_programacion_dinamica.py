# La_funcion_de_Fibonacci_por_programacion_dinamica.hs
# La función de Fibonacci por programación dinámica.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 14-septiembre-2023
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Los primeros términos de la sucesión de Fibonacci son
#    0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, ...
#
# Escribir dos definiciones (una recursiva y otra con programación
# dinámica) de la función
#    fib :: Integer -> Integer
# tal que (fib n) es el n-ésimo término de la sucesión de Fibonacci. Por
# ejemplo,
#    fib(6) == 8
#
# Comparar la eficiencia de las dos definiciones.
# ---------------------------------------------------------------------

from sys import setrecursionlimit
from timeit import Timer, default_timer

import numpy as np
import numpy.typing as npt

setrecursionlimit(10**6)

# 1ª definición (por recursión)
# =============================

def fib1(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib1(n - 1) + fib1(n - 2)

# 2ª definición (con programación dinámica)
# =========================================

def fib2(n: int) -> int:
    return vectorFib2(n)[n]

# (vectorFib2 n) es el vector con índices de 0 a n tal que el valor
# de la posición i es el i-ésimo número de Finonacci. Por ejemplo,
#    >>> vectorFib2(7)
#    [0, 1, 1, 2, 3, 5, 8, 13]
def vectorFib2(n: int) -> list[int]:
    v = [0] * (n + 1)
    v[0] = 0
    v[1] = 1
    for i in range(2, n + 1):
        v[i] = v[i - 1] + v[i - 2]
    return v

# 3ª definición (con programación dinámica y array)
# =================================================

def fib3(n: int) -> int:
    return vectorFib3(n)[n]

# (vectorFib3 n) es el vector con índices de 0 a n tal que el valor
# de la posición i es el i-ésimo número de Finonacci. Por ejemplo,
#    >>> vectorFib3(7)
#    array([ 0,  1,  1,  2,  3,  5,  8, 13])
def vectorFib3(n: int) -> npt.NDArray[np.int_]:
    v = np.zeros(n + 1, dtype=int)
    v[0] = 0
    v[1] = 1
    for i in range(2, n + 1):
        v[i] = v[i - 1] + v[i - 2]
    return v

# Comparación de eficiencia
# =========================

def tiempo(e: str) -> None:
    """Tiempo (en segundos) de evaluar la expresión e."""
    t = Timer(e, "", default_timer, globals()).timeit(1)
    print(f"{t:0.2f} segundos")

# La comparación es
#    >>> tiempo('fib1(34)')
#    2.10 segundos
#    >>> tiempo('fib2(34)')
#    0.00 segundos
#    >>> tiempo('fib3(34)')
#    0.00 segundos
#
#    >>> tiempo('fib2(100000)')
#    0.37 segundos
#    >>> tiempo('fib3(100000)')
#    0.08 segundos

# Verificación
# ============

def test_fib() -> None:
    assert fib1(6) == 8
    assert fib2(6) == 8
    assert fib3(6) == 8
    print("Verificado")

# La verificación es
#    >>> test_fib()
#    Verificado
