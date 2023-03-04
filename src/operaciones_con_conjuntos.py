# operaciones_con_conjuntos.py
# Operaciones con el tipo abstracto de datos de los conjuntos.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 3-marzo-2023
# ======================================================================

# =====================================================================
# Introducción
# =====================================================================

# El objetivo de esta relación de ejercicios es definir operaciones
# entre conjuntos utilizando el tipo abstracto de datos de los
# conjuntos.

# =====================================================================
# Librerías auxiliares
# =====================================================================

from __future__ import annotations

from abc import abstractmethod
from copy import deepcopy
from functools import reduce
from typing import Callable, Protocol, TypeVar

from hypothesis import given
from hypothesis import strategies as st

from src.TAD.conjunto import (Conj, conjuntoAleatorio, elimina, esVacio,
                              inserta, menor, pertenece, vacio)


class Comparable(Protocol):
    @abstractmethod
    def __lt__(self: A, otro: A) -> bool:
        pass

A = TypeVar('A', bound=Comparable)
B = TypeVar('B', bound=Comparable)

# =====================================================================
# Ejercicios
# =====================================================================

# ---------------------------------------------------------------------
# Ejercicio 1. Definir la función
#    listaAconjunto : (list[A]) -> Conj[A]
# tal que
# listaAconjunto(xs) es el conjunto formado por los elementos de xs.
# Por ejemplo,
#    >>> listaAconjunto([3, 2, 5])
#    {2, 3, 5}
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def listaAconjunto(xs: list[A]) -> Conj[A]:
    if not xs:
        return vacio()
    return inserta(xs[0], listaAconjunto(xs[1:]))

# 2ª solución
# ===========

def listaAconjunto2(xs: list[A]) -> Conj[A]:
    return reduce(lambda ys, y: inserta(y, ys), xs, vacio())

# 3ª solución
# ===========

def listaAconjunto3(xs: list[A]) -> Conj[A]:
    c: Conj[A] = Conj()
    for x in xs:
        c.inserta(x)
    return c

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.lists(st.integers()))
def test_listaAconjunto(xs: list[int]) -> None:
    r = listaAconjunto(xs)
    assert listaAconjunto2(xs) == r
    assert listaAconjunto3(xs) == r

# ---------------------------------------------------------------------
# Ejercicio 2. Definir la función
#    conjuntoAlista : (Conj[A]) -> list[A]
# tal que conjuntoAlista(c) es la lista formada por los elementos del
# conjunto c. Por ejemplo,
#    >>> conjuntoAlista(inserta(5, inserta(2, inserta(3, vacio()))))
#    [2, 3, 5]
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def conjuntoAlista(c: Conj[A]) -> list[A]:
    if esVacio(c):
        return []
    mc = menor(c)
    rc = elimina(mc, c)
    return [mc] + conjuntoAlista(rc)

# 2ª solución
# ===========

def conjuntoAlista2Aux(c: Conj[A]) -> list[A]:
    if c.esVacio():
        return []
    mc = c.menor()
    c.elimina(mc)
    return [mc] + conjuntoAlista2Aux(c)

def conjuntoAlista2(c: Conj[A]) -> list[A]:
    c1 = deepcopy(c)
    return conjuntoAlista2Aux(c1)

# 3ª solución
# ===========

def conjuntoAlista3Aux(c: Conj[A]) -> list[A]:
    r = []
    while not c.esVacio():
        mc = c.menor()
        r.append(mc)
        c.elimina(mc)
    return r

def conjuntoAlista3(c: Conj[A]) -> list[A]:
    c1 = deepcopy(c)
    return conjuntoAlista3Aux(c1)

# Comprobación de equivalencia
# ============================

@given(c=conjuntoAleatorio())
def test_conjuntoAlista(c: Conj[int]) -> None:
    r = conjuntoAlista(c)
    assert conjuntoAlista2(c) == r
    assert conjuntoAlista3(c) == r

# ---------------------------------------------------------------------
# Ejercicio 3. Comprobar con Hypothesis que ambas funciones son inversa;
# es decir,
#    conjuntoAlista (listaAconjunto xs) = sorted(list(set(xs)))
#    listaAconjunto (conjuntoAlista c)  = c
# ---------------------------------------------------------------------

# La primera propiedad es
@given(st.lists(st.integers()))
def test_1_listaAconjunto(xs: list[int]) -> None:
    assert conjuntoAlista(listaAconjunto(xs)) == sorted(list(set(xs)))

# La segunda propiedad es
@given(c=conjuntoAleatorio())
def test_2_listaAconjunto(c: Conj[int]) -> None:
    assert listaAconjunto(conjuntoAlista(c)) == c

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    subconjunto :: Ord a => Conj a -> Conj a -> Bool
# tal que (subconjunto c1 c2) se verifica si todos los elementos de c1
# pertenecen a c2. Por ejemplo,
#    >>> ej1 = inserta(5, inserta(2, vacio()))
#    >>> ej2 = inserta(3, inserta(2, inserta(5, vacio())))
#    >>> ej3 = inserta(3, inserta(4, inserta(5, vacio())))
#    >>> subconjunto(ej1, ej2)
#    True
#    >>> subconjunto(ej1, ej3)
#    False
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def subconjunto(c1: Conj[A], c2: Conj[A]) -> bool:
    if esVacio(c1):
        return True
    mc1 = menor(c1)
    rc1 = elimina(mc1, c1)
    return pertenece(mc1, c2) and subconjunto(rc1, c2)

# 2ª solución
# ===========

def subconjunto2(c1: Conj[A], c2: Conj[A]) -> bool:
    return all((pertenece(x, c2) for x in conjuntoAlista(c1)))

# 3ª solución
# ===========

# (sublista xs ys) se verifica si xs es una sublista de ys. Por
# ejemplo,
#    sublista [5, 2] [3, 2, 5]  ==  True
#    sublista [5, 2] [3, 4, 5]  ==  False
def sublista(xs: list[A], ys: list[A]) -> bool:
    if not xs:
        return True
    return xs[0] in ys and sublista(xs[1:], ys)

def subconjunto3(c1: Conj[A], c2: Conj[A]) -> bool:
    return sublista(conjuntoAlista(c1), conjuntoAlista(c2))

# 4ª solución
# ===========

def subconjunto4(c1: Conj[A], c2: Conj[A]) -> bool:
    while not esVacio(c1):
        mc1 = menor(c1)
        if not pertenece(mc1, c2):
            return False
        c1 = elimina(mc1, c1)
    return True

# 5ª solución
# ===========

def subconjunto5Aux(c1: Conj[A], c2: Conj[A]) -> bool:
    while not c1.esVacio():
        mc1 = c1.menor()
        if not c2.pertenece(mc1):
            return False
        c1.elimina(mc1)
    return True

def subconjunto5(c1: Conj[A], c2: Conj[A]) -> bool:
    _c1 = deepcopy(c1)
    return subconjunto5Aux(_c1, c2)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(c1=conjuntoAleatorio(), c2=conjuntoAleatorio())
def test_subconjunto(c1: Conj[int], c2: Conj[int]) -> None:
    r = subconjunto(c1, c2)
    assert subconjunto2(c1, c2) == r
    assert subconjunto3(c1, c2) == r
    assert subconjunto4(c1, c2) == r
    assert subconjunto5(c1, c2) == r

# ---------------------------------------------------------------------
# Ejercicio 5. Definir la función
#    subconjuntoPropio : (Conj[A], Conj[A]) -> bool
# tal subconjuntoPropio(c1, c2) se verifica si c1 es un subconjunto
# propio de c2. Por ejemplo,
#    >>> ej1 = inserta(5, inserta(2, vacio()))
#    >>> ej2 = inserta(3, inserta(2, inserta(5, vacio())))
#    >>> ej3 = inserta(3, inserta(4, inserta(5, vacio())))
#    >>> ej4 = inserta(2, inserta(5, vacio()))
#    >>> subconjuntoPropio(ej1, ej2)
#    True
#    >>> subconjuntoPropio(ej1, ej3)
#    False
#    >>> subconjuntoPropio(ej1, ej4)
#    False
# ---------------------------------------------------------------------

def subconjuntoPropio(c1: Conj[A], c2: Conj[A]) -> bool:
    return subconjunto(c1, c2) and c1 != c2

# ---------------------------------------------------------------------
# Ejercicio 6. Definir la función
#    unitario :: Ord a => a -> Conj a
# tal que (unitario x) es el conjunto {x}. Por ejemplo,
#    unitario 5 == {5}
# ---------------------------------------------------------------------

def unitario(x: A) -> Conj[A]:
    return inserta(x, vacio())

# ---------------------------------------------------------------------
# Ejercicio 7. Definir la función
#    cardinal : (Conj[A]) -> int
# tal que cardinal(c) es el número de elementos del conjunto c. Por
# ejemplo,
#    cardinal(inserta(4, inserta(5, vacio()))) == 2
#    cardinal(inserta(4, inserta(5, inserta(4, vacio())))) == 2
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def cardinal(c: Conj[A]) -> int:
    if esVacio(c):
        return 0
    return 1 + cardinal(elimina(menor(c), c))

# 2ª solución
# ===========

def cardinal2(c: Conj[A]) -> int:
    return len(conjuntoAlista(c))

# 3ª solución
# ===========

def cardinal3(c: Conj[A]) -> int:
    r = 0
    while not esVacio(c):
        r = r + 1
        c = elimina(menor(c), c)
    return r

# 4ª solución
# ===========

def cardinal4Aux(c: Conj[A]) -> int:
    r = 0
    while not c.esVacio():
        r = r + 1
        c.elimina(menor(c))
    return r

def cardinal4(c: Conj[A]) -> int:
    _c = deepcopy(c)
    return cardinal4Aux(_c)

# Comprobación de equivalencia
# ============================

@given(c=conjuntoAleatorio())
def test_cardinal(c: Conj[int]) -> None:
    r = cardinal(c)
    assert cardinal2(c) == r
    assert cardinal3(c) == r
    assert cardinal3(c) == r

# ---------------------------------------------------------------------
# Ejercicio 8. Definir la función
#    union : (Conj[A], Conj[A]) -> Conj[A]
# tal (union c1 c2) es la unión de ambos conjuntos. Por ejemplo,
#    >>> ej1 = inserta(3, inserta(5, vacio()))
#    >>> ej2 = inserta(4, inserta(3, vacio()))
#    >>> union(ej1, ej2)
#    {3, 4, 5}
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def union(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    if esVacio(c1):
        return c2
    mc1 = menor(c1)
    rc1 = elimina(mc1, c1)
    return inserta(mc1, union(rc1, c2))

# 2ª solución
# ===========

def union2(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    return reduce(lambda c, x: inserta(x, c), conjuntoAlista(c1), c2)

# 3ª solución
# ===========

def union3(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    r = c2
    while not esVacio(c1):
        mc1 = menor(c1)
        r = inserta(mc1, r)
        c1 = elimina(mc1, c1)
    return r

# 4ª solución
# ===========

def union4Aux(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    while not c1.esVacio():
        mc1 = menor(c1)
        c2.inserta(mc1)
        c1.elimina(mc1)
    return c2

def union4(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    _c1 = deepcopy(c1)
    _c2 = deepcopy(c2)
    return union4Aux(_c1, _c2)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(c1=conjuntoAleatorio(), c2=conjuntoAleatorio())
def test_union(c1: Conj[int], c2: Conj[int]) -> None:
    r = union(c1, c2)
    assert union2(c1, c2) == r
    assert union3(c1, c2) == r
    assert union4(c1, c2) == r

# ---------------------------------------------------------------------
# Ejercicio 9. Definir la función
#    unionG : (list[Conj[A]]) -> Conj[A]
# tal unionG(cs) calcule la unión de la lista de conjuntos cd. Por
# ejemplo,
#    >>> ej1 = inserta(3, inserta(5, vacio()))
#    >>> ej2 = inserta(5, inserta(6, vacio()))
#    >>> ej3 = inserta(3, inserta(6, vacio()))
#    >>> unionG([ej1, ej2, ej3])
#    {3, 5, 6}
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def unionG(cs: list[Conj[A]]) -> Conj[A]:
    if not cs:
        return vacio()
    return union(cs[0], unionG(cs[1:]))

# 2ª solución
# ===========

def unionG2(cs: list[Conj[A]]) -> Conj[A]:
    return reduce(union, cs, vacio())

# 3ª solución
# ===========

def unionG3(cs: list[Conj[A]]) -> Conj[A]:
    r: Conj[A] = vacio()
    for c in cs:
        r = union(c, r)
    return r

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.lists(conjuntoAleatorio(), max_size=10))
def test_unionG(cs: list[Conj[int]]) -> None:
    r = unionG(cs)
    assert unionG2(cs) == r
    assert unionG3(cs) == r

# ---------------------------------------------------------------------
# Ejercicio 10. Definir la función
#    interseccion : (Conj[A], Conj[A]) -> Conj[A]
# tal que interseccion(c1, c2) es la intersección de los conjuntos c1 y
# c2. Por ejemplo,
#    >>> ej1 = inserta(3, inserta(5, inserta(2, vacio())))
#    >>> ej2 = inserta(2, inserta(4, inserta(3, vacio())))
#    >>> interseccion(ej1, ej2)
#    {2, 3}
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def interseccion(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    if esVacio(c1):
        return vacio()
    mc1 = menor(c1)
    rc1 = elimina(mc1, c1)
    if pertenece(mc1, c2):
        return inserta(mc1, interseccion(rc1, c2))
    return interseccion(rc1, c2)

# 2ª solución
# ===========

def interseccion2(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    return listaAconjunto([x for x in conjuntoAlista(c1)
                           if pertenece(x, c2)])

# 3ª solución
# ===========

def interseccion3(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    r: Conj[A] = vacio()
    while not esVacio(c1):
        mc1 = menor(c1)
        c1 = elimina(mc1, c1)
        if pertenece(mc1, c2):
            r = inserta(mc1, r)
    return r

# 4ª solución
# ===========

def interseccion4Aux(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    r: Conj[A] = vacio()
    while not c1.esVacio():
        mc1 = c1.menor()
        c1.elimina(mc1)
        if c2.pertenece(mc1):
            r.inserta(mc1)
    return r

def interseccion4(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    _c1 = deepcopy(c1)
    return interseccion4Aux(_c1, c2)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(c1=conjuntoAleatorio(), c2=conjuntoAleatorio())
def test_interseccion(c1: Conj[int], c2: Conj[int]) -> None:
    r = interseccion(c1, c2)
    assert interseccion2(c1, c2) == r
    assert interseccion3(c1, c2) == r
    assert interseccion4(c1, c2) == r

# ---------------------------------------------------------------------
# Ejercicio 11. Definir la función
#    interseccionG : (list[Conj[A]]) -> Conj[A]
# tal que interseccionG(cs) es la intersección de la lista de
# conjuntos cs. Por ejemplo,
#    >>> ej1 = inserta(2, inserta(3, inserta(5, vacio())))
#    >>> ej2 = inserta(5, inserta(2, inserta(7, vacio())))
#    >>> ej3 = inserta(3, inserta(2, inserta(5, vacio())))
#    >>> interseccionG([ej1, ej2, ej3])
#    {2, 5}
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def interseccionG(cs: list[Conj[A]]) -> Conj[A]:
    if len(cs) == 1:
        return cs[0]
    return interseccion(cs[0], interseccionG(cs[1:]))

# 2ª solución
# ===========

def interseccionG2(cs: list[Conj[A]]) -> Conj[A]:
    return reduce(interseccion, cs[1:], cs[0])

# 3ª solución
# ===========

def interseccionG3(cs: list[Conj[A]]) -> Conj[A]:
    r = cs[0]
    for c in cs[1:]:
        r = interseccion(c, r)
    return r

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.lists(conjuntoAleatorio(), min_size=1, max_size=10))
def test_interseccionG(cs: list[Conj[int]]) -> None:
    r = interseccionG(cs)
    assert interseccionG2(cs) == r
    assert interseccionG3(cs) == r

# ---------------------------------------------------------------------
# Ejercicio 12. Definir la función
#    disjuntos : (Conj[A], Conj[A]) -> bool
# tal que disjuntos(c1, c2) se verifica si los conjuntos c1 y c2 son
# disjuntos. Por ejemplo,
#    >>> ej1 = inserta(2, inserta(5, vacio()))
#    >>> ej2 = inserta(4, inserta(3, vacio()))
#    >>> ej3 = inserta(5, inserta(3, vacio()))
#    >>> disjuntos(ej1, ej2)
#    True
#    >>> disjuntos(ej1, ej3)
#    False
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def disjuntos(c1: Conj[A], c2: Conj[A]) -> bool:
    return esVacio(interseccion(c1, c2))

# 2ª solución
# ===========

def disjuntos2(c1: Conj[A], c2: Conj[A]) -> bool:
    if esVacio(c1):
        return True
    mc1 = menor(c1)
    rc1 = elimina(mc1, c1)
    if pertenece(mc1, c2):
        return False
    return disjuntos2(rc1, c2)

# 3ª solución
# ===========

def disjuntos3(c1: Conj[A], c2: Conj[A]) -> bool:
    xs = conjuntoAlista(c1)
    ys = conjuntoAlista(c2)
    return all((x not in ys for x in xs))

# 4ª solución
# ===========

def disjuntos4Aux(c1: Conj[A], c2: Conj[A]) -> bool:
    while not esVacio(c1):
        mc1 = menor(c1)
        if pertenece(mc1, c2):
            return False
        c1 = elimina(mc1, c1)
    return True

def disjuntos4(c1: Conj[A], c2: Conj[A]) -> bool:
    _c1 = deepcopy(c1)
    return disjuntos4Aux(_c1, c2)

# 5ª solución
# ===========

def disjuntos5Aux(c1: Conj[A], c2: Conj[A]) -> bool:
    while not c1.esVacio():
        mc1 = c1.menor()
        if c2.pertenece(mc1):
            return False
        c1.elimina(mc1)
    return True

def disjuntos5(c1: Conj[A], c2: Conj[A]) -> bool:
    _c1 = deepcopy(c1)
    return disjuntos5Aux(_c1, c2)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(c1=conjuntoAleatorio(), c2=conjuntoAleatorio())
def test_disjuntos(c1: Conj[int], c2: Conj[int]) -> None:
    r = disjuntos(c1, c2)
    assert disjuntos2(c1, c2) == r
    assert disjuntos3(c1, c2) == r
    assert disjuntos4(c1, c2) == r
    assert disjuntos5(c1, c2) == r

# ---------------------------------------------------------------------
# Ejercicio 13. Definir la función
#    diferencia : (Conj[A], Conj[A]) -> Conj[A]
# tal que diferencia(c1, c2) es el conjunto de los elementos de c1 que
# no son elementos de c2. Por ejemplo,
#    >>> ej1 = inserta(5, inserta(3, inserta(2, inserta(7, vacio()))))
#    >>> ej2 = inserta(7, inserta(4, inserta(3, vacio())))
#    >>> diferencia(ej1, ej2)
#    {2, 5}
#    >>> diferencia(ej2, ej1)
#    {4}
#    >>> diferencia(ej1, ej1)
#    {}
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def diferencia(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    if esVacio(c1):
        return vacio()
    mc1 = menor(c1)
    rc1 = elimina(mc1, c1)
    if pertenece(mc1, c2):
        return diferencia(rc1, c2)
    return inserta(mc1, diferencia(rc1, c2))

# 2ª solución
# ===========

def diferencia2(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    return listaAconjunto([x for x in conjuntoAlista(c1)
                           if not pertenece(x, c2)])

# 3ª solución
# ===========

def diferencia3Aux(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    r: Conj[A] = vacio()
    while not esVacio(c1):
        mc1 = menor(c1)
        if not pertenece(mc1, c2):
            r = inserta(mc1, r)
        c1 = elimina(mc1, c1)
    return r

def diferencia3(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    _c1 = deepcopy(c1)
    return diferencia3Aux(_c1, c2)

# 4ª solución
# ===========

def diferencia4Aux(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    r: Conj[A] = Conj()
    while not c1.esVacio():
        mc1 = c1.menor()
        if not c2.pertenece(mc1):
            r.inserta(mc1)
        c1.elimina(mc1)
    return r

def diferencia4(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    _c1 = deepcopy(c1)
    return diferencia4Aux(_c1, c2)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(c1=conjuntoAleatorio(), c2=conjuntoAleatorio())
def test_diferencia(c1: Conj[int], c2: Conj[int]) -> None:
    r = diferencia(c1, c2)
    assert diferencia2(c1, c2) == r
    assert diferencia3(c1, c2) == r
    assert diferencia4(c1, c2) == r

# ---------------------------------------------------------------------
# Ejercicio 14. Definir la función
#    diferenciaSimetrica : (Conj[A], Conj[A]) -> Conj[A]
# tal que diferenciaSimetrica(c1, c2) es la diferencia simétrica de los
# conjuntos c1 y c2. Por ejemplo,
#    >>> ej1 = inserta(5, inserta(3, inserta(2, inserta(7, vacio()))))
#    >>> ej2 = inserta(7, inserta(4, inserta(3, vacio())))
#    >>> diferenciaSimetrica(ej1, ej2)
#    {2, 4, 5}
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def diferenciaSimetrica(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    return diferencia(union(c1, c2), interseccion(c1, c2))

# 2ª solución
# ===========

def diferenciaSimetrica2(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    xs = conjuntoAlista(c1)
    ys = conjuntoAlista(c2)
    return listaAconjunto([x for x in xs if x not in ys] +
                          [y for y in ys if y not in xs])

# 3ª solución
# ===========

def diferenciaSimetrica3(c1: Conj[A], c2: Conj[A]) -> Conj[A]:
    r: Conj[A] = vacio()
    _c1 = deepcopy(c1)
    _c2 = deepcopy(c2)
    while not esVacio(_c1):
        mc1 = menor(_c1)
        if not pertenece(mc1, c2):
            r = inserta(mc1, r)
        _c1 = elimina(mc1, _c1)
    while not esVacio(_c2):
        mc2 = menor(_c2)
        if not pertenece(mc2, c1):
            r = inserta(mc2, r)
        _c2 = elimina(mc2, _c2)
    return r

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(c1=conjuntoAleatorio(), c2=conjuntoAleatorio())
def test_diferenciaSimetrica(c1: Conj[int], c2: Conj[int]) -> None:
    r = diferenciaSimetrica(c1, c2)
    assert diferenciaSimetrica2(c1, c2) == r
    assert diferenciaSimetrica3(c1, c2) == r

# ---------------------------------------------------------------------
# Ejercicio 15. Definir la función
#    filtra : (Callable[[A], bool], Conj[A]) -> Conj[A]
# tal (filtra p c) es el conjunto de elementos de c que verifican el
# predicado p. Por ejemplo,
#    >>> ej = inserta(5, inserta(4, inserta(7, inserta(2, vacio()))))
#    >>> filtra(lambda x: x % 2 == 0, ej)
#    {2, 4}
#    >>> filtra(lambda x: x % 2 == 1, ej)
#    {5, 7}
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def filtra(p: Callable[[A], bool], c: Conj[A]) -> Conj[A]:
    if esVacio(c):
        return vacio()
    mc = menor(c)
    rc = elimina(mc, c)
    if p(mc):
        return inserta(mc, filtra(p, rc))
    return filtra(p, rc)

# 2ª solución
# ===========

def filtra2(p: Callable[[A], bool], c: Conj[A]) -> Conj[A]:
    return listaAconjunto(list(filter(p, conjuntoAlista(c))))

# 3ª solución
# ===========

def filtra3Aux(p: Callable[[A], bool], c: Conj[A]) -> Conj[A]:
    r: Conj[A] = vacio()
    while not esVacio(c):
        mc = menor(c)
        c = elimina(mc, c)
        if p(mc):
            r = inserta(mc, r)
    return r

def filtra3(p: Callable[[A], bool], c: Conj[A]) -> Conj[A]:
    _c = deepcopy(c)
    return filtra3Aux(p, _c)

# 4ª solución
# ===========

def filtra4Aux(p: Callable[[A], bool], c: Conj[A]) -> Conj[A]:
    r: Conj[A] = Conj()
    while not c.esVacio():
        mc = c.menor()
        c.elimina(mc)
        if p(mc):
            r.inserta(mc)
    return r

def filtra4(p: Callable[[A], bool], c: Conj[A]) -> Conj[A]:
    _c = deepcopy(c)
    return filtra4Aux(p, _c)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(c=conjuntoAleatorio())
def test_filtra(c: Conj[int]) -> None:
    r = filtra(lambda x: x % 2 == 0, c)
    assert filtra2(lambda x: x % 2 == 0, c) == r
    assert filtra3(lambda x: x % 2 == 0, c) == r
    assert filtra4(lambda x: x % 2 == 0, c) == r

# ---------------------------------------------------------------------
# Ejercicio 16. Definir la función
#    particion : (Callable[[A], bool], Conj[A]) -> tuple[Conj[A], Conj[A]]
# tal que particion(c) es el par formado por dos conjuntos: el de sus
# elementos que verifican p y el de los elementos que no lo
# verifica. Por ejemplo,
#    >>> ej = inserta(5, inserta(4, inserta(7, inserta(2, vacio()))))
#    >>> particion(lambda x: x % 2 == 0, ej)
#    ({2, 4}, {5, 7})
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def particion(p: Callable[[A], bool],
              c: Conj[A]) -> tuple[Conj[A], Conj[A]]:
    return (filtra(p, c), filtra(lambda x: not p(x), c))

# 2ª solución
# ===========

def particion2Aux(p: Callable[[A], bool],
                  c: Conj[A]) -> tuple[Conj[A], Conj[A]]:
    r: Conj[A] = vacio()
    s: Conj[A] = vacio()
    while not esVacio(c):
        mc = menor(c)
        c = elimina(mc, c)
        if p(mc):
            r = inserta(mc, r)
        else:
            s = inserta(mc, s)
    return (r, s)

def particion2(p: Callable[[A], bool],
               c: Conj[A]) -> tuple[Conj[A], Conj[A]]:
    _c = deepcopy(c)
    return particion2Aux(p, _c)

# 3ª solución
# ===========

def particion3Aux(p: Callable[[A], bool],
                  c: Conj[A]) -> tuple[Conj[A], Conj[A]]:
    r: Conj[A] = Conj()
    s: Conj[A] = Conj()
    while not c.esVacio():
        mc = c.menor()
        c.elimina(mc)
        if p(mc):
            r.inserta(mc)
        else:
            s.inserta(mc)
    return (r, s)

def particion3(p: Callable[[A], bool],
               c: Conj[A]) -> tuple[Conj[A], Conj[A]]:
    _c = deepcopy(c)
    return particion3Aux(p, _c)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(c=conjuntoAleatorio())
def test_particion(c: Conj[int]) -> None:
    r = particion(lambda x: x % 2 == 0, c)
    assert particion2(lambda x: x % 2 == 0, c) == r
    assert particion3(lambda x: x % 2 == 0, c) == r

# ---------------------------------------------------------------------
# Ejercicio 17. Definir la función
#    divide : (A, Conj[A]) -> tuple[Conj[A], Conj[A]]
# tal que (divide x c) es el par formado por dos subconjuntos de c: el
# de los elementos menores o iguales que x y el de los mayores que x.
# Por ejemplo,
#    >>> divide(5, inserta(7, inserta(2, inserta(8, vacio()))))
#    ({2}, {7, 8})
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def divide(x: A, c: Conj[A]) -> tuple[Conj[A], Conj[A]]:
    if esVacio(c):
        return (vacio(), vacio())
    mc = menor(c)
    rc = elimina(mc, c)
    (c1, c2) = divide(x, rc)
    if mc < x or mc == x:
        return (inserta(mc, c1), c2)
    return (c1, inserta(mc, c2))

# 2ª solución
# ===========

def divide2(x: A, c: Conj[A]) -> tuple[Conj[A], Conj[A]]:
    return particion(lambda y: y < x or y == x, c)

# 3ª solución
# ===========

def divide3Aux(x: A, c: Conj[A]) -> tuple[Conj[A], Conj[A]]:
    r: Conj[A] = vacio()
    s: Conj[A] = vacio()
    while not esVacio(c):
        mc = menor(c)
        c = elimina(mc, c)
        if mc < x or mc == x:
            r = inserta(mc, r)
        else:
            s = inserta(mc, s)
    return (r, s)

def divide3(x: A, c: Conj[A]) -> tuple[Conj[A], Conj[A]]:
    _c = deepcopy(c)
    return divide3Aux(x, _c)

# 4ª solución
# ===========

def divide4Aux(x: A, c: Conj[A]) -> tuple[Conj[A], Conj[A]]:
    r: Conj[A] = Conj()
    s: Conj[A] = Conj()
    while not c.esVacio():
        mc = c.menor()
        c.elimina(mc)
        if mc < x or mc == x:
            r.inserta(mc)
        else:
            s.inserta(mc)
    return (r, s)

def divide4(x: A, c: Conj[A]) -> tuple[Conj[A], Conj[A]]:
    _c = deepcopy(c)
    return divide4Aux(x, _c)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(x=st.integers(), c=conjuntoAleatorio())
def test_divide(x: int, c: Conj[int]) -> None:
    r = divide(x, c)
    assert divide2(x, c) == r
    assert divide3(x, c) == r
    assert divide4(x, c) == r

# ---------------------------------------------------------------------
# Ejercicio 18. Definir la función
#    mapC : (Callable[[A], B], Conj[A]) -> Conj[B]
# tal que map(f, c) es el conjunto formado por las imágenes de los
# elementos de c, mediante f. Por ejemplo,
#    >>> mapC(lambda x: 2 * x, inserta(3, inserta(1, vacio())))
#    {2, 6}
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def mapC(f: Callable[[A], B], c: Conj[A]) -> Conj[B]:
    if esVacio(c):
        return vacio()
    mc = menor(c)
    rc = elimina(mc, c)
    return inserta(f(mc), mapC(f, rc))

# 2ª solución
# ===========

def mapC2(f: Callable[[A], B], c: Conj[A]) -> Conj[B]:
    return listaAconjunto(list(map(f, conjuntoAlista(c))))

# 3ª solución
# ===========

def mapC3Aux(f: Callable[[A], B], c: Conj[A]) -> Conj[B]:
    r: Conj[B] = vacio()
    while not esVacio(c):
        mc = menor(c)
        c = elimina(mc, c)
        r = inserta(f(mc), r)
    return r

def mapC3(f: Callable[[A], B], c: Conj[A]) -> Conj[B]:
    _c = deepcopy(c)
    return mapC3Aux(f, _c)

# 4ª solución
# ===========

def mapC4Aux(f: Callable[[A], B], c: Conj[A]) -> Conj[B]:
    r: Conj[B] = Conj()
    while not c.esVacio():
        mc = c.menor()
        c.elimina(mc)
        r.inserta(f(mc))
    return r

def mapC4(f: Callable[[A], B], c: Conj[A]) -> Conj[B]:
    _c = deepcopy(c)
    return mapC4Aux(f, _c)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(c=conjuntoAleatorio())
def test_mapPila(c: Conj[int]) -> None:
    r = mapC(lambda x: 2 * x, c)
    assert mapC2(lambda x: 2 * x, c) == r
    assert mapC3(lambda x: 2 * x, c) == r
    assert mapC4(lambda x: 2 * x, c) == r

# ---------------------------------------------------------------------
# Ejercicio 19. Definir la función
#    todos : (Callable[[A], bool], Conj[A]) -> bool
# tal que todos(p, c) se verifica si todos los elemsntos de c
# verifican el predicado p.  Por ejemplo,
#    >>> todos(lambda x: x % 2 == 0, inserta(4, inserta(6, vacio())))
#    True
#    >>> todos(lambda x: x % 2 == 0, inserta(4, inserta(7, vacio())))
#    False
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def todos(p: Callable[[A], bool], c: Conj[A]) -> bool:
    if esVacio(c):
        return True
    mc = menor(c)
    rc = elimina(mc, c)
    return p(mc) and todos(p, rc)

# 2ª solución
# ===========

def todos2(p: Callable[[A], bool], c: Conj[A]) -> bool:
    return all(p(x) for x in conjuntoAlista(c))

# 3ª solución
# ===========

def todos3Aux(p: Callable[[A], bool], c: Conj[A]) -> bool:
    while not esVacio(c):
        mc = menor(c)
        c = elimina(mc, c)
        if not p(mc):
            return False
    return True

def todos3(p: Callable[[A], bool], c: Conj[A]) -> bool:
    _c = deepcopy(c)
    return todos3Aux(p, _c)

# 4ª solución
# ===========

def todos4Aux(p: Callable[[A], bool], c: Conj[A]) -> bool:
    while not c.esVacio():
        mc = c.menor()
        c.elimina(mc)
        if not p(mc):
            return False
    return True

def todos4(p: Callable[[A], bool], c: Conj[A]) -> bool:
    _c = deepcopy(c)
    return todos4Aux(p, _c)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(c=conjuntoAleatorio())
def test_todos(c: Conj[int]) -> None:
    r = todos(lambda x: x % 2 == 0, c)
    assert todos2(lambda x: x % 2 == 0, c) == r
    assert todos3(lambda x: x % 2 == 0, c) == r
    assert todos4(lambda x: x % 2 == 0, c) == r

# ---------------------------------------------------------------------
# Ejercicio 20. Definir la función
#    algunos : algunos(Callable[[A], bool], Conj[A]) -> bool
# tal que algunos(p, c) se verifica si algún elemento de c verifica el
# predicado p. Por ejemplo,
#    >>> algunos(lambda x: x % 2 == 0, inserta(4, inserta(7, vacio())))
#    True
#    >>> algunos(lambda x: x % 2 == 0, inserta(3, inserta(7, vacio())))
#    False
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def algunos(p: Callable[[A], bool], c: Conj[A]) -> bool:
    if esVacio(c):
        return False
    mc = menor(c)
    rc = elimina(mc, c)
    return p(mc) or algunos(p, rc)

# 2ª solución
# ===========

def algunos2(p: Callable[[A], bool], c: Conj[A]) -> bool:
    return any(p(x) for x in conjuntoAlista(c))

# 3ª solución
# ===========

def algunos3Aux(p: Callable[[A], bool], c: Conj[A]) -> bool:
    while not esVacio(c):
        mc = menor(c)
        c = elimina(mc, c)
        if p(mc):
            return True
    return False

def algunos3(p: Callable[[A], bool], c: Conj[A]) -> bool:
    _c = deepcopy(c)
    return algunos3Aux(p, _c)

# 4ª solución
# ===========

def algunos4Aux(p: Callable[[A], bool], c: Conj[A]) -> bool:
    while not c.esVacio():
        mc = c.menor()
        c.elimina(mc)
        if p(mc):
            return True
    return False

def algunos4(p: Callable[[A], bool], c: Conj[A]) -> bool:
    _c = deepcopy(c)
    return algunos4Aux(p, _c)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(c=conjuntoAleatorio())
def test_algunos(c: Conj[int]) -> None:
    r = algunos(lambda x: x % 2 == 0, c)
    assert algunos2(lambda x: x % 2 == 0, c) == r
    assert algunos3(lambda x: x % 2 == 0, c) == r
    assert algunos4(lambda x: x % 2 == 0, c) == r

# ---------------------------------------------------------------------
# Ejercicio 21. Definir la función
#    productoC : (A, Conj[B]) -> Any
# tal que (productoC c1 c2) es el producto cartesiano de los
# conjuntos c1 y c2. Por ejemplo,
#    >>> ej1 = inserta(2, inserta(5, vacio()))
#    >>> ej2 = inserta(9, inserta(4, inserta(3, vacio())))
#    >>> productoC(ej1, ej2)
#    {(2, 3), (2, 4), (2, 9), (5, 3), (5, 4), (5, 9)}
# ---------------------------------------------------------------------

# 1ª solución
# ===========

# (agrega x c) es el conjunto de los pares de x con los elementos de
# c. Por ejemplo,
#    >>> agrega(2, inserta(9, inserta(4, inserta(3, vacio()))))
#    {(2, 3), (2, 4), (2, 9)}
def agrega(x: A, c: Conj[B]) -> Conj[tuple[A, B]]:
    if esVacio(c):
        return vacio()
    mc = menor(c)
    rc = elimina(mc, c)
    return inserta((x, mc), agrega(x, rc))

def productoC(c1: Conj[A], c2: Conj[B]) -> Conj[tuple[A, B]]:
    if esVacio(c1):
        return vacio()
    mc1 = menor(c1)
    rc1 = elimina(mc1, c1)
    return union(agrega(mc1, c2), productoC(rc1, c2))

# 2ª solución
# ===========

def productoC2(c1: Conj[A], c2: Conj[B]) -> Conj[tuple[A, B]]:
    xs = conjuntoAlista(c1)
    ys = conjuntoAlista(c2)
    return reduce(lambda bs, a: inserta(a, bs), [(x,y) for x in xs for y in ys], vacio())

# 3ª solución
# ===========

def productoC3(c1: Conj[A], c2: Conj[B]) -> Conj[tuple[A, B]]:
    xs = conjuntoAlista(c1)
    ys = conjuntoAlista(c2)
    return listaAconjunto([(x,y) for x in xs for y in ys])

# 4ª solución
# ===========

def agrega4Aux(x: A, c: Conj[B]) -> Conj[tuple[A, B]]:
    r: Conj[tuple[A, B]] = vacio()
    while not esVacio(c):
        mc = menor(c)
        c = elimina(mc, c)
        r = inserta((x, mc), r)
    return r

def agrega4(x: A, c: Conj[B]) -> Conj[tuple[A, B]]:
    _c = deepcopy(c)
    return agrega4Aux(x, _c)

def productoC4(c1: Conj[A], c2: Conj[B]) -> Conj[tuple[A, B]]:
    r: Conj[tuple[A, B]] = vacio()
    while not esVacio(c1):
        mc1 = menor(c1)
        c1 = elimina(mc1, c1)
        r = union(agrega4(mc1, c2), r)
    return r

# 5ª solución
# ===========

def agrega5Aux(x: A, c: Conj[B]) -> Conj[tuple[A, B]]:
    r: Conj[tuple[A, B]] = Conj()
    while not c.esVacio():
        mc = c.menor()
        c.elimina(mc)
        r.inserta((x, mc))
    return r

def agrega5(x: A, c: Conj[B]) -> Conj[tuple[A, B]]:
    _c = deepcopy(c)
    return agrega5Aux(x, _c)

def productoC5(c1: Conj[A], c2: Conj[B]) -> Conj[tuple[A, B]]:
    r: Conj[tuple[A, B]] = Conj()
    while not c1.esVacio():
        mc1 = c1.menor()
        c1.elimina(mc1)
        r = union(agrega5(mc1, c2), r)
    return r

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(c1=conjuntoAleatorio(), c2=conjuntoAleatorio())
def test_productoC(c1: Conj[int], c2: Conj[int]) -> None:
    r = productoC(c1, c2)
    assert productoC2(c1, c2) == r
    assert productoC3(c1, c2) == r
    assert productoC4(c1, c2) == r
# ---------------------------------------------------------------------

# La comprobación de las propiedades es
#    > poetry run pytest -v operaciones_con_conjuntos.py
