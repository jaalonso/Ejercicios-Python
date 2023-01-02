# tipos_de_datos_algebraicos_Arboles.py
# Tipos de datos algebraicos: Árboles.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 1-enero-2023
# ======================================================================

# ---------------------------------------------------------------------
# Introducción                                                       --
# ---------------------------------------------------------------------

# En esta relación se presenta ejercicios sobre distintos tipos de
# datos algebraicos. Concretamente,
# + Árboles binarios:
#   + Árboles binarios con valores en los nodos.
#   + Árboles binarios con valores en las hojas.
#   + Árboles binarios con valores en las hojas y en los nodos.
#   + Árboles booleanos.
# + Árboles generales
#
# Los ejercicios corresponden al tema 9 que se encuentran en
#    https://jaalonso.github.io/cursos/i1m/temas/tema-9.html

# ---------------------------------------------------------------------
# Librerías auxiliares
# ---------------------------------------------------------------------

from dataclasses import dataclass
from math import ceil, sqrt
from typing import Callable, Generic, TypeVar

A = TypeVar("A")
B = TypeVar("B")

# ---------------------------------------------------------------------
# Ejercicio 1.1. Los árboles binarios con valores en los nodos se pueden
# definir por
#    @dataclass
#    class Arbol1(Generic[A]):
#        pass
#
#    @dataclass
#    class H1(Arbol1[A]):
#        pass
#
#    @dataclass
#    class N1(Arbol1[A]):
#        x: A
#        i: Arbol1
#        d: Arbol1
# Por ejemplo, el árbol
#         9
#        / \
#       /   \
#      8     6
#     / \   / \
#    3   2 4   5
# se puede representar por
#    N1(9,
#      N1(8, N1(3, H1(), H1()), N1(2, H1(), H1())),
#      N1(6, N1(4, H1(), H1()), N1(5, H1(), H1())))
#
# Definir la función
#    sumaArbol : (Arbol1) -> int
# tal sumaArbol(x) es la suma de los valores que hay en el árbol x.
# Por ejemplo,
#    >>> sumaArbol(N1(2,
#                     N1(5, N1(3, H1(), H1()), N1(7, H1(), H1())),
#                     N1(4, H1(), H1())))
#    21
# ---------------------------------------------------------------------

@dataclass
class Arbol1(Generic[A]):
    pass

@dataclass
class H1(Arbol1[A]):
    pass

@dataclass
class N1(Arbol1[A]):
    x: A
    i: Arbol1
    d: Arbol1

def sumaArbol(a: Arbol1[int]) -> int:
    match a:
        case H1():
            return 0
        case N1(x, i, d):
            return x + sumaArbol(i) + sumaArbol(d)
    assert False

# ---------------------------------------------------------------------
# Ejercicio 1.2. Definir la función
#    mapArbol : (Callable[[A], B], Arbol1[A]) -> Arbol1[B]
# tal que mapArbol(f, t) es el árbolo obtenido aplicando la función f a
# los elementos del árbol t. Por ejemplo,
#    >>> mapArbol(lambda x: 1 + x,
#                 N1(2,
#                   N1(5, N1(3, H1(), H1()), N1(7, H1(), H1())),
#                   N1(4, H1(), H1())))
#    N1(3, N1(6, N1(4, H1(), H1()), N1(8, H1(), H1())), N1(5, H1(), H1()))
# ---------------------------------------------------------------------

def mapArbol(f: Callable[[A], B], a: Arbol1[A]) -> Arbol1[B]:
    match a:
        case H1():
            return H1()
        case N1(x, i, d):
            return N1(f(x), mapArbol(f, i), mapArbol(f, d))
    assert False

# ---------------------------------------------------------------------
# Ejercicio 1.3. Definir la función
#    ramaIzquierda : (Arbol1[A]) -> list[A]
# tal que ramaIzquierda(a) es la lista de los valores de los nodos de
# la rama izquierda del árbol a. Por ejemplo,
#    >>> ramaIzquierda(N1(2,
#                        N1(5, N1(3, H1(), H1()), N1(7, H1(), H1())),
#                        N1(4, H1(), H1())))
#    [2, 5, 3]
# ---------------------------------------------------------------------

def ramaIzquierda(a: Arbol1[A]) -> list[A]:
    match a:
        case H1():
            return []
        case N1(x, i, _):
            return [x] + ramaIzquierda(i)
    assert False

# ---------------------------------------------------------------------
# Ejercicio 1.4. Diremos que un árbol está balanceado si para cada nodo
# la diferencia entre el número de nodos de sus subárboles izquierdo y
# derecho es menor o igual que uno.
#
# Definir la función
#    balanceado : (Arbol1[A]) -> bool
# tal que balanceado(a) se verifica si el árbol a está balanceado. Por
# ejemplo,
#    >>> balanceado(N1(5, H1(), N1(3, H1(), H1())))
#    True
#    >>> balanceado(N1(4,
#                     N1(3, N1(2, H1(), H1()), H1()),
#                     N1(5, H1(), N1(6, H1(), N1(7, H1(), H1())))))
#    False
# ---------------------------------------------------------------------

def numeroNodos(a: Arbol1[A]) -> int:
    match a:
        case H1():
            return 0
        case N1(_, i, d):
            return 1 + numeroNodos(i) + numeroNodos(d)
    assert False

def balanceado(a: Arbol1[A]) -> bool:
    match a:
        case H1():
            return True
        case N1(_, i, d):
            return abs(numeroNodos(i) - numeroNodos(d)) <= 1 \
                and balanceado(i) and balanceado(d)
    assert False

# ---------------------------------------------------------------------
# Ejercicio 2. Los árboles binarios con valores en las hojas se pueden
# definir por
#    @dataclass
#    class Arbol2(Generic[A]):
#        pass
#
#    @dataclass
#    class H2(Arbol2[A]):
#        x: A
#
#    @dataclass
#    class N2(Arbol2[A]):
#        i: Arbol2[A]
#        d: Arbol2[A]
# Por ejemplo, los árboles
#    árbol1          árbol2       árbol3     árbol4
#       o              o           o           o
#      / \            / \         / \         / \
#     1   o          o   3       o   3       o   1
#        / \        / \         / \         / \
#       2   3      1   2       1   4       2   3
# se representan por
#    arbol1: Arbol2[int] = N2(H2(1), N2(H2(2), H2(3)))
#    arbol2: Arbol2[int] = N2(N2(H2(1), H2(2)), H2(3))
#    arbol3: Arbol2[int] = N2(N2(H2(1), H2(4)), H2(3))
#    arbol4: Arbol2[int] = N2(N2(H2(2), H2(3)), H2(1))
#
# Definir la función
#    igualBorde : (Arbol2[A], Arbol2[A]) -> bool
# tal que igualBorde(t1, t2) se verifica si los bordes de los árboles
# t1 y t2 son iguales. Por ejemplo,
#    igualBorde(arbol1, arbol2)  ==  True
#    igualBorde(arbol1, arbol3)  ==  False
#    igualBorde(arbol1, arbol4)  ==  False
# ---------------------------------------------------------------------

@dataclass
class Arbol2(Generic[A]):
    pass

@dataclass
class H2(Arbol2[A]):
    x: A

@dataclass
class N2(Arbol2[A]):
    i: Arbol2[A]
    d: Arbol2[A]

arbol1: Arbol2[int] = N2(H2(1), N2(H2(2), H2(3)))
arbol2: Arbol2[int] = N2(N2(H2(1), H2(2)), H2(3))
arbol3: Arbol2[int] = N2(N2(H2(1), H2(4)), H2(3))
arbol4: Arbol2[int] = N2(N2(H2(2), H2(3)), H2(1))

# borde(t) es el borde del árbol t; es decir, la lista de las hojas
# del árbol t leídas de izquierda a derecha. Por ejemplo,
#    borde(arbol4)  ==  [2, 3, 1]
def borde(a: Arbol2[A]) -> list[A]:
    match a:
        case H2(x):
            return [x]
        case N2(i, d):
            return borde(i) + borde(d)
    assert False

def igualBorde(t1: Arbol2[A], t2: Arbol2[A]) -> bool:
    return borde(t1) == borde(t2)

# ---------------------------------------------------------------------
# Ejercicio 3.1. Los árboles binarios con valores en las hojas y en los
# nodos se definen por
#    @dataclass
#    class Arbol3(Generic[A]):
#        pass
#
#    @dataclass
#    class H3(Arbol3[A]):
#        x: A
#
#    @dataclass
#    class N3(Arbol3[A]):
#        x: A
#        i: Arbol3[A]
#        d: Arbol3[A]
# Por ejemplo, los árboles
#         5              8             5           5
#        / \            / \           / \         / \
#       /   \          /   \         /   \       /   \
#      9     7        9     3       9     2     4     7
#     / \   / \      / \   / \     / \               / \
#    1   4 6   8    1   4 6   2   1   4             6   2
# se pueden representar por
#     ej3arbol1: Arbol3[int] = N3(5, N3(9, H3(1), H3(4)), N3(7, H3(6), H3(8)))
#     ej3arbol2: Arbol3[int] = N3(8, N3(9, H3(1), H3(4)), N3(3, H3(6), H3(2)))
#     ej3arbol3: Arbol3[int] = N3(5, N3(9, H3(1), H3(4)), H3(2))
#     ej3arbol4: Arbol3[int] = N3(5, H3(4), N3(7, H3(6), H3(2)))
#
# Definir la función
#    igualEstructura : (Arbol3[A], Arbol3[A]) -> bool
# tal que igualEstructura(a1, a2) se verifica si los árboles a1 y a2
# tienen la misma estructura. Por ejemplo,
#    igualEstructura(ej3arbol1, ej3arbol2) == True
#    igualEstructura(ej3arbol1, ej3arbol3) == False
#    igualEstructura(ej3arbol1, ej3arbol4) == False
# ---------------------------------------------------------------------

@dataclass
class Arbol3(Generic[A]):
    pass

@dataclass
class H3(Arbol3[A]):
    x: A

@dataclass
class N3(Arbol3[A]):
    x: A
    i: Arbol3[A]
    d: Arbol3[A]

ej3arbol1: Arbol3[int] = N3(5, N3(9, H3(1), H3(4)), N3(7, H3(6), H3(8)))
ej3arbol2: Arbol3[int] = N3(8, N3(9, H3(1), H3(4)), N3(3, H3(6), H3(2)))
ej3arbol3: Arbol3[int] = N3(5, N3(9, H3(1), H3(4)), H3(2))
ej3arbol4: Arbol3[int] = N3(5, H3(4), N3(7, H3(6), H3(2)))

def igualEstructura(a: Arbol3[A], b: Arbol3[A]) -> bool:
    match (a, b):
        case (H3(_), H3(_)):
            return True
        case (N3(_, i1, d1), N3(_, i2, d2)):
            return igualEstructura(i1, i2) and igualEstructura(d1, d2)
        case (_, _):
            return False
    assert False

# ---------------------------------------------------------------------
# Ejercicio 3.2. Definir la función
#    algunoArbol3 : (Arbol3[A], Callable[[A], bool]) -> bool
# tal que algunoArbol(a, p) se verifica si algún elemento del árbol a
# cumple la propiedad p. Por ejemplo,
#    >>> algunoArbol(N3(5, N3(3, H3(1), H3(4)), H3(2)), lambda x: x > 4)
#    True
#    >>> algunoArbol(N3(5, N3(3, H3(1), H3(4)), H3(2)), lambda x: x > 7)
#    False
# ---------------------------------------------------------------------

def algunoArbol(a: Arbol3[A], p: Callable[[A], bool]) -> bool:
    match a:
        case H3(x):
            return p(x)
        case N3(x, i, d):
            return p(x) or algunoArbol(i, p) or algunoArbol(d, p)
    assert False

# ---------------------------------------------------------------------
# Ejercicio 3.3. Un elemento de un árbol se dirá de nivel k si aparece
# en el árbol a distancia k  de la raíz.
#
# Definir la función
#    nivel : (int, Arbol3[A]) -> list[A]
# tal que nivel(k, a) es la lista de los elementos de nivel k del árbol
# a. Por ejemplo,
#     >>> nivel(0, N3(7, N3(2, H3(5), H3(4)), H3(9)))
#     [7]
#     >>> nivel(1, N3(7, N3(2, H3(5), H3(4)), H3(9)))
#     [2, 9]
#     >>> nivel(2, N3(7, N3(2, H3(5), H3(4)), H3(9)))
#     [5, 4]
#     >>> nivel(3, N3(7, N3(2, H3(5), H3(4)), H3(9)))
#     []
# ---------------------------------------------------------------------

def nivel(k: int, a: Arbol3[A]) -> list[A]:
    match (k, a):
        case (0, H3(x)):
            return [x]
        case (0, N3(x, _, _)):
            return [x]
        case (_, H3(_)):
            return []
        case (_, N3(_, i, d)):
            return nivel(k - 1, i) + nivel(k - 1, d)
    assert False

# ---------------------------------------------------------------------
# Ejercicio 3.4. Los divisores medios de un número son los que ocupan la
# posición media entre los divisores de n, ordenados de menor a
# mayor. Por ejemplo, los divisores de 60 son [1, 2, 3, 4, 5, 6, 10, 12,
# 15, 20, 30, 60] y sus divisores medios son 6 y 10. Para los números
# que son cuadrados perfectos, sus divisores medios de son sus raíces
# cuadradas; por ejemplos, los divisores medios de 9 son 3 y 3.
#
# El árbol de factorización de un número compuesto n se construye de la
# siguiente manera:
#    * la raíz es el número n,
#    * la rama izquierda es el árbol de factorización de su divisor
#      medio menor y
#    * la rama derecha es el árbol de factorización de su divisor
#      medio mayor
# Si el número es primo, su árbol de factorización sólo tiene una hoja
# con dicho número. Por ejemplo, el árbol de factorización de 60 es
#        60
#       /  \
#      6    10
#     / \   / \
#    2   3 2   5
#
# Definir la función
#    arbolFactorizacion : (int) -> Arbol3[int]
# tal que arbolFactorizacion(n) es el árbol de factorización de n. Por
# ejemplo,
#    arbolFactorizacion(60) == N3(60,
#                                 N3(6, H3(2), H3(3)),
#                                 N3(10, H3(2), H3(5)))
#    arbolFactorizacion(45) == N3(45, H3(5), N3(9, H3(3), H3(3)))
#    arbolFactorizacion(7)  == H3(7)
#    arbolFactorizacion(9)  == N3(9, H3(3), H3(3))
#    arbolFactorizacion(14) == N3(14, H3(2), H3(7))
#    arbolFactorizacion(28) == N3(28, N3(4, H3(2), H3(2)), H3(7))
#    arbolFactorizacion(84) == N3(84,
#                                 H3(7),
#                                 N3(12, H3(3), N3(4, H3(2), H3(2))))
# ---------------------------------------------------------------------

# 1ª solución
# ===========

# divisores(n) es la lista de los divisores de n. Por ejemplo,
#    divisores(30)  ==  [1,2,3,5,6,10,15,30]
def divisores(n: int) -> list[int]:
    return [x for x in range(1, n + 1) if n % x == 0]

# divisoresMedio(n) es el par formado por los divisores medios de
# n. Por ejemplo,
#    divisoresMedio(30)  ==  (5,6)
#    divisoresMedio(7)   ==  (1,7)
#    divisoresMedio(16)  ==  (4,4)
def divisoresMedio(n: int) -> tuple[int, int]:
    xs = divisores(n)
    x = xs[len(xs) // 2]
    return (n // x, x)

# esPrimo(n) se verifica si n es primo. Por ejemplo,
#    esPrimo(7)  ==  True
#    esPrimo(9)  ==  False
def esPrimo(n: int) -> bool:
    return divisores(n) == [1, n]

def arbolFactorizacion1(n: int) -> Arbol3[int]:
    if esPrimo(n):
        return H3(n)
    (x, y) = divisoresMedio(n)
    return N3(n, arbolFactorizacion1(x), arbolFactorizacion1(y))

# 2ª solución
# ===========

# divisoresMedio2(n) es el par formado por los divisores medios de
# n. Por ejemplo,
#    divisoresMedio2(30) ==  (5,6)
#    divisoresMedio2(7)  ==  (1,7)
#    divisoresMedio2(16) ==  (4,4)
def divisoresMedio2(n: int) -> tuple[int, int]:
    m = ceil(sqrt(n))
    x = [y for y in range(m, n + 1) if n % y == 0][0]
    return (n // x, x)

def arbolFactorizacion2(n: int) -> Arbol3[int]:
    if esPrimo(n):
        return H3(n)
    (x, y) = divisoresMedio2(n)
    return N3(n, arbolFactorizacion2(x), arbolFactorizacion2(y))

# ---------------------------------------------------------------------
# Ejercicio 4. Se consideran los árboles con operaciones booleanas
# definidos por
#    @dataclass
#    class ArbolB:
#        pass
#
#    @dataclass
#    class H(ArbolB):
#        x: bool
#
#    @dataclass
#    class Conj(ArbolB):
#        i: ArbolB
#        d: ArbolB
#
#    @dataclass
#    class Disy(ArbolB):
#        i: ArbolB
#        d: ArbolB
#
#    @dataclass
#    class Neg(ArbolB):
#        a: ArbolB
#
# Por ejemplo, los árboles
#                Conj                            Conj
#               /   \                           /   \
#              /     \                         /     \
#           Disy      Conj                  Disy      Conj
#          /   \       /  \                /   \      /   \
#       Conj    Neg   Neg True          Conj    Neg   Neg  True
#       /  \    |     |                 /  \    |     |
#    True False False False          True False True  False
#
# se definen por
#    ej1: ArbolB = Conj(Disy(Conj(H(True), H(False)),
#                            (Neg(H(False)))),
#                       (Conj(Neg(H(False)),
#                             (H(True)))))
#
#    ej2: ArbolB = Conj(Disy(Conj(H(True), H(False)),
#                            (Neg(H(True)))),
#                       (Conj(Neg(H(False)),
#                             (H(True)))))
#
# Definir la función
#    valorB : (ArbolB) -> bool
# tal que valorB(a) es el resultado de procesar el árbol a realizando
# las operaciones booleanas especificadas en los nodos. Por ejemplo,
#    valorB(ej1) == True
#    valorB(ej2) == False
# ---------------------------------------------------------------------

@dataclass
class ArbolB:
    pass

@dataclass
class H(ArbolB):
    x: bool

@dataclass
class Conj(ArbolB):
    i: ArbolB
    d: ArbolB

@dataclass
class Disy(ArbolB):
    i: ArbolB
    d: ArbolB

@dataclass
class Neg(ArbolB):
    a: ArbolB

ej1: ArbolB = Conj(Disy(Conj(H(True), H(False)),
                        (Neg(H(False)))),
                   (Conj(Neg(H(False)),
                         (H(True)))))

ej2: ArbolB = Conj(Disy(Conj(H(True), H(False)),
                        (Neg(H(True)))),
                   (Conj(Neg(H(False)),
                         (H(True)))))

def valorB(a: ArbolB) -> bool:
    match a:
        case H(x):
            return x
        case Neg(b):
            return not valorB(b)
        case Conj(i, d):
            return valorB(i) and valorB(d)
        case Disy(i, d):
            return valorB(i) or valorB(d)
    assert False

# ---------------------------------------------------------------------
# Ejercicio 5. Los árboles generales se pueden representar mediante el
# siguiente tipo de dato
#    @dataclass
#    class ArbolG(Generic[A]):
#        pass
#
#    @dataclass
#    class NG(ArbolG[A]):
#        x: A
#        y: list[ArbolG[A]]
# Por ejemplo, los árboles
#      1               3               3
#     / \             /|\            / | \
#    2   3           / | \          /  |  \
#        |          5  4  7        5   4   7
#        4          |     /\       |   |  / \
#                   6    2  1      6   1 2   1
#                                     / \
#                                    2   3
#                                        |
#                                        4
# se representan por
#    ejG1: ArbolG[int] = NG(1, [NG(2, []), NG(3, [NG(4, [])])])
#    ejG2: ArbolG[int] = NG(3, [NG(5, [NG(6, [])]),
#                               NG(4, []),
#                               NG(7, [NG(2, []), NG(1, [])])])
#    ejG3: ArbolG[int] = NG(3, [NG(5, [NG(6, [])]),
#                               NG(4, [NG(1, [NG(2, []),
#                                             NG(3, [NG(4, [])])])]),
#                               NG(7, [NG(2, []), NG(1, [])])])
#
# Definir la función
#     ramifica : (ArbolG[A], ArbolG[A], Callable[[A], bool]) -> ArbolG[A]
# tal que ramifica(a1, a2, p) es el árbol que resulta de añadir una copia
# del árbol a2 a los nodos de a1 que cumplen un predicado p. Por
# ejemplo,
#    >>> ramifica(ejG1, NG(8, []), lambda x: x > 4)
#    NG(1, [NG(2, []), NG(3, [NG(4, [])])])
#    >>> ramifica(ejG1, NG(8, []), lambda x: x > 3)
#    NG(1, [NG(2, []), NG(3, [NG(4, [NG(8, [])])])])
#    >>> ramifica(ejG1, NG(8, []), lambda x: x > 2)
#    NG(1, [NG(2, []), NG(3, [NG(4, [NG(8, [])]), NG(8, [])])])
#    >>> ramifica(ejG1, NG(8, []), lambda x: x > 1)
#    NG(1, [NG(2, [NG(8, [])]), NG(3, [NG(4, [NG(8, [])]), NG(8, [])])])
#    >>> ramifica(ejG1, NG(8, []), lambda x: x > 0)
#    NG(1, [NG(2, [NG(8, [])]),
#           NG(3, [NG(4, [NG(8, [])]), NG(8, [])]),
#           NG(8, [])])
# -- ---------------------------------------------------------------------

@dataclass
class ArbolG(Generic[A]):
    pass

@dataclass
class NG(ArbolG[A]):
    x: A
    y: list[ArbolG[A]]

ejG1: ArbolG[int] = NG(1, [NG(2, []), NG(3, [NG(4, [])])])
ejG2: ArbolG[int] = NG(3, [NG(5, [NG(6, [])]),
                           NG(4, []),
                           NG(7, [NG(2, []), NG(1, [])])])
ejG3: ArbolG[int] = NG(3, [NG(5, [NG(6, [])]),
                           NG(4, [NG(1, [NG(2, []), NG(3, [NG(4, [])])])]),
                           NG(7, [NG(2, []), NG(1, [])])])

def ramifica(a1: ArbolG[A],
             a2: ArbolG[A],
             p: Callable[[A], bool]) -> ArbolG[A]:
    match a1:
        case NG(x, xs):
            if p(x):
                return NG(x, [ramifica(a, a2, p) for a in xs] + [a2])
            return NG(x, [ramifica(a, a2, p) for a in xs])
    assert False
