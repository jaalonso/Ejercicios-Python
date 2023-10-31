# Division_y_factorizacion_de_polinomios.py
# División y factorización de polinomios mediante la regla de Ruffini.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 31-octubre-2023
# ======================================================================

# ---------------------------------------------------------------------
# Introducción                                                       --
# ---------------------------------------------------------------------

# El objetivo de esta relación de ejercicios es implementar la regla de
# Ruffini y sus aplicaciones utilizando las implementaciones del TAD de
# polinomio estudiadas en los ejercicios anteriores.

# ---------------------------------------------------------------------
# Importación de librerías                                           --
# ---------------------------------------------------------------------

# pylint: disable=unused-import

from typing import TypeVar

from hypothesis import given
from hypothesis import strategies as st

from src.El_TAD_de_polinomios_operaciones import (coeficiente, creaTermino,
                                                  densaApolinomio, multPol,
                                                  polinomioAdensa, sumaPol)
from src.TAD.Polinomio import (Polinomio, consPol, esPolCero, polCero,
                               polinomioAleatorio)

A = TypeVar('A', int, float, complex)

# ---------------------------------------------------------------------
# Ejercicio 1. Definir la función
#    terminoIndep : (Polinomio[A]) -> A
# tal que terminoIndep(p) es el término independiente del polinomio
# p. Por ejemplo,
#    >>> ejPol1 = consPol(4, 3, consPol(2, 5, consPol(0, 3, polCero())))
#    >>> ejPol1
#    3*x^4 + 5*x^2 + 3
#    >>> terminoIndep(ejPol1)
#    3
#    >>> ejPol2 = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
#    >>> ejPol2
#    x^5 + 5*x^2 + 4*x
#    >>> terminoIndep(ejPol2)
#    0
# ---------------------------------------------------------------------

def terminoIndep(p: Polinomio[A]) -> A:
    return coeficiente(0, p)

# ---------------------------------------------------------------------
# Ejercicio 2. Definir la función
#    ruffiniDensa : (int, list[int]) -> list[int]
# tal que ruffiniDensa(r, cs) es la lista de los coeficientes del
# cociente junto con el rsto que resulta de aplicar la regla de Ruffini
# para dividir el polinomio cuya representación densa es cs entre
# x-r. Por ejemplo,
#    ruffiniDensa(2, [1, 2, -1, -2]) == [1, 4, 7, 12]
#    ruffiniDensa(1, [1, 2, -1, -2]) == [1, 3, 2, 0]
# ya que
#      | 1  2  -1  -2           | 1  2  -1  -2
#    2 |    2   8  14         1 |    1   3   2
#    --+--------------        --+-------------
#      | 1  4   7  12           | 1  3   2   0
# ---------------------------------------------------------------------

def ruffiniDensa(r: int, p: list[int]) -> list[int]:
    if not p:
        return []
    res = [p[0]]
    for x in p[1:]:
        res.append(x + r * res[-1])
    return res

# ---------------------------------------------------------------------
# Ejercicio 3. Definir la función
#    cocienteRuffini : (int, Polinomio[int]) -> Polinomio[int]
# tal que cocienteRuffini(r, p) es el cociente de dividir el polinomio p
# por el polinomio x-r. Por ejemplo:
#      >>> ejPol = consPol(3, 1, consPol(2, 2, consPol(1, -1, consPol(0, -2, polCero()))))
#      >>> ejPol
#      x^3 + 2*x^2 + -1*x + -2
#      >>> cocienteRuffini(2, ejPol)
#      x^2 + 4*x + 7
#      >>> cocienteRuffini(-2, ejPol)
#      x^2 + -1
#      >>> cocienteRuffini(3, ejPol)
#      x^2 + 5*x + 14
# ---------------------------------------------------------------------

def cocienteRuffini(r: int, p: Polinomio[int]) -> Polinomio[int]:
    if esPolCero(p):
        return polCero()
    return densaApolinomio(ruffiniDensa(r, polinomioAdensa(p))[:-1])

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    restoRuffini    : (int, Polinomio[int]) -> int
# tal que restoRuffini(r, p) es el resto de dividir el polinomio p por
# el polinomio x-r. Por ejemplo,
#    >>> restoRuffini(2, ejPol)
#    12
#    >>> restoRuffini(-2, ejPol)
#    0
#    >>> restoRuffini(3, ejPol)
#    40
# ---------------------------------------------------------------------

def restoRuffini(r: int, p: Polinomio[int]) -> int:
    if esPolCero(p):
        return 0
    return ruffiniDensa(r, polinomioAdensa(p))[-1]

# ---------------------------------------------------------------------
# Ejercicio 5. Comprobar con Hypothesis que, dado un polinomio p y un
# número entero r, las funciones anteriores verifican la propiedad de la
# división euclídea.
# ---------------------------------------------------------------------

# La propiedad es
@given(r=st.integers(), p=polinomioAleatorio())
def test_diviEuclidea (r: int, p: Polinomio[int]) -> None:
    coci = cocienteRuffini(r, p)
    divi = densaApolinomio([1, -r])
    rest = creaTermino(0, restoRuffini(r, p))
    assert p == sumaPol(multPol(coci, divi), rest)

# La comprobación es
#    >>> test_diviEuclidea()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 6. Definir la función
#    esRaizRuffini : (int, Polinomio[int]) -> bool
# tal que esRaizRuffini(r, p) se verifica si r es una raiz de p, usando
# para ello el regla de Ruffini. Por ejemplo,
#    >>> ejPol = consPol(4, 6, consPol(1, 2, polCero()))
#    >>> ejPol
#    6*x^4 + 2*x
#    >>> esRaizRuffini(0, ejPol)
#    True
#    >>> esRaizRuffini(1, ejPol)
#    False
# ---------------------------------------------------------------------

def esRaizRuffini(r: int, p: Polinomio[int]) -> bool:
    return restoRuffini(r, p) == 0

# ---------------------------------------------------------------------
# Ejercicio 6. Definir la función
#    divisores : (int) -> list[int]
# tal que divisores(n) es la lista de todos los divisores enteros de
# n. Por ejemplo,
#    divisores(4)  == [1, 2, 4, -1, -2, -4]
#    divisores(-6) == [1, 2, 3, 6, -1, -2, -3, -6]
# ---------------------------------------------------------------------

def divisores(n: int) -> list[int]:
    xs = [x for x in range(1, abs(n)+1) if n % x == 0]
    return xs + [-x for x in xs]

# ---------------------------------------------------------------------
# Ejercicio 7. Definir la función
#     raicesRuffini : (Polinomio[int]) -> list[int]
# tal que raicesRuffini(p) es la lista de las raices enteras de p,
# calculadas usando el regla de Ruffini. Por ejemplo,
#    >>> ejPol1 = consPol(4, 3, consPol(2, -5, consPol(0, 3, polCero())))
#    >>> ejPol1
#    3*x^4 + -5*x^2 + 3
#    >>> raicesRuffini(ejPol1)
#    []
#    >>> ejPol2 = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
#    >>> ejPol2
#    x^5 + 5*x^2 + 4*x
#    >>> raicesRuffini(ejPol2)
#    [0, -1]
#    >>> ejPol3 = consPol(4, 6, consPol(1, 2, polCero()))
#    >>> ejPol3
#    6*x^4 + 2*x
#    >>> raicesRuffini(ejPol3)
#    [0]
#    >>> ejPol4 = consPol(3, 1, consPol(2, 2, consPol(1, -1, consPol(0, -2, polCero()))))
#    >>> ejPol4
#    x^3 + 2*x^2 + -1*x + -2
#    >>> raicesRuffini(ejPol4)
#    [1, -1, -2]
# ---------------------------------------------------------------------

def raicesRuffini(p: Polinomio[int]) -> list[int]:
    if esPolCero(p):
        return []
    def aux(rs: list[int]) -> list[int]:
        if not rs:
            return []
        x, *xs = rs
        if esRaizRuffini(x, p):
            return [x] + raicesRuffini(cocienteRuffini(x, p))
        return aux(xs)

    return aux([0] + divisores(terminoIndep(p)))

# ---------------------------------------------------------------------
# Ejercicio 8. Definir la función
#    factorizacion : (Polinomio[int]) -> list[Polinomio[int]]
# tal que factorizacion(p) es la lista de la descomposición del
# polinomio p en factores obtenida mediante el regla de Ruffini. Por
# ejemplo,
#    >>> ejPol1 = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
#    >>> ejPol1
#    x^5 + 5*x^2 + 4*x
#    >>> factorizacion(ejPol1)
#    [1*x, 1*x + 1, x^3 + -1*x^2 + 1*x + 4]
#    >>> ejPol2 = consPol(3, 1, consPol(2, 2, consPol(1, -1, consPol(0, -2, polCero()))))
#    >>> ejPol2
#    x^3 + 2*x^2 + -1*x + -2
#    >>> factorizacion(ejPol2)
#    [1*x + -1, 1*x + 1, 1*x + 2, 1]
# ---------------------------------------------------------------------

def factorizacion(p: Polinomio[int]) -> list[Polinomio[int]]:
    def aux(xs: list[int]) -> list[Polinomio[int]]:
        if not xs:
            return [p]
        r, *rs = xs
        if esRaizRuffini(r, p):
            return [densaApolinomio([1, -r])] + factorizacion(cocienteRuffini(r, p))
        return aux(rs)

    if esPolCero(p):
        return [p]
    return aux([0] + divisores(terminoIndep(p)))

# Comprobación de propiedades
# ===========================

# La comprobación es
#    src> poetry run pytest -v Division_y_factorizacion_de_polinomios.py
#    test_diviEuclidea PASSED
#    ========= 1 passed in 0.32s ==========
