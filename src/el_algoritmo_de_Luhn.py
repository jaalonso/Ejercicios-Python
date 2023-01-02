# el_algoritmo_de_Luhn.py
# El algoritmo de Luhn.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 22-diciembre-2022
# ======================================================================

# ---------------------------------------------------------------------
# § Introducción                                                     --
# ---------------------------------------------------------------------

# El objetivo de esta relación es estudiar un algoritmo para validar
# algunos identificadores numéricos como los números de algunas tarjetas
# de crédito; por ejemplo, las de tipo Visa o Master Card.
#
# El algoritmo que vamos a estudiar es el algoritmo de Luhn consistente
# en aplicar los siguientes pasos a los dígitos del número de la
# tarjeta.
#    1. Se invierten los dígitos del número; por ejemplo, [9,4,5,5] se
#       transforma en [5,5,4,9].
#    2. Se duplican los dígitos que se encuentra en posiciones impares
#       (empezando a contar en 0); por ejemplo, [5,5,4,9] se transforma
#       en [5,10,4,18].
#    3. Se suman los dígitos de cada número; por ejemplo, [5,10,4,18]
#       se transforma en 5 + (1 + 0) + 4 + (1 + 8) = 19.
#    4. Si el último dígito de la suma es 0, el número es válido; y no
#       lo es, en caso contrario.
#
# A los números válidos, los llamaremos números de Luhn.

# ---------------------------------------------------------------------
# Ejercicio 1. Definir la función
#    digitosInv : : (int) -> list[int]
# tal que digitosInv(n) es la lista de los dígitos del número n. en orden
#   inverso. Por ejemplo,
#      digitosInv(320274)  ==  [4,7,2,0,2,3]
# ---------------------------------------------------------------------

def digitosInv(n: int) -> list[int]:
    return [int(x) for x in reversed(str(n))]

# ---------------------------------------------------------------------
# Ejercicio 2. Definir la función
#    doblePosImpar : (list[int]) -> list[int]
# tal que doblePosImpar(ns) es la lista obtenida doblando los elementos
# en las posiciones impares (empezando a contar en cero y dejando igual
# a los que están en posiciones pares. Por ejemplo,
#    doblePosImpar([4,9,5,5])    ==  [4,18,5,10]
#    doblePosImpar([4,9,5,5,7])  ==  [4,18,5,10,7]
# ---------------------------------------------------------------------

# 1ª definición
def doblePosImpar(xs: list[int]) -> list[int]:
    if len(xs) <= 1:
        return xs
    return [xs[0]] + [2*xs[1]] + doblePosImpar(xs[2:])

# 2ª definición
def doblePosImpar2(xs: list[int]) -> list[int]:
    def f(n: int, x: int) -> int:
        if n % 2 == 1:
            return 2 * x
        return x
    return [f(n, x) for (n, x) in enumerate(xs)]

# ---------------------------------------------------------------------
# Ejercicio 3. Definir la función
#    sumaDigitos : (list[int]) -> int
# tal que sumaDigitos(ns) es la suma de los dígitos de ns. Por ejemplo,
#      sumaDigitos([10,5,18,4]) = 1 + 0 + 5 + 1 + 8 + 4 =
#                               = 19
# ---------------------------------------------------------------------

def sumaDigitos(ns: list[int]) -> int:
    return sum((sum(digitosInv(n)) for n in ns))

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    ultimoDigito : (int) -> int
# tal que ultimoDigito(n) es el último dígito de n. Por ejemplo,
#      ultimoDigito(123) == 3
#      ultimoDigito(0)   == 0
# ---------------------------------------------------------------------

def ultimoDigito(n: int) -> int:
    return n % 10

# ---------------------------------------------------------------------
# Ejercicio 5. Definir la función
#    luhn :: (int) -> bool
# tal que luhn(n) se verifica si n es un número de Luhn. Por ejemplo,
#      luhn(5594589764218858)  ==  True
#      luhn(1234567898765432)  ==  False
# ---------------------------------------------------------------------

def luhn(n: int) -> bool:
    return ultimoDigito(sumaDigitos(doblePosImpar(digitosInv(n)))) == 0

# ---------------------------------------------------------------------
# § Referencias                                                      --
# ---------------------------------------------------------------------

# Esta relación es una adaptación del primer trabajo del curso "CIS 194:
# Introduction to Haskell (Spring 2015)" de la Univ. de Pensilvania,
# impartido por Noam Zilberstein. El trabajo se encuentra en
# http://www.cis.upenn.edu/~cis194/hw/01-intro.pdf
#
# En el artículo [Algoritmo de Luhn](http://bit.ly/1FGGWsC) de la
# Wikipedia se encuentra información del algoritmo
