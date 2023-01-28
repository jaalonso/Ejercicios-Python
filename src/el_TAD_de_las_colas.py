# el_TAD_de_las_colas.py
# El tipo abstracto de datos de las colas.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 28-enero-2023
# ======================================================================

# ---------------------------------------------------------------------
# Introducción                                                       --
# ---------------------------------------------------------------------

# El objetivo de esta relación de ejercicios es definir funciones sobre
# el TAD de las colas, utilizando sus implementaciones estudiadas en las
# secciones anteriores.

# ---------------------------------------------------------------------
# Importación de librerías                                           --
# ---------------------------------------------------------------------

from copy import deepcopy
from functools import reduce
from typing import Callable, TypeVar

from hypothesis import assume, given
from hypothesis import strategies as st

from src.TAD.cola import (Cola, colaAleatoria, esVacia, inserta, primero,
                          resto, vacia)

A = TypeVar('A', int, float, str)

# ---------------------------------------------------------------------
# Ejercicio 1.1 Definir la función
#    listaAcola : (list[A]) -> Cola[A]
# tal que listaAcola(xs) es la cola formada por los elementos de xs. Por
# ejemplo,
#    >>> print(listaAcola([3, 2, 5]))
#    3 | 2 | 5
# ---------------------------------------------------------------------

# 1ª solución
def listaAcola(ys: list[A]) -> Cola[A]:
    def aux(xs: list[A]) -> Cola[A]:
        if not xs:
            return vacia()
        return inserta(xs[0], aux(xs[1:]))

    return aux(list(reversed(ys)))

# 2ª solución
def listaAcola2(xs: list[A]) -> Cola[A]:
    p: Cola[A] = Cola()
    for x in xs:
        p.inserta(x)
    return p

# Comprobación de equivalencia
@given(st.lists(st.integers()))
def test_listaAcola(xs: list[int]) -> None:
    assert listaAcola(xs) == listaAcola2(xs)

# ---------------------------------------------------------------------
# Ejercicio 1.2. Definir la función
#    colaAlista : (Cola[A]) -> list[A]
# tal que colaAlista(c) es la lista formada por los elementos de la cola
# c. Por ejemplo,
#    >>> ej = inserta(5, inserta(2, inserta(3, vacia())))
#    >>> colaAlista(ej)
#    [3, 2, 5]
#    >>> print(ej)
#    3 | 2 | 5
# ---------------------------------------------------------------------

# 1ª solución
def colaAlista(c: Cola[A]) -> list[A]:
    if esVacia(c):
        return []
    pc = primero(c)
    rc = resto(c)
    return [pc] + colaAlista(rc)

# 2ª solución
def colaAlista2Aux(c: Cola[A]) -> list[A]:
    if c.esVacia():
        return []
    pc = c.primero()
    c.resto()
    return [pc] + colaAlista2Aux(c)

def colaAlista2(c: Cola[A]) -> list[A]:
    c1 = deepcopy(c)
    return colaAlista2Aux(c1)

# 3ª solución
def colaAlista3Aux(c: Cola[A]) -> list[A]:
    r = []
    while not c.esVacia():
        r.append(c.primero())
        c.resto()
    return r

def colaAlista3(c: Cola[A]) -> list[A]:
    c1 = deepcopy(c)
    return colaAlista3Aux(c1)

# Comprobación de equivalencia
@given(p=colaAleatoria())
def test_colaAlista(p: Cola[int]) -> None:
    assert colaAlista(p) == colaAlista2(p)
    assert colaAlista(p) == colaAlista3(p)

# ---------------------------------------------------------------------
# Ejercicio 1.3. Comprobar con Hypothesis que ambas funciones son
# inversas; es decir,
#    colaAlista(listaAcola(xs)) == xs
#    listaAcola(colaAlista(c))  == c
# ---------------------------------------------------------------------

@given(st.lists(st.integers()))
def test_1_listaAcola(xs: list[int]) -> None:
    assert colaAlista(listaAcola(xs)) == xs

@given(c=colaAleatoria())
def test_2_listaAcola(c: Cola[int]) -> None:
    assert listaAcola(colaAlista(c)) == c

# ---------------------------------------------------------------------
# Ejercicio 2. Definir la función
#    ultimoCola : (Cola[A]) -> A
# tal que ultimoCola(c) es el último elemento de la cola c. Por
# ejemplo:
#    >>> ultimoCola(inserta(3, inserta(5, inserta(2, vacia()))))
#    3
#    >>> ultimoCola(inserta(2, vacia()))
#    2
# ---------------------------------------------------------------------

# 1ª solución
def ultimoCola(c: Cola[A]) -> A:
    if esVacia(c):
        raise ValueError("cola vacia")
    pc = primero(c)
    rc = resto(c)
    if esVacia(rc):
        return pc
    return ultimoCola(rc)

# 2ª solución
def ultimoCola2Aux(c: Cola[A]) -> A:
    if c.esVacia():
        raise ValueError("cola vacia")
    pc = primero(c)
    c.resto()
    if c.esVacia():
        return pc
    return ultimoCola2(c)

def ultimoCola2(c: Cola[A]) -> A:
    _c = deepcopy(c)
    return ultimoCola2Aux(_c)

# 3ª solución
def ultimoCola3(c: Cola[A]) -> A:
    if esVacia(c):
        raise ValueError("cola vacia")
    while not esVacia(resto(c)):
        c = resto(c)
    return primero(c)

# 4ª solución
def ultimoCola4Aux(c: Cola[A]) -> A:
    if c.esVacia():
        raise ValueError("cola vacia")
    r = primero(c)
    while not c.esVacia():
        c.resto()
        if not c.esVacia():
            r = primero(c)
    return r

def ultimoCola4(c: Cola[A]) -> A:
    _c = deepcopy(c)
    return ultimoCola4Aux(_c)

# 5ª solución
def ultimoCola5(c: Cola[A]) -> A:
    if esVacia(c):
        raise ValueError("cola vacia")
    return colaAlista(c)[-1]

# Comprobación de equivalencia
@given(c=colaAleatoria())
def test_ultimoCola(c: Cola[int]) -> None:
    assume(not esVacia(c))
    r = ultimoCola(c)
    assert ultimoCola2(c) == r
    assert ultimoCola3(c) == r
    assert ultimoCola4(c) == r
    assert ultimoCola5(c) == r

# ---------------------------------------------------------------------
# Ejercicio 3. Definir la función
#    longitudCola : (Cola[A]) -> int
# tal que longitudCola(c) es el número de elementos de la cola c. Por
# ejemplo,
#    >>> longitudCola(inserta(4, inserta(2, inserta(5, vacia()))))
#    3
# ---------------------------------------------------------------------

# 1ª solución
def longitudCola1(c: Cola[A]) -> int:
    if esVacia(c):
        return 0
    return 1 + longitudCola1(resto(c))

# 2ª solución
def longitudCola2(c: Cola[A]) -> int:
    return len(colaAlista(c))

# 3ª solución
def longitudCola3Aux(c: Cola[A]) -> int:
    if c.esVacia():
        return 0
    c.resto()
    return 1 + longitudCola3Aux(c)

def longitudCola3(c: Cola[A]) -> int:
    _c = deepcopy(c)
    return longitudCola3Aux(_c)

# 4ª solución
def longitudCola4Aux(c: Cola[A]) -> int:
    r = 0
    while not esVacia(c):
        r = r + 1
        c = resto(c)
    return r

def longitudCola4(c: Cola[A]) -> int:
    _c = deepcopy(c)
    return longitudCola4Aux(_c)

# 5ª solución
def longitudCola5Aux(c: Cola[A]) -> int:
    r = 0
    while not c.esVacia():
        r = r + 1
        c.resto()
    return r

def longitudCola5(c: Cola[A]) -> int:
    _c = deepcopy(c)
    return longitudCola5Aux(_c)

# Comprobación de equivalencia
@given(c=colaAleatoria())
def test_longitudCola_(c: Cola[int]) -> None:
    r = longitudCola1(c)
    assert longitudCola2(c) == r
    assert longitudCola3(c) == r
    assert longitudCola4(c) == r
    assert longitudCola5(c) == r

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    todosVerifican : (Callable[[A], bool], Cola[A]) -> bool
# tal que todosVerifican(p, c) se verifica si todos los elementos de la
# cola c cumplen la propiedad p. Por ejemplo,
#    >>> todosVerifican(lambda x: x > 0, inserta(3, inserta(2, vacia())))
#    True
#    >>> todosVerifican(lambda x: x > 0, inserta(3, inserta(-2, vacia())))
#    False
# ---------------------------------------------------------------------

# 1ª solución
def todosVerifican1(p: Callable[[A], bool], c: Cola[A]) -> bool:
    if esVacia(c):
        return True
    pc = primero(c)
    rc = resto(c)
    return p(pc) and todosVerifican1(p, rc)

# 2ª solución
def todosVerifican2(p: Callable[[A], bool], c: Cola[A]) -> bool:
    return all(p(x) for x in colaAlista(c))

# 3ª solución
def todosVerifican3Aux(p: Callable[[A], bool], c: Cola[A]) -> bool:
    if c.esVacia():
        return True
    pc = c.primero()
    c.resto()
    return p(pc) and todosVerifican3Aux(p, c)

def todosVerifican3(p: Callable[[A], bool], c: Cola[A]) -> bool:
    _c = deepcopy(c)
    return todosVerifican3Aux(p, _c)

# 4ª solución
def todosVerifican4Aux(p: Callable[[A], bool], c: Cola[A]) -> bool:
    if c.esVacia():
        return True
    pc = c.primero()
    c.resto()
    return p(pc) and todosVerifican4Aux(p, c)

def todosVerifican4(p: Callable[[A], bool], c: Cola[A]) -> bool:
    _c = deepcopy(c)
    return todosVerifican4Aux(p, _c)

# 5ª solución
def todosVerifican5Aux(p: Callable[[A], bool], c: Cola[A]) -> bool:
    while not c.esVacia():
        if not p(c.primero()):
            return False
        c.resto()
    return True

def todosVerifican5(p: Callable[[A], bool], c: Cola[A]) -> bool:
    _c = deepcopy(c)
    return todosVerifican5Aux(p, _c)

# Comprobación de equivalencia
@given(c=colaAleatoria())
def test_todosVerifican(c: Cola[int]) -> None:
    r = todosVerifican1(lambda x: x > 0, c)
    assert todosVerifican2(lambda x: x > 0, c) == r
    assert todosVerifican3(lambda x: x > 0, c) == r
    assert todosVerifican4(lambda x: x > 0, c) == r
    assert todosVerifican5(lambda x: x > 0, c) == r

# ---------------------------------------------------------------------
# Ejercicio 5. Definir la función
#    algunoVerifica : (Callable[[A], bool], Cola[A]) -> bool
# tal que algunoVerifica(p, c) se verifica si alguno de los elementos de la
# cola c cumplen la propiedad p. Por ejemplo,
#    >>> algunoVerifica(lambda x: x > 0, inserta(-3, inserta(2, vacia())))
#    True
#    >>> algunoVerifica(lambda x: x > 0, inserta(-3, inserta(-2, vacia())))
#    False
# ---------------------------------------------------------------------

# 1ª solución
def algunoVerifica1(p: Callable[[A], bool], c: Cola[A]) -> bool:
    if esVacia(c):
        return False
    pc = primero(c)
    rc = resto(c)
    return p(pc) or algunoVerifica1(p, rc)

# 2ª solución
def algunoVerifica2(p: Callable[[A], bool], c: Cola[A]) -> bool:
    return any(p(x) for x in colaAlista(c))

# 3ª solución
def algunoVerifica3Aux(p: Callable[[A], bool], c: Cola[A]) -> bool:
    if c.esVacia():
        return False
    pc = c.primero()
    c.resto()
    return p(pc) or algunoVerifica3Aux(p, c)

def algunoVerifica3(p: Callable[[A], bool], c: Cola[A]) -> bool:
    _c = deepcopy(c)
    return algunoVerifica3Aux(p, _c)

# 4ª solución
def algunoVerifica4Aux(p: Callable[[A], bool], c: Cola[A]) -> bool:
    if c.esVacia():
        return False
    pc = c.primero()
    c.resto()
    return p(pc) or algunoVerifica4Aux(p, c)

def algunoVerifica4(p: Callable[[A], bool], c: Cola[A]) -> bool:
    _c = deepcopy(c)
    return algunoVerifica4Aux(p, _c)

# 5ª solución
def algunoVerifica5Aux(p: Callable[[A], bool], c: Cola[A]) -> bool:
    while not c.esVacia():
        if p(c.primero()):
            return True
        c.resto()
    return False

def algunoVerifica5(p: Callable[[A], bool], c: Cola[A]) -> bool:
    _c = deepcopy(c)
    return algunoVerifica5Aux(p, _c)

# Comprobación de equivalencia
@given(c=colaAleatoria())
def test_algunoVerifica(c: Cola[int]) -> None:
    r = algunoVerifica1(lambda x: x > 0, c)
    assert algunoVerifica2(lambda x: x > 0, c) == r
    assert algunoVerifica3(lambda x: x > 0, c) == r
    assert algunoVerifica4(lambda x: x > 0, c) == r
    assert algunoVerifica5(lambda x: x > 0, c) == r

# ---------------------------------------------------------------------
# Ejercicio 6. Definir la función
#    extiendeCola : (Cola[A], Cola[A]) -> Cola[A]
# tal que extiendeCola(c1, c2) es la cola que resulta de poner los
# elementos de la cola c2 a continuación de los de la cola de c1. Por
# ejemplo,
#    >>> ej1 = inserta(3, inserta(2, vacia()))
#    >>> ej2 = inserta(5, inserta(3, inserta(4, vacia())))
#    >>> print(ej1)
#    2 | 3
#    >>> print(ej2)
#    4 | 3 | 5
#    >>> print(extiendeCola(ej1, ej2))
#    2 | 3 | 4 | 3 | 5
#    >>> print(extiendeCola(ej2, ej1))
#    4 | 3 | 5 | 2 | 3
# ---------------------------------------------------------------------

# 1ª solución
def extiendeCola(c1: Cola[A], c2: Cola[A]) -> Cola[A]:
    if esVacia(c2):
        return c1
    pc2 = primero(c2)
    rc2 = resto(c2)
    return extiendeCola(inserta(pc2, c1), rc2)

# 2ª solución
def extiendeCola2(c1: Cola[A], c2: Cola[A]) -> Cola[A]:
    return listaAcola(colaAlista(c1) + colaAlista(c2))

# 3ª solución
def extiendeCola3Aux(c1: Cola[A], c2: Cola[A]) -> Cola[A]:
    if c2.esVacia():
        return c1
    pc2 = c2.primero()
    c2.resto()
    return extiendeCola(inserta(pc2, c1), c2)

def extiendeCola3(c1: Cola[A], c2: Cola[A]) -> Cola[A]:
    _c2 = deepcopy(c2)
    return extiendeCola3Aux(c1, _c2)

# 4ª solución
def extiendeCola4Aux(c1: Cola[A], c2: Cola[A]) -> Cola[A]:
    r = c1
    while not esVacia(c2):
        r = inserta(primero(c2), r)
        c2 = resto(c2)
    return r

def extiendeCola4(c1: Cola[A], c2: Cola[A]) -> Cola[A]:
    _c2 = deepcopy(c2)
    return extiendeCola4Aux(c1, _c2)

# 5ª solución
def extiendeCola5Aux(c1: Cola[A], c2: Cola[A]) -> Cola[A]:
    r = c1
    while not c2.esVacia():
        r.inserta(primero(c2))
        c2.resto()
    return r

def extiendeCola5(c1: Cola[A], c2: Cola[A]) -> Cola[A]:
    _c1 = deepcopy(c1)
    _c2 = deepcopy(c2)
    return extiendeCola5Aux(_c1, _c2)

# Comprobación de equivalencia
@given(c1=colaAleatoria(), c2=colaAleatoria())
def test_extiendeCola(c1: Cola[int], c2: Cola[int]) -> None:
    r = extiendeCola(c1, c2)
    assert extiendeCola2(c1, c2) == r
    assert extiendeCola3(c1, c2) == r
    assert extiendeCola4(c1, c2) == r

# ---------------------------------------------------------------------
# Ejercicio 7. Definir la función
#    intercalaColas : (Cola[A], Cola[A]) -> Cola[A]
# tal que (intercalaColas c1 c2) es la cola formada por los elementos de
# c1 y c2 colocados en una cola, de forma alternativa, empezando por
# los elementos de c1. Por ejemplo,
#    >>> ej1 = inserta(3, inserta(5, vacia()))
#    >>> ej2 = inserta(0, inserta(7, inserta(4, inserta(9, vacia()))))
#    >>> print(intercalaColas(ej1, ej2))
#    5 | 9 | 3 | 4 | 7 | 0
#    >>> print(intercalaColas(ej2, ej1))
#    9 | 5 | 4 | 3 | 7 | 0
# ---------------------------------------------------------------------

# 1ª solución
def intercalaColas(c1: Cola[A], c2: Cola[A]) -> Cola[A]:
    if esVacia(c1):
        return c2
    if esVacia(c2):
        return c1
    pc1 = primero(c1)
    rc1 = resto(c1)
    pc2 = primero(c2)
    rc2 = resto(c2)
    return extiendeCola(inserta(pc2, inserta(pc1, vacia())),
                        intercalaColas(rc1, rc2))

# 2ª solución
def intercalaColas2(c1: Cola[A], c2: Cola[A]) -> Cola[A]:
    def aux(d1: Cola[A], d2: Cola[A], d3: Cola[A]) -> Cola[A]:
        if esVacia(d1):
            return extiendeCola(d3, d2)
        if esVacia(d2):
            return extiendeCola(d3, d1)
        pd1 = primero(d1)
        rd1 = resto(d1)
        pd2 = primero(d2)
        rd2 = resto(d2)
        return aux(rd1, rd2, inserta(pd2, inserta(pd1, d3)))

    return aux(c1, c2, vacia())

# 3ª solución
def intercalaListas(xs: list[A], ys: list[A]) -> list[A]:
    if not xs:
        return ys
    if not ys:
        return xs
    return [xs[0], ys[0]] + intercalaListas(xs[1:], ys[1:])

def intercalaColas3(c1: Cola[A], c2: Cola[A]) -> Cola[A]:
    return listaAcola(intercalaListas(colaAlista(c1), colaAlista(c2)))

# 4ª solución
def intercalaColas4Aux(c1: Cola[A], c2: Cola[A]) -> Cola[A]:
    if c1.esVacia():
        return c2
    if c2.esVacia():
        return c1
    pc1 = c1.primero()
    c1.resto()
    pc2 = c2.primero()
    c2.resto()
    return extiendeCola(inserta(pc2, inserta(pc1, vacia())),
                        intercalaColas4Aux(c1, c2))

def intercalaColas4(c1: Cola[A], c2: Cola[A]) -> Cola[A]:
    _c1 = deepcopy(c1)
    _c2 = deepcopy(c2)
    return intercalaColas4Aux(_c1, _c2)

# 5ª solución
def intercalaColas5Aux(c1: Cola[A], c2: Cola[A]) -> Cola[A]:
    r: Cola[A] = vacia()
    while not esVacia(c1) and not esVacia(c2):
        pc1 = primero(c1)
        c1.resto()
        pc2 = primero(c2)
        c2.resto()
        r = inserta(pc2, inserta(pc1, r))
    if esVacia(c1):
        return extiendeCola(r, c2)
    return extiendeCola(r, c1)

def intercalaColas5(c1: Cola[A], c2: Cola[A]) -> Cola[A]:
    _c1 = deepcopy(c1)
    _c2 = deepcopy(c2)
    return intercalaColas5Aux(_c1, _c2)

# Comprobación de equivalencia
@given(c1=colaAleatoria(), c2=colaAleatoria())
def test_intercalaCola(c1: Cola[int], c2: Cola[int]) -> None:
    r = intercalaColas(c1, c2)
    assert intercalaColas2(c1, c2) == r
    assert intercalaColas3(c1, c2) == r
    assert intercalaColas4(c1, c2) == r
    assert intercalaColas5(c1, c2) == r

# ---------------------------------------------------------------------
# Ejercicio 8. Definir la función
#    agrupaColas : (list[Cola[A]]) -> Cola[A]
# tal que (agrupaColas [c1,c2,c3,...,cn]) es la cola formada mezclando
# las colas de la lista como sigue: mezcla c1 con c2, el resultado con
# c3, el resultado con c4, y así sucesivamente. Por ejemplo,
#    >>> ej1 = inserta(2, inserta(5, vacia()))
#    >>> ej2 = inserta(3, inserta(7, inserta(4, vacia())))
#    >>> ej3 = inserta(9, inserta(0, inserta(1, inserta(6, vacia()))))
#    >>> print(agrupaColas([ej1]))
#    5 | 2
#    >>> print(agrupaColas([ej1, ej2]))
#    5 | 4 | 2 | 7 | 3
#    >>> print(agrupaColas([ej1, ej2, ej3]))
#    5 | 6 | 4 | 1 | 2 | 0 | 7 | 9 | 3
# ---------------------------------------------------------------------

# 1ª solución
def agrupaColas1(cs: list[Cola[A]]) -> Cola[A]:
    if not cs:
        return vacia()
    if len(cs) == 1:
        return cs[0]
    return agrupaColas1([intercalaColas(cs[0], cs[1])] + cs[2:])

# 2ª solución
def agrupaColas2(cs: list[Cola[A]]) -> Cola[A]:
    return reduce(intercalaColas, cs, vacia())

# Comprobación de equivalencia
@given(st.lists(colaAleatoria(), max_size=4))
def test_agrupaCola(cs: list[Cola[int]]) -> None:
    assert agrupaColas1(cs) == agrupaColas2(cs)

# ---------------------------------------------------------------------
# Ejercicio 9. Definir la función
#    perteneceCola : (A, Cola[A]) -> bool
# tal que perteneceCola(x, c) se verifica si x es un elemento de la
# cola p. Por ejemplo,
#    >>> perteneceCola(2, inserta(5, inserta(2, inserta(3, vacia()))))
#    True
#    >>> perteneceCola(4, inserta(5, inserta(2, inserta(3, vacia()))))
#    False
# ---------------------------------------------------------------------

# 1ª solución
def perteneceCola(x: A, c: Cola[A]) -> bool:
    if esVacia(c):
        return False
    return x == primero(c) or perteneceCola(x, resto(c))

# 2ª solución
def perteneceCola2(x: A, c: Cola[A]) -> bool:
    return x in colaAlista(c)

# 3ª solución
def perteneceCola3Aux(x: A, c: Cola[A]) -> bool:
    if c.esVacia():
        return False
    pc = c.primero()
    c.resto()
    return x == pc or perteneceCola3Aux(x, c)

def perteneceCola3(x: A, c: Cola[A]) -> bool:
    c1 = deepcopy(c)
    return perteneceCola3Aux(x, c1)

# 4ª solución
def perteneceCola4Aux(x: A, c: Cola[A]) -> bool:
    while not c.esVacia():
        pc = c.primero()
        c.resto()
        if x == pc:
            return True
    return False

def perteneceCola4(x: A, c: Cola[A]) -> bool:
    c1 = deepcopy(c)
    return perteneceCola4Aux(x, c1)

# Comprobación de equivalencia de las definiciones
@given(x=st.integers(), c=colaAleatoria())
def test_perteneceCola(x: int, c: Cola[int]) -> None:
    r = perteneceCola(x, c)
    assert perteneceCola2(x, c) == r
    assert perteneceCola3(x, c) == r
    assert perteneceCola4(x, c) == r

# ---------------------------------------------------------------------
# Ejercicio 10. Definir la función
#    contenidaCola : (Cola[A], Cola[A]) -> bool
# tal que contenidaCola(c1, c2) se verifica si todos los elementos de la
# cola c1 son elementos de la cola c2. Por ejemplo,
#    >>> ej1 = inserta(3, inserta(2, vacia()))
#    >>> ej2 = inserta(3, inserta(4, vacia()))
#    >>> ej3 = inserta(5, inserta(2, inserta(3, vacia())))
#    >>> contenidaCola(ej1, ej3)
#    True
#    >>> contenidaCola(ej2, ej3)
#    False
# ---------------------------------------------------------------------

# 1ª solución
def contenidaCola1(c1: Cola[A], c2: Cola[A]) -> bool:
    if esVacia(c1):
        return True
    return perteneceCola(primero(c1), c2) and contenidaCola1(resto(c1), c2)

# 2ª solución
def contenidaCola2(c1: Cola[A], c2: Cola[A]) -> bool:
    return set(colaAlista(c1)) <= set(colaAlista(c2))

# 3ª solución
def contenidaCola3Aux(c1: Cola[A], c2: Cola[A]) -> bool:
    if c1.esVacia():
        return True
    pc1 = c1.primero()
    c1.resto()
    return perteneceCola(pc1, c2) and contenidaCola1(c1, c2)

def contenidaCola3(c1: Cola[A], c2: Cola[A]) -> bool:
    _c1 = deepcopy(c1)
    return contenidaCola3Aux(_c1, c2)

# 4ª solución
def contenidaCola4Aux(c1: Cola[A], c2: Cola[A]) -> bool:
    while not c1.esVacia():
        pc1 = c1.primero()
        c1.resto()
        if not perteneceCola(pc1, c2):
            return False
    return True

def contenidaCola4(c1: Cola[A], c2: Cola[A]) -> bool:
    _c1 = deepcopy(c1)
    return contenidaCola4Aux(_c1, c2)

# Comprobación de equivalencia de las definiciones
@given(c1=colaAleatoria(), c2=colaAleatoria())
def test_contenidaCola(c1: Cola[int], c2: Cola[int]) -> None:
    r = contenidaCola1(c1, c2)
    assert contenidaCola2(c1, c2) == r
    assert contenidaCola3(c1, c2) == r
    assert contenidaCola4(c1, c2) == r

# ---------------------------------------------------------------------
# Ejercicio 11. Definir la función
#    prefijoCola : (Cola[A], Cola[A]) -> bool
# tal que prefijoCola(c1, c2) se verifica si la cola c1 es justamente
# un prefijo de la cola c2. Por ejemplo,
#    >>> ej1 = inserta(4, inserta(2, vacia()))
#    >>> ej2 = inserta(5, inserta(4, inserta(2, vacia())))
#    >>> ej3 = inserta(5, inserta(2, inserta(4, vacia())))
#    >>> prefijoCola(ej1, ej2)
#    True
#    >>> prefijoCola(ej1, ej3)
#    False
# ---------------------------------------------------------------------

# 1ª solución
def prefijoCola(c1: Cola[A], c2: Cola[A]) -> bool:
    if esVacia(c1):
        return True
    if esVacia(c2):
        return False
    return primero(c1) == primero(c2) and prefijoCola(resto(c1), resto(c2))

# 2ª solución
def esPrefijoLista(xs: list[A], ys: list[A]) -> bool:
    return ys[:len(xs)] == xs

def prefijoCola2(c1: Cola[A], c2: Cola[A]) -> bool:
    return esPrefijoLista(colaAlista(c1), colaAlista(c2))

# 3ª solución
def prefijoCola3Aux(c1: Cola[A], c2: Cola[A]) -> bool:
    if c1.esVacia():
        return True
    if c2.esVacia():
        return False
    cc1 = c1.primero()
    c1.resto()
    cc2 = c2.primero()
    c2.resto()
    return cc1 == cc2 and prefijoCola3(c1, c2)

def prefijoCola3(c1: Cola[A], c2: Cola[A]) -> bool:
    q1 = deepcopy(c1)
    q2 = deepcopy(c2)
    return prefijoCola3Aux(q1, q2)

# 4ª solución
def prefijoCola4Aux(c1: Cola[A], c2: Cola[A]) -> bool:
    while not c2.esVacia() and not c1.esVacia():
        if c1.primero() != c2.primero():
            return False
        c1.resto()
        c2.resto()
    return c1.esVacia()

def prefijoCola4(c1: Cola[A], c2: Cola[A]) -> bool:
    q1 = deepcopy(c1)
    q2 = deepcopy(c2)
    return prefijoCola4Aux(q1, q2)

# Comprobación de equivalencia de las definiciones
@given(c1=colaAleatoria(), c2=colaAleatoria())
def test_prefijoCola(c1: Cola[int], c2: Cola[int]) -> None:
    r = prefijoCola(c1, c2)
    assert prefijoCola2(c1, c2) == r
    assert prefijoCola3(c1, c2) == r
    assert prefijoCola4(c1, c2) == r

# ---------------------------------------------------------------------
# Ejercicio 12. Definir la función
#    subCola : (Cola[A], Cola[A]) -> bool
# tal que subCola(c1, c2) se verifica si c1 es una subcola de c2. Por
# ejemplo,
#    >>> ej1 = inserta(2, inserta(3, vacia()))
#    >>> ej2 = inserta(7, inserta(2, inserta(3, inserta(5, vacia()))))
#    >>> ej3 = inserta(2, inserta(7, inserta(3, inserta(5, vacia()))))
#    >>> subCola(ej1, ej2)
#    True
#    >>> subCola(ej1, ej3)
#    False
# ---------------------------------------------------------------------

# 1ª solución
def subCola1(c1: Cola[A], c2: Cola[A]) -> bool:
    if esVacia(c1):
        return True
    if esVacia(c2):
        return False
    pc1 = primero(c1)
    rc1 = resto(c1)
    pc2 = primero(c2)
    rc2 = resto(c2)
    if pc1 == pc2:
        return prefijoCola(rc1, rc2) or subCola1(c1, rc2)
    return subCola1(c1, rc2)

# 2ª solución
def sublista(xs: list[A], ys: list[A]) -> bool:
    return any(xs == ys[i:i+len(xs)] for i in range(len(ys) - len(xs) + 1))

def subCola2(c1: Cola[A], c2: Cola[A]) -> bool:
    return sublista(colaAlista(c1), colaAlista(c2))

# 3ª solución
def subCola3Aux(c1: Cola[A], c2: Cola[A]) -> bool:
    if c1.esVacia():
        return True
    if c2.esVacia():
        return False
    if c1.primero() != c2.primero():
        c2.resto()
        return subCola3Aux(c1, c2)
    q1 = deepcopy(c1)
    c1.resto()
    c2.resto()
    return prefijoCola(c1, c2) or subCola3Aux(q1, c2)

def subCola3(c1: Cola[A], c2: Cola[A]) -> bool:
    q1 = deepcopy(c1)
    q2 = deepcopy(c2)
    return subCola3Aux(q1, q2)

# Comprobación de equivalencia de las definiciones
@given(c1=colaAleatoria(), c2=colaAleatoria())
def test_subCola(c1: Cola[int], c2: Cola[int]) -> None:
    r = subCola1(c1, c2)
    assert subCola2(c1, c2) == r
    assert subCola3(c1, c2) == r

# ---------------------------------------------------------------------
# Ejercicio 13. Definir la función
#    ordenadaCola : (Cola[A]) -> bool
# tal que ordenadaCola(c) se verifica si los elementos de la cola c
# están ordenados en orden creciente. Por ejemplo,
#    >>> ordenadaCola(inserta(6, inserta(5, inserta(1, vacia()))))
#    True
#    >>> ordenadaCola(inserta(1, inserta(0, inserta(6, vacia()))))
#    False
# ---------------------------------------------------------------------

# 1ª solución
def ordenadaCola(c: Cola[A]) -> bool:
    if esVacia(c):
        return True
    pc = primero(c)
    rc = resto(c)
    if esVacia(rc):
        return True
    prc = primero(rc)
    return pc <= prc and ordenadaCola(rc)

# 2ª solución
def ordenadaLista(xs: list[A]) -> bool:
    return all((x <= y for (x, y) in zip(xs, xs[1:])))

def ordenadaCola2(p: Cola[A]) -> bool:
    return ordenadaLista(colaAlista(p))

# 3ª solución
def ordenadaCola3Aux(c: Cola[A]) -> bool:
    if c.esVacia():
        return True
    pc = c.primero()
    c.resto()
    if c.esVacia():
        return True
    return pc <= c.primero() and ordenadaCola3Aux(c)

def ordenadaCola3(c: Cola[A]) -> bool:
    _c = deepcopy(c)
    return ordenadaCola3Aux(_c)

# 4ª solución
def ordenadaCola4Aux(c: Cola[A]) -> bool:
    while not c.esVacia():
        pc = c.primero()
        c.resto()
        if not c.esVacia() and pc > c.primero():
            return False
    return True

def ordenadaCola4(c: Cola[A]) -> bool:
    _c = deepcopy(c)
    return ordenadaCola4Aux(_c)

# Comprobación de equivalencia de las definiciones
@given(p=colaAleatoria())
def test_ordenadaCola(p: Cola[int]) -> None:
    r = ordenadaCola(p)
    assert ordenadaCola2(p) == r
    assert ordenadaCola3(p) == r
    assert ordenadaCola4(p) == r

# ---------------------------------------------------------------------
# Ejercicio 14. Definir la función
#    maxCola : (Cola[A]) -> A
# tal que maxCola(c) sea el mayor de los elementos de la cola c. Por
# ejemplo,
#    >>> maxCola(inserta(3, inserta(5, inserta(1, vacia()))))
#    5
# ---------------------------------------------------------------------

# 1ª solución
def maxCola1(c: Cola[A]) -> A:
    pc = primero(c)
    rc = resto(c)
    if esVacia(rc):
        return pc
    return max(pc, maxCola1(rc))

# 2ª solución
def maxCola2(c: Cola[A]) -> A:
    return max(colaAlista(c))

# 3ª solución
def maxCola3Aux(c: Cola[A]) -> A:
    pc = c.primero()
    c.resto()
    if esVacia(c):
        return pc
    return max(pc, maxCola3Aux(c))

def maxCola3(c: Cola[A]) -> A:
    _c = deepcopy(c)
    return maxCola3Aux(_c)

# 4ª solución
def maxCola4Aux(c: Cola[A]) -> A:
    r = c.primero()
    while not esVacia(c):
        pc = c.primero()
        if pc > r:
            r = pc
        c.resto()
    return r

def maxCola4(c: Cola[A]) -> A:
    _c = deepcopy(c)
    return maxCola4Aux(_c)

# Comprobación de equivalencia de las definiciones
@given(c=colaAleatoria())
def test_maxCola(c: Cola[int]) -> None:
    assume(not esVacia(c))
    r = maxCola1(c)
    assert maxCola2(c) == r
    assert maxCola3(c) == r
    assert maxCola4(c) == r

# ---------------------------------------------------------------------
# Comprobaciones
# ---------------------------------------------------------------------

# Las comprobación de las propiedades es
#    > poetry run pytest -v el_TAD_de_las_colas.py
#         test_listaAcola PASSED
#         test_colaAlista PASSED
#         test_1_listaAcola PASSED
#         test_2_listaAcola PASSED
#         test_ultimoCola PASSED
#         test_longitudCola_ PASSED
#         test_todosVerifican PASSED
#         test_algunoVerifica PASSED
#         test_extiendeCola PASSED
#         test_intercalaCola PASSED
#         test_agrupaCola PASSED
#         test_perteneceCola PASSED
#         test_contenidaCola PASSED
#         test_prefijoCola PASSED
#         test_subCola PASSED
#         test_ordenadaCola PASSED
#         test_maxCola PASSED
