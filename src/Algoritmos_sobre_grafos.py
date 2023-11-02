# Algoritmos_sobre_grafos.py
# Algoritmos sobre grafos.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 1-noviembre-2023
# ======================================================================

# ----------------------------------------------------------------------
# Introducción                                                        --
# ----------------------------------------------------------------------

# En esta relación se presentan los algoritmos fundamentales sobre
# grafos.

# ----------------------------------------------------------------------
# Librerías auxiliares                                                --
# ----------------------------------------------------------------------

from typing import TypeVar

from src.TAD.Grafo import (Grafo, Orientacion, Peso, Vertice, adyacentes,
                           aristas, creaGrafo, creaGrafo_, nodos)

A = TypeVar('A')

# ---------------------------------------------------------------------
# Ejercicio 1. Definir la función,
#    recorridoEnProfundidad : (Vertice, Grafo) -> list[Vertice]
# tal que recorridoEnProfundidad(i, g) es el recorrido en profundidad
# del grafo g desde el vértice i. Por ejemplo, en el grafo
#
#    +---> 2 <---+
#    |           |
#    |           |
#    1 --> 3 --> 6 --> 5
#    |                 |
#    |                 |
#    +---> 4 <---------+
#
# definido por
#    grafo2: Grafo = creaGrafo_(Orientacion.D,
#                               (1,6),
#                               [(1,2),(1,3),(1,4),(3,6),(5,4),(6,2),(6,5)])
# entonces
#    recorridoEnProfundidad(1, grafo2)  ==  [1,2,3,6,5,4]
# -----------------------------------------------------------

grafo2: Grafo = creaGrafo_(Orientacion.D,
                           (1,6),
                           [(1,2),(1,3),(1,4),(3,6),(5,4),(6,2),(6,5)])

# 1ª solución
# ===========

def recorridoEnProfundidad1(i: Vertice, g: Grafo) -> list[Vertice]:
    def rp(cs: list[Vertice], vis: list[Vertice]) -> list[Vertice]:
        if not cs:
            return vis
        d, *ds = cs
        if d in vis:
            return rp(ds, vis)
        return rp(adyacentes(g, d) + ds, vis + [d])
    return rp([i], [])

# Traza del cálculo de recorridoEnProfundidad1(1, grafo1)
#    recorridoEnProfundidad1(1, grafo1)
#    = rp([1],     [])
#    = rp([2,3,4], [1])
#    = rp([3,4],   [1,2])
#    = rp([6,4],   [1,2,3])
#    = rp([2,5,4], [1,2,3,6])
#    = rp([5,4],   [1,2,3,6])
#    = rp([4,4],   [1,2,3,6,5])
#    = rp([4],     [1,2,3,6,5,4])
#    = rp([],      [1,2,3,6,5,4])
#    = [1,2,3,6,5,4]

# 2ª solución
# ===========

def recorridoEnProfundidad(i: Vertice, g: Grafo) -> list[Vertice]:
    def rp(cs: list[Vertice], vis: list[Vertice]) -> list[Vertice]:
        if not cs:
            return vis
        d, *ds = cs
        if d in vis:
            return rp(ds, vis)
        return rp(adyacentes(g, d) + ds, [d] + vis)
    return list(reversed(rp([i], [])))

# Traza del cálculo de (recorridoEnProfundidad(1, grafo1)
#    recorridoEnProfundidad(1, grafo1)
#    = reverse(rp([1],     []))
#    = reverse(rp([2,3,4], [1]))
#    = reverse(rp([3,4],   [2,1]))
#    = reverse(rp([6,4],   [3,2,1]))
#    = reverse(rp([2,5,4], [6,3,2,1]))
#    = reverse(rp([5,4],   [6,3,2,1]))
#    = reverse(rp([4,4],   [5,6,3,2,1]))
#    = reverse(rp([4],     [4,5,6,3,2,1]))
#    = reverse(rp([],      [4,5,6,3,2,1]))
#    = reverse([4,5,6,3,2,1])
#    = [1,2,3,6,5,4]

# Verificación
# ============

def test_recorridoEnProfundidad() -> None:
    grafo3 = creaGrafo_(Orientacion.ND,
                        (1,6),
                        [(1,2),(1,3),(1,4),(3,6),(5,4),(6,2),(6,5)])
    assert recorridoEnProfundidad1(1, grafo2) == [1,2,3,6,5,4]
    assert recorridoEnProfundidad1(1, grafo3) == [1,2,6,3,5,4]
    assert recorridoEnProfundidad(1, grafo2) == [1,2,3,6,5,4]
    assert recorridoEnProfundidad(1, grafo3) == [1,2,6,3,5,4]
    print("Verificado")

# La verificación es
#    >>> test_recorridoEnProfundidad()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 2. Definir la función,
#    recorridoEnAnchura : (Vertice, Grafo) -> list[Vertice]
# tal que recorridoEnAnchura(i, g) es el recorrido en anchura
# del grafo g desde el vértice i. Por ejemplo, en el grafo
#
#    +---> 2 <---+
#    |           |
#    |           |
#    1 --> 3 --> 6 --> 5
#    |                 |
#    |                 |
#    +---> 4 <---------+
#
# definido por
#    grafo4: Grafo = creaGrafo_(Orientacion.D,
#                               (1,6),
#                               [(1,2),(1,3),(1,4),(3,6),(5,4),(6,2),(6,5)])
# entonces
#    recorridoEnAnchura(1, grafo4)  ==  [1,2,3,4,6,5]
# -----------------------------------------------------------

grafo4: Grafo = creaGrafo_(Orientacion.D,
                           (1,6),
                           [(1,2),(1,3),(1,4),(3,6),(5,4),(6,2),(6,5)])

def recorridoEnAnchura(i: Vertice, g: Grafo) -> list[Vertice]:
    def ra(cs: list[Vertice], vis: list[Vertice]) -> list[Vertice]:
        if not cs:
            return vis
        d, *ds = cs
        if d in vis:
            return ra(ds, vis)
        return ra(ds + adyacentes(g, d), [d] + vis)
    return list(reversed(ra([i], [])))

# Traza del cálculo de recorridoEnAnchura(1, grafo4)
#    recorridoEnAnchura(1, grafo4
#    = ra([1],     [])
#    = ra([2,3,4], [1])
#    = ra([3,4],   [2,1])
#    = ra([4,6],   [3,2,1])
#    = ra([6],     [4,3,2,1])
#    = ra([2,5],   [6,4,3,2,1])
#    = ra([5],     [6,4,3,2,1])
#    = ra([4],     [5,6,4,3,2,1])
#    = ra([],      [5,6,4,3,2,1])
#    = [1,2,3,4,6,5]

# Verificación
# ============

def test_recorridoEnAnchura() -> None:
    grafo5 = creaGrafo_(Orientacion.ND,
                        (1,6),
                        [(1,2),(1,3),(1,4),(3,6),(5,4),(6,2),(6,5)])
    assert recorridoEnAnchura(1, grafo4) == [1,2,3,4,6,5]
    assert recorridoEnAnchura(1, grafo5) == [1,2,3,4,6,5]
    print("Verificado")

# La verificación es
#    >>> test_recorridoEnAnchura()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 3. El [algoritmo de Kruskal]()https://bit.ly/3N8bOOg)
# calcula un árbol recubridor mínimo en un grafo conexo y ponderado. Es
# decir, busca un subconjunto de aristas que, formando un árbol,
# incluyen todos los vértices y donde el valor de la suma de todas las
# aristas del árbol es el mínimo.
#
# El algoritmo de Kruskal funciona de la siguiente manera:
# + se crea un bosque B (un conjunto de árboles), donde cada vértice
#   del grafo es un árbol separado
# + se crea un conjunto C que contenga a todas las aristas del grafo
# + mientras C es no vacío,
#   + eliminar una arista de peso mínimo de C
#   + si esa arista conecta dos árboles diferentes se añade al bosque,
#     combinando los dos árboles en un solo árbol
#   + en caso contrario, se desecha la arista
# Al acabar el algoritmo, el bosque tiene un solo componente, el cual
# forma un árbol de expansión mínimo del grafo.
#
# Definir la función,
#    kruskal : (Grafo) -> list[tuple[Peso, Vertice, Vertice]]
# tal que kruskal(g) es el árbol de expansión mínimo del grafo g calculado
# mediante el algoritmo de Kruskal. Por ejemplo, si g1, g2, g3 y g4 son
# los grafos definidos por
#    g1 = creaGrafo (Orientacion.ND,
#                    (1,5),
#                    [((1,2),12),((1,3),34),((1,5),78),
#                     ((2,4),55),((2,5),32),
#                     ((3,4),61),((3,5),44),
#                     ((4,5),93)])
#    g2 = creaGrafo (Orientacion.ND,
#                    (1,5),
#                    [((1,2),13),((1,3),11),((1,5),78),
#                     ((2,4),12),((2,5),32),
#                     ((3,4),14),((3,5),44),
#                     ((4,5),93)])
#    g3 = creaGrafo (Orientacion.ND,
#                    (1,7),
#                    [((1,2),5),((1,3),9),((1,5),15),((1,6),6),
#                     ((2,3),7),
#                     ((3,4),8),((3,5),7),
#                     ((4,5),5),
#                     ((5,6),3),((5,7),9),
#                     ((6,7),11)])
#    g4 = creaGrafo (Orientacion.ND,
#                    (1,7),
#                    [((1,2),5),((1,3),9),((1,5),15),((1,6),6),
#                     ((2,3),7),
#                     ((3,4),8),((3,5),1),
#                     ((4,5),5),
#                     ((5,6),3),((5,7),9),
#                     ((6,7),11)])
# entonces
#    kruskal(g1) == [(55,2,4),(34,1,3),(32,2,5),(12,1,2)]
#    kruskal(g2) == [(32,2,5),(13,1,2),(12,2,4),(11,1,3)]
#    kruskal(g3) == [(9,5,7),(7,2,3),(6,1,6),(5,4,5),(5,1,2),(3,5,6)]
#    kruskal(g4) == [(9,5,7),(6,1,6),(5,4,5),(5,1,2),(3,5,6),(1,3,5)]
# ---------------------------------------------------------------------

g1 = creaGrafo (Orientacion.ND,
                (1,5),
                [((1,2),12),((1,3),34),((1,5),78),
                 ((2,4),55),((2,5),32),
                 ((3,4),61),((3,5),44),
                 ((4,5),93)])
g2 = creaGrafo (Orientacion.ND,
                (1,5),
                [((1,2),13),((1,3),11),((1,5),78),
                 ((2,4),12),((2,5),32),
                 ((3,4),14),((3,5),44),
                 ((4,5),93)])
g3 = creaGrafo (Orientacion.ND,
                (1,7),
                [((1,2),5),((1,3),9),((1,5),15),((1,6),6),
                 ((2,3),7),
                 ((3,4),8),((3,5),7),
                 ((4,5),5),
                 ((5,6),3),((5,7),9),
                 ((6,7),11)])
g4 = creaGrafo (Orientacion.ND,
                (1,7),
                [((1,2),5),((1,3),9),((1,5),15),((1,6),6),
                 ((2,3),7),
                 ((3,4),8),((3,5),1),
                 ((4,5),5),
                 ((5,6),3),((5,7),9),
                 ((6,7),11)])

# raiz(d, n) es la raíz de n en el diccionario. Por ejemplo,
#    raiz({1:1, 3:1, 4:3, 5:4, 2:6, 6:6}, 5)  == 1
#    raiz({1:1, 3:1, 4:3, 5:4, 2:6, 6:6}, 2)  == 6
def raiz(d: dict[Vertice, Vertice], x: Vertice) -> Vertice:
    v = d[x]
    if v == x:
        return v
    return raiz(d, v)

# modificaR(x, y, y_, d) actualiza d como sigue:
# + el valor de todas las claves z con valor y es y_
# + el valor de todas las claves z con (z > x) con valor x es y_
def modificaR(x: Vertice,
              y: Vertice,
              y_: Vertice,
              d: dict[Vertice, Vertice]) -> dict[Vertice, Vertice]:
    def aux1(vs: list[Vertice],
             tb: dict[Vertice, Vertice],
             y: Vertice) -> dict[Vertice, Vertice]:
        for a in vs:
            if tb[a] == y:
                tb[a] = y_
        return tb

    def aux2(vs: list[Vertice],
             tb: dict[Vertice, Vertice],
             y_: Vertice) -> dict[Vertice, Vertice]:
        for b in vs:
            if tb[b] == x:
                tb[b] = y_
        return tb

    cs = list(d.keys())
    ds = [c for c in cs if c > x]

    tb = aux1(cs, d, y)
    tb = aux2(ds, tb, y_)

    return tb

# buscaActualiza(a, d) es el par formado por False y el diccionario d,
# si los dos vértices de la arista a tienen la misma raíz en d y el par
# formado por True y la tabla obtenida añadiéndole a d la arista
# formada por el vértice de a de mayor raíz y la raíz del vértice de a
# de menor raíz. Y actualizando las raices de todos los elementos
# afectados por la raíz añadida. Por ejemplo,
#    >>> buscaActualiza((5,4), {1:1, 2:1, 3:3, 4:4, 5:5, 6:5, 7:7})
#    (True, {1: 1, 2: 1, 3: 3, 4: 4, 5: 4, 6: 4, 7: 7})
#    >>> buscaActualiza((6,1), {1:1, 2:1, 3:3, 4:4, 5:4, 6:4, 7:7})
#    (True, {1: 1, 2: 1, 3: 3, 4: 1, 5: 1, 6: 1, 7: 7})
#    >>> buscaActualiza((6,2), {1:1, 2:1, 3:3, 4:1, 5:4, 6:5, 7:7})
#    (False, {1: 1, 2: 1, 3: 3, 4: 1, 5: 4, 6: 5, 7: 7})
def buscaActualiza(a: tuple[Vertice, Vertice],
                   d: dict[Vertice, Vertice]) -> tuple[bool,
                                                       dict[Vertice, Vertice]]:
    x, y = a
    x_ = raiz(d, x)
    y_ = raiz(d, y)

    if x_ == y_:
        return False, d
    if y_ < x_:
        return True, modificaR(x, d[x], y_, d)
    return True, modificaR(y, d[y], x_, d)

def kruskal(g: Grafo) -> list[tuple[Peso, Vertice, Vertice]]:
    def aux(as_: list[tuple[Peso, Vertice, Vertice]],
            d: dict[Vertice, Vertice],
            ae: list[tuple[Peso, Vertice, Vertice]],
            n: int) -> list[tuple[Peso, Vertice, Vertice]]:
        if n == 0:
            return ae
        p, x, y = as_[0]
        actualizado, d = buscaActualiza((x, y), d)
        if actualizado:
            return aux(as_[1:], d, [(p, x, y)] + ae, n - 1)
        return aux(as_[1:], d, ae, n)
    return aux(list(sorted([(p, x, y) for ((x, y), p) in aristas(g)])),
               {x: x for x in nodos(g)},
               [],
               len(nodos(g)) - 1)

# Traza del diccionario correspondiente al grafo g3
# =================================================

# Lista de aristas, ordenadas según su peso:
# [(3,5,6),(5,1,2),(5,4,5),(6,1,6),(7,2,3),(7,3,5),(8,3,4),(9,1,3),(9,5,7),(11,6,7),(15,1,5)]
#
# Inicial
#   {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7}
#
# Después de añadir la arista (5,6) de peso 3
#   {1:1, 2:2, 3:3, 4:4, 5:5, 6:5, 7:7}
#
# Después de añadir la arista (1,2) de peso 5
#   {1:1, 2:1, 3:3, 4:4, 5:5, 6:5, 7:7}
#
# Después de añadir la arista (4,5) de peso 5
#   {1:1, 2:1, 3:3, 4:4, 5:4, 6:4, 7:7}
#
# Después de añadir la arista (1,6) de peso 6
#   {1:1, 2:1, 3:3, 4:1, 5:1, 6:1, 7:7}
#
# Después de añadir la arista (2,3) de peso 7
#   {1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:7}
#
# Las posibles aristas a añadir son:
# + la (3,5) con peso 7, que no es posible pues la raíz de 3
#   coincide con la raíz de 5, por lo que formaría un ciclo
# + la (3,4) con peso 8, que no es posible pues la raíz de 3
#   coincide con la raíz de 4, por lo que formaría un ciclo
# + la (1,3) con peso 9, que no es posible pues la raíz de 3
#   coincide con la raíz de 1, por lo que formaría un ciclo
# + la (5,7) con peso 9, que no forma ciclo
#
# Después de añadir la arista (5,7) con peso 9
#    {1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1}
#
# No es posible añadir más aristas, pues formarían ciclos.

# Verificación
# ============

def test_kruskal() -> None:
    assert kruskal(g1) == [(55,2,4),(34,1,3),(32,2,5),(12,1,2)]
    assert kruskal(g2) == [(32,2,5),(13,1,2),(12,2,4),(11,1,3)]
    assert kruskal(g3) == [(9,5,7),(7,2,3),(6,1,6),(5,4,5),(5,1,2),(3,5,6)]
    assert kruskal(g4) == [(9,5,7),(6,1,6),(5,4,5),(5,1,2),(3,5,6),(1,3,5)]
    print("Vefificado")

# La verificación es
#    >>> test_kruskal()
#    Vefificado

# ---------------------------------------------------------------------
# Ejercicio 4. El [algoritmo de Prim](https://bit.ly/466fwRe) calcula un
# árbol recubridor mínimo en un grafo conexo y ponderado. Es decir,
# busca un subconjunto de aristas que, formando un árbol, incluyen todos
# los vértices y donde el valor de la suma de todas las aristas del
# árbol es el mínimo.
#
# El algoritmo de Prim funciona de la siguiente manera:
# + Inicializar un árbol con un único vértice, elegido arbitrariamente,
#   del grafo.
# + Aumentar el árbol por un lado. Llamamos lado a la unión entre dos
#   vértices: de las posibles uniones que pueden conectar el árbol a los
#   vértices que no están aún en el árbol, encontrar el lado de menor
#   distancia y unirlo al árbol.
# + Repetir el paso 2 (hasta que todos los vértices pertenezcan al
#   árbol)
#
# Usando el [tipo abstracto de datos de los grafos](https://bit.ly/45cQ3Fo),
# definir la función,
#    prim : (Grafo) -> list[tuple[Peso, Vertice, Vertice]]
# tal que prim(g) es el árbol de expansión mínimo del grafo g
# calculado mediante el algoritmo de Prim. Por ejemplo, si g1, g2, g3 y
# g4 son los grafos definidos en el ejercicio anterior,
# entonces
#    prim(g1)  == [(55,2,4),(34,1,3),(32,2,5),(12,1,2)]
#    prim(g2)  == [(32,2,5),(12,2,4),(13,1,2),(11,1,3)]
#    prim(g3)  == [(9,5,7),(7,2,3),(5,5,4),(3,6,5),(6,1,6),(5,1,2)]
# ---------------------------------------------------------------------

def prim(g: Grafo) -> list[tuple[Peso, Vertice, Vertice]]:
    n, *ns = nodos(g)
    def prim_(t: list[Vertice],
              r: list[Vertice],
              ae: list[tuple[Peso, Vertice, Vertice]],
              as_: list[tuple[tuple[Vertice, Vertice], Peso]]) \
              -> list[tuple[Peso, Vertice, Vertice]]:
        if not as_:
            return []
        if not r:
            return ae
        e = min(((c,u,v)
                 for ((u,v),c) in as_
                 if u in t and v in r))
        (_,_, v_) = e
        return prim_([v_] + t, [x for x in r if x != v_], [e] + ae, as_)
    return prim_([n], ns, [], aristas(g))

# Verificación
# ============

def test_prim() -> None:
    assert prim(g1)  == [(55,2,4),(34,1,3),(32,2,5),(12,1,2)]
    assert prim(g2)  == [(32,2,5),(12,2,4),(13,1,2),(11,1,3)]
    assert prim(g3)  == [(9,5,7),(7,2,3),(5,5,4),(3,6,5),(6,1,6),(5,1,2)]
    print("Verificado")

# La verificación es
#    >>> test_prim()
#    Verificado

# Verificación
# ============

# La comprobación es
#    src> poetry run pytest -v Algoritmos_sobre_grafos.py
#    === session starts ==================================================
#    test_recorridoEnProfundidad PASSED
#    test_recorridoEnAnchura PASSED
#    test_kruskal PASSED
#    test_prim PASSED
#    === passed in 0.12s ===================================================
