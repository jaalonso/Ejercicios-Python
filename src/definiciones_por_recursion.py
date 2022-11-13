# definiciones_por_recursion.py
# Definiciones por recursión
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 11-noviembre-2022
# =====================================================================

# ---------------------------------------------------------------------
# Introducción                                                       --
# ---------------------------------------------------------------------

# En esta relación se presentan ejercicios con definiciones por
# recursión correspondientes al tema 6 que se encuentra en
#    https://jaalonso.github.io/cursos/i1m/temas/tema-6.html

# ---------------------------------------------------------------------
# Importación de librerías auxiliares                                --
# ---------------------------------------------------------------------

from itertools import islice
from sys import setrecursionlimit
from timeit import Timer, default_timer
from typing import Iterator, TypeVar

from hypothesis import given
from hypothesis import strategies as st

setrecursionlimit(10**6)

A = TypeVar('A')

# ---------------------------------------------------------------------
# Ejercio 1. Definir, por recursión, la función
#    potencia : (int, int) -> int
# tal que potencia(x, n) es x elevado al número natural n. Por ejemplo,
#    potencia(2, 3)  ==  8
# ---------------------------------------------------------------------

def potencia(m: int, n: int) -> int:
    if n == 0:
        return 1
    return m * potencia(m, n-1)

# ---------------------------------------------------------------------
# Ejercicio 1.2. Comprobar con Hypothesis que la función potencia es
# equivalente a la predefinida (^).
# ---------------------------------------------------------------------

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.integers(),
       st.integers(min_value=0, max_value=100))
def test_potencia(m: int, n: int) -> None:
    assert potencia(m, n) == m ** n

# La comprobación está al final.

# ---------------------------------------------------------------------
# Ejercicio 2. Dados dos números naturales, a y b, es posible calcular
# su máximo común divisor mediante el Algoritmo de Euclides. Este
# algoritmo se puede resumir en la siguiente fórmula:
#    mcd(a,b) = a,                   si b = 0
#             = mcd (b, a módulo b), si b > 0
#
# Definir la función
#    mcd : (int, nt) -> int
# tal que mcd(a, b) es el máximo común divisor de a y b calculado
# mediante el algoritmo de Euclides. Por ejemplo,
#    mcd(30, 45)  ==  15
#    mcd(45, 30)  ==  15
#
# Comprobar con Hypothesis que el máximo común divisor de dos números a
# y b (ambos mayores que 0) es siempre mayor o igual que 1 y además es
# menor o igual que el menor de los números a  y b.
# ---------------------------------------------------------------------

def mcd(a: int, b: int) -> int:
    if b == 0:
        return a
    return mcd(b, a % b)

# La propiedad es
@given(st.integers(min_value=1, max_value=1000),
       st.integers(min_value=1, max_value=1000))
def test_mcd(a: int, b: int) -> None:
    assert 1 <= mcd(a, b) <= min(a, b)

# La comprobación es
#    src> poetry run pytest -q algoritmo_de_Euclides_del_mcd.py
#    1 passed in 0.22s

# ---------------------------------------------------------------------
# Ejercicio 3.1, Definir por recursión la función
#    pertenece : (A, list[A]) -> bool
# tal que pertenece(x, ys) se verifica si x pertenece a la lista ys.
# Por ejemplo,
#    pertenece(3, [2, 3, 5])  ==  True
#    pertenece(4, [2, 3, 5])  ==  False
# ---------------------------------------------------------------------

def pertenece(x: A, ys: list[A]) -> bool:
    if ys:
        return x == ys[0] or pertenece(x, ys[1:])
    return False

# ---------------------------------------------------------------------
# Ejercicio 3.2. Comprobar con Hypothesis que pertenece es equivalente
# a in.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.integers(),
       st.lists(st.integers()))
def test_pertenece(x: int, ys: list[int]) -> None:
    assert pertenece(x, ys) == (x in ys)

# La comprobación está al final.

# ---------------------------------------------------------------------
# Ejercicio 4. Definir por recursión la función
#    concatenaListas :: [[a]] -> [a]
# tal que (concatenaListas xss) es la lista obtenida concatenando las
# listas de xss. Por ejemplo,
#    concatenaListas([[1, 3], [5], [2, 4, 6]]) == [1, 3, 5, 2, 4, 6]
# ---------------------------------------------------------------------

def concatenaListas(xss: list[list[A]]) -> list[A]:
    if xss:
        return xss[0] + concatenaListas(xss[1:])
    return []

# ---------------------------------------------------------------------
# Ejercicio 5.1. Definir por recursión la función
#    coge : (int, list[A]) -> list[A]
# tal que coge(n, xs) es la lista de los n primeros elementos de
# xs. Por ejemplo,
#    coge(3, range(4, 12)) == [4, 5, 6]
# ---------------------------------------------------------------------

def coge(n: int, xs: list[A]) -> list[A]:
    if n <= 0:
        return []
    if not xs:
        return []
    return [xs[0]] + coge(n - 1, xs[1:])

# ---------------------------------------------------------------------
# Ejercicio 5.2. Comprobar con Hypothesis que coge(n, xs) es equivalente
# a xs[:n], suponiendo que n >= 0.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.integers(min_value=0),
       st.lists(st.integers()))
def test_coge(n: int, xs: list[int]) -> None:
    assert coge(n, xs) == xs[:n]

# La comprobación está al final.

# ---------------------------------------------------------------------
# Ejercicio 6.1. Definir, por recursión  la función
#    sumaDeCuadradosR : (int) -> int
# tal sumaDeCuadradosR(n) es la suma de los cuadrados de los n primeros
# números naturales. Por ejemplo,
#    sumaDeCuadradosR(3)   ==  14
#    sumaDeCuadradosR(100) ==  338350
# ---------------------------------------------------------------------

def sumaDeCuadradosR(n: int) -> int:
    if n == 1:
        return 1
    return n**2 + sumaDeCuadradosR(n - 1)

# ---------------------------------------------------------------------
# Ejercicio 6.2. Comprobar con Hypothesis que sumaCuadradosR(n) es igual
# a n(n+1)(2n+1)/6.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.integers(min_value=1, max_value=1000))
def test_sumaDeCuadrados(n: int) -> None:
    assert sumaDeCuadradosR(n) == n * (n + 1) * (2 * n + 1) // 6

# La comprobación está al final.

# ---------------------------------------------------------------------
# Ejercicio 6.3. Definir, por comprensión, la función
#    sumaDeCuadradosC : (int) -> int
# tal sumaDeCuadradosC(n) es la suma de los cuadrados de los n primeros
# números naturales. Por ejemplo,
#    sumaDeCuadradosC(3)   ==  14
#    sumaDeCuadradosC(100) ==  338350
# ---------------------------------------------------------------------

def sumaDeCuadradosC(n: int) -> int:
    return sum(x**2 for x in range(1, n + 1))

# ---------------------------------------------------------------------
# Ejercicio 6.4. Comprobar con Hypothesis que las funciones
# sumaCuadradosR y sumaCuadradosC son equivalentes sobre los números
# naturales.
# ---------------------------------------------------------------------

@given(st.integers(min_value=1, max_value=1000))
def test_sumaDeCuadrados2(n: int) -> None:
    assert sumaDeCuadradosR(n) == sumaDeCuadradosC(n)

# La comprobación está al final.

# ---------------------------------------------------------------------
# Ejercicio 7.1. Definir, por recursión, la función
#    digitosR : (int) -> list[int]
# tal que digitosR(n) es la lista de los dígitos del número n. Por
# ejemplo,
#    digitosR(320274)  ==  [3, 2, 0, 2, 7, 4]
# ---------------------------------------------------------------------

def digitosR(n: int) -> list[int]:
    if n < 10:
        return [n]
    return digitosR(n // 10) + [n % 10]

# ---------------------------------------------------------------------
# Ejercicio 7.2. Definir, por comprensión, la función
#    digitosC : (int) -> list[int]
# tal que digitosC(n) es la lista de los dígitos del número n. Por
# ejemplo,
#    digitosC(320274)  ==  [3, 2, 0, 2, 7, 4]
# ---------------------------------------------------------------------

def digitosC(n: int) -> list[int]:
    return [int(x) for x in str(n)]

# ---------------------------------------------------------------------
# Ejercicio 7.3. Comprobar con Hypothesis que las funciones digitosR y
# digitosC son equivalentes.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.integers(min_value=1, max_value=1000))
def test_digitos(n: int) -> None:
    assert digitosR(n) == digitosC(n)

# La comprobación está al final.

# ---------------------------------------------------------------------
# Ejercicio 8.1. Definir, por recursión, la función
#    sumaDigitosR : (int) -> int
# tal que sumaDigitosR(n) es la suma de los dígitos de n. Por ejemplo,
#    sumaDigitosR(3)     ==  3
#    sumaDigitosR(2454)  == 15
#    sumaDigitosR(20045) == 11
# ---------------------------------------------------------------------

def sumaDigitosR(n: int) -> int:
    if n < 10:
        return n
    return n % 10 + sumaDigitosR(n // 10)

# ---------------------------------------------------------------------
# Ejercicio 8.2. Definir, sin usar recursión, la función
#    sumaDigitosNR : (int) -> int
# tal que sumaDigitosNR(n) es la suma de los dígitos de n. Por ejemplo,
#    sumaDigitosNR(3)     ==  3
#    sumaDigitosNR(2454)  == 15
#    sumaDigitosNR(20045) == 11
# ---------------------------------------------------------------------

def sumaDigitosNR(n: int) -> int:
    return sum(digitosC(n))

# ---------------------------------------------------------------------
# Ejercicio 8.3. Comprobar con Hypothesis que las funciones sumaDigitosR
# y sumaDigitosNR son equivalentes.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.integers(min_value=1, max_value=1000))
def test_sumaDigitos(n: int) -> None:
    assert sumaDigitosR(n) == sumaDigitosNR(n)

# La comprobación está al final.

# ---------------------------------------------------------------------
# Ejercicio 9.1. Definir, por recursión, la función
#    listaNumeroR : (list[int]) -> int
# tal que listaNumeroR(xs) es el número formado por los dígitos xs. Por
# ejemplo,
#    listaNumeroR([5])           == 5
#    listaNumeroR([1, 3, 4, 7])  == 1347
#    listaNumeroR([0, 0, 1])     == 1
# ---------------------------------------------------------------------

def listaNumeroR(xs: list[int]) -> int:
    def aux(ys: list[int]) -> int:
        if ys:
            return ys[0] + 10 * aux(ys[1:])
        return 0
    return aux(list(reversed(xs)))

# ---------------------------------------------------------------------
# Ejercicio 9.2. Definir, por comprensión, la función
#    listaNumeroC : (list[int]) -> int
# tal que listaNumeroC(xs) es el número formado por los dígitos xs. Por
# ejemplo,
#    listaNumeroC([5])           == 5
#    listaNumeroC([1, 3, 4, 7])  == 1347
#    listaNumeroC([0, 0, 1])     == 1
# ---------------------------------------------------------------------

def listaNumeroC(xs: list[int]) -> int:
    return sum((y * 10**n
                for (y, n) in zip(list(reversed(xs)), range(0, len(xs)))))

# ---------------------------------------------------------------------
# Ejercicio 9.3. Comprobar con Hypothesis que las funciones
# listaNumeroR y listaNumeroC son equivalentes.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.lists(st.integers(min_value=0, max_value=9), min_size=1))
def test_listaNumero(xs: list[int]) -> None:
    print("listaNumero")
    assert listaNumeroR(xs) == listaNumeroC(xs)

# La comprobación está al final.

# ---------------------------------------------------------------------
# Ejercicio 10.1. Definir, por recursión, la función
#    mayorExponenteR : (int, int) -> int
# tal que mayorExponenteR(a, b) es el exponente de la mayor potencia de
# a que divide b. Por ejemplo,
#    mayorExponenteR(2, 8)    ==  3
#    mayorExponenteR(2, 9)    ==  0
#    mayorExponenteR(5, 100)  ==  2
#    mayorExponenteR(2, 60)   ==  2
#
# Nota: Se supone que a > 1 y b > 0.
# ---------------------------------------------------------------------

def mayorExponenteR(a: int, b: int) -> int:
    if b % a != 0:
        return 0
    return 1 + mayorExponenteR(a, b // a)

# ---------------------------------------------------------------------
# Ejercicio 10.2. Definir, por comprensión, la función
#    mayorExponenteC : (int, int) -> int
# tal que mayorExponenteC(a, b) es el exponente de la mayor potencia de
# a que divide b. Por ejemplo,
#    mayorExponenteC(2, 8)    ==  3
#    mayorExponenteC(2, 9)    ==  0
#    mayorExponenteC(5, 100)  ==  2
#    mayorExponenteC(2, 60)   ==  2
#
# Nota: Se supone que a > 1 y b > 0.
# ---------------------------------------------------------------------

# naturales es el generador de los números naturales, Por ejemplo,
#    >>> list(islice(naturales(), 5))
#    [0, 1, 2, 3, 4]
def naturales() -> Iterator[int]:
    i = 0
    while True:
        yield i
        i += 1

def mayorExponenteC(a: int, b: int) -> int:
    return list(islice((x - 1 for x in naturales() if b % (a**x) != 0), 1))[0]

# ---------------------------------------------------------------------
# Ejercicio 10.3. Comprobar con Hypothesis que las funciones
# mayorExponenteR y mayorExponenteC son equivalentes.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.integers(min_value=2, max_value=10),
       st.integers(min_value=1, max_value=10))
def test_mayorExponente(a: int, b: int) -> None:
    assert mayorExponenteR(a, b) == mayorExponenteC(a, b)

# La comprobación está al final.

# La comprobación de las propiedades es
#    src> poetry run pytest -q definiciones_por_recursion.py
#    10 passed in 0.98s
