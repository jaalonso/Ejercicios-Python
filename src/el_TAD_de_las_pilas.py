# el_TAD_de_las_pilas.py
# El tipo abstracto de dato de las pilas.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 16-enero-2023
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Introducción                                                       --
# ---------------------------------------------------------------------

# El objetivo de esta relación de ejercicios es definir funciones sobre
# el tipo abstracto de datos de las pilas, utilizando las
# implementación del ejercicio anterior, cuyo código es
# pilaConListas.py que se encuentra en https://bit.ly/3VVt8by

# ---------------------------------------------------------------------
# Importación de librerías                                           --
# ---------------------------------------------------------------------

from copy import deepcopy
from typing import Callable, TypeVar

from hypothesis import assume, given
from hypothesis import strategies as st

from src.TAD.pilaConListas import (Pila, apila, cima, desapila, esVacia,
                                   pilaAleatoria, vacia)

A = TypeVar('A', int, float, str)

# ---------------------------------------------------------------------
# Ejercicio 1. Definir la función
#    listaApila : (list[A]) -> Pila[A]
# tal que listaApila(xs) es la pila formada por los elementos de xs.
# Por ejemplo,
#    >>> print(listaApila([3, 2, 5]))
#    5 | 2 | 3
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def listaApila(ys: list[A]) -> Pila[A]:
    def aux(xs: list[A]) -> Pila[A]:
        if not xs:
            return vacia()
        return apila(xs[0], aux(xs[1:]))

    return aux(list(reversed(ys)))

# 2ª solución
# ===========

def listaApila2(xs: list[A]) -> Pila[A]:
    p: Pila[A] = Pila()
    for x in xs:
        p.apila(x)
    return p

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.lists(st.integers()))
def test_listaApila(xs: list[int]) -> None:
    assert listaApila(xs) == listaApila2(xs)

# ---------------------------------------------------------------------
# Ejercicio 2. Definir la función
#    pilaALista : (Pila[A]) -> list[A]
# tal que pilaAlista(p) es la lista formada por los elementos de la
# lista p. Por ejemplo,
#    >>> ej = apila(5, apila(2, apila(3, vacia())))
#    >>> pilaAlista(ej)
#    [3, 2, 5]
#    >>> print(ej)
#    5 | 2 | 3
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def pilaAlista(p: Pila[A]) -> list[A]:
    if esVacia(p):
        return []
    cp = cima(p)
    dp = desapila(p)
    return pilaAlista(dp) + [cp]

# 2ª solución
# ===========

def pilaAlista2Aux(p: Pila[A]) -> list[A]:
    if p.esVacia():
        return []
    cp = p.cima()
    p.desapila()
    return pilaAlista2Aux(p) + [cp]

def pilaAlista2(p: Pila[A]) -> list[A]:
    p1 = deepcopy(p)
    return pilaAlista2Aux(p1)

# 3ª solución
# ===========

def pilaAlista3Aux(p: Pila[A]) -> list[A]:
    r = []
    while not p.esVacia():
        r.append(p.cima())
        p.desapila()
    return r[::-1]

def pilaAlista3(p: Pila[A]) -> list[A]:
    p1 = deepcopy(p)
    return pilaAlista3Aux(p1)

# Comprobación de equivalencia
# ============================

@given(p=pilaAleatoria())
def test_pilaAlista(p: Pila[int]) -> None:
    assert pilaAlista(p) == pilaAlista2(p)
    assert pilaAlista(p) == pilaAlista3(p)

# ---------------------------------------------------------------------
# Ejercicio 3. Comprobar con Hypothesis que ambas funciones son
# inversas; es decir,
#    pilaAlista(listaApila(xs)) == xs
#    listaApila(pilaAlista(p))  == p
# ---------------------------------------------------------------------

# La primera propiedad es
@given(st.lists(st.integers()))
def test_1_listaApila(xs: list[int]) -> None:
    assert pilaAlista(listaApila(xs)) == xs

# La segunda propiedad es
@given(p=pilaAleatoria())
def test_2_listaApila(p: Pila[int]) -> None:
    assert listaApila(pilaAlista(p)) == p

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    filtraPila : (Callable[[A], bool], Pila[A]) -> Pila[A]
# tal que filtraPila(p, q) es la pila obtenida con los elementos de
# pila q que verifican el predicado p, en el mismo orden. Por ejemplo,
#    >>> ej = apila(3, apila(4, apila(6, apila(5, vacia()))))
#    >>> print(filtraPila(lambda x: x % 2 == 0, ej))
#    4 | 6
#    >>> print(filtraPila(lambda x: x % 2 == 1, ej))
#    3 | 5
#    >>> print(ej)
#    3 | 4 | 6 | 5
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def filtraPila1(p: Callable[[A], bool], q: Pila[A]) -> Pila[A]:
    if esVacia(q):
        return q
    cq = cima(q)
    dq = desapila(q)
    r = filtraPila1(p, dq)
    if p(cq):
        return apila(cq, r)
    return r

# 2ª solución
# ===========

def filtraPila2(p: Callable[[A], bool], q: Pila[A]) -> Pila[A]:
    return listaApila(list(filter(p, pilaAlista(q))))

# 3ª solución
# ===========

def filtraPila3Aux(p: Callable[[A], bool], q: Pila[A]) -> Pila[A]:
    if q.esVacia():
        return q
    cq = q.cima()
    q.desapila()
    r = filtraPila3Aux(p, q)
    if p(cq):
        r.apila(cq)
    return r

def filtraPila3(p: Callable[[A], bool], q: Pila[A]) -> Pila[A]:
    q1 = deepcopy(q)
    return filtraPila3Aux(p, q1)

# 4ª solución
# ===========

def filtraPila4Aux(p: Callable[[A], bool], q: Pila[A]) -> Pila[A]:
    r: Pila[A] = Pila()
    while not q.esVacia():
        cq = q.cima()
        q.desapila()
        if p(cq):
            r.apila(cq)
    r1: Pila[A] = Pila()
    while not r.esVacia():
        r1.apila(r.cima())
        r.desapila()
    return r1

def filtraPila4(p: Callable[[A], bool], q: Pila[A]) -> Pila[A]:
    q1 = deepcopy(q)
    return filtraPila4Aux(p, q1)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(p=pilaAleatoria())
def test_filtraPila(p: Pila[int]) -> None:
    r = filtraPila1(lambda x: x % 2 == 0, p)
    assert filtraPila2(lambda x: x % 2 == 0, p) == r
    assert filtraPila3(lambda x: x % 2 == 0, p) == r
    assert filtraPila4(lambda x: x % 2 == 0, p) == r

# ---------------------------------------------------------------------
# Ejercicio 5. Definir la función
#    mapPila : (Callable[[A], A], Pila[A]) -> Pila[A]
# tal que mapPila(f, p) es la pila formada con las imágenes por f de
# los elementos de pila p, en el mismo orden. Por ejemplo,
#    >>> ej = apila(5, apila(2, apila(7, vacia())))
#    >>> print(mapPila(lambda x: x + 1, ej))
#    6 | 3 | 8
#    >>> print(ej)
#    5 | 2 | 7
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def mapPila1(f: Callable[[A], A], p: Pila[A]) -> Pila[A]:
    if esVacia(p):
        return p
    cp = cima(p)
    dp = desapila(p)
    return apila(f(cp), mapPila1(f, dp))

# 2ª solución
# ===========

def mapPila2(f: Callable[[A], A], p: Pila[A]) -> Pila[A]:
    return listaApila(list(map(f, pilaAlista(p))))

# 3ª solución
# ===========

def mapPila3Aux(f: Callable[[A], A], p: Pila[A]) -> Pila[A]:
    if p.esVacia():
        return p
    cp = p.cima()
    p.desapila()
    r = mapPila3Aux(f, p)
    r.apila(f(cp))
    return r

def mapPila3(f: Callable[[A], A], p: Pila[A]) -> Pila[A]:
    p1 = deepcopy(p)
    return mapPila3Aux(f, p1)

# 4ª solución
# ===========

def mapPila4Aux(f: Callable[[A], A], p: Pila[A]) -> Pila[A]:
    r: Pila[A] = Pila()
    while not p.esVacia():
        cp = p.cima()
        p.desapila()
        r.apila(f(cp))
    r1: Pila[A] = Pila()
    while not r.esVacia():
        r1.apila(r.cima())
        r.desapila()
    return r1

def mapPila4(f: Callable[[A], A], p: Pila[A]) -> Pila[A]:
    p1 = deepcopy(p)
    return mapPila4Aux(f, p1)

# Comprobación de equivalencia de las definiciones
# ================================================

# La propiedad es
@given(p=pilaAleatoria())
def test_mapPila(p: Pila[int]) -> None:
    r = mapPila1(lambda x: x + 1 == 0, p)
    assert mapPila2(lambda x: x + 1 == 0, p) == r
    assert mapPila3(lambda x: x + 1 == 0, p) == r
    assert mapPila4(lambda x: x + 1 == 0, p) == r

# ---------------------------------------------------------------------
# Ejercicio 6. Definir la función
#    pertenecePila : (A, Pila[A]) -> bool
# tal que pertenecePila(x, p) se verifica si x es un elemento de la
# pila p. Por ejemplo,
#    >>> pertenecePila(2, apila(5, apila(2, apila(3, vacia()))))
#    True
#    >>> pertenecePila(4, apila(5, apila(2, apila(3, vacia()))))
#    False
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def pertenecePila(x: A, p: Pila[A]) -> bool:
    if esVacia(p):
        return False
    cp = cima(p)
    dp = desapila(p)
    return x == cp or pertenecePila(x, dp)

# 2ª solución
# ===========

def pertenecePila2(x: A, p: Pila[A]) -> bool:
    return x in pilaAlista(p)

# 3ª solución
# ===========

def pertenecePila3Aux(x: A, p: Pila[A]) -> bool:
    if p.esVacia():
        return False
    cp = p.cima()
    p.desapila()
    return x == cp or pertenecePila3Aux(x, p)

def pertenecePila3(x: A, p: Pila[A]) -> bool:
    p1 = deepcopy(p)
    return pertenecePila3Aux(x, p1)

# 4ª solución
# ===========

def pertenecePila4Aux(x: A, p: Pila[A]) -> bool:
    while not p.esVacia():
        cp = p.cima()
        p.desapila()
        if x == cp:
            return True
    return False

def pertenecePila4(x: A, p: Pila[A]) -> bool:
    p1 = deepcopy(p)
    return pertenecePila4Aux(x, p1)

# Comprobación de equivalencia de las definiciones
# ================================================

# La propiedad es
@given(x=st.integers(), p=pilaAleatoria())
def test_pertenecePila(x: int, p: Pila[int]) -> None:
    r = pertenecePila(x, p)
    assert pertenecePila2(x, p) == r
    assert pertenecePila3(x, p) == r
    assert pertenecePila4(x, p) == r

# ---------------------------------------------------------------------
# Ejercicio 7. Definir la función
#    contenidaPila : (Pila[A], Pila[A]) -> bool
# tal que contenidaPila(p1, p2) se verifica si todos los elementos de
# de la pila p1 son elementos de la pila p2. Por ejemplo,
#    >>> ej1 = apila(3, apila(2, vacia()))
#    >>> ej2 = apila(3, apila(4, vacia()))
#    >>> ej3 = apila(5, apila(2, apila(3, vacia())))
#    >>> contenidaPila(ej1, ej3)
#    True
#    >>> contenidaPila(ej2, ej3)
#    False
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def contenidaPila1(p1: Pila[A], p2: Pila[A]) -> bool:
    if esVacia(p1):
        return True
    cp1 = cima(p1)
    dp1 = desapila(p1)
    return pertenecePila(cp1, p2) and contenidaPila1(dp1, p2)

# 2ª solución
# ===========

def contenidaPila2(p1: Pila[A], p2: Pila[A]) -> bool:
    return set(pilaAlista(p1)) <= set(pilaAlista(p2))

# 3ª solución
# ===========

def contenidaPila3Aux(p1: Pila[A], p2: Pila[A]) -> bool:
    if p1.esVacia():
        return True
    cp1 = p1.cima()
    p1.desapila()
    return pertenecePila(cp1, p2) and contenidaPila1(p1, p2)

def contenidaPila3(p1: Pila[A], p2: Pila[A]) -> bool:
    q = deepcopy(p1)
    return contenidaPila3Aux(q, p2)

# 4ª solución
# ===========

def contenidaPila4Aux(p1: Pila[A], p2: Pila[A]) -> bool:
    while not p1.esVacia():
        cp1 = p1.cima()
        p1.desapila()
        if not pertenecePila(cp1, p2):
            return False
    return True

def contenidaPila4(p1: Pila[A], p2: Pila[A]) -> bool:
    q = deepcopy(p1)
    return contenidaPila4Aux(q, p2)

# Comprobación de equivalencia de las definiciones
# ================================================

# La propiedad es
@given(p1=pilaAleatoria(), p2=pilaAleatoria())
def test_contenidaPila(p1: Pila[int], p2: Pila[int]) -> None:
    r = contenidaPila1(p1, p2)
    assert contenidaPila2(p1, p2) == r
    assert contenidaPila3(p1, p2) == r
    assert contenidaPila4(p1, p2) == r

# ---------------------------------------------------------------------
# Ejercicio 8. Definir la función
#    prefijoPila : (Pila[A], Pila[A]) -> bool
# tal que prefijoPila(p1, p2) se verifica si la pila p1 es justamente
# un prefijo de la pila p2. Por ejemplo,
#    >>> ej1 = apila(4, apila(2, vacia()))
#    >>> ej2 = apila(4, apila(2, apila(5, vacia())))
#    >>> ej3 = apila(5, apila(4, apila(2, vacia())))
#    >>> prefijoPila(ej1, ej2)
#    True
#    >>> prefijoPila(ej1, ej3)
#    False
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def prefijoPila(p1: Pila[A], p2: Pila[A]) -> bool:
    if esVacia(p1):
        return True
    if esVacia(p2):
        return False
    cp1 = cima(p1)
    dp1 = desapila(p1)
    cp2 = cima(p2)
    dp2 = desapila(p2)
    return cp1 == cp2 and prefijoPila(dp1, dp2)

# 2ª solución
# ===========

def esSufijoLista(xs: list[A], ys: list[A]) -> bool:
    if not xs:
        return True
    return xs == ys[-len(xs):]

def prefijoPila2(p1: Pila[A], p2: Pila[A]) -> bool:
    return esSufijoLista(pilaAlista(p1), pilaAlista(p2))

# 3ª solución
# ===========

def prefijoPila3Aux(p1: Pila[A], p2: Pila[A]) -> bool:
    if p1.esVacia():
        return True
    if p2.esVacia():
        return False
    cp1 = p1.cima()
    p1.desapila()
    cp2 = p2.cima()
    p2.desapila()
    return cp1 == cp2 and prefijoPila3(p1, p2)

def prefijoPila3(p1: Pila[A], p2: Pila[A]) -> bool:
    q1 = deepcopy(p1)
    q2 = deepcopy(p2)
    return prefijoPila3Aux(q1, q2)

# 4ª solución
# ===========

def prefijoPila4Aux(p1: Pila[A], p2: Pila[A]) -> bool:
    while not p2.esVacia() and not p1.esVacia():
        if p1.cima() != p2.cima():
            return False
        p1.desapila()
        p2.desapila()
    return p1.esVacia()

def prefijoPila4(p1: Pila[A], p2: Pila[A]) -> bool:
    q1 = deepcopy(p1)
    q2 = deepcopy(p2)
    return prefijoPila4Aux(q1, q2)

# Comprobación de equivalencia de las definiciones
# ================================================

# La propiedad es
@given(p1=pilaAleatoria(), p2=pilaAleatoria())
def test_prefijoPila(p1: Pila[int], p2: Pila[int]) -> None:
    r = prefijoPila(p1, p2)
    assert prefijoPila2(p1, p2) == r
    assert prefijoPila3(p1, p2) == r
    assert prefijoPila4(p1, p2) == r

# ---------------------------------------------------------------------
# Ejercicio 9. Definir la función
#    subPila : (Pila[A], Pila[A]) -> bool
# tal que subPila(p1, p2) se verifica si p1 es una subpila de p2. Por
# ejemplo,
#    >>> ej1 = apila(2, apila(3, vacia()))
#    >>> ej2 = apila(7, apila(2, apila(3, apila(5, vacia()))))
#    >>> ej3 = apila(2, apila(7, apila(3, apila(5, vacia()))))
#    >>> subPila(ej1, ej2)
#    True
#    >>> subPila(ej1, ej3)
#    False
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def subPila1(p1: Pila[A], p2: Pila[A]) -> bool:
    if esVacia(p1):
        return True
    if esVacia(p2):
        return False
    cp1 = cima(p1)
    dp1 = desapila(p1)
    cp2 = cima(p2)
    dp2 = desapila(p2)
    if cp1 == cp2:
        return prefijoPila(dp1, dp2) or subPila1(p1, dp2)
    return subPila1(p1, dp2)

# 2ª solución
# ===========

# sublista(xs, ys) se verifica si xs es una sublista de ys. Por
# ejemplo,
#    >>> sublista([3,2], [5,3,2,7])
#    True
#    >>> sublista([3,2], [5,3,7,2])
#    False
def sublista(xs: list[A], ys: list[A]) -> bool:
    return any(xs == ys[i:i+len(xs)] for i in range(len(ys) - len(xs) + 1))

def subPila2(p1: Pila[A], p2: Pila[A]) -> bool:
    return sublista(pilaAlista(p1), pilaAlista(p2))

# 3ª solución
# ===========

def subPila3Aux(p1: Pila[A], p2: Pila[A]) -> bool:
    if p1.esVacia():
        return True
    if p2.esVacia():
        return False
    if p1.cima() != p2.cima():
        p2.desapila()
        return subPila3Aux(p1, p2)
    q1 = deepcopy(p1)
    p1.desapila()
    p2.desapila()
    return prefijoPila(p1, p2) or subPila3Aux(q1, p2)

def subPila3(p1: Pila[A], p2: Pila[A]) -> bool:
    q1 = deepcopy(p1)
    q2 = deepcopy(p2)
    return subPila3Aux(q1, q2)

# Comprobación de equivalencia de las definiciones
# ================================================

# La propiedad es
@given(p1=pilaAleatoria(), p2=pilaAleatoria())
def test_subPila(p1: Pila[int], p2: Pila[int]) -> None:
    r = subPila1(p1, p2)
    assert subPila2(p1, p2) == r
    assert subPila3(p1, p2) == r

# ---------------------------------------------------------------------
# Ejercicio 10. Definir la función
#    ordenadaPila : (Pila[A]) -> bool
# tal que ordenadaPila(p) se verifica si los elementos de la pila p
# están ordenados en orden creciente. Por ejemplo,
#    >>> ordenadaPila(apila(1, apila(5, apila(6, vacia()))))
#    True
#    >>> ordenadaPila(apila(1, apila(0, apila(6, vacia()))))
#    False
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def ordenadaPila(p: Pila[A]) -> bool:
    if esVacia(p):
        return True
    cp = cima(p)
    dp = desapila(p)
    if esVacia(dp):
        return True
    cdp = cima(dp)
    return cp <= cdp and ordenadaPila(dp)

# 2ª solución
# ===========

# ordenadaLista(xs, ys) se verifica si xs es una lista ordenada. Por
# ejemplo,
#    >>> ordenadaLista([2, 5, 8])
#    True
#    >>> ordenadalista([2, 8, 5])
#    False
def ordenadaLista(xs: list[A]) -> bool:
    return all((x <= y for (x, y) in zip(xs, xs[1:])))

def ordenadaPila2(p: Pila[A]) -> bool:
    return ordenadaLista(list(reversed(pilaAlista(p))))

# 3ª solución
# ===========

def ordenadaPila3Aux(p: Pila[A]) -> bool:
    if p.esVacia():
        return True
    cp = p.cima()
    p.desapila()
    if p.esVacia():
        return True
    return cp <= p.cima() and ordenadaPila3Aux(p)

def ordenadaPila3(p: Pila[A]) -> bool:
    q = deepcopy(p)
    return ordenadaPila3Aux(q)

# 4ª solución
# ===========

def ordenadaPila4Aux(p: Pila[A]) -> bool:
    while not p.esVacia():
        cp = p.cima()
        p.desapila()
        if not p.esVacia() and cp > p.cima():
            return False
    return True

def ordenadaPila4(p: Pila[A]) -> bool:
    q = deepcopy(p)
    return ordenadaPila4Aux(q)

# Comprobación de equivalencia de las definiciones
# ================================================

# La propiedad es
@given(p=pilaAleatoria())
def test_ordenadaPila(p: Pila[int]) -> None:
    r = ordenadaPila(p)
    assert ordenadaPila2(p) == r
    assert ordenadaPila3(p) == r
    assert ordenadaPila4(p) == r

# ---------------------------------------------------------------------
# Ejercicio 11.1. Definir la función
#    ordenaInserPila : (A, Pila[A]) -> Pila[A]
# tal que ordenaInserPila(p) es la pila obtenida ordenando por
# inserción los los elementos de la pila p. Por ejemplo,
#    >>> print(ordenaInserPila(apila(4, apila(1, apila(3, vacia())))))
#    1 | 3 | 4
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def insertaPila(x: A, p: Pila[A]) -> Pila[A]:
    if esVacia(p):
        return apila(x, p)
    cp = cima(p)
    if x < cp:
        return apila(x, p)
    dp = desapila(p)
    return apila(cp, insertaPila(x, dp))

def ordenaInserPila1(p: Pila[A]) -> Pila[A]:
    if esVacia(p):
        return p
    cp = cima(p)
    dp = desapila(p)
    return insertaPila(cp, ordenaInserPila1(dp))

# 2ª solución
# ===========

def insertaLista(x: A, ys: list[A]) -> list[A]:
    if not ys:
        return [x]
    if x < ys[0]:
        return [x] + ys
    return [ys[0]] + insertaLista(x, ys[1:])

def ordenaInserLista(xs: list[A]) -> list[A]:
    if not xs:
        return []
    return insertaLista(xs[0], ordenaInserLista(xs[1:]))

def ordenaInserPila2(p: Pila[A]) -> Pila[A]:
    return listaApila(list(reversed(ordenaInserLista(pilaAlista(p)))))

# 3ª solución
# ===========

def ordenaInserPila3Aux(p: Pila[A]) -> Pila[A]:
    if p.esVacia():
        return p
    cp = p.cima()
    p.desapila()
    return insertaPila(cp, ordenaInserPila3Aux(p))

def ordenaInserPila3(p: Pila[A]) -> Pila[A]:
    q = deepcopy(p)
    return ordenaInserPila3Aux(q)

# Comprobación de equivalencia de las definiciones
# ================================================

# La propiedad es
@given(p=pilaAleatoria())
def test_ordenaInserPila(p: Pila[int]) -> None:
    r = ordenaInserPila1(p)
    assert ordenaInserPila2(p) == r
    assert ordenaInserPila3(p) == r

# ---------------------------------------------------------------------
# Ejercicio 11.2. Comprobar con Hypothesis que la pila
# ordenaInserPila(p) está ordenada.
# ---------------------------------------------------------------------

# La propiedad es
@given(p=pilaAleatoria())
def test_ordenadaOrdenaInserPila(p: Pila[int]) -> None:
    ordenadaPila(ordenaInserPila1(p))

# ---------------------------------------------------------------------
# Ejercicio 12. Definir la función
#    nubPila : (Pila[A]) -> Pila[A]
# tal que nubPila(p) es la pila con los elementos de p sin repeticiones.
# Por ejemplo,
#    >>> ej = apila(3, apila(1, apila(3, apila(5, vacia()))))
#    >>> print(ej)
#    3 | 1 | 3 | 5
#    >>> print(nubPila1(ej))
#    1 | 3 | 5
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def nubPila1(p: Pila[A]) -> Pila[A]:
    if esVacia(p):
        return p
    cp = cima(p)
    dp = desapila(p)
    if pertenecePila(cp, dp):
        return nubPila1(dp)
    return apila(cp, nubPila1(dp))

# 2ª solución
# ===========

def nub(xs: list[A]) -> list[A]:
    return [x for i, x in enumerate(xs) if x not in xs[:i]]

def nubPila2(p: Pila[A]) -> Pila[A]:
    return listaApila(nub(pilaAlista(p)))

# 3ª solución
# ===========

def nubPila3Aux(p: Pila[A]) -> Pila[A]:
    if p.esVacia():
        return p
    cp = p.cima()
    p.desapila()
    if pertenecePila(cp, p):
        return nubPila3Aux(p)
    return apila(cp, nubPila3Aux(p))

def nubPila3(p: Pila[A]) -> Pila[A]:
    q = deepcopy(p)
    return nubPila3Aux(q)

# Comprobación de equivalencia de las definiciones
# ================================================

# La propiedad es
@given(p=pilaAleatoria())
def test_nubPila(p: Pila[int]) -> None:
    r = nubPila1(p)
    assert nubPila2(p) == r
    assert nubPila3(p) == r

# ---------------------------------------------------------------------
# Ejercicio 13. Definir la función
#    maxPila : (Pila[A]) -> A
# tal que maxPila(p) sea el mayor de los elementos de la pila p. Por
# ejemplo,
#    >>> maxPila(apila(3, apila(5, apila(1, vacia()))))
#    5
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def maxPila1(p: Pila[A]) -> A:
    cp = cima(p)
    dp = desapila(p)
    if esVacia(dp):
        return cp
    return max(cp, maxPila1(dp))

# 2ª solución
# ===========

def maxPila2(p: Pila[A]) -> A:
    return max(pilaAlista(p))

# 3ª solución
# ===========

def maxPila3Aux(p: Pila[A]) -> A:
    cp = p.cima()
    p.desapila()
    if esVacia(p):
        return cp
    return max(cp, maxPila3Aux(p))

def maxPila3(p: Pila[A]) -> A:
    q = deepcopy(p)
    return maxPila3Aux(q)

# 4ª solución
# ===========

def maxPila4Aux(p: Pila[A]) -> A:
    r = p.cima()
    while not esVacia(p):
        cp = p.cima()
        if cp > r:
            r = cp
        p.desapila()
    return r

def maxPila4(p: Pila[A]) -> A:
    q = deepcopy(p)
    return maxPila4Aux(q)

# Comprobación de equivalencia de las definiciones
# ================================================

# La propiedad es
@given(p=pilaAleatoria())
def test_maxPila(p: Pila[int]) -> None:
    assume(not esVacia(p))
    r = maxPila1(p)
    assert maxPila2(p) == r
    assert maxPila3(p) == r
    assert maxPila4(p) == r

# ---------------------------------------------------------------------
# Comprobación de las propiedades
# ---------------------------------------------------------------------

# La comprobación es
#    src> poetry run pytest -v el_TAD_de_las_pilas.py
#       test_listaApila PASSED
#       test_pilaAlista PASSED
#       test_1_listaApila PASSED
#       test_2_listaApila PASSED
#       test_filtraPila PASSED
#       test_mapPila PASSED
#       test_pertenecePila PASSED
#       test_contenidaPila PASSED
#       test_prefijoPila PASSED
#       test_subPila PASSED
#       test_ordenadaPila PASSED
#       test_ordenaInserPila PASSED
#       test_ordenadaOrdenaInserPila PASSED
#       test_nubPila PASSED
#       test_maxPila PASSED
#   15 passed in 2.91s
