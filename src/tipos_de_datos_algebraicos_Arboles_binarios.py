# tipos_de_datos_algebraicos_Arboles_binarios.py
# Tipos de datos algebraicos: Árboles binarios.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 22-diciembre-2022
# ======================================================================

# ---------------------------------------------------------------------
# Introducción                                                       --
# ---------------------------------------------------------------------

# En esta relación se presenta ejercicios sobre árboles binarios
# definidos como tipos de datos algebraicos.
#
# Los ejercicios corresponden al tema 9 que se encuentran en
#    https://jaalonso.github.io/cursos/i1m/temas/tema-9.html

# ---------------------------------------------------------------------
# Librerías auxiliares
# ---------------------------------------------------------------------

from dataclasses import dataclass
from random import choice, randint
from typing import Callable, Generic, TypeVar

from hypothesis import given
from hypothesis import strategies as st

A = TypeVar("A")
B = TypeVar("B")

# ---------------------------------------------------------------------
# Nota 1. En los siguientes ejercicios se trabajará con los árboles
# binarios definidos como sigue
#    @dataclass
#    class Arbol(Generic[A]):
#        pass
#
#    @dataclass
#    class H(Arbol[A]):
#        x: A
#
#    @dataclass
#    class N(Arbol[A]):
#        x: A
#        i: Arbol[A]
#        d: Arbol[A]
# Por ejemplo, el árbol
#         9
#        / \
#       /   \
#      3     7
#     / \
#    2   4
# se representa por
#    N(9, N(3, H(2), H(4)), H(7))
# ---------------------------------------------------------------------

@dataclass
class Arbol(Generic[A]):
    pass

@dataclass
class H(Arbol[A]):
    x: A

@dataclass
class N(Arbol[A]):
    x: A
    i: Arbol[A]
    d: Arbol[A]

# ---------------------------------------------------------------------
# Nota 2. En las comprobación de propiedades se usará el generador
#    arbolArbitrario(int) -> Arbol[int]
# tal que (arbolArbitrario n) es un árbol aleatorio de orden n. Por ejemplo,
#    >>> arbolArbitrario(4)
#    N(x=2, i=H(x=1), d=H(x=9))
#    >>> arbolArbitrario(4)
#    H(x=10)
#    >>> arbolArbitrario(4)
#    N(x=4, i=N(x=7, i=H(x=4), d=H(x=0)), d=H(x=6))
# ---------------------------------------------------------------------

def arbolArbitrario(n: int) -> Arbol[int]:
    if n <= 1:
        return H(randint(0, 10))
    m = n // 2
    return choice([H(randint(0, 10)),
                   N(randint(0, 10),
                     arbolArbitrario(m),
                     arbolArbitrario(m))])

# ---------------------------------------------------------------------
# Ejercicio 1.1. Definir la función
#    nHojas : (Arbol[A]) -> int
# tal que nHojas(x) es el número de hojas del árbol x. Por ejemplo,
#    nHojas(N(9, N(3, H(2), H(4)), H(7)))  ==  3
# ---------------------------------------------------------------------

def nHojas(a: Arbol[A]) -> int:
    match a:
        case H(_):
            return 1
        case N(_, i, d):
            return nHojas(i) + nHojas(d)
    assert False

# ---------------------------------------------------------------------
# Ejercicio 1.2. Definir la función
#    nNodos : (Arbol[A]) -> int
# tal que nNodos(x) es el número de nodos del árbol x. Por ejemplo,
#      nNodos(N(9, N(3, H(2), H(4)), H(7)))  ==  2
# ---------------------------------------------------------------------

def nNodos(a: Arbol[A]) -> int:
    match a:
        case H(_):
            return 0
        case N(_, i, d):
            return 1 + nNodos(i) + nNodos(d)
    assert False

# ---------------------------------------------------------------------
# Ejercicio 1.3. Comprobar con Hypothesis que en todo árbol binario el
# número de sus hojas es igual al número de sus nodos más uno.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.integers(min_value=1, max_value=10))
def test_nHojas(n: int) -> None:
    a = arbolArbitrario(n)
    assert nHojas(a) == nNodos(a) + 1

# ---------------------------------------------------------------------
# Ejercicio 2.1. Definir la función
#    profundidad : (Arbol[A]) -> int
# tal que profundidad(x) es la profundidad del árbol x. Por ejemplo,
#    profundidad(N(9, N(3, H(2), H(4)), H(7)))              ==  2
#    profundidad(N(9, N(3, H(2), N(1, H(4), H(5))), H(7)))  ==  3
#    profundidad(N(4, N(5, H(4), H(2)), N(3, H(7), H(4))))  ==  2
# ---------------------------------------------------------------------

def profundidad(a: Arbol[A]) -> int:
    match a:
        case H(_):
            return 0
        case N(_, i, d):
            return 1 + max(profundidad(i), profundidad(d))
    assert False

# ---------------------------------------------------------------------
# Ejercicio 2.2. Comprobar con Hypothesis que para todo árbol biario
# x, se tiene que
#    nNodos(x) <= 2^profundidad(x) - 1
# ---------------------------------------------------------------------

# La propiedad es
@given(st.integers(min_value=1, max_value=10))
def test_nHojas(n: int) -> None:
    a = arbolArbitrario(n)
    assert nNodos(a) <= 2 ** profundidad(a) - 1

# ---------------------------------------------------------------------
# Ejercicio 3.1. Definir la función
#    preorden  : (Arbol[A]) -> list[A]
# tal que preorden(x) es la lista correspondiente al recorrido preorden del
# árbol x; es decir, primero visita la raíz del árbol, a continuación
# recorre el subárbol izquierdo y, finalmente, recorre el subárbol
# derecho. Por ejemplo,
#    >>> preorden(N(9, N(3, H(2), H(4)), H(7)))
#    [9, 3, 2, 4, 7]
# ---------------------------------------------------------------------

def preorden(a: Arbol[A]) -> list[A]:
    match a:
        case H(x):
            return [x]
        case N(x, i, d):
            return [x] + preorden(i) + preorden(d)
    assert False

# ---------------------------------------------------------------------
# Ejercicio 3.2. Comprobar con Hypothesis que la longitud de la lista
# obtenida recorriendo un árbol en sentido preorden es igual al número
# de nodos del árbol más el número de hojas.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.integers(min_value=1, max_value=10))
def test_recorrido(n: int) -> None:
    a = arbolArbitrario(n)
    assert len(preorden(a)) == nNodos(a) + nHojas(a)

# ---------------------------------------------------------------------
# Ejercicio 3.3. Definir la función
#    postorden : (Arbol[A]) -> list[A]
# tal que (postorden x) es la lista correspondiente al recorrido postorden
# del árbol x; es decir, primero recorre el subárbol izquierdo, a
# continuación el subárbol derecho y, finalmente, la raíz del
# árbol. Por ejemplo,
#    >>> postorden(N(9, N(3, H(2), H(4)), H(7)))
#    [2, 4, 3, 7, 9]
# ---------------------------------------------------------------------

def postorden(a: Arbol[A]) -> list[A]:
    match a:
        case H(x):
            return [x]
        case N(x, i, d):
            return postorden(i) + postorden(d) + [x]
    assert False

# ---------------------------------------------------------------------
# Ejercicio 4.1. Definir la función
#    espejo : (Arbol[A]) -> Arbol[A]
# tal que espejo(x) es la imagen especular del árbol x. Por ejemplo,
#    espejo(N(9, N(3, H(2), H(4)), H(7))) == N(9, H(7), N(3, H(4), H(2)))
# ---------------------------------------------------------------------

def espejo(a: Arbol[A]) -> Arbol[A]:
    match a:
        case H(x):
            return H(x)
        case N(x, i, d):
            return N(x, espejo(d), espejo(i))
    assert False

# ---------------------------------------------------------------------
# Ejercicio 4.2. Comprobar con Hypothesis que para todo árbol x,
#    espejo(espejo(x)) = x
# ---------------------------------------------------------------------

@given(st.integers(min_value=1, max_value=10))
def test_espejo1(n: int) -> None:
    x = arbolArbitrario(n)
    assert espejo(espejo(x)) == x

# ---------------------------------------------------------------------
# Ejercicio 4.3. Comprobar con Hypothesis que para todo árbol binario
# x, se tiene que
#    reversed(preorden(espejo(x))) = postorden(x)
# ---------------------------------------------------------------------

@given(st.integers(min_value=1, max_value=10))
def test_espejo2(n: int) -> None:
    x = arbolArbitrario(n)
    assert list(reversed(preorden(espejo(x)))) == postorden(x)

# ---------------------------------------------------------------------
# Ejercicio 4.4. Comprobar con Hypothesis que para todo árbol x,
#    postorden(espejo(x)) = reversed(preorden(x))
# ---------------------------------------------------------------------

@given(st.integers(min_value=1, max_value=10))
def test_espejo(n: int) -> None:
    x = arbolArbitrario(n)
    assert postorden(espejo(x)) == list(reversed(preorden(x)))

# ---------------------------------------------------------------------
# Ejercicio 5.1. Definir la función
#    takeArbol : (int, Arbol[A]) -> Arbol[A]
# tal que takeArbol(n, t) es el subárbol de t de profundidad n. Por
# ejemplo,
#    >>> takeArbol(0, N(9, N(3, H(2), H(4)), H(7)))
#    H(9)
#    >>> takeArbol(1, N(9, N(3, H(2), H(4)), H(7)))
#    N(9, H(3), H(7))
#    >>> takeArbol(2, N(9, N(3, H(2), H(4)), H(7)))
#    N(9, N(3, H(2), H(4)), H(7))
#    >>> takeArbol(3, N(9, N(3, H(2), H(4)), H(7)))
#    N(9, N(3, H(2), H(4)), H(7))
# ---------------------------------------------------------------------

def takeArbol(n: int, a: Arbol[A]) -> Arbol[A]:
    match (n, a):
        case (_, H(x)):
            return H(x)
        case (0, N(x, _, _)):
            return H(x)
        case (n, N(x, i, d)):
            return N(x, takeArbol(n - 1, i), takeArbol(n - 1, d))
    assert False

# ---------------------------------------------------------------------
# Ejercicio 5.2. Comprobar con Hypothesis que la profundidad de
# takeArbol(n, x) es menor o igual que n, para todo número natural n y
# todo árbol x.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.integers(min_value=0, max_value=12),
       st.integers(min_value=1, max_value=10))
def test_takeArbol(n: int, m: int) -> None:
    x = arbolArbitrario(m)
    assert profundidad(takeArbol(n, x)) <= n

# ---------------------------------------------------------------------
# Ejercicio 6.2. Definir la función
#    replicateArbol : (int, A) -> Arbol[A]
# tal que (replicate n x) es el árbol de profundidad n cuyos nodos son
# x. Por ejemplo,
#    >>> replicateArbol(0, 5)
#    H(5)
#    >>> replicateArbol(1, 5)
#    N(5, H(5), H(5))
#    >>> replicateArbol(2, 5)
#    N(5, N(5, H(5), H(5)), N(5, H(5), H(5)))
# ---------------------------------------------------------------------

def replicateArbol(n: int, x: A) -> Arbol[A]:
    match n:
        case 0:
            return H(x)
        case n:
            t = replicateArbol(n - 1, x)
            return N(x, t, t)
    assert False

# ---------------------------------------------------------------------
# Ejercicio 6.2. Comprobar con Hypothesis que el número de hojas de
# replicateArbol(n,x) es 2^n, para todo número natural n
# ---------------------------------------------------------------------

# La propiedad es
@given(st.integers(min_value=1, max_value=10),
       st.integers(min_value=1, max_value=10))
def test_nHojas(n: int, x: int) -> None:
    assert nHojas(replicateArbol(n, x)) == 2**n

# ---------------------------------------------------------------------
# Ejercicio 7.1. Definir la función
#    mapArbol : (Callable[[A], B], Arbol[A]) -> Arbol[B]
# tal que mapArbol(f, x) es el árbol obtenido aplicándole a cada nodo de
# x la función f. Por ejemplo,
#    >>> mapArbol(lambda x: 2 * x, N(9, N(3, H(2), H(4)), H(7)))
#    N(x8, N(6, H(4), H(8)), H(14))
# ---------------------------------------------------------------------

def mapArbol(f: Callable[[A], B], a: Arbol[A]) -> Arbol[B]:
    match a:
        case H(x):
            return H(f(x))
        case N(x, i, d):
            return N(f(x), mapArbol(f, i), mapArbol(f, d))
    assert False

# ---------------------------------------------------------------------
# Ejercicio 7.2. Comprobar con Hypothesis que
#    (mapArbol (1+)) . espejo = espejo . (mapArbol (1+))
# ---------------------------------------------------------------------



# La propiedad es
# prop_mapArbol_espejo :: Arbol Int -> Bool
# prop_mapArbol_espejo x =
#     (mapArbol (1+) . espejo) x == (espejo . mapArbol (1+)) x
#
# La comprobación es
#    λ> quickCheck prop_mapArbol_espejo
#    OK, passed 100 tests.
#
# ---------------------------------------------------------------------
# Ejercicio 7.3. Comprobar con Hypothesis que
#    list(map(lambda n: 1 + n, preorden(x))) ==
#    list(preorden(mapArbol(lambda n: 1 + n, x)))
# ---------------------------------------------------------------------

@given(st.integers(min_value=1, max_value=10))
def test_map_preorden(n: int) -> None:
    x = arbolArbitrario(n)
    print(x)
    assert list(map(lambda n: 1 + n, preorden(x))) == \
        list(preorden(mapArbol(lambda n: 1 + n, x)))

# ---------------------------------------------------------------------
# Comprobación de las propiedades
# ---------------------------------------------------------------------

# La comprobación es
#    src> poetry run pytest -q tipos_de_datos_algebraicos_Arboles_binarios.py
#    7 passed in 0.49s
