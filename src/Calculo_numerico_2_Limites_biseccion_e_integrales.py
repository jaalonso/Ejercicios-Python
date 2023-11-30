# Calculo_numerico_2_Limites_biseccion_e_integrales.py
# Cálculo numérico (2): Límites, bisección e integrales.
# Departamento de Ciencias de la Computación e I.A.
# Universidad de Sevilla
# =====================================================================

# ---------------------------------------------------------------------
# Introducción                                                       --
# ---------------------------------------------------------------------

# En esta relación se definen funciones para resolver los siguientes
# problemas de cálculo numérico:
# + Cálculo de límites.
# + Cálculo de los ceros de una función por el método de la bisección.
# + Cálculo de raíces enteras.
# + Cálculo de integrales por el método de los rectángulos.
# + Algoritmo de bajada para resolver un sistema triangular inferior.

# ---------------------------------------------------------------------
# Librerías auxiliares                                               --
# ---------------------------------------------------------------------

from itertools import count, takewhile
from math import cos, floor, log, pi
from sys import setrecursionlimit
from timeit import Timer, default_timer
from typing import Callable

from hypothesis import given
from hypothesis import strategies as st

setrecursionlimit(10**6)

# ---------------------------------------------------------------------
# Cálculo de límites                                                 --
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 1. Definir la función
#    limite : (Callable[[float], float], float) -> float
# tal que limite(f, a) es el valor de f en el primer término x tal que,
# para todo y entre x+1 y x+100, el valor absoluto de la diferencia
# entre f(y) y f(x) es menor que a. Por ejemplo,
#    limite(lambda n :  (2*n+1)/(n+5), 0.001) ==  1.9900110987791344
#    limite(lambda n : (1+1/n)**n, 0.001)     ==  2.714072874546881
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def limite(f: Callable[[float], float], a: float) -> float:
    x = 1
    while True:
        maximum_diff = max(abs(f(y) - f(x)) for y in range(x+1, x+101))
        if maximum_diff < a:
            return f(x)
        x += 1

# 2ª solución
# ===========

def limite2(f: Callable[[float], float], a: float) -> float:
    x = 1
    while True:
        y = f(x)
        if max(abs(y - f(x + i)) for i in range(1, 101)) < a:
            break
        x += 1
    return y

# 3ª solución
# ===========

def limite3(f: Callable[[float], float], a: float) -> float:
    for x in count(1):
        if max(abs(f(y) - f(x)) for y in range(x + 1, x + 101)) < a:
            r = f(x)
            break
    return r

# Verificación
# ============

def test_limite() -> None:
    assert limite(lambda n :  (2*n+1)/(n+5), 0.001) ==  1.9900110987791344
    assert limite(lambda n : (1+1/n)**n, 0.001)     ==  2.714072874546881
    assert limite2(lambda n :  (2*n+1)/(n+5), 0.001) ==  1.9900110987791344
    assert limite2(lambda n : (1+1/n)**n, 0.001)     ==  2.714072874546881
    assert limite3(lambda n :  (2*n+1)/(n+5), 0.001) ==  1.9900110987791344
    assert limite3(lambda n : (1+1/n)**n, 0.001)     ==  2.714072874546881
    print("Verificado")

# La comprobación es
#    >>> test_limite()
#    Verificado

# ---------------------------------------------------------------------
# Ceros de una función por el método de la bisección                 --
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 2. El método de bisección para calcular un cero de una
# función en el intervalo [a,b] se basa en el teorema de Bolzano:
#    "Si f(x) es una función continua en el intervalo [a, b], y si,
#    además, en los extremos del intervalo la función f(x) toma valores
#    de signo opuesto (f(a) * f(b) < 0), entonces existe al menos un
#    valor c en (a, b) para el que f(c) = 0".
#
# El método para calcular un cero de la función f en el intervalo [a,b]
# con un error menor que e consiste en tomar el punto medio del
# intervalo c = (a+b)/2 y considerar los siguientes casos:
# (*) Si |f(c)| < e, hemos encontrado una aproximación del punto que
#     anula f en el intervalo con un error aceptable.
# (*) Si f(c) tiene signo distinto de f(a), repetir el proceso en el
#     intervalo [a,c].
# (*) Si no, repetir el proceso en el intervalo [c,b].
#
# Definir la función
#    biseccion : (Callable[[float], float], float, float, float) -> float
# tal que biseccion(f, a, b, e) es una aproximación del punto del
# intervalo [a,b] en el que se anula la función f, con un error menor
# que e, calculada mediante el método de la bisección. Por ejemplo,
#    biseccion(lambda x : x**2 - 3, 0, 5, 0.01)        == 1.7333984375
#    biseccion(lambda x : x**3 - x - 2, 0, 4, 0.01)    == 1.521484375
#    biseccion(cos, 0, 2, 0.01)                        == 1.5625
#    biseccion(lambda x : log(50-x) - 4, -10, 3, 0.01) == -5.125
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def biseccion(f: Callable[[float], float],
              a: float,
              b: float,
              e: float) -> float:
    c = (a+b)/2
    if abs(f(c)) < e:
        return c
    if f(a) * f(c) < 0:
        return biseccion(f, a, c, e)
    return biseccion(f, c, b, e)

# 2ª solución
# ===========

def biseccion2(f: Callable[[float], float],
               a: float,
               b: float,
               e: float) -> float:
    def aux(a1: float,  b1: float) -> float:
        c = (a1+b1)/2
        if abs(f(c)) < e:
            return c
        if f(a1) * f(c) < 0:
            return aux(a1, c)
        return aux(c, b1)
    return aux(a, b)

# Verificación
# ============

def test_biseccion() -> None:
    assert biseccion(lambda x : x**2 - 3, 0, 5, 0.01) == 1.7333984375
    assert biseccion(lambda x : x**3 - x - 2, 0, 4, 0.01) == 1.521484375
    assert biseccion(cos, 0, 2, 0.01) == 1.5625
    assert biseccion(lambda x : log(50-x) - 4, -10, 3, 0.01) == -5.125
    assert biseccion2(lambda x : x**2 - 3, 0, 5, 0.01) == 1.7333984375
    assert biseccion2(lambda x : x**3 - x - 2, 0, 4, 0.01) == 1.521484375
    assert biseccion2(cos, 0, 2, 0.01) == 1.5625
    assert biseccion2(lambda x : log(50-x) - 4, -10, 3, 0.01) == -5.125
    print("Verificado")

# La comprobación es
#    >>> test_biseccion()
#    Verificado

# ---------------------------------------------------------------------
# Cálculo de raíces enteras                                          --
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 3.1. Definir la función
#    raizEnt : (int, int) -> int
# tal que raizEnt(x, n) es la raíz entera n-ésima de x; es decir, el
# mayor número entero y tal que y^n <= x. Por ejemplo,
#    raizEnt(8, 3)      ==  2
#    raizEnt(9, 3)      ==  2
#    raizEnt(26, 3)     ==  2
#    raizEnt(27, 3)     ==  3
#    raizEnt(10**50, 2) ==  10000000000000000000000000
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def raizEnt(x: int, n: int) -> int:
    return list(takewhile(lambda y : y ** n <= x, count(0)))[-1]

# 2ª solución
# ===========

def raizEnt2(x: int, n: int) -> int:
    return floor(x ** (1 / n))

# Nota. La solución anterior falla para números grandes. Por ejemplo,
#    >>> raizEnt2(10**50, 2) == 10 **25
#    False

# 3ª solución
# ===========

def raizEnt3(x: int, n: int) -> int:
    def aux(a: int, b: int) -> int:
        c = (a + b) // 2
        d = c ** n
        if d == x:
            return c
        if c == a:
            return c
        if d < x:
            return aux(c, b)
        return aux(a, c)
    return aux(1, x)

# Comparación de eficiencia
# =========================

def tiempo(e: str) -> None:
    """Tiempo (en segundos) de evaluar la expresión e."""
    t = Timer(e, "", default_timer, globals()).timeit(1)
    print(f"{t:0.2f} segundos")

# La comparación es
#    >>> tiempo('raizEnt(10**14, 2)')
#    2.71 segundos
#    >>> tiempo('raizEnt2(10**14, 2)')
#    0.00 segundos
#    >>> tiempo('raizEnt3(10**14, 2)')
#    0.00 segundos
#
#    >>> raizEnt2(10**50, 2)
#    10000000000000000905969664
#    >>> raizEnt3(10**50, 2)
#    10000000000000000000000000

# Verificación
# ============

def test_raizEnt() -> None:
    assert raizEnt(8, 3) == 2
    assert raizEnt(9, 3) == 2
    assert raizEnt(26, 3) == 2
    assert raizEnt(27, 3) == 3
    assert raizEnt2(8, 3) == 2
    assert raizEnt2(9, 3) == 2
    assert raizEnt2(26, 3) == 2
    assert raizEnt2(27, 3) == 3
    assert raizEnt3(8, 3) == 2
    assert raizEnt3(9, 3) == 2
    assert raizEnt3(26, 3) == 2
    assert raizEnt3(27, 3) == 3
    print("Verificado")

# La comprobación es
#    >>> test_raizEnt()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 3.2. Comprobar con Hypothesis que para todo número natural
# n, raizEnt(10**(2*n), 2) == 10**n
# ---------------------------------------------------------------------

# La propiedad es
@given(st.integers(min_value=0, max_value=1000))
def test_raizEntP(n: int) -> None:
    assert raizEnt3(10**(2*n), 2) == 10**n

# La comprobación es
#    >>> test_raizEntP()
#    >>>

# ---------------------------------------------------------------------
# Integración por el método de los rectángulos                       --
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 4. La integral definida de una función f entre los límites
# a y b puede calcularse mediante la regla del rectángulo
# (ver en http://bit.ly/1FDhZ1z) usando la fórmula
#    h * (f(a+h/2) + f(a+h+h/2) + f(a+2h+h/2) + ... + f(a+n*h+h/2))
# con a+n*h+h/2 <= b < a+(n+1)*h+h/2 y usando valores pequeños para h.
#
# Definir la función
#    integral : (float, float, Callable[[float], float], float) -> float
# tal que integral(a, b, f, h) es el valor de dicha expresión. Por
# ejemplo, el cálculo de la integral de f(x) = x^3 entre 0 y 1, con
# paso 0.01, es
#    integral(0, 1, lambda x : x**3, 0.01) == 0.24998750000000042
# Otros ejemplos son
#    integral(0, 1, lambda x : x**4, 0.01) == 0.19998333362500054
#    integral(0, 1, lambda x : 3*x**2 + 4*x**3, 0.01) == 1.9999250000000026
#    log(2) - integral(1, 2, lambda x : 1/x, 0.01) == 3.124931644782336e-6
#    pi - 4 * integral(0, 1, lambda x : 1/(x**2+1), 0.01) == -8.333333331389525e-6
# ---------------------------------------------------------------------

# 1ª solución
# ===========

# sucesion(x, y, s) es la lista
#    [a, s(a), s(s(a), ..., s(...(s(a))...)]
# hasta que s(s(...(s(a))...)) > b. Por ejemplo,
#    sucesion(3, 20, lambda x : x+2)  ==  [3,5,7,9,11,13,15,17,19]
def sucesion(a: float, b: float, s: Callable[[float], float]) -> list[float]:
    xs = []
    while a <= b:
        xs.append(a)
        a = s(a)
    return xs

# suma(a, b, s, f) es el valor de
#    f(a) + f(s(a)) + f(s(s(a)) + ... + f(s(...(s(a))...))
# hasta que s(s(...(s(a))...)) > b. Por ejemplo,
#    suma(2, 5, lambda x: x+1, lambda x: x**3)  ==  224
def suma(a: float,
         b: float,
         s: Callable[[float], float],
         f: Callable[[float], float]) -> float:
    return sum(f(x) for x in sucesion(a, b, s))

def integral(a: float,
             b: float,
             f: Callable[[float], float],
             h: float) -> float:
    return h * suma(a+h/2, b, lambda x: x+h, f)

# 2ª solución
# ===========

def integral2(a: float,
              b: float,
              f: Callable[[float], float],
              h: float) -> float:
    if a+h/2 > b:
        return 0
    return h * f(a+h/2) + integral2(a+h, b, f, h)

# 3ª solución
# ===========

def integral3(a: float,
              b: float,
              f: Callable[[float], float],
              h: float) -> float:
    def aux(x: float) -> float:
        if x+h/2 > b:
            return 0
        return h * f(x+h/2) + aux(x+h)
    return aux(a)

# Verificación
# ============

def test_integral() -> None:
    def aproximado(a: float, b: float) -> bool:
        return abs(a - b) < 0.00001
    assert integral(0, 1, lambda x : x**3, 0.01) == 0.24998750000000042
    assert integral(0, 1, lambda x : x**4, 0.01) == 0.19998333362500054
    assert integral(0, 1, lambda x : 3*x**2 + 4*x**3, 0.01) == 1.9999250000000026
    assert log(2) - integral(1, 2, lambda x : 1/x, 0.01) == 3.124931644782336e-6
    assert pi - 4 * integral(0, 1, lambda x : 1/(x**2+1), 0.01) == -8.333333331389525e-6
    assert aproximado(integral2(0, 1, lambda x : x**3, 0.01),
                      0.24998750000000042)
    assert aproximado(integral2(0, 1, lambda x : x**4, 0.01),
                      0.19998333362500054)
    assert aproximado(integral2(0, 1, lambda x : 3*x**2 + 4*x**3, 0.01),
                      1.9999250000000026)
    assert aproximado(log(2) - integral2(1, 2, lambda x : 1/x, 0.01),
                      3.124931644782336e-6)
    assert aproximado(pi - 4 * integral2(0, 1, lambda x : 1/(x**2+1), 0.01),
                      -8.333333331389525e-6)
    assert aproximado(integral3(0, 1, lambda x : x**3, 0.01),
                      0.24998750000000042)
    assert aproximado(integral3(0, 1, lambda x : x**4, 0.01),
                      0.19998333362500054)
    assert aproximado(integral3(0, 1, lambda x : 3*x**2 + 4*x**3, 0.01),
                      1.9999250000000026)
    assert aproximado(log(2) - integral3(1, 2, lambda x : 1/x, 0.01),
                      3.124931644782336e-6)
    assert aproximado(pi - 4 * integral3(0, 1, lambda x : 1/(x**2+1), 0.01),
                      -8.333333331389525e-6)
    print("Verificado")

# La verificación es
#    >>> test_integral()
#    Verificado

# ---------------------------------------------------------------------
# Algoritmo de bajada para resolver un sistema triangular inferior   --
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 5. Un sistema de ecuaciones lineales Ax = b es triangular
# inferior si todos los elementos de la matriz A que están por encima
# de la diagonal principal son nulos; es decir, es de la forma
#    a(1,1)*x(1)                                               = b(1)
#    a(2,1)*x(1) + a(2,2)*x(2)                                 = b(2)
#    a(3,1)*x(1) + a(3,2)*x(2) + a(3,3)*x(3)                   = b(3)
#    ...
#    a(n,1)*x(1) + a(n,2)*x(2) + a(n,3)*x(3) +...+ a(x,x)*x(n) = b(n)
#
# El sistema es compatible si, y sólo si, el producto de los elementos
# de la diagonal principal es distinto de cero. En este caso, la
# solución se puede calcular mediante el algoritmo de bajada:
#    x(1) = b(1) / a(1,1)
#    x(2) = (b(2) - a(2,1)*x(1)) / a(2,2)
#    x(3) = (b(3) - a(3,1)*x(1) - a(3,2)*x(2)) / a(3,3)
#    ...
#    x(n) = (b(n) - a(n,1)*x(1) - a(n,2)*x(2) -...- a(n,n-1)*x(n-1)) / a(n,n)
#
# Definir la función
#    bajada : (list[list[float]], list[list[float]]) -> list[list[float]]
# tal que bajada(a, b) es la solución, mediante el algoritmo de bajada,
# del sistema compatible triangular superior ax = b. Por ejemplo,
#    >>> bajada([[2,0,0],[3,1,0],[4,2,5.0]], [[3],[6.5],[10]])
#    [[1.5], [2.0], [0.0]]
# Es decir, la solución del sistema
#    2x            = 3
#    3x + y        = 6.5
#    4x + 2y + 5 z = 10
# es x=1.5, y=2 y z=0.
# ---------------------------------------------------------------------

def bajada(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    n = len(a)
    def x(k: int) -> float:
        return (b[k][0] - sum((a[k][j] * x(j) for j in range(0, k)))) / a[k][k]
    return [[x(i)] for i in range(0, n)]

# Verificación
# ============

def test_bajada() -> None:
    assert bajada([[2,0,0],[3,1,0],[4,2,5.0]], [[3],[6.5],[10]]) == \
        [[1.5], [2.0], [0.0]]
    print("Verificado")

# La verificación es
#    >>> test_bajada()
#    Verificado

# Verificación de todo
# ====================

# La comprobación es
#    > poetry run pytest Calculo_numerico_2_Limites_biseccion_e_integrales.py
#    ===== passed in 2.36s =====
