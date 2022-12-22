# funciones_de_orden_superior_y_definiciones_por_plegados.py
# Funciones de orden superior y definiciones por plegados.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 22-diciembre-2022
# ======================================================================

# ---------------------------------------------------------------------
# Introducción                                                       --
# ---------------------------------------------------------------------

# Esta relación contiene ejercicios con funciones de orden superior y
# definiciones por plegado correspondientes al tema 7 que se encuentra
# en
#    https://jaalonso.github.io/cursos/i1m/temas/tema-7.html

# ---------------------------------------------------------------------
# Importación de librerías auxiliares                                --
# ---------------------------------------------------------------------

from abc import abstractmethod
from functools import reduce
from operator import concat
from itertools import dropwhile, takewhile
from sys import setrecursionlimit
from timeit import Timer, default_timer
from typing import Any, Callable, Protocol, TypeVar

from more_itertools import split_at
from hypothesis import given
from hypothesis import strategies as st
from numpy import array, transpose

setrecursionlimit(10**6)

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C', bound="Comparable")

class Comparable(Protocol):
    """Para comparar"""
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __lt__(self: A, other: A) -> bool:
        pass

    def __gt__(self: A, other: A) -> bool:
        return (not self < other) and self != other

    def __le__(self: A, other: A) -> bool:
        return self < other or self == other

    def __ge__(self: A, other: A) -> bool:
        return not self < other

# ---------------------------------------------------------------------
# Ejercicio 1. Definir la función
#    segmentos : (Callable[[A], bool], list[A]) -> list[list[A]]
# tal que segmentos(p, xs) es la lista de los segmentos de xs cuyos
# elementos verifican la propiedad p. Por ejemplo,
#    >>> segmentos1((lambda x: x % 2 == 0), [1,2,0,4,9,6,4,5,7,2])
#    [[2, 0, 4], [6, 4], [2]]
#    >>> segmentos1((lambda x: x % 2 == 1), [1,2,0,4,9,6,4,5,7,2])
#    [[1], [9], [5, 7]]
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def segmentos1(p: Callable[[A], bool], xs: list[A]) -> list[list[A]]:
    if not xs:
        return []
    if p(xs[0]):
        return [list(takewhile(p, xs))] + \
            segmentos1(p, list(dropwhile(p, xs[1:])))
    return segmentos1(p, xs[1:])

# 2ª solución
# ===========

def segmentos(p: Callable[[A], bool], xs: list[A]) -> list[list[A]]:
    return list(filter((lambda x: x), split_at(xs, lambda x: not p(x))))

# Comparación de eficiencia
# =========================

def tiempo(e: str) -> None:
    """Tiempo (en segundos) de evaluar la expresión e."""
    t = Timer(e, "", default_timer, globals()).timeit(1)
    print(f"{t:0.2f} segundos")

# La comparación es
#    >>> tiempo('segmentos1(lambda x: x % 2 == 0, range(10**4))')
#    0.55 segundos
#    >>> tiempo('segmentos(lambda x: x % 2 == 0, range(10**4))')
#    0.00 segundos

# ---------------------------------------------------------------------
# Ejercicio 2.1. Definir, por comprensión, la función
#    relacionadosC : (Callable[[A, A], bool], list[A]) -> bool
# tal que relacionadosC(r, xs) se verifica si para todo par (x,y) de
# elementos consecutivos de xs se cumple la relación r. Por ejemplo,
#    >>> relacionadosC(lambda x, y: x < y, [2, 3, 7, 9])
#    True
#    >>> relacionadosC(lambda x, y: x < y, [2, 3, 1, 9])
#    False
# ---------------------------------------------------------------------

def relacionadosC(r: Callable[[A, A], bool], xs: list[A]) -> bool:
    return all((r(x, y) for (x, y) in zip(xs, xs[1:])))

# ---------------------------------------------------------------------
# Ejercicio 2.2. Definir, por recursión, la función
#    relacionadosR : (Callable[[A, A], bool], list[A]) -> bool
# tal que relacionadosC(r, xs) se verifica si para todo par (x,y) de
# elementos consecutivos de xs se cumple la relación r. Por ejemplo,
#    >>> relacionadosR(lambda x, y: x < y, [2, 3, 7, 9])
#    True
#    >>> relacionadosR(lambda x, y: x < y, [2, 3, 1, 9])
#    False
# ---------------------------------------------------------------------

def relacionadosR(r: Callable[[A, A], bool], xs: list[A]) -> bool:
    if len(xs) >= 2:
        return r(xs[0], xs[1]) and relacionadosR(r, xs[1:])
    return True

# ---------------------------------------------------------------------
# Ejercicio 3.1. Definir la función
#    agrupa : (list[list[A]]) -> list[list[A]]
# tal que agrupa(xss) es la lista de las listas obtenidas agrupando
# los primeros elementos, los segundos, ... Por ejemplo,
#    >>> agrupa([[1,6],[7,8,9],[3,4,5]])
#    [[1, 7, 3], [6, 8, 4]]
# ---------------------------------------------------------------------

# 1ª solución
# ===========

# primeros(xss) es la lista de los primeros elementos de xss. Por
# ejemplo,
#    primeros([[1,6],[7,8,9],[3,4,5]])  ==  [1, 7, 3]
def primeros(xss: list[list[A]]) -> list[A]:
    return [xs[0] for xs in xss]

# restos(xss) es la lista de los restos de elementos de xss. Por
# ejemplo,
#    >>> restos([[1,6],[7,8,9],[3,4,5]])
#    [[6], [8, 9], [4, 5]]
def restos(xss: list[list[A]]) -> list[list[A]]:
    return [xs[1:] for xs in xss]

def agrupa1(xss: list[list[A]]) -> list[list[A]]:
    if not xss:
        return []
    if [] in xss:
        return []
    return [primeros(xss)] + agrupa1(restos(xss))

# 2ª solución
# ===========

# conIgualLongitud(xss) es la lista obtenida recortando los elementos
# de xss para que todos tengan la misma longitud. Por ejemplo,
#    >>> conIgualLongitud([[1,6],[7,8,9],[3,4,5]])
#    [[1, 6], [7, 8], [3, 4]]
def conIgualLongitud(xss: list[list[A]]) -> list[list[A]]:
    n = min(map(len, xss))
    return [xs[:n] for xs in xss]

def agrupa2(xss: list[list[A]]) -> list[list[A]]:
    yss = conIgualLongitud(xss)
    return [[ys[i] for ys in yss] for i in range(len(yss[0]))]

# 3ª solución
# ===========

def agrupa3(xss: list[list[A]]) -> list[list[A]]:
    yss = conIgualLongitud(xss)
    return list(map(list, zip(*yss)))

# 4ª solución
# ===========

def agrupa4(xss: list[list[A]]) -> list[list[A]]:
    yss = conIgualLongitud(xss)
    return (transpose(array(yss))).tolist()

# 5ª solución
# ===========

def agrupa5(xss: list[list[A]]) -> list[list[A]]:
    yss = conIgualLongitud(xss)
    r = []
    for i in range(len(yss[0])):
        f = []
        for xs in xss:
            f.append(xs[i])
        r.append(f)
    return r

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.lists(st.lists(st.integers()), min_size=1))
def test_agrupa(xss: list[list[int]]) -> None:
    r = agrupa1(xss)
    assert agrupa2(xss) == r
    assert agrupa3(xss) == r
    assert agrupa4(xss) == r
    assert agrupa5(xss) == r

# Comparación de eficiencia
# =========================

# La comparación es
#    >>> tiempo('agrupa1([list(range(10**3)) for _ in range(10**3)])')
#    4.44 segundos
#    >>> tiempo('agrupa2([list(range(10**3)) for _ in range(10**3)])')
#    0.10 segundos
#    >>> tiempo('agrupa3([list(range(10**3)) for _ in range(10**3)])')
#    0.10 segundos
#    >>> tiempo('agrupa4([list(range(10**3)) for _ in range(10**3)])')
#    0.12 segundos
#    >>> tiempo('agrupa5([list(range(10**3)) for _ in range(10**3)])')
#    0.15 segundos
#
#    >>> tiempo('agrupa2([list(range(10**4)) for _ in range(10**4)])')
#    21.25 segundos
#    >>> tiempo('agrupa3([list(range(10**4)) for _ in range(10**4)])')
#    20.82 segundos
#    >>> tiempo('agrupa4([list(range(10**4)) for _ in range(10**4)])')
#    13.46 segundos
#    >>> tiempo('agrupa5([list(range(10**4)) for _ in range(10**4)])')
#    21.70 segundos

# ---------------------------------------------------------------------
# Ejercicio 3.2. Comprobar con Hypothesis que la longitud de todos los
# elementos de agrupa(xs) es igual a la longitud de xs.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.lists(st.lists(st.integers()), min_size=1))
def test_agrupa_length(xss: list[list[int]]) -> None:
    n = len(xss)
    assert all((len(xs) == n for xs in agrupa2(xss)))

# ---------------------------------------------------------------------
# Ejercicio 4.1. Definir, por comprensión, la función
#    concC : (list[list[A]]) -> list[A]
# tal que concC(xss) es la concenación de las listas de xss. Por
# ejemplo,
#    concC([[1,3],[2,4,6],[1,9]])  ==  [1,3,2,4,6,1,9]
# ---------------------------------------------------------------------

def concC(xss: list[list[A]]) -> list[A]:
    return [x for xs in xss for x in xs]

# ---------------------------------------------------------------------
# Ejercicio 4.2. Definir, por recursión, la función
#    concR : (list[list[A]]) -> list[A]
# tal que concR(xss) es la concenación de las listas de xss. Por
# ejemplo,
#    concR([[1,3],[2,4,6],[1,9]])  ==  [1,3,2,4,6,1,9]
# ---------------------------------------------------------------------

def concR(xss: list[list[A]]) -> list[A]:
    if not xss:
        return []
    return xss[0] + concR(xss[1:])

# ---------------------------------------------------------------------
# Ejercicio 4.3. Definir, usando reduce, la función
#    concP : (Any) -> Any:
# tal que concP(xss) es la concenación de las listas de xss. Por
# ejemplo,
#    concP([[1,3],[2,4,6],[1,9]])  ==  [1,3,2,4,6,1,9]
# ---------------------------------------------------------------------

def concP(xss: Any) -> Any:
    return reduce(concat, xss)

# ---------------------------------------------------------------------
# Ejercicio 4.4. Comprobar con Hypothesis que la funciones concC,
# concatR y concP son equivalentes.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.lists(st.lists(st.integers()), min_size=1))
def test_conc(xss: list[list[int]]) -> None:
    r = concC(xss)
    assert concR(xss) == r
    assert concP(xss) == r

# Comparación de eficiencia
# =========================

# La comparación es
#    >>> tiempo('concC([list(range(n)) for n in range(1500)])')
#    0.04 segundos
#    >>> tiempo('concR([list(range(n)) for n in range(1500)])')
#    6.28 segundos
#    >>> tiempo('concP([list(range(n)) for n in range(1500)])')
#    2.55 segundos

# ---------------------------------------------------------------------
# Ejercicio 4.5. Comprobar con Hypothesis que la longitud de
# concatP(xss) es la suma de las longitudes de los elementos de xss.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.lists(st.lists(st.integers()), min_size=1))
def test_long_conc(xss: list[list[int]]) -> None:
    assert len(concP(xss)) == sum(map(len, xss))

# ---------------------------------------------------------------------
# Ejercicio 5.1. Definir, por comprensión, la función
#    filtraAplicaC : (Callable[[A], B], Callable[[A], bool], list[A])
#                    -> list[B]
# tal que filtraAplicaC(f, p, xs) es la lista obtenida aplicándole a los
# elementos de xs que cumplen el predicado p la función f. Por ejemplo,
#    >>> filtraAplicaC(lambda x: x + 4, lambda x: x < 3, range(1, 7))
#    [5, 6]
# ---------------------------------------------------------------------

def filtraAplicaC(f: Callable[[A], B],
                  p: Callable[[A], bool],
                  xs: list[A]) -> list[B]:
    return [f(x) for x in xs if p(x)]

# ---------------------------------------------------------------------
# Ejercicio 5.2. Definir, usando map y filter, la función
#    filtraAplicaMF : (Callable[[A], B], Callable[[A], bool], list[A])
#                     -> list[B]
# tal que filtraAplicaMF(f, p, xs) es la lista obtenida aplicándole a los
# elementos de xs que cumplen el predicado p la función f. Por ejemplo,
#    >>> filtraAplicaMF(lambda x: x + 4, lambda x: x < 3, range(1, 7))
#    [5, 6]
# ---------------------------------------------------------------------

def filtraAplicaMF(f: Callable[[A], B],
                   p: Callable[[A], bool],
                   xs: list[A]) -> list[B]:
    return list(map(f, filter(p, xs)))

# ---------------------------------------------------------------------
# Ejercicio 5.3. Definir, por recursión, la función
#    filtraAplicaR : (Callable[[A], B], Callable[[A], bool], list[A])
#                    -> list[B]
# tal que filtraAplicaR(f, p, xs) es la lista obtenida aplicándole a los
# elementos de xs que cumplen el predicado p la función f. Por ejemplo,
#    >>> filtraAplicaR(lambda x: x + 4, lambda x: x < 3, range(1, 7))
#    [5, 6]
# ---------------------------------------------------------------------

def filtraAplicaR(f: Callable[[A], B],
                  p: Callable[[A], bool],
                  xs: list[A]) -> list[B]:
    if not xs:
        return []
    if p(xs[0]):
        return [f(xs[0])] + filtraAplicaR(f, p, xs[1:])
    return filtraAplicaR(f, p, xs[1:])

# ---------------------------------------------------------------------
# Ejercicio 5.4. Definir, por plegado, la función
#    filtraAplicaP : (Callable[[A], B], Callable[[A], bool], list[A])
#                    -> list[B]
# tal que filtraAplicaP(f, p, xs) es la lista obtenida aplicándole a los
# elementos de xs que cumplen el predicado p la función f. Por ejemplo,
#    >>> filtraAplicaP(lambda x: x + 4, lambda x: x < 3, range(1, 7))
#    [5, 6]
# ---------------------------------------------------------------------

def filtraAplicaP(f: Callable[[A], B],
                  p: Callable[[A], bool],
                  xs: list[A]) -> list[B]:
    def g(ys: list[B], x: A) -> list[B]:
        if p(x):
            return ys + [f(x)]
        return ys

    return reduce(g, xs, [])

# ---------------------------------------------------------------------
# Ejercicio 5.5. Definir, por iteración, la función
#    filtraAplicaI : (Callable[[A], B], Callable[[A], bool], list[A])
#                    -> list[B]
# tal que filtraAplicaI(f, p, xs) es la lista obtenida aplicándole a los
# elementos de xs que cumplen el predicado p la función f. Por ejemplo,
#    >>> filtraAplicaI(lambda x: x + 4, lambda x: x < 3, range(1, 7))
#    [5, 6]
# ---------------------------------------------------------------------

def filtraAplicaI(f: Callable[[A], B],
                  p: Callable[[A], bool],
                  xs: list[A]) -> list[B]:
    r = []
    for x in xs:
        if p(x):
            r.append(f(x))
    return r

# ---------------------------------------------------------------------
# Ejercicio 5.6. Comprobar que las definiciones de filtraAplica son
# equivalentes.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.lists(st.integers()))
def test_filtraAplica(xs: list[int]) -> None:
    f = lambda x: x + 4
    p = lambda x: x < 3
    r = filtraAplicaC(f, p, xs)
    assert filtraAplicaMF(f, p, xs) == r
    assert filtraAplicaR(f, p, xs) == r
    assert filtraAplicaP(f, p, xs) == r
    assert filtraAplicaI(f, p, xs) == r

# ---------------------------------------------------------------------
# Ejercicio 5.7. Comparar la eficiencia de las definiciones de
# filtraAplica.
# ---------------------------------------------------------------------

# La comparación es
#    >>> tiempo('filtraAplicaC(lambda x: x, lambda x: x % 2 == 0, range(10**5))')
#    0.02 segundos
#    >>> tiempo('filtraAplicaMF(lambda x: x, lambda x: x % 2 == 0, range(10**5))')
#    0.01 segundos
#    >>> tiempo('filtraAplicaR(lambda x: x, lambda x: x % 2 == 0, range(10**5))')
#    Process Python violación de segmento (core dumped)
#    >>> tiempo('filtraAplicaP(lambda x: x, lambda x: x % 2 == 0, range(10**5))')
#    4.07 segundos
#    >>> tiempo('filtraAplicaI(lambda x: x, lambda x: x % 2 == 0, range(10**5))')
#    0.01 segundos
#
#    >>> tiempo('filtraAplicaC(lambda x: x, lambda x: x % 2 == 0, range(10**7))')
#    1.66 segundos
#    >>> tiempo('filtraAplicaMF(lambda x: x, lambda x: x % 2 == 0, range(10**7))')
#    1.00 segundos
#    >>> tiempo('filtraAplicaI(lambda x: x, lambda x: x % 2 == 0, range(10**7))')
#    1.21 segundos

# ---------------------------------------------------------------------
# Ejercicio 6.1. Definir la función
#    maximo : (list[C]) -> C:
# tal que maximo(xs) es el máximo de la lista xs. Por ejemplo,
#    maximo([3,7,2,5])                  ==  7
#    maximo(["todo","es","falso"])      ==  "todo"
#    maximo(["menos","alguna","cosa"])  ==  "menos"
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def maximo1(xs: list[C]) -> C:
    if len(xs) == 1:
        return xs[0]
    return max(xs[0], maximo1(xs[1:]))

# 2ª solución
# ===========

def maximo2(xs: list[C]) -> C:
    return reduce(max, xs)

# 3ª solución
# ===========

def maximo3(xs: list[C]) -> C:
    return max(xs)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.lists(st.integers(), min_size=2))
def test_maximo(xs: list[int]) -> None:
    r = maximo1(xs)
    assert maximo2(xs) == r
    assert maximo3(xs) == r

# ---------------------------------------------------------------------
# Comprobación de las propiedades
# ---------------------------------------------------------------------

# La comprobación es
#    src> poetry run pytest -q funciones_de_orden_superior_y_definiciones_por_plegados.py
#    1 passed in 0.74s
