# relaciones_binarias_homogeneas.py
# Relaciones binarias homogéneas.
# Departamento de Ciencias de la Computación e I.A.
# Universidad de Sevilla
# =====================================================================

# ---------------------------------------------------------------------
# Introducción                                                       --
# ---------------------------------------------------------------------

# El objetivo de esta relación de ejercicios es definir propiedades y
# operaciones sobre las relaciones binarias (homogéneas).
#
# Como referencia se puede usar el artículo de la wikipedia
# http://bit.ly/HVHOPS

# ---------------------------------------------------------------------
# § Librerías auxiliares                                             --
# ---------------------------------------------------------------------

from random import randint, sample
from sys import setrecursionlimit
from timeit import Timer, default_timer
from typing import TypeVar

from hypothesis import given
from hypothesis import strategies as st

A = TypeVar('A')

setrecursionlimit(10**6)

# ---------------------------------------------------------------------
# Ejercicio 1. Una relación binaria R sobre un conjunto A se puede
# representar mediante un par (u,g) donde u es la lista de los elementos
# de tipo A (el universo de R) y g es la lista de pares de elementos de
# u (el grafo de R).
#
# Definir el tipo de dato (Rel a), para representar las relaciones
# binarias sobre a, y la función
#    esRelacionBinaria : (Rel[A]) -> bool
# tal que esRelacionBinaria(r) se verifica si r es una relación
# binaria. Por ejemplo,
#    >>> esRelacionBinaria(([1, 3], [(3, 1), (3, 3)]))
#    True
#    >>> esRelacionBinaria(([1, 3], [(3, 1), (3, 2)]))
#    False
#
# Además, definir un generador de relaciones binarias y comprobar que
# las relaciones que genera son relaciones binarias.
# ---------------------------------------------------------------------

Rel = tuple[list[A], list[tuple[A, A]]]

# 1ª solución
# ===========

def esRelacionBinaria(r: Rel[A]) -> bool:
    (u, g) = r
    return all((x in u and y in u for (x, y) in g))

# 2ª solución
# ===========

def esRelacionBinaria2(r: Rel[A]) -> bool:
    (u, g) = r
    if not g:
        return True
    (x, y) = g[0]
    return x in u and y in u and esRelacionBinaria2((u, g[1:]))

# 3ª solución
# ===========

def esRelacionBinaria3(r: Rel[A]) -> bool:
    (u, g) = r
    for (x, y) in g:
        if x not in u or y not in u:
            return False
    return True

# Generador de relaciones binarias
# ================================

# conjuntoArbitrario(n) es un conjunto arbitrario cuyos elementos están
# entre 0 y n-1. Por ejemplo,
#    >>> conjuntoArbitrario(10)
#    [8, 9, 4, 5]
#    >>> conjuntoArbitrario(10)
#    [1, 2, 3, 4, 5, 6, 7, 8, 9]
#    >>> conjuntoArbitrario(10)
#    [0, 1, 2, 3, 6, 7, 9]
#    >>> conjuntoArbitrario(10)
#    [8, 2, 3, 7]
def conjuntoArbitrario(n: int) -> list[int]:
    xs = sample(range(n), randint(0, n))
    return list(set(xs))

# productoCartesiano(xs, ys) es el producto cartesiano de xs e ys. Por
# ejemplo,
#    >>> productoCartesiano([2, 3], [1, 7, 5])
#    [(2, 1), (2, 7), (2, 5), (3, 1), (3, 7), (3, 5)]
def productoCartesiano(xs: list[int], ys: list[int]) -> list[tuple[int, int]]:
    return [(x, y) for x in xs for y in ys]

# sublistaArbitraria(xs) es una sublista arbitraria de xs. Por ejemplo,
#    >>> sublistaArbitraria(range(10))
#    [3, 7]
#    >>> sublistaArbitraria(range(10))
#    []
#    >>> sublistaArbitraria(range(10))
#    [4, 1, 0, 9, 8, 7, 5, 6, 2, 3]
def sublistaArbitraria(xs: list[A]) -> list[A]:
    n = len(xs)
    k = randint(0, n)
    return sample(xs, k)

# relacionArbitraria(n) es una relación arbitraria tal que los elementos
# de su universo están entre 0 y n-1. Por ejemplo,
#    >>> relacionArbitraria(3)
#    ([0, 1], [(1, 0), (1, 1)])
#    >>> relacionArbitraria(3)
#    ([], [])
#    >>> relacionArbitraria(5)
#    ([0, 2, 3, 4], [(2, 0), (3, 3), (2, 3), (4, 0), (3, 4), (4, 2)])
def relacionArbitraria(n: int) -> Rel[int]:
    u = conjuntoArbitrario(n)
    g = sublistaArbitraria(productoCartesiano(u, u))
    return (u, g)

# Comprobación de la propiedad
# ============================

# La propiedad es
@given(st.integers(min_value=0, max_value=10))
def test_esRelacionBinaria(n: int) -> None:
    r = relacionArbitraria(n)
    assert esRelacionBinaria(r)
    assert esRelacionBinaria2(r)
    assert esRelacionBinaria3(r)

# La comprobación está al final
#    > poetry run pytest -q Relaciones_binarias.py
#    1 passed in 0.14s

# ---------------------------------------------------------------------
# Ejercicio 2. Definir la función
#    universo : (Rel[A]) -> list[A]
# tal que universo(r) es el universo de la relación r. Por ejemplo,
#    >>> universo(([3, 2, 5], [(2, 3), (3, 5)]))
#    [3, 2, 5]
# ---------------------------------------------------------------------

def universo(r: Rel[A]) -> list[A]:
    return r[0]

# ---------------------------------------------------------------------
# Ejercicio 3. Definir la función
#    grafo    : (Rel[A]) -> list[tuple[A, A]]
# tal que grafo(r) es el grafo de la relación r. Por ejemplo,
#    >>> grafo(([3, 2, 5], [(2, 3), (3, 5)]))
#    [(2, 3), (3, 5)]
# ---------------------------------------------------------------------

def grafo(r: Rel[A]) -> list[tuple[A, A]]:
    return r[1]

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    reflexiva : (Rel) -> bool
# tal que reflexiva(r) se verifica si la relación r es reflexiva. Por
# ejemplo,
#    >>> reflexiva(([1, 3], [(1, 1),(1, 3),(3, 3)]))
#    True
#    >>> reflexiva(([1, 2, 3], [(1, 1),(1, 3),(3, 3)]))
#    False
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def reflexiva(r: Rel[A]) -> bool:
    (us, ps) = r
    if not us:
        return True
    return (us[0], us[0]) in ps and reflexiva((us[1:], ps))

# 2ª solución
# ===========

def reflexiva2(r: Rel[A]) -> bool:
    (us, ps) = r
    return all(((x,x) in ps for x in us))

# 3ª solución
# ===========

def reflexiva3(r: Rel[A]) -> bool:
    (us, ps) = r
    for x in us:
        if (x, x) not in ps:
            return False
    return True

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.integers(min_value=0, max_value=10))
def test_reflexiva(n: int) -> None:
    r = relacionArbitraria(n)
    res = reflexiva(r)
    assert reflexiva2(r) == res
    assert reflexiva3(r) == res

# ---------------------------------------------------------------------
# Ejercicio 5. Definir la función
#    simetrica : (Rel[A]) -> bool
# tal que simetrica(r) se verifica si la relación r es simétrica. Por
# ejemplo,
#    >>> simetrica(([1, 3], [(1, 1), (1, 3), (3, 1)]))
#    True
#    >>> simetrica(([1, 3], [(1, 1), (1, 3), (3, 2)]))
#    False
#    >>> simetrica(([1, 3], []))
#    True
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def simetrica(r: Rel[A]) -> bool:
    (_, g) = r
    return all(((y, x) in g for (x, y) in g))

# 2ª solución
# ===========

def simetrica2(r: Rel[A]) -> bool:
    (_, g) = r
    def aux(ps: list[tuple[A, A]]) -> bool:
        if not ps:
            return True
        (x, y) = ps[0]
        return (y, x) in g and aux(ps[1:])

    return aux(g)

# 3ª solución
# ===========

def simetrica3(r: Rel[A]) -> bool:
    (_, g) = r
    for (x, y) in g:
        if (y, x) not in g:
            return False
    return True

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.integers(min_value=0, max_value=10))
def test_simetrica(n: int) -> None:
    r = relacionArbitraria(n)
    res = simetrica(r)
    assert simetrica2(r) == res
    assert simetrica3(r) == res

# ---------------------------------------------------------------------
# Ejercicio 6. Definir la función
#    subconjunto : (list[A], list[A]) -> bool
# tal que (subconjunto xs ys) se verifica si xs es un subconjunto de
# ys. por ejemplo,
#    subconjunto([3, 2, 3], [2, 5, 3, 5])  ==  True
#    subconjunto([3, 2, 3], [2, 5, 6, 5])  ==  False
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def subconjunto1(xs: list[A], ys: list[A]) -> bool:
    return [x for x in xs if x in ys] == xs

# 2ª solución
# ===========

def subconjunto2(xs: list[A], ys: list[A]) -> bool:
    if not xs:
        return True
    return xs[0] in ys and subconjunto2(xs[1:], ys)

# 3ª solución
# ===========

def subconjunto3(xs: list[A], ys: list[A]) -> bool:
    return all(elem in ys for elem in xs)

# 4ª solución
# ===========

def subconjunto4(xs: list[A], ys: list[A]) -> bool:
    return set(xs) <= set(ys)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.lists(st.integers()),
       st.lists(st.integers()))
def test_filtraAplica(xs: list[int], ys: list[int]) -> None:
    r = subconjunto1(xs, ys)
    assert subconjunto2(xs, ys) == r
    assert subconjunto3(xs, ys) == r
    assert subconjunto4(xs, ys) == r

# La comprobación es
#    src> poetry run pytest -q Reconocimiento_de_subconjunto.py
#    1 passed in 0.31s

# Comparación de eficiencia
# =========================

def tiempo(e: str) -> None:
    """Tiempo (en segundos) de evaluar la expresión e."""
    t = Timer(e, "", default_timer, globals()).timeit(1)
    print(f"{t:0.2f} segundos")

# La comparación es
#    >>> xs = list(range(2*10**4))
#    >>> tiempo("subconjunto1(xs, xs)")
#    1.15 segundos
#    >>> tiempo("subconjunto2(xs, xs)")
#    2.27 segundos
#    >>> tiempo("subconjunto3(xs, xs)")
#    1.14 segundos
#    >>> tiempo("subconjunto4(xs, xs)")
#    0.00 segundos

# En lo sucesivo usaremos la cuarta definición
subconjunto = subconjunto4

# ---------------------------------------------------------------------
# Ejercicio 7. Definir la función
#    composicion : (Rel[A], Rel[A]) -> Rel[A]
# tal que composicion(r, s) es la composición de las relaciones r y
# s. Por ejemplo,
#    >>> composicion(([1,2],[(1,2),(2,2)]), ([1,2],[(2,1)]))
#    ([1, 2], [(1, 1), (2, 1)])
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def composicion(r1: Rel[A], r2: Rel[A]) -> Rel[A]:
    (u1, g1) = r1
    (_,  g2) = r2
    return (u1, [(x, z) for (x, y) in g1 for (u, z) in g2 if y == u])

# 2ª solución
# ===========

def composicion2(r1: Rel[A], r2: Rel[A]) -> Rel[A]:
    (u1, g1) = r1
    (_,  g2) = r2
    def aux(g: list[tuple[A, A]]) -> list[tuple[A, A]]:
        if not g:
            return []
        (x, y) = g[0]
        return [(x, z) for (u, z) in g2 if y == u] + aux(g[1:])

    return (u1, aux(g1))

# 2ª solución
# ===========

def composicion3(r1: Rel[A], r2: Rel[A]) -> Rel[A]:
    (u1, g1) = r1
    (_,  g2) = r2
    r: list[tuple[A, A]] = []
    for (x, y) in g1:
        r = r + [(x, z) for (u, z) in g2 if y == u]
    return (u1, r)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.integers(min_value=0, max_value=10),
       st.integers(min_value=0, max_value=10))
def test_composicion(n: int, m: int) -> None:
    r1 = relacionArbitraria(n)
    r2 = relacionArbitraria(m)
    res = composicion(r1, r2)
    assert composicion2(r1, r2) == res
    assert composicion2(r1, r2) == res

# ---------------------------------------------------------------------
# Ejercicio 8. Definir la función
#    transitiva : (Rel[A]) -> bool
# tal que transitiva(r) se verifica si la relación r es transitiva.
# Por ejemplo,
#    >>> transitiva(([1, 3, 5], [(1, 1), (1, 3), (3, 1), (3, 3), (5, 5)]))
#    True
#    >>> transitiva(([1, 3, 5], [(1, 1), (1, 3), (3, 1), (5, 5)]))
#    False
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def transitiva1(r: Rel[A]) -> bool:
    g = grafo(r)
    return subconjunto(grafo(composicion(r, r)), g)

# 2ª solución
# ===========

def transitiva2(r: Rel[A]) -> bool:
    g = grafo(r)
    def aux(g1: list[tuple[A,A]]) -> bool:
        if not g1:
            return True
        (x, y) = g1[0]
        return all(((x, z) in g for (u,z) in g if u == y)) and aux(g1[1:])

    return aux(g)

# 3ª solución
# ===========

def transitiva3(r: Rel[A]) -> bool:
    g = grafo(r)
    g1 = list(g)
    for (x, y) in g1:
        if not all(((x, z) in g for (u,z) in g if u == y)):
            return False
    return True


# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.integers(min_value=0, max_value=10))
def test_transitiva(n: int) -> None:
    r = relacionArbitraria(n)
    res = transitiva1(r)
    assert transitiva2(r) == res
    assert transitiva3(r) == res

# Comparación de eficiencia
# =========================

# La comparación es
#    >>> u1 = range(6001)
#    >>> g1 = [(x, x+1) for x in range(6000)]
#    >>> tiempo("transitiva1((u1, g1))")
#    1.04 segundos
#    >>> tiempo("transitiva2((u1, g1))")
#    0.00 segundos
#    >>> tiempo("transitiva3((u1, g1))")
#    0.00 segundos
#
#    >>> u2 = range(60)
#    >>> g2 = [(x, y) for x in u2 for y in u2]
#    >>> tiempo("transitiva1((u2, g2))")
#    0.42 segundos
#    >>> tiempo("transitiva2((u2, g2))")
#    5.24 segundos
#    >>> tiempo("transitiva3((u2, g2))")
#    4.83 segundos

# En lo sucesivo usaremos la 1ª definición
transitiva = transitiva1

# ---------------------------------------------------------------------
# Ejercicio 9. Definir la función
#    esEquivalencia : (Rel[A]) -> bool
# tal que esEquivalencia(r) se verifica si la relación r es de
# equivalencia. Por ejemplo,
#    >>> esEquivalencia (([1,3,5],[(1,1),(1,3),(3,1),(3,3),(5,5)]))
#    True
#    >>> esEquivalencia (([1,2,3,5],[(1,1),(1,3),(3,1),(3,3),(5,5)]))
#    False
#    >>> esEquivalencia (([1,3,5],[(1,1),(1,3),(3,3),(5,5)]))
#    False
# ---------------------------------------------------------------------

def esEquivalencia(r: Rel[A]) -> bool:
    return reflexiva(r) and simetrica(r) and transitiva(r)

# ---------------------------------------------------------------------
# Ejercicio 10. Definir la función
#    irreflexiva : (Rel[A]) -> bool
# tal que irreflexiva(r) se verifica si la relación r es irreflexiva;
# es decir, si ningún elemento de su universo está relacionado con
# él mismo. Por ejemplo,
#    irreflexiva(([1, 2, 3], [(1, 2), (2, 1), (2, 3)]))  ==  True
#    irreflexiva(([1, 2, 3], [(1, 2), (2, 1), (3, 3)]))  ==  False
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def irreflexiva(r: Rel[A]) -> bool:
    (u, g) = r
    return all(((x, x) not in g for x in u))

# 2ª solución
# ===========

def irreflexiva2(r: Rel[A]) -> bool:
    (u, g) = r
    def aux(xs: list[A]) -> bool:
        if not xs:
            return True
        return (xs[0], xs[0]) not in g and aux(xs[1:])

    return aux(u)

# 3ª solución
# ===========

def irreflexiva3(r: Rel[A]) -> bool:
    (u, g) = r
    for x in u:
        if (x, x) in g:
            return False
    return True

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.integers(min_value=0, max_value=10))
def test_irreflexiva(n: int) -> None:
    r = relacionArbitraria(n)
    res = irreflexiva(r)
    assert irreflexiva2(r) == res
    assert irreflexiva3(r) == res

# ---------------------------------------------------------------------
# Ejercicio 11. Definir la función
#    antisimetrica : (Rel[A]) -> bool
# tal que antisimetrica(r) se verifica si la relación r es
# antisimétrica; es decir, si (x,y) e (y,x) están relacionado, entonces
# x=y. Por ejemplo,
#    >>> antisimetrica(([1,2],[(1,2)]))
#    True
#    >>> antisimetrica(([1,2],[(1,2),(2,1)]))
#    False
#    >>> antisimetrica(([1,2],[(1,1),(2,1)]))
#    True
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def antisimetrica(r: Rel[A]) -> bool:
    (_, g) = r
    return [(x, y) for (x, y) in g if x != y and (y, x) in g] == []

# 2ª solución
# ===========

def antisimetrica2(r: Rel[A]) -> bool:
    (_, g) = r
    return all(((y, x) not in g for (x, y) in g if x != y))

# 3ª solución
# ===========

def antisimetrica3(r: Rel[A]) -> bool:
    (u, g) = r
    return all ((not ((x, y) in g and (y, x) in g) or x == y
                 for x in u for y in u))

# 4ª solución
# ===========

def antisimetrica4(r: Rel[A]) -> bool:
    (_, g) = r
    def aux(xys: list[tuple[A, A]]) -> bool:
        if not xys:
            return True
        (x, y) = xys[0]
        return ((y, x) not in g or x == y) and aux(xys[1:])

    return aux(g)

# 5ª solución
# ===========

def antisimetrica5(r: Rel[A]) -> bool:
    (_, g) = r
    for (x, y) in g:
        if (y, x) in g and x != y:
            return False
    return True

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.integers(min_value=0, max_value=10))
def test_antisimetrica(n: int) -> None:
    r = relacionArbitraria(n)
    res = antisimetrica(r)
    assert antisimetrica2(r) == res
    assert antisimetrica3(r) == res
    assert antisimetrica4(r) == res
    assert antisimetrica5(r) == res

# ---------------------------------------------------------------------
# Ejercicio 12. Definir la función
#    total : (Rel[A]) -> bool
# tal que total(r) se verifica si la relación r es total; es decir, si
# para cualquier par x, y de elementos del universo de r, se tiene que
# x está relacionado con y o y está relacionado con x. Por ejemplo,
#    total (([1,3],[(1,1),(3,1),(3,3)]))  ==  True
#    total (([1,3],[(1,1),(3,1)]))        ==  False
#    total (([1,3],[(1,1),(3,3)]))        ==  False
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def total(r: Rel[A]) -> bool:
    (u, g) = r
    return all(((x, y) in g or (y, x) in g for x in u for y in u))

# 2ª solución
# ===========

# producto(xs, ys) es el producto cartesiano de xs e ys. Por ejemplo,
#    >>> producto([2, 5], [1, 4, 6])
#    [(2, 1), (2, 4), (2, 6), (5, 1), (5, 4), (5, 6)]
def producto(xs: list[A], ys: list[A]) -> list[tuple[A,A]]:
    return [(x, y) for x in xs for y in ys]

# relacionados(g, (x, y)) se verifica si los elementos x e y están
# relacionados por la relación de grafo g. Por ejemplo,
#    relacionados([(2, 3), (3, 1)], (2, 3))  ==  True
#    relacionados([(2, 3), (3, 1)], (3, 2))  ==  True
#    relacionados([(2, 3), (3, 1)], (1, 2))  ==  False
def relacionados(g: list[tuple[A,A]], p: tuple[A,A]) -> bool:
    (x, y) = p
    return (x, y) in g or (y, x) in g

def total2(r: Rel[A]) -> bool:
    (u, g) = r
    return all(relacionados(g, p) for p in producto(u, u))

# 3ª solución
# ===========

def total3(r: Rel[A]) -> bool:
    u, g = r
    return all(relacionados(g, (x, y)) for x in u for y in u)

# 4ª solución
# ===========

def total4(r: Rel[A]) -> bool:
    (u, g) = r
    def aux2(x: A, ys: list[A]) -> bool:
        if not ys:
            return True
        return relacionados(g, (x, ys[0])) and aux2(x, ys[1:])

    def aux1(xs: list[A]) -> bool:
        if not xs:
            return True
        return aux2(xs[0], u) and aux1(xs[1:])

    return aux1(u)

# 5ª solución
# ===========

def total5(r: Rel[A]) -> bool:
    (u, g) = r
    for x in u:
        for y in u:
            if not relacionados(g, (x, y)):
                return False
    return True

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.integers(min_value=0, max_value=10))
def test_total(n: int) -> None:
    r = relacionArbitraria(n)
    res = total(r)
    assert total2(r) == res
    assert total3(r) == res
    assert total4(r) == res
    assert total5(r) == res

# ---------------------------------------------------------------------
# § Clausuras                                                        --
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 13. Definir la función
#    clausuraReflexiva : (Rel[A]) -> Rel[A]
# tal que clausuraReflexiva(r) es la clausura reflexiva de r; es
# decir, la menor relación reflexiva que contiene a r. Por ejemplo,
#    >>> clausuraReflexiva (([1,3],[(1,1),(3,1)]))
#    ([1, 3], [(3, 1), (1, 1), (3, 3)])
# ---------------------------------------------------------------------

def clausuraReflexiva(r: Rel[A]) -> Rel[A]:
    (u, g) = r
    return (u, list(set(g) | {(x, x) for x in u}))

# ---------------------------------------------------------------------
# Ejercicio 14. Definir la función
#    clausuraSimetrica : (Rel[A]) -> Rel[A]
# tal que clausuraSimetrica(r) es la clausura simétrica de r; es
# decir, la menor relación simétrica que contiene a r. Por ejemplo,
#    >>> clausuraSimetrica(([1, 3, 5], [(1, 1), (3, 1), (1, 5)]))
#    ([1, 3, 5], [(1, 5), (3, 1), (1, 1), (1, 3), (5, 1)])
# ---------------------------------------------------------------------

def clausuraSimetrica(r: Rel[A]) -> Rel[A]:
    (u, g) = r
    return (u, list(set(g) | {(y, x) for (x,y) in g}))

# ---------------------------------------------------------------------
# Ejercicio 15. Comprobar con Hipothesis que clausuraSimetrica es
# simétrica.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.integers(min_value=0, max_value=10))
def test_clausuraSimetrica(n: int) -> None:
    r = relacionArbitraria(n)
    assert simetrica(clausuraSimetrica(r))

# ---------------------------------------------------------------------
# Ejercicio 16. Definir la función
#    clausuraTransitiva : (Rel[A]) -> Rel[A]
# tal que clausuraTransitiva(r) es la clausura transitiva de r; es
# decir, la menor relación transitiva que contiene a r. Por ejemplo,
#    >>> clausuraTransitiva (([1, 2, 3, 4, 5, 6], [(1, 2), (2, 5), (5, 6)]))
#    ([1, 2, 3, 4, 5, 6], [(1, 2), (2, 5), (5, 6), (2, 6), (1, 5), (1, 6)])
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def clausuraTransitiva(r: Rel[A]) -> Rel[A]:
    (u, g) = r

    def comp(r: list[tuple[A, A]], s: list[tuple[A, A]]) -> list[tuple[A, A]]:
        return list({(x, z) for (x, y) in r for (y1, z) in s if y == y1})

    def cerradoTr(r: list[tuple[A, A]]) -> bool:
        return subconjunto(comp(r, r), r)

    def union(xs: list[tuple[A, A]], ys: list[tuple[A, A]]) -> list[tuple[A, A]]:
        return xs + [y for y in ys if y not in xs]

    def aux(u1: list[tuple[A, A]]) -> list[tuple[A, A]]:
        if cerradoTr(u1):
            return u1
        return aux(union(u1, comp(u1, u1)))

    return (u, aux(g))

# 2ª solución
# ===========

def clausuraTransitiva2(r: Rel[A]) -> Rel[A]:
    (u, g) = r

    def comp(r: list[tuple[A, A]], s: list[tuple[A, A]]) -> list[tuple[A, A]]:
        return list({(x, z) for (x, y) in r for (y1, z) in s if y == y1})

    def cerradoTr(r: list[tuple[A, A]]) -> bool:
        return subconjunto(comp(r, r), r)

    def union(xs: list[tuple[A, A]], ys: list[tuple[A, A]]) -> list[tuple[A, A]]:
        return xs + [y for y in ys if y not in xs]

    def aux(u1: list[tuple[A, A]]) -> list[tuple[A, A]]:
        if cerradoTr(u1):
            return u1
        return aux(union(u1, comp(u1, u1)))

    g1: list[tuple[A, A]] = g
    while not cerradoTr(g1):
        g1 = union(g1, comp(g1, g1))
    return (u, g1)

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(st.integers(min_value=0, max_value=10))
def test_clausuraTransitiva(n: int) -> None:
    r = relacionArbitraria(n)
    assert clausuraTransitiva(r) == clausuraTransitiva2(r)

# ---------------------------------------------------------------------
# Ejercicio 17. Comprobar con QuickCheck que clausuraTransitiva es
# transitiva.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.integers(min_value=0, max_value=10))
def test_cla(n: int) -> None:
    r = relacionArbitraria(n)
    assert transitiva(clausuraTransitiva(r))

# La comprobación de las propiedades es
#    > poetry run pytest -q relaciones_binarias_homogeneas.py
#    12 passed in 0.66s
