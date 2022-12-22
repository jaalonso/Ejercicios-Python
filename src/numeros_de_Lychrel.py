# numeros_de_Lychrel.py
# Números de Lychrel.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 22-diciembre-2022
# ======================================================================

# ---------------------------------------------------------------------
# Introducción                                                       --
# ---------------------------------------------------------------------

# Según la Wikipedia http://bit.ly/2X4DzMf, un número de Lychrel es un
# número natural para el que nunca se obtiene un capicúa mediante el
# proceso de invertir las cifras y sumar los dos números. Por ejemplo,
# los siguientes números no son números de Lychrel:
#    * 56, ya que en un paso se obtiene un capicúa: 56+65=121.
#    * 57, ya que en dos pasos se obtiene un capicúa: 57+75=132,
#      132+231=363
#    * 59, ya que en dos pasos se obtiene un capicúa: 59+95=154,
#      154+451=605, 605+506=1111
#    * 89, ya que en 24 pasos se obtiene un capicúa.
# En esta relación vamos a buscar el primer número de Lychrel.

# ---------------------------------------------------------------------
# Librerías auxiliares                                               --
# ---------------------------------------------------------------------

from itertools import islice
from sys import setrecursionlimit
from typing import Generator, Iterator

from hypothesis import given, settings
from hypothesis import strategies as st

setrecursionlimit(10**6)

# ---------------------------------------------------------------------
# Ejercicio 1. Definir la función
#    esCapicua : (int) -> bool
# tal que esCapicua(x) se verifica si x es capicúa. Por ejemplo,
#    esCapicua(252)  ==  True
#    esCapicua(253)  ==  False
# ---------------------------------------------------------------------

def esCapicua(x: int) -> bool:
    return x == int(str(x)[::-1])

# ---------------------------------------------------------------------
# Ejercicio 2. Definir la función
#    inverso : (int) -> int
# tal que inverso(x) es el número obtenido escribiendo las cifras de x
# en orden inverso. Por ejemplo,
#    inverso(253)  ==  352
# ---------------------------------------------------------------------

def inverso(x: int) -> int:
    return int(str(x)[::-1])

# ---------------------------------------------------------------------
# Ejercicio 3. Definir la función
#    siguiente : (int) -> int
# tal que siguiente(x) es el número obtenido sumándole a x su
# inverso. Por ejemplo,
#    siguiente(253)  ==  605
# ---------------------------------------------------------------------

def siguiente(x: int) -> int:
    return x + inverso(x)

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    busquedaDeCapicua : (int) -> list[int]
# tal que busquedaDeCapicua(x) es la lista de los números tal que el
# primero es x, el segundo es (siguiente de x) y así sucesivamente
# hasta que se alcanza un capicúa. Por ejemplo,
#    busquedaDeCapicua(253)  ==  [253,605,1111]
# ---------------------------------------------------------------------

def busquedaDeCapicua(x: int) -> list[int]:
    if esCapicua(x):
        return [x]
    return [x] + busquedaDeCapicua(siguiente(x))

# ---------------------------------------------------------------------
# Ejercicio 5. Definir la función
#    capicuaFinal : (int) -> int
# tal que (capicuaFinal x) es la capicúa con la que termina la búsqueda
# de capicúa a partir de x. Por ejemplo,
#    capicuaFinal(253)  ==  1111
# ---------------------------------------------------------------------

def capicuaFinal(x: int) -> int:
    return busquedaDeCapicua(x)[-1]

# ---------------------------------------------------------------------
# Ejercicio 6. Definir la función
#    orden : (int) -> int
# tal que orden(x) es el número de veces que se repite el proceso de
# calcular el inverso a partir de x hasta alcanzar un número capicúa.
# Por ejemplo,
#    orden(253)  ==  2
# ---------------------------------------------------------------------

def orden(x: int) -> int:
    if esCapicua(x):
        return 0
    return 1 + orden(siguiente(x))

# ---------------------------------------------------------------------
# Ejercicio 7. Definir la función
#    ordenMayor : (int, int) -> bool:
# tal que ordenMayor(x, n) se verifica si el orden de x es mayor o
# igual que n. Dar la definición sin necesidad de evaluar el orden de
# x. Por ejemplo,
#    >>> ordenMayor(1186060307891929990, 2)
#    True
#    >>> orden(1186060307891929990)
#    261
# ---------------------------------------------------------------------

def ordenMayor(x: int, n: int) -> bool:
    if esCapicua(x):
        return n == 0
    if n <= 0:
        return True
    return ordenMayor(siguiente(x), n - 1)

# ---------------------------------------------------------------------
# Ejercicio 8. Definir la función
#    ordenEntre : (int, int) -> Generator[int, None, None]
# tal que ordenEntre(m, n) es la lista de los elementos cuyo orden es
# mayor o igual que m y menor que n. Por ejemplo,
#    >>> list(islice(ordenEntre(10, 11), 5))
#    [829, 928, 9059, 9149, 9239]
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

def ordenEntre(m: int, n: int) -> Generator[int, None, None]:
    return (x for x in naturales()
            if ordenMayor(x, m) and not ordenMayor(x, n))

# ---------------------------------------------------------------------
# Ejercicio 9. Definir la función
#    menorDeOrdenMayor : (int) -> int
# tal que menorDeOrdenMayor(n) es el menor elemento cuyo orden es
# mayor que n. Por ejemplo,
#    menorDeOrdenMayor(2)   ==  19
#    menorDeOrdenMayor(20)  ==  89
# ---------------------------------------------------------------------

def menorDeOrdenMayor(n: int) -> int:
    return list(islice((x for x in naturales() if ordenMayor(x, n)), 1))[0]

# ---------------------------------------------------------------------
# Ejercicio 10. Definir la función
#    menoresdDeOrdenMayor : (int) -> list[tuple[int, int]]
# tal que (menoresdDeOrdenMayor m) es la lista de los pares (n,x) tales
# que n es un número entre 1 y m y x es el menor elemento de orden
# mayor que n. Por ejemplo,
#    menoresdDeOrdenMayor(5)  ==  [(1,10),(2,19),(3,59),(4,69),(5,79)]
# ---------------------------------------------------------------------

def menoresdDeOrdenMayor(m: int) -> list[tuple[int, int]]:
    return [(n, menorDeOrdenMayor(n)) for n in range(1, m + 1)]

# ---------------------------------------------------------------------
# Ejercicio 11. A la vista de los resultados de (menoresdDeOrdenMayor 5)
# conjeturar sobre la última cifra de menorDeOrdenMayor.
# ---------------------------------------------------------------------

# Solución: La conjetura es que para n mayor que 1, la última cifra de
# (menorDeOrdenMayor n) es 9.

# ---------------------------------------------------------------------
# Ejercicio 12. Decidir con Hypothesis la conjetura.
# ---------------------------------------------------------------------

# La conjetura es
# @given(st.integers(min_value=2, max_value=200))
# def test_menorDeOrdenMayor(n: int) -> None:
#     assert menorDeOrdenMayor(n) % 10 == 9

# La comprobación es
#    src> poetry run pytest -q numeros_de_Lychrel.py
#    E       assert (196 % 10) == 9
#    E        +  where 196 = menorDeOrdenMayor(25)
#    E       Falsifying example: test_menorDeOrdenMayor(
#    E           n=25,
#    E       )

# Se puede comprobar que 25 es un contraejemplo,
#    >>> menorDeOrdenMayor(25)
#    196

# ---------------------------------------------------------------------
# Ejercicio 13. Calcular menoresdDeOrdenMayor(50)
# ---------------------------------------------------------------------

# Solución: El cálculo es
#    λ> menoresdDeOrdenMayor 50
#    [(1,10),(2,19),(3,59),(4,69),(5,79),(6,79),(7,89),(8,89),(9,89),
#     (10,89),(11,89),(12,89),(13,89),(14,89),(15,89),(16,89),(17,89),
#     (18,89),(19,89),(20,89),(21,89),(22,89),(23,89),(24,89),(25,196),
#     (26,196),(27,196),(28,196),(29,196),(30,196),(31,196),(32,196),
#     (33,196),(34,196),(35,196),(36,196),(37,196),(38,196),(39,196),
#     (40,196),(41,196),(42,196),(43,196),(44,196),(45,196),(46,196),
#     (47,196),(48,196),(49,196),(50,196)]

# ---------------------------------------------------------------------
# Ejercicio 14. A la vista de menoresdDeOrdenMayor(50), conjeturar el
# orden de 196.
# ---------------------------------------------------------------------

# Solución: El orden de 196 es infinito y, por tanto, 196 es un número
# del Lychrel.

# ---------------------------------------------------------------------
# Ejercicio 15. Comprobar con Hypothesis la conjetura sobre el orden de
# 196.
# ---------------------------------------------------------------------

# La propiedad es
@settings(deadline=None)
@given(st.integers(min_value=2, max_value=5000))
def test_ordenDe196(n: int) -> None:
    assert ordenMayor(196, n)

# La comprobación es
#    src> poetry run pytest -q numeros_de_Lychrel.py
#    1 passed in 7.74s
