# definiciones_por_comprension.py
# Definiciones por comprensión.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 7-septiembre-2022
# ======================================================================

# ---------------------------------------------------------------------
# Introducción                                                       --
# ---------------------------------------------------------------------

# En esta relación se presentan ejercicios con definiciones por
# comprensión correspondientes al tema 5 que se encuentra en
#    https://jaalonso.github.io/cursos/i1m/temas/tema-5.html

# ---------------------------------------------------------------------
# Librerías auxiliares                                             --
# ---------------------------------------------------------------------

from itertools import islice
from math import ceil, e, pi, sin, sqrt, trunc
from sys import setrecursionlimit
from timeit import Timer, default_timer
from typing import Iterator, TypeVar

from hypothesis import given
from hypothesis import strategies as st

A = TypeVar('A')
setrecursionlimit(10**6)

# ---------------------------------------------------------------------
# Ejercicio 1.1. (Problema 6 del proyecto Euler) En los distintos
# apartados de este ejercicio se definen funciones para resolver el
# problema 6 del proyecto Euler https://www.projecteuler.net/problem=6
#
# Definir, por comprensión, la función
#    suma : (int) -> int
# tal suma(n) es la suma de los n primeros números. Por ejemplo,
#    suma(3)  ==  6
#    len(str(suma2(10**100)))  ==  200
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def suma1(n: int) -> int:
    return sum(range(1, n + 1))

# 2ª solución
# ===========

def suma2(n: int) -> int:
    return (1 + n) * n // 2

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.integers(min_value=1, max_value=1000))
def test_suma(n: int) -> None:
    assert suma1(n) == suma2(n)

# La comprobación se hace al final.

# Comparación de eficiencia
# =========================

def tiempo(ex: str) -> None:
    """Tiempo (en segundos) de evaluar la expresión e."""
    t = Timer(ex, "", default_timer, globals()).timeit(1)
    print(f"{t:0.2f} segundos")

# La comparación es
#    >>> tiempo('suma1(10**8)')
#    1.55 segundos
#    >>> tiempo('suma2(10**8)')
#    0.00 segundos

# ---------------------------------------------------------------------
# Ejercicio 1.2. Definir, por comprensión, la función
#    sumaDeCuadrados : (int) -> int
# tal sumaDeCuadrados(n) es la suma de los xuadrados de los n primeros
# números naturales. Por ejemplo,
#    sumaDeCuadrados(3)   ==  14
#    sumaDeCuadrados(100) ==  338350
#    len(str(sumaDeCuadrados2(10**100)))  ==  300
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def sumaDeCuadrados1(n: int) -> int:
    return sum(x**2 for x in range(1, n + 1))

# 2ª solución
# ===========

def sumaDeCuadrados2(n: int) -> int:
    return n * (n + 1) * (2 * n + 1) // 6

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.integers(min_value=1, max_value=1000))
def test_sumaDeCuadrados(n: int) -> None:
    assert sumaDeCuadrados1(n) == sumaDeCuadrados2(n)

# La comprobación está al final.

# Comparación de eficiencia
# =========================

# La comparación es
#    >>> tiempo('sumaDeCuadrados1(10**7)')
#    2.19 segundos
#    >>> tiempo('sumaDeCuadrados2(10**7)')
#    0.00 segundos

# ---------------------------------------------------------------------
# Ejercicio 1.3. Definir la función
#    euler6 : (int) -> int
# tal que euler6(n) es la diferencia entre el cuadrado de la suma
# de los n primeros números y la suma de los cuadrados de los n
# primeros números. Por ejemplo,
#    euler6(10)       ==  2640
#    euler6(10^10)  ==  2500000000166666666641666666665000000000
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def euler6a(n: int) -> int:
    return suma1(n)**2 - sumaDeCuadrados1(n)

# 2ª solución
# ===========

def euler6b(n: int) -> int:
    return suma2(n)**2 - sumaDeCuadrados2(n)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.integers(min_value=1, max_value=1000))
def test_euler6(n: int) -> None:
    assert euler6a(n) == euler6b(n)

# La comprobación está al final

# Comparación de eficiencia
# =========================

# La comparación es
#    >>> tiempo('euler6a(10**7)')
#    2.26 segundos
#    >>> tiempo('euler6b(10**7)')
#    0.00 segundos

# ---------------------------------------------------------------------
# Ejercicio 2. Definir, por comprensión, la función
#    replica : (int, A) -> list[A]
# tal que replica(n, x) es la lista formada por n copias del elemento
# x. Por ejemplo,
#    replica(4, 7)     ==  [7,7,7,7]
#    replica(3, True)  ==  [True, True, True]
# ---------------------------------------------------------------------

def replica(n: int, x: A) -> list[A]:
    return [x for _ in range(0, n)]

# ---------------------------------------------------------------------
# Ejercicio 3.1. Los triángulos aritméticos se forman como sigue
#     1
#     2  3
#     4  5  6
#     7  8  9 10
#    11 12 13 14 15
#    16 17 18 19 20 21
#
# Definir la función
#    linea : (int) -> list[int]
# tal que linea(n) es la línea n-ésima de los triángulos
# aritméticos. Por ejemplo,
#    linea(4)  ==  [7, 8, 9, 10]
#    linea(5)  ==  [11, 12, 13, 14, 15]
#    linea(10**8)[0] == 4999999950000001
# ---------------------------------------------------------------------

# 1ª definición
# =============

def linea1(n: int) -> list[int]:
    return list(range(suma1(n - 1) + 1, suma1(n) + 1))

# 2ª definición
# =============

def linea2(n: int) -> list[int]:
    s = suma1(n-1)
    return list(range(s + 1, s + n + 1))

# 3ª definición
# =============

def linea3(n: int) -> list[int]:
    s = suma2(n-1)
    return list(range(s + 1, s + n + 1))

# Comprobación de equivalencia
# ============================

@given(st.integers(min_value=1, max_value=1000))
def test_linea(n: int) -> None:
    r = linea1(n)
    assert linea2(n) == r
    assert linea3(n) == r

# La comprobación está al final

# Comparación de eficiencia
# =========================

# La comparación es
#    >>> tiempo('linea1(10**7)')
#    0.53 segundos
#    >>> tiempo('linea2(10**7)')
#    0.40 segundos
#    >>> tiempo('linea3(10**7)')
#    0.29 segundos

# ---------------------------------------------------------------------
# Ejercicio 3.2. Definir la función
#    triangulo : (int) -> list[list[int]]
# tale que triangulo(n) es el triángulo aritmético de altura n. Por
# ejemplo,
#    triangulo(3)  ==  [[1], [2, 3], [4, 5, 6]]
#    triangulo(4)  ==  [[1], [2, 3], [4, 5, 6], [7, 8, 9, 10]]
# ---------------------------------------------------------------------

# 1ª definición
# =============

def triangulo1(n: int) -> list[list[int]]:
    return [linea1(m) for m in range(1, n + 1)]

# 2ª definición
# =============

def triangulo2(n: int) -> list[list[int]]:
    return [linea2(m) for m in range(1, n + 1)]

# 3ª definición
# =============

def triangulo3(n: int) -> list[list[int]]:
    return [linea3(m) for m in range(1, n + 1)]

# Comprobación de equivalencia
# ============================

@given(st.integers(min_value=1, max_value=1000))
def test_triangulo(n: int) -> None:
    r = triangulo1(n)
    assert triangulo2(n) == r
    assert triangulo3(n) == r

# La comprobación está al final.

# Comparación de eficiencia
# =========================

# La comparación es
#    >>> tiempo('triangulo1(10**4)')
#    2.58 segundos
#    >>> tiempo('triangulo2(10**4)')
#    1.91 segundos
#    >>> tiempo('triangulo3(10**4)')
#    1.26 segundos

# ---------------------------------------------------------------------
# Ejercicio 4. Un números entero positivo es perfecto si es igual a la
# suma de sus divisores, excluyendo el propio número. Por ejemplo, 6 es
# un número perfecto porque sus divisores propios son 1, 2 y 3; y
# 6 = 1 + 2 + 3.
#
# Definir, por comprensión, la función
#    perfectos (int) -> list[int]
# tal que perfectos(n) es la lista de todos los números perfectos
# menores que n. Por ejemplo,
#    perfectos(500)    ==  [6, 28, 496]
#    perfectos(10**5)  ==  [6, 28, 496, 8128]
# ---------------------------------------------------------------------

# divisores(n) es la lista de los divisores del número n. Por ejemplo,
#    divisores(30)  ==  [1,2,3,5,6,10,15,30]
def divisores(n: int) -> list[int]:
    return [x for x in range(1, n + 1) if n % x == 0]

# sumaDivisores(x) es la suma de los divisores de x. Por ejemplo,
#    sumaDivisores(12)                ==  28
#    sumaDivisores(25)                ==  31
def sumaDivisores(n: int) -> int:
    return sum(divisores(n))

# esPerfecto(x) se verifica si x es un número perfecto. Por ejemplo,
#    esPerfecto(6)  ==  True
#    esPerfecto(8)  ==  False
def esPerfecto(x: int) -> bool:
    return sumaDivisores(x) - x == x

def perfectos(n: int) -> list[int]:
    return [x for x in range(1, n + 1) if esPerfecto(x)]

# ---------------------------------------------------------------------
# Ejercicio 5.1. Un número natural n se denomina abundante si es menor
# que la suma de sus divisores propios. Por ejemplo, 12 es abundante ya
# que la suma de sus divisores propios es 16 (= 1 + 2 + 3 + 4 + 6), pero
# 5 y 28 no lo son.
#
# Definir la función
#    numeroAbundante : (int) -> bool
# tal que numeroAbundante(n) se verifica si n es un número
# abundante. Por ejemplo,
#    numeroAbundante(5)  == False
#    numeroAbundante(12) == True
#    numeroAbundante(28) == False
#    numeroAbundante(30) == True
#    numeroAbundante(100000000)  ==  True
#    numeroAbundante(100000001)  ==  False
# ---------------------------------------------------------------------

def numeroAbundante(x: int) -> bool:
    return x < sumaDivisores(x) - x

# ---------------------------------------------------------------------
# Ejercicio 5.2. Definir la función
#    numerosAbundantesMenores : (int) -> list[Int]
# tal que numerosAbundantesMenores(n) es la lista de números
# abundantes menores o iguales que n. Por ejemplo,
#    numerosAbundantesMenores(50)  ==  [12,18,20,24,30,36,40,42,48]
#    numerosAbundantesMenores(48)  ==  [12,18,20,24,30,36,40,42,48]
#    leng(numerosAbundantesMenores(10**6)) ==  247545
# ---------------------------------------------------------------------

def numerosAbundantesMenores(n: int) -> list[int]:
    return [x for x in range(1, n + 1) if numeroAbundante(x)]

# ---------------------------------------------------------------------
# Ejercicio 5.3. Definir la función
#    todosPares : (int) -> bool
# tal que todosPares(n) se verifica si todos los números abundantes
# menores o iguales que n son pares. Por ejemplo,
#    todosPares(10)    ==  True
#    todosPares(100)   ==  True
#    todosPares(1000)  ==  False
# ---------------------------------------------------------------------

def todosPares(n: int) -> bool:
    return False not in [x % 2 == 0 for x in numerosAbundantesMenores(n)]

# ---------------------------------------------------------------------
# Ejercicio 6. Definir la función
#    euler1 : (int) -> int
# tal que euler1(n) es la suma de todos los múltiplos de 3 ó 5 menores
# que n. Por ejemplo,
#    euler1(10)     == 23
#    euler1(10**2)  == 2318
#    euler1(10**3)  == 233168
#    euler1(10**4)  == 23331668
#    euler1(10**5)  == 2333316668
#    euler1(10**10) == 23333333331666666668
#    euler1(10**20) == 2333333333333333333316666666666666666668
#
# Nota: Este ejercicio está basado en el problema 1 del Proyecto Euler
# https://projecteuler.net/problem=1
# ---------------------------------------------------------------------

# multiplo(x, y) se verifica si x es un múltiplo de y. Por ejemplo.
#    multiplo(12, 3)  ==  True
#    multiplo(14, 3)  ==  False
def multiplo(x: int, y: int) -> int:
    return x % y == 0

def euler1(n: int) -> int:
    return sum(x for x in range(1, n)
               if (multiplo(x, 3) or multiplo(x, 5)))

# El cálculo es
#    >>> euler1(1000)
#    233168

# ---------------------------------------------------------------------
# Ejercicio 7. En el círculo de radio 2 hay 6 puntos cuyas coordenadas
# son puntos naturales:
#    (0,0),(0,1),(0,2),(1,0),(1,1),(2,0)
# y en de radio 3 hay 11:
#    (0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2),(3,0)
#
# Definir la función
#    circulo : (int) -> int
# tal que circulo(n) es el la cantidad de pares de números naturales
# (x,y) que se encuentran en el círculo de radio n. Por ejemplo,
#    circulo(1)    ==  3
#    circulo(2)    ==  6
#    circulo(3)    ==  11
#    circulo(4)    ==  17
#    circulo(100)  ==  7955
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def circulo1(n: int) -> int:
    return len([(x, y)
                for x in range(0, n + 1)
                for y in range(0, n + 1)
                if x * x + y * y <= n * n])

# 2ª solución
# ===========

def enSemiCirculo(n: int) -> list[tuple[int, int]]:
    return [(x, y)
            for x in range(0, ceil(sqrt(n**2)) + 1)
            for y in range(x+1, trunc(sqrt(n**2 - x**2)) + 1)]

def circulo2(n: int) -> int:
    if n == 0:
        return 1
    return (2 * len(enSemiCirculo(n)) + ceil(n / sqrt(2)))

# 3ª solución
# ===========

def circulo3(n: int) -> int:
    r = 0
    for x in range(0, n + 1):
        for y in range(0, n + 1):
            if x**2 + y**2 <= n**2:
                r = r + 1
    return r

# 4ª solución
# ===========

def circulo4(n: int) -> int:
    r = 0
    for x in range(0, ceil(sqrt(n**2)) + 1):
        for y in range(x + 1, trunc(sqrt(n**2 - x**2)) + 1):
            if x**2 + y**2 <= n**2:
                r = r + 1
    return 2 * r + ceil(n / sqrt(2))

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.integers(min_value=1, max_value=100))
def test_circulo(n: int) -> None:
    r = circulo1(n)
    assert circulo2(n) == r
    assert circulo3(n) == r
    assert circulo4(n) == r

# La comprobación está al final.

# Comparación de eficiencia
# =========================

# La comparación es
#    >>> tiempo('circulo1(2000)')
#    0.71 segundos
#    >>> tiempo('circulo2(2000)')
#    0.76 segundos
#    >>> tiempo('circulo3(2000)')
#    2.63 segundos
#    >>> tiempo('circulo4(2000)')
#    1.06 segundos

# ---------------------------------------------------------------------
# Ejercicio 8.1. El número e se define como el límite de la sucesión
# (1+1/n)**n; es decir,
#    e = lim (1+1/n)**n
#
# Definir la función
#    aproxE      : (int) -> list[float]
# tal que aproxE(k) es la lista de los k primeros términos de la
# sucesión (1+1/n)**m. Por ejemplo,
#    aproxE(4) == [2.0, 2.25, 2.37037037037037, 2.44140625]
#    aproxE6(7*10**7)[-1] ==  2.7182818287372563
# ---------------------------------------------------------------------

def aproxE(k: int) -> list[float]:
    return [(1 + 1/n)**n for n in range(1, k + 1)]

# ---------------------------------------------------------------------
# Ejercicio 8.2. Definir la función
#    errorAproxE : (float) -> int
# tal que errorE(x) es el menor número de términos de la sucesión
# (1+1/m)**m necesarios para obtener su límite con un error menor que
# x. Por ejemplo,
#    errorAproxE(0.1)    ==  13
#    errorAproxE(0.01)   ==  135
#    errorAproxE(0.001)  ==  1359
# ---------------------------------------------------------------------

# naturales es el generador de los números naturales positivos, Por
# ejemplo,
#    >>> list(islice(naturales(), 5))
#    [1, 2, 3, 4, 5]
def naturales() -> Iterator[int]:
    i = 1
    while True:
        yield i
        i += 1

def errorAproxE(x: float) -> int:
    return list(islice((n for n in naturales()
                        if abs(e - (1 + 1/n)**n) < x), 1))[0]

# ---------------------------------------------------------------------
# Ejercicio 9.1. El limite de sen(x)/x, cuando x tiende a cero, se puede
# calcular como el límite de la sucesión sen(1/n)/(1/n), cuando n tiende
# a infinito.
#
# Definir la función
#    aproxLimSeno : (int) -> list[float]
# tal que aproxLimSeno(n) es la lista cuyos elementos son los n primeros
# términos de la sucesión sen(1/m)/(1/m). Por ejemplo,
#    aproxLimSeno(1) == [0.8414709848078965]
#    aproxLimSeno(2) == [0.8414709848078965,0.958851077208406]
# ---------------------------------------------------------------------

def aproxLimSeno(k: int) -> list[float]:
    return [sin(1/n)/(1/n) for n in range(1, k + 1)]

# ---------------------------------------------------------------------
# Ejercicio 9.2. Definir la función
#    errorLimSeno : (float) -> int
# tal que errorLimSeno(x) es el menor número de términos de la sucesión
# sen(1/m)/(1/m) necesarios para obtener su límite con un error menor
# que x. Por ejemplo,
#    errorLimSeno(0.1)     ==   2
#    errorLimSeno(0.01)    ==   5
#    errorLimSeno(0.001)   ==  13
#    errorLimSeno(0.0001)  ==  41
# ---------------------------------------------------------------------

# 1ª definición de errorLimSeno
# ============================

def errorLimSeno(x: float) -> int:
    return list(islice((n for n in naturales()
                        if abs(1 - sin(1/n)/(1/n)) < x), 1))[0]

# ---------------------------------------------------------------------
# Ejercicio 10.1. El número π puede calcularse con la fórmula de
# Leibniz
#    π/4 = 1 - 1/3 + 1/5 - 1/7 + ...+ (-1)**n/(2*n+1) + ...
#
# Definir la función
#    calculaPi : (int) -> float
# tal que calculaPi(n) es la aproximación del número π calculada
# mediante la expresión
#    4*(1 - 1/3 + 1/5 - 1/7 + ...+ (-1)**n/(2*n+1))
# Por ejemplo,
#    calculaPi(3)    ==  2.8952380952380956
#    calculaPi(300)  ==  3.1449149035588526
# ---------------------------------------------------------------------

def calculaPi(k: int) -> float:
    return 4 * sum(((-1)**n/(2*n+1) for n in range(0, k+1)))

# ---------------------------------------------------------------------
# Ejercicio 10.2. Definir la función
#    errorPi   : (float) -> int
# tal que errorPi(x) es el menor número de términos de la serie
# necesarios para obtener pi con un error menor que x. Por ejemplo,
#    errorPi(0.1)    ==    9
#    errorPi(0.01)   ==   99
#    errorPi(0.001)  ==  999
# ---------------------------------------------------------------------

def errorPi(x: float) -> int:
    return list(islice((n for n in naturales()
                        if abs(pi - calculaPi(n)) < x), 1))[0]

# ---------------------------------------------------------------------
# Ejercicio 11.1. Una terna (x,y,z) de enteros positivos es pitagórica
# si x^2 + y^2 = z^2 y x < y < z.
#
# Definir, por comprensión, la función
#    pitagoricas : (int) -> list[tuple[int,int,int]]
# tal que pitagoricas(n) es la lista de todas las ternas pitagóricas
# cuyas componentes están entre 1 y n. Por ejemplo,
#    pitagoricas(10) == [(3, 4, 5), (6, 8, 10)]
#    pitagoricas(15) == [(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15)]
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def pitagoricas1(n: int) -> list[tuple[int, int, int]]:
    return [(x, y, z)
            for x in range(1, n+1)
            for y in range(1, n+1)
            for z in range(1, n+1)
            if x**2 + y**2 == z**2 and x < y < z]

# 2ª solución
# ===========

def pitagoricas2(n: int) -> list[tuple[int, int, int]]:
    return [(x, y, z)
            for x in range(1, n+1)
            for y in range(x+1, n+1)
            for z in range(ceil(sqrt(x**2+y**2)), n+1)
            if x**2 + y**2 == z**2]

# 3ª solución
# ===========

def pitagoricas3(n: int) -> list[tuple[int, int, int]]:
    return [(x, y, z)
            for x in range(1, n+1)
            for y in range(x+1, n+1)
            for z in [ceil(sqrt(x**2+y**2))]
            if y < z <= n and x**2 + y**2 == z**2]

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.integers(min_value=1, max_value=50))
def test_pitagoricas(n: int) -> None:
    r = pitagoricas1(n)
    assert pitagoricas2(n) == r
    assert pitagoricas3(n) == r

# La comprobación está al final.

# Comparación de eficiencia
# =========================

# La comparación es
#    >>> tiempo('pitagoricas1(200)')
#    4.76 segundos
#    >>> tiempo('pitagoricas2(200)')
#    0.69 segundos
#    >>> tiempo('pitagoricas3(200)')
#    0.02 segundos

# ---------------------------------------------------------------------
# Ejercicio 11.2. Definir la función
#    numeroDePares : (int, int, int) -> int
# tal que numeroDePares(t) es el número de elementos pares de la terna
# t. Por ejemplo,
#    numeroDePares(3, 5, 7)  ==  0
#    numeroDePares(3, 6, 7)  ==  1
#    numeroDePares(3, 6, 4)  ==  2
#    numeroDePares(4, 6, 4)  ==  3
# ---------------------------------------------------------------------

def numeroDePares(x: int, y: int, z: int) -> int:
    return len([1 for n in [x, y, z] if n % 2 == 0])

# ---------------------------------------------------------------------
# Ejercicio 11.3. Definir la función
#    conjetura : (int) -> bool
# tal que conjetura(n) se verifica si todas las ternas pitagóricas
# cuyas componentes están entre 1 y n tiene un número impar de números
# pares. Por ejemplo,
#    conjetura(10)  ==  True
# ---------------------------------------------------------------------

def conjetura(n: int) -> bool:
    return False not in [numeroDePares(x, y, z) % 2 == 1
                         for (x, y, z) in pitagoricas1(n)]

# ---------------------------------------------------------------------
# Ejercicio 11.4. Demostrar la conjetura para todas las ternas
# pitagóricas.
# ---------------------------------------------------------------------
#
# Sea (x,y,z) una terna pitagórica. Entonces x^2+y^2=z^2. Pueden darse
# 4 casos:
#
# Caso 1: x e y son pares. Entonces, x^2, y^2 y z^2 también lo
# son. Luego el número de componentes pares es 3 que es impar.
#
# Caso 2: x es par e y es impar. Entonces, x^2 es par, y^2 es impar y
# z^2 es impar. Luego el número de componentes pares es 1 que es impar.
#
# Caso 3: x es impar e y es par. Análogo al caso 2.
#
# Caso 4: x e y son impares. Entonces, x^2 e y^2 también son impares y
# z^2 es par. Luego el número de componentes pares es 1 que es impar.

# ---------------------------------------------------------------------
# Ejercicio 12.1. (Problema 9 del proyecto Euler). Una terna pitagórica
# es una terna de números naturales (a,b,c) tal que a<b<c y
# a^2+b^2=c^2. Por ejemplo (3,4,5) es una terna pitagórica.
#
# Definir la función
#    ternasPitagoricas : (int) -> list[tuple[int, int, int]]
# tal que ternasPitagoricas(x) es la lista de las ternas pitagóricas
# cuya suma es x. Por ejemplo,
#    ternasPitagoricas(12)    == [(3, 4, 5)]
#    ternasPitagoricas(60)    == [(10, 24, 26), (15, 20, 25)]
#    ternasPitagoricas(10**6) == [(218750, 360000, 421250),
#                                 (200000, 375000, 425000)]
# ---------------------------------------------------------------------

# 1ª solución                                                   --
# ===========

def ternasPitagoricas1(x: int) -> list[tuple[int, int, int]]:
    return [(a, b, c)
            for a in range(0, x+1)
            for b in range(a+1, x+1)
            for c in range(b+1, x+1)
            if a**2 + b**2 == c**2 and a + b + c == x]

# 2ª solución                                                   --
# ===========

def ternasPitagoricas2(x: int) -> list[tuple[int, int, int]]:
    return [(a, b, c)
            for a in range(1, x+1)
            for b in range(a+1, x-a+1)
            for c in [x - a - b]
            if a**2 + b**2 == c**2]

# 3ª solución                                                   --
# ===========

# Todas las ternas pitagóricas primitivas (a,b,c) pueden representarse
# por
#    a = m^2 - n^2, b = 2*m*n, c = m^2 + n^2,
# con 1 <= n < m. (Ver en https://bit.ly/35UNY6L ).

def ternasPitagoricas3(x: int) -> list[tuple[int, int, int]]:
    def aux(y: int) -> list[tuple[int, int, int]]:
        return [(a, b, c)
                for m in range(2, 1 + ceil(sqrt(y)))
                for n in range(1, m)
                for a in [min(m**2 - n**2, 2*m*n)]
                for b in [max(m**2 - n**2, 2*m*n)]
                for c in [m**2 + n**2]
                if a+b+c == y]

    return list(set(((d*a, d*b, d*c)
                     for d in range(1, x+1)
                     for (a, b, c) in aux(x // d)
                     if x % d == 0)))

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.integers(min_value=1, max_value=50))
def test_ternasPitagoricas(n: int) -> None:
    r = set(ternasPitagoricas1(n))
    assert set(ternasPitagoricas2(n)) == r
    assert set(ternasPitagoricas3(n)) == r

# La comprobación está al final.

# Comparación de eficiencia
# =========================

# La comparación es
#    >>> tiempo('ternasPitagoricas1(300)')
#    2.83 segundos
#    >>> tiempo('ternasPitagoricas2(300)')
#    0.01 segundos
#    >>> tiempo('ternasPitagoricas3(300)')
#    0.00 segundos
#
#    >>> tiempo('ternasPitagoricas2(3000)')
#    1.48 segundos
#    >>> tiempo('ternasPitagoricas3(3000)')
#    0.02 segundos

# ---------------------------------------------------------------------
# Ejercicio 12.2. Definir la función
#    euler9 : () -> int
# tal que euler9() es producto abc donde (a,b,c) es la única terna
# pitagórica tal que a+b+c=1000.
#
# Calcular el valor de euler9().
# ---------------------------------------------------------------------

def euler9() -> int:
    (a, b, c) = ternasPitagoricas3(1000)[0]
    return a * b * c

# El cálculo del valor de euler9 es
#    >>> euler9()
#    31875000

# ---------------------------------------------------------------------
# Ejercicio 13. El producto escalar de dos listas de enteros xs y ys de
# longitud n viene dado por la suma de los productos de los elementos
# correspondientes.
#
# Definir, por comprensión, la función
#    productoEscalar : (list[int], list[int]) -> int
# tal que productoEscalar(xs, ys) es el producto escalar de las listas
# xs e ys. Por ejemplo,
#    productoEscalar([1, 2, 3], [4, 5, 6])  ==  32
# ---------------------------------------------------------------------

def productoEscalar(xs: list[int], ys: list[int]) -> int:
    return sum(x * y for (x, y) in zip(xs, ys))

# ---------------------------------------------------------------------
# Ejercicio 14. Definir , por comprensión,la función
#    sumaConsecutivos : (list[int]) -> list[int]
# tal que sumaConsecutivos(xs) es la suma de los pares de elementos
# consecutivos de la lista xs. Por ejemplo,
#    sumaConsecutivos([3, 1, 5, 2])           ==  [4, 6, 7]
#    sumaConsecutivos([3])                    ==  []
#    sumaConsecutivos(range(1, 1+10**8))[-1]  ==  199999999
# ---------------------------------------------------------------------

def sumaConsecutivos(xs: list[int]) -> list[int]:
    return [x + y for (x, y) in zip(xs, xs[1:])]

# ---------------------------------------------------------------------
# Ejercicio 15. Los polinomios pueden representarse de forma dispersa o
# densa. Por ejemplo, el polinomio 6x^4-5x^2+4x-7 se puede representar
# de forma dispersa por [6,0,-5,4,-7] y de forma densa por
# [(4,6),(2,-5),(1,4),(0,-7)].
#
# Definir la función
#    densa : (list[int]) -> list[tuple[int, int]]
# tal que densa(xs) es la representación densa del polinomio cuya
# representación dispersa es xs. Por ejemplo,
#   densa([6, 0, -5, 4, -7])  == [(4, 6), (2, -5), (1, 4), (0, -7)]
#   densa([6, 0, 0, 3, 0, 4]) == [(5, 6), (2, 3), (0, 4)]
#   densa([0])                == [(0, 0)]
# ---------------------------------------------------------------------

def densa(xs: list[int]) -> list[tuple[int, int]]:
    n = len(xs)
    return [(x, y)
            for (x, y) in zip(range(n-1, 0, -1), xs)
            if y != 0] + [(0, xs[-1])]

# ---------------------------------------------------------------------
# Ejercicio 16. Las bases de datos sobre actividades de personas pueden
# representarse mediante listas de elementos de la forma (a,b,c,d),
# donde a es el nombre de la persona, b su actividad, c su fecha de
# nacimiento y d la de su fallecimiento. Un ejemplo es la siguiente que
# usaremos a lo largo de este ejercicio,
#    BD = list[tuple[str, str, int, int]]
#
#    personas: BD = [
#        ("Cervantes", "Literatura", 1547, 1616),
#        ("Velazquez", "Pintura", 1599, 1660),
#        ("Picasso", "Pintura", 1881, 1973),
#        ("Beethoven", "Musica", 1770, 1823),
#        ("Poincare", "Ciencia", 1854, 1912),
#        ("Quevedo", "Literatura", 1580, 1654),
#        ("Goya", "Pintura", 1746, 1828),
#        ("Einstein", "Ciencia", 1879, 1955),
#        ("Mozart", "Musica", 1756, 1791),
#        ("Botticelli", "Pintura", 1445, 1510),
#        ("Borromini", "Arquitectura", 1599, 1667),
#        ("Bach", "Musica", 1685, 1750)]
# ---------------------------------------------------------------------

BD = list[tuple[str, str, int, int]]

personas: BD = [
    ("Cervantes", "Literatura", 1547, 1616),
    ("Velazquez", "Pintura", 1599, 1660),
    ("Picasso", "Pintura", 1881, 1973),
    ("Beethoven", "Musica", 1770, 1823),
    ("Poincare", "Ciencia", 1854, 1912),
    ("Quevedo", "Literatura", 1580, 1654),
    ("Goya", "Pintura", 1746, 1828),
    ("Einstein", "Ciencia", 1879, 1955),
    ("Mozart", "Musica", 1756, 1791),
    ("Botticelli", "Pintura", 1445, 1510),
    ("Borromini", "Arquitectura", 1599, 1667),
    ("Bach", "Musica", 1685, 1750)]

# ---------------------------------------------------------------------
# Ejercicio 16.1. Definir la función
#    nombres : (BD) -> list[str]
# tal que nombres(bd) es la lista de los nombres de las personas de la-
# base de datos bd. Por ejemplo,
#    >>> nombres(personas)
#    ['Cervantes', 'Velazquez', 'Picasso', 'Beethoven', 'Poincare',
#     'Quevedo', 'Goya', 'Einstein', 'Mozart', 'Botticelli', 'Borromini',
#     'Bach']
# ---------------------------------------------------------------------

def nombres(bd: BD) -> list[str]:
    return [p[0] for p in bd]

# ---------------------------------------------------------------------
# Ejercicio 16.2. Definir la función
#    musicos : (BD) -> list[str]
# tal que musicos(bd) es la lista de los nombres de los músicos de la
# base de datos bd. Por ejemplo,
#    musicos(personas)  ==  ['Beethoven', 'Mozart', 'Bach']
# ---------------------------------------------------------------------

def musicos(bd: BD) -> list[str]:
    return [p[0] for p in bd if p[1] == "Musica"]

# ---------------------------------------------------------------------
# Ejercicio 16.3. Definir la función
#    seleccion : (BD, str) -> list[str]
# tal que seleccion(bd, m) es la lista de los nombres de las personas de
# la base de datos bd cuya actividad es m. Por ejemplo,
#    >>> seleccion(personas, 'Pintura')
#    ['Velazquez', 'Picasso', 'Goya', 'Botticelli']
#    >>> seleccion(personas, 'Musica')
#    ['Beethoven', 'Mozart', 'Bach']
# ---------------------------------------------------------------------

def seleccion(bd: BD, m: str) -> list[str]:
    return [p[0] for p in bd if p[1] == m]

# ---------------------------------------------------------------------
# Ejercicio 16.4. Definir la función
#    musicos2 : (BD) -> list[str]
# tal que musicos2(bd) es la lista de los nombres de los músicos de la
# base de datos bd. Por ejemplo,
#    musicos2(personas)  ==  ['Beethoven','Mozart','Bach']
# ---------------------------------------------------------------------

def musicos2(bd: BD) -> list[str]:
    return seleccion(bd, "Musica")

# ---------------------------------------------------------------------
# Ejercicio 16.5. Definir la función
#    vivas : (BD, int) -> list[str]
# tal que vivas(bd, a) es la lista de los nombres de las personas de la
# base de datos bd  que estaban vivas en el año a. Por ejemplo,
#    >>> vivas(personas, 1600)
#    ['Cervantes', 'Velazquez', 'Quevedo', 'Borromini']
# ---------------------------------------------------------------------

def vivas(bd: BD, a: int) -> list[str]:
    return [p[0] for p in bd if p[2] <= a <= p[3]]

# ---------------------------------------------------------------------
# Comprobación
# ---------------------------------------------------------------------

# La comprobación es
#    src> poetry run pytest -q definiciones_por_comprension.py
#    8 passed in 4.23s
