# Problemas_basicos_de_grafos.py
# Problemas básicos con el TAD de los grafos.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla,  1-noviembre-2023
# ======================================================================

# ----------------------------------------------------------------------
# Introducción                                                        --
# ----------------------------------------------------------------------

# El objetivo de esta relación de ejercicios es definir funciones sobre
# el TAD de los grafos usando las implementaciones de los ejercicios
# anteriores.

# ----------------------------------------------------------------------
# Importación de librerías                                            --
# ----------------------------------------------------------------------

from typing import Any, Optional

from hypothesis import given
from hypothesis import strategies as st
from hypothesis.strategies import composite

from src.TAD.Grafo import (Grafo, Orientacion, Vertice, adyacentes, aristaEn,
                           aristas, creaGrafo_, dirigido, nodos)

# ---------------------------------------------------------------------
# Ejercicio 1. El grafo completo de orden n, K(n), es un grafo no
# dirigido cuyos conjunto de vértices es {1,..n} y tiene una arista
# entre cada par de vértices distintos.
#
# Usando el [tipo abstracto de datos de los grafos](https://bit.ly/45cQ3Fo),
# definir la función,
#    completo : (int) -> Grafo
# tal que completo(n) es el grafo completo de orden n. Por ejemplo,
#    >>> completo(4)
#    G ND ([1, 2, 3, 4],
#          [((1, 2), 0), ((1, 3), 0), ((1, 4), 0),
#           ((2, 1), 0), ((2, 3), 0), ((2, 4), 0),
#           ((3, 1), 0), ((3, 2), 0), ((3, 4), 0),
#           ((4, 1), 0), ((4, 2), 0), ((4, 3), 0)])
# ---------------------------------------------------------------------

def completo(n: int) -> Grafo:
    return creaGrafo_(Orientacion.ND,
                      (1, n),
                      [(x, y)
                       for x in range(1, n + 1)
                       for y in range(x + 1, n+1)])

# Verificación
# ============

def test_completo() -> None:
    assert str(completo(4)) == \
        "G ND ([1, 2, 3, 4], [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)])"
    print("Verificado")

# La verificación es
#    >>> test_completo()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 2. El ciclo de orden n, C(n), es un grafo no dirigido cuyo
# conjunto de vértices es {1,...,n} y las aristas son
#    (1,2), (2,3), ..., (n-1,n), (n,1)
#
# Definir la función,
#    grafoCiclo : (Int) -> Grafo
# tal que grafoCiclo(n) es el grafo ciclo de orden n. Por ejemplo,
#    >>> grafoCiclo(3)
#    G ND ([1, 2, 3], [(1, 2), (1, 3), (2, 3)])
# ---------------------------------------------------------------------

def grafoCiclo(n: int) -> Grafo:
    return creaGrafo_(Orientacion.ND,
                      (1, n),
                      [(n,1)] + [(x, x + 1) for x in range(1, n)])

# Verificación
# ============

def test_grafoCiclo() -> None:
    assert str(grafoCiclo(3)) == \
        "G ND ([1, 2, 3], [(1, 2), (1, 3), (2, 3)])"
    print("Verificado")

# La verificación es
#    >>> test_grafoCiclo()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 3. Definir la función,
#    nVertices : (Grafo) -> int
# tal que nVertices(g) es el número de vértices del grafo g. Por
# ejemplo,
#    >>> nVertices(creaGrafo_(Orientacion.D, (1,5), [(1,2),(3,1)]))
#    5
#    >>> nVertices(creaGrafo_(Orientacion.ND, (2,4), [(1,2),(3,1)]))
#    3
# ---------------------------------------------------------------------

def nVertices(g: Grafo) -> int:
    return len(nodos(g))

# Verificación
# ============

def test_nVertices() -> None:
    assert nVertices(creaGrafo_(Orientacion.D, (1,5), [(1,2),(3,1)])) == 5
    assert nVertices(creaGrafo_(Orientacion.ND, (2,4), [(1,2),(3,1)])) == 3
    print("Verificado")

# La verificación es
#    >>> test_nVertices()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 4. En un un grafo g, los incidentes de un vértice v es el
# conjuntos de vértices x de g para los que hay un arco (o una arista)
# de x a v; es decir, que v es adyacente a x.
#
# Definir la función,
#    incidentes :: (Ix v,Num p) => (Grafo v p) -> v -> [v]
# tal que (incidentes g v) es la lista de los vértices incidentes en el
# vértice v. Por ejemplo,
#    λ> g1 = creaGrafo_(Orientacion.D, (1,3), [(1,2),(2,2),(3,1),(3,2)])
#    λ> incidentes(g1,1)
#    [3]
#    λ> incidentes g1 2
#    [1,2,3]
#    λ> incidentes g1 3
#    []
#    λ> g2 = creaGrafo_(Orientacion.ND, (1,3), [(1,2),(2,2),(3,1),(3,2)])
#    λ> incidentes g2 1
#    [2,3]
#    λ> incidentes g2 2
#    [1,2,3]
#    λ> incidentes g2 3
#    [1,2]
# ---------------------------------------------------------------------

def incidentes(g: Grafo, v: Vertice) -> list[Vertice]:
    return [x for x in nodos(g) if v in adyacentes(g, x)]

# Verificación
# ============

def test_incidentes() -> None:
    g1 = creaGrafo_(Orientacion.D, (1,3), [(1,2),(2,2),(3,1),(3,2)])
    g2 = creaGrafo_(Orientacion.ND, (1,3), [(1,2),(2,2),(3,1),(3,2)])
    assert incidentes(g1,1) == [3]
    assert incidentes(g1,2) == [1, 2, 3]
    assert incidentes(g1,3) == []
    assert incidentes(g2, 1) == [2, 3]
    assert incidentes(g2, 2) == [1, 2, 3]
    assert incidentes(g2, 3) == [1, 2]
    print("Verificado")

# La verificación es
#    >>> test_incidentes()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 5. En un un grafo g, los contiguos de un vértice v es el
# conjuntos de vértices x de g tales que x es adyacente o incidente con v.
#
# Definir la función,
#    contiguos : (Grafo, Vertice) -> list[Vertice]
# tal que (contiguos g v) es el conjunto de los vértices de g contiguos
# con el vértice v. Por ejemplo,
#    >>> g1 = creaGrafo_(Orientacion.D, (1,3), [(1,2),(2,2),(3,1),(3,2)])
#    >>> contiguos(g1, 1)
#    [2, 3]
#    >>> contiguos(g1, 2)
#    [1, 2, 3]
#    >>> contiguos(g1, 3)
#    [1, 2]
#    >>> g2 = creaGrafo_(Orientacion.ND, (1,3), [(1,2),(2,2),(3,1),(3,2)])
#    >>> contiguos(g2, 1)
#    [2, 3]
#    >>> contiguos(g2, 2)
#    [1, 2, 3]
#    >>> contiguos(g2, 3)
#    [1, 2]
# ---------------------------------------------------------------------

def contiguos(g: Grafo, v: Vertice) -> list[Vertice]:
    return list(set(adyacentes(g, v) + incidentes(g, v)))

# Verificación
# ============

def test_contiguos() -> None:
    g1 = creaGrafo_(Orientacion.D, (1,3), [(1,2),(2,2),(3,1),(3,2)])
    g2 = creaGrafo_(Orientacion.ND, (1,3), [(1,2),(2,2),(3,1),(3,2)])
    assert contiguos(g1, 1) == [2, 3]
    assert contiguos(g1, 2) == [1, 2, 3]
    assert contiguos(g1, 3) == [1, 2]
    assert contiguos(g2, 1) == [2, 3]
    assert contiguos(g2, 2) == [1, 2, 3]
    assert contiguos(g2, 3) == [1, 2]
    print("Verificado")

# La verificación es
#    >>> test_contiguos()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 6. Definir la función
#    lazos  : (Grafo) -> list[tuple[Vertice, Vertice]]
# tal que lazos(g) es el conjunto de los lazos (es decir, aristas cuyos
# extremos son iguales) del grafo g. Por ejemplo,
#    >>> ej1 = creaGrafo_(Orientacion.D, (1,3), [(1,1),(2,3),(3,2),(3,3)])
#    >>> ej2 = creaGrafo_(Orientacion.ND, (1,3), [(2,3),(3,1)])
#    >>> lazos(ej1)
#    [(1,1),(3,3)]
#    >>> lazos(ej2)
#    []
# ---------------------------------------------------------------------

def lazos(g: Grafo) -> list[tuple[Vertice, Vertice]]:
    return [(x, x) for x in nodos(g) if aristaEn(g, (x, x))]

# Verificación
# ============

def test_lazos() -> None:
    ej1 = creaGrafo_(Orientacion.D, (1,3), [(1,1),(2,3),(3,2),(3,3)])
    ej2 = creaGrafo_(Orientacion.ND, (1,3), [(2,3),(3,1)])
    assert lazos(ej1) == [(1,1),(3,3)]
    assert lazos(ej2) == []
    print("Verificado")

# La verificación es
#    >>> test_lazos()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 7. Definir la función
#    nLazos : (Grafo) -> int
# tal que nLazos(g) es el número de lazos del grafo g. Por ejemplo,
#    >>> nLazos(ej1)
#    2
#    >>> nLazos(ej2)
#    0
# ---------------------------------------------------------------------

def nLazos(g: Grafo) -> int:
    return len(lazos(g))

# Verificación
# ============

def test_nLazos() -> None:
    ej1 = creaGrafo_(Orientacion.D, (1,3), [(1,1),(2,3),(3,2),(3,3)])
    ej2 = creaGrafo_(Orientacion.ND, (1,3), [(2,3),(3,1)])
    assert nLazos(ej1) == 2
    assert nLazos(ej2) == 0
    print("Verificado")

# La verificación es
#    >>> test_nLazos()
#    Verificado

#  ---------------------------------------------------------------------
#  Ejercicio 8. Definir la función,
#     nAristas : (Grafo) -> int
#  tal que nAristas(g) es el número de aristas del grafo g. Si g es no
#  dirigido, las aristas de v1 a v2 y de v2 a v1 sólo se cuentan una
#  vez. Por ejemplo,
#     g1 = creaGrafo_(Orientacion.ND, (1,5), [(1,2),(1,3),(1,5),(2,4),(2,5),(3,4),(3,5),(4,5)])
#     g2 = creaGrafo_(Orientacion.D, (1,5), [(1,2),(1,3),(1,5),(2,4),(2,5),(4,3),(4,5)])
#     g3 = creaGrafo_(Orientacion.ND, (1,3), [(1,2),(1,3),(2,3),(3,3)])
#     g4 = creaGrafo_(Orientacion.ND, (1,4), [(1,1),(1,2),(3,3)])
#     >>> nAristas(g1)
#     8
#     >>> nAristas(g2)
#     7
#     >>> nAristas(g3)
#     4
#     >>> nAristas(g4)
#     3
#     >>> nAristas(completo(4))
#     6
#     >>> nAristas(completo(5))
#     10
#  ---------------------------------------------------------------------

# 1ª solución
# ===========

def nAristas(g: Grafo) -> int:
    if dirigido(g):
        return len(aristas(g))
    return (len(aristas(g)) + nLazos(g)) // 2

# 2ª solución
# ===========

def nAristas2(g: Grafo) -> int:
    if dirigido(g):
        return len(aristas(g))
    return len([(x, y) for ((x,y),_) in aristas(g) if x <= y])

# Verificación
# ============

def test_nAristas() -> None:
    g1 = creaGrafo_(Orientacion.ND, (1,5),
                    [(1,2),(1,3),(1,5),(2,4),(2,5),(3,4),(3,5),(4,5)])
    g2 = creaGrafo_(Orientacion.D, (1,5),
                    [(1,2),(1,3),(1,5),(2,4),(2,5),(4,3),(4,5)])
    g3 = creaGrafo_(Orientacion.ND, (1,3), [(1,2),(1,3),(2,3),(3,3)])
    g4 = creaGrafo_(Orientacion.ND, (1,4), [(1,1),(1,2),(3,3)])
    for nAristas_ in [nAristas, nAristas2]:
        assert nAristas_(g1) == 8
        assert nAristas_(g2) == 7
        assert nAristas_(g3) == 4
        assert nAristas_(g4) == 3
        assert nAristas_(completo(4)) == 6
        assert nAristas_(completo(5)) == 10
    print("Verificado")

# La verificación es
#    >>> test_nAristas()
#    Verificado

# ---------------------------------------------------------------------
#  Ejercicio 9. Definir la función
#     prop_nAristasCompleto : (int) -> bool
#  tal que prop_nAristasCompleto(n) se verifica si el número de aristas
#  del grafo completo de orden n es n*(n-1)/2 y, usando la función,
#  comprobar que la propiedad se cumple para n de 1 a 20.
# ---------------------------------------------------------------------

def prop_nAristasCompleto(n: int) -> bool:
    return nAristas(completo(n)) == n*(n-1) // 2

# La comprobación es
#    >>> all(prop_nAristasCompleto(n) for n in range(1, 21))
#    True

# ---------------------------------------------------------------------
# Ejercicio 10. El grado positivo de un vértice v de un grafo g es el
# número de vértices de g adyacentes con v.
#
# Definir la función
#    gradoPos : (Grafo, Vertice) -> int
# tal que gradoPos(g, v) es el grado positivo del vértice v en el grafo
# g. Por ejemplo,
#    g1 = creaGrafo_(Orientacion.ND, (1,5),
#                    [(1,2),(1,3),(1,5),(2,4),(2,5),(3,4),(3,5),(4,5)])
#    g2 = creaGrafo_(Orientacion.D, (1,5),
#                    [(1,2),(1,3),(1,5),(2,4),(2,5),(4,3),(4,5)])
#    λ> gradoPos(g1, 5)
#    4
#    λ> gradoPos(g2, 5)
#    0
#    λ> gradoPos(g2, 1)
#    3
# ---------------------------------------------------------------------

def gradoPos(g: Grafo, v: Vertice) -> int:
    return len(adyacentes(g, v))

# Verificación
# ============

def test_GradoPos() -> None:
    g1 = creaGrafo_(Orientacion.ND, (1,5),
                    [(1,2),(1,3),(1,5),(2,4),(2,5),(3,4),(3,5),(4,5)])
    g2 = creaGrafo_(Orientacion.D, (1,5),
                    [(1,2),(1,3),(1,5),(2,4),(2,5),(4,3),(4,5)])
    assert gradoPos(g1, 5) == 4
    assert gradoPos(g2, 5) == 0
    assert gradoPos(g2, 1) == 3
    print("Verificado")

# La verificación es
#    >>> test_GradoPos()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 11. El grado negativo de un vértice v de un grafo g es el
# número de vértices de g incidentes con v.
#
# Definir la función
#    gradoNeg : (Grafo, Vertice) -> int
# tal que gradoNeg(g, v) es el grado negativo del vértice v en el grafo
# g. Por ejemplo,
#      g1 = creaGrafo_(Orientacion.ND, (1,5),
#                      [(1,2),(1,3),(1,5),(2,4),(2,5),(3,4),(3,5),(4,5)])
#      g2 = creaGrafo_(Orientacion.D, (1,5),
#                      [(1,2),(1,3),(1,5),(2,4),(2,5),(4,3),(4,5)])
#      λ> gradoNeg(g1, 5)
#      4
#      λ> gradoNeg(g2, 5)
#      3
#      λ> gradoNeg(g2, 1)
#      0
# ---------------------------------------------------------------------

def gradoNeg(g: Grafo, v: Vertice) -> int:
    return len(incidentes(g, v))

# Verificación
# ============

def test_GradoNeg() -> None:
    g1 = creaGrafo_(Orientacion.ND, (1,5),
                    [(1,2),(1,3),(1,5),(2,4),(2,5),(3,4),(3,5),(4,5)])
    g2 = creaGrafo_(Orientacion.D, (1,5),
                    [(1,2),(1,3),(1,5),(2,4),(2,5),(4,3),(4,5)])
    assert gradoNeg(g1, 5) == 4
    assert gradoNeg(g2, 5) == 3
    assert gradoNeg(g2, 1) == 0
    print("Verificado")

# La verificación es
#    >>> test_GradoPosNeg()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 12. Definir un generador de grafos para comprobar
# propiedades de grafos con Hypothesis.
# ---------------------------------------------------------------------

# Generador de aristas. Por ejemplo,
#    >>> gen_aristas(5).example()
#    [(2, 5), (4, 5), (1, 2), (2, 3), (4, 1)]
#    >>> gen_aristas(5).example()
#    [(3, 4)]
#    >>> gen_aristas(5).example()
#    [(5, 3), (3, 2), (1, 3), (5, 2)]
@composite
def gen_aristas(draw: Any, n: int) -> list[tuple[int, int]]:
    as_ = draw(st.lists(st.tuples(st.integers(1,n),
                                  st.integers(1,n)),
                        unique=True))
    return as_

# Generador de grafos no dirigidos. Por ejemplo,
#    >>> gen_grafoND().example()
#    G ND ([1, 2, 3, 4, 5], [(1, 4), (5, 5)])
#    >>> gen_grafoND().example()
#    G ND ([1], [])
#    >>> gen_grafoND().example()
#    G ND ([1, 2, 3, 4, 5, 6, 7, 8], [(7, 7)])
#    >>> gen_grafoND().example()
#    G ND ([1, 2, 3, 4, 5, 6], [(1, 3), (2, 4), (3, 3), (3, 5)])
@composite
def gen_grafoND(draw: Any) -> Grafo:
    n = draw(st.integers(1,10))
    as_ = [(x, y) for (x, y ) in draw(gen_aristas(n)) if x <= y]
    return creaGrafo_(Orientacion.ND, (1,n), as_)

# Generador de grafos dirigidos. Por ejemplo,
#    >>> gen_grafoD().example()
#    G D ([1, 2, 3, 4], [(3, 3), (4, 1)])
#    >>> gen_grafoD().example()
#    G D ([1, 2], [(1, 1), (2, 1), (2, 2)])
#    >>> gen_grafoD().example()
#    G D ([1, 2], [])
@composite
def gen_grafoD(draw: Any) -> Grafo:
    n = draw(st.integers(1,10))
    as_ = draw(gen_aristas(n))
    return creaGrafo_(Orientacion.D, (1,n), as_)

# Generador de grafos. Por ejemplo,
#    >>> gen_grafo().example()
#    G ND ([1, 2, 3, 4, 5, 6, 7], [(1, 3)])
#    >>> gen_grafo().example()
#    G D ([1], [])
#    >>> gen_grafo().example()
#    G D ([1, 2, 3, 4, 5, 6, 7], [(1, 3), (3, 4), (5, 5)])
@composite
def gen_grafo(draw: Any) -> Grafo:
    o = draw(st.sampled_from([Orientacion.D, Orientacion.ND]))
    if o == Orientacion.ND:
        return draw(gen_grafoND())
    return draw(gen_grafoD())

# ---------------------------------------------------------------------
# Ejercicio 13. Comprobar con Hypothesis que para cualquier grafo g, las
# sumas de los grados positivos y la de los grados negativos de los
# vértices de g son iguales
# ---------------------------------------------------------------------

# La propiedad es
@given(gen_grafo())
def test_sumaGrados(g: Grafo) -> None:
    vs = nodos(g)
    assert sum((gradoPos(g, v) for v in vs)) == sum((gradoNeg(g, v) for v in vs))

# La comprobación es
#    >>> test_sumaGrados()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 14. El grado de un vértice v de un grafo dirigido g, es el
# número de aristas de g que contiene a v. Si g es no dirigido, el grado
# de un vértice v es el número de aristas incidentes en v, teniendo en
# cuenta que los lazos se cuentan dos veces.
#
# Definir las funciones,
#    grado : (Grafo, Vertice) -> int
# tal que grado(g, v) es el grado del vértice v en el grafo g. Por
# ejemplo,
#    >>> g1 = creaGrafo_(Orientacion.ND, (1,5),
#                        [(1,2),(1,3),(1,5),(2,4),(2,5),(3,4),(3,5),(4,5)])
#    >>> g2 = creaGrafo_(Orientacion.D, (1,5),
#                        [(1,2),(1,3),(1,5),(2,4),(2,5),(4,3),(4,5)])
#    >>> g3 = creaGrafo_(Orientacion.D, (1,3),
#                        [(1,2),(2,2),(3,1),(3,2)])
#    >>> g4 = creaGrafo_(Orientacion.D, (1,1),
#                        [(1,1)])
#    >>> g5 = creaGrafo_(Orientacion.ND, (1,3),
#                        [(1,2),(1,3),(2,3),(3,3)])
#    >>> g6 = creaGrafo_(Orientacion.D, (1,3),
#                        [(1,2),(1,3),(2,3),(3,3)])
#    >>> grado(g1, 5)
#    4
#    >>> grado(g2, 5)
#    3
#    >>> grado(g2, 1)
#    3
#    >>> grado(g3, 2)
#    4
#    >>> grado(g3, 1)
#    2
#    >>> grado(g3, 3)
#    2
#    >>> grado(g4, 1)
#    2
#    >>> grado(g5, 3)
#    4
#    >>> grado(g6, 3)
#    4
# ---------------------------------------------------------------------

def grado(g: Grafo, v: Vertice) -> int:
    if dirigido(g):
        return gradoNeg(g, v) + gradoPos(g, v)
    if (v, v) in lazos(g):
        return len(incidentes(g, v)) + 1
    return len(incidentes(g, v))

# Verificación
# ============

def test_grado() -> None:
    g1 = creaGrafo_(Orientacion.ND, (1,5),
                    [(1,2),(1,3),(1,5),(2,4),(2,5),(3,4),(3,5),(4,5)])
    g2 = creaGrafo_(Orientacion.D, (1,5),
                    [(1,2),(1,3),(1,5),(2,4),(2,5),(4,3),(4,5)])
    g3 = creaGrafo_(Orientacion.D, (1,3),
                    [(1,2),(2,2),(3,1),(3,2)])
    g4 = creaGrafo_(Orientacion.D, (1,1),
                    [(1,1)])
    g5 = creaGrafo_(Orientacion.ND, (1,3),
                    [(1,2),(1,3),(2,3),(3,3)])
    g6 = creaGrafo_(Orientacion.D, (1,3),
                    [(1,2),(1,3),(2,3),(3,3)])
    assert grado(g1, 5) == 4
    assert grado(g2, 5) == 3
    assert grado(g2, 1) == 3
    assert grado(g3, 2) == 4
    assert grado(g3, 1) == 2
    assert grado(g3, 3) == 2
    assert grado(g4, 1) == 2
    assert grado(g5, 3) == 4
    assert grado(g6, 3) == 4
    print("Verificado")

# La verificación es
#    >>> test_grado()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 15. Comprobar con Hypothesis que en todo grafo, el número de
# nodos de grado impar es par.
# ---------------------------------------------------------------------

# La propiedad es
@given(gen_grafo())
def test_grado1(g: Grafo) -> None:
    assert len([v for v in nodos(g) if grado(g, v) % 2 == 1]) % 2 == 0

# La comprobación es
#    >>> test_grado1()
#    >>>

# ---------------------------------------------------------------------
#  Ejercicio 16. En la teoría de grafos, se conoce como "Lema del
#  apretón de manos" la siguiente propiedad: la suma de los grados de
#  los vértices de g es el doble del número de aristas de g.
#
# Comprobar con Hypothesis que para cualquier grafo g, se verifica
# dicha propiedad.
# ---------------------------------------------------------------------

# La propiedad es
@given(gen_grafo())
def test_apreton(g: Grafo) -> None:
    assert sum((grado(g, v) for v in nodos(g))) == 2 * nAristas(g)

# La comprobación es
#    >>> test_apreton()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 17. Comprobar con QuickCheck que en todo grafo, el número
# de nodos de grado impar es par.
# ---------------------------------------------------------------------

# La propiedad es
@given(gen_grafo())
def test_numNodosGradoImpar(g: Grafo) -> None:
    vs = nodos(g)
    m = len([v for v in vs if grado(g, v) % 2 == 1])
    assert m % 2 == 0

# La comprobación es
#    >>> test_numNodosGradoImpar()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 18. Definir la propiedad
#   prop_GradoCompleto :: Int -> Bool
# tal que (prop_GradoCompleto n) se verifica si todos los vértices del
# grafo completo K(n) tienen grado n-1. Usarla para comprobar que dicha
# propiedad se verifica para los grafos completos de grados 1 hasta 30.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.integers(min_value=1, max_value=20))
def test_GradoCompleto(n: int) -> None:
    g = completo(n)
    assert all(grado(g, v) == (n - 1) for v in nodos(g))

# La comprobación es
#    >>> test_GradoCompleto()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 19. Un grafo es regular si todos sus vértices tienen el
# mismo grado.
#
# Definir la función,
#    regular : (Grafo) -> bool
# tal que regular(g) se verifica si el grafo g es regular. Por ejemplo,
#    >>> regular(creaGrafo_(Orientacion.D, (1,3), [(1,2),(2,3),(3,1)]))
#    True
#    >>> regular(creaGrafo_(Orientacion.ND, (1,3), [(1,2),(2,3)]))
#    False
#    >>> regular(completo(4))
#    True
# ---------------------------------------------------------------------

def regular(g: Grafo) -> bool:
    vs = nodos(g)
    k = grado(g, vs[0])
    return all(grado(g, v) == k for v in vs)

# Verificación
# ============

def test_regular() -> None:
    g1 = creaGrafo_(Orientacion.D, (1,3), [(1,2),(2,3),(3,1)])
    g2 = creaGrafo_(Orientacion.ND, (1,3), [(1,2),(2,3)])
    assert regular(g1)
    assert not regular(g2)
    assert regular(completo(4))
    print("Verificado")

# La verificación es
#    >>> test_regular()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 20. Comprobar que los grafos completos son regulares.
# ---------------------------------------------------------------------

# La propiedad de la regularidad de todos los grafos completos de orden
# entre m y n es
def prop_CompletoRegular(m: int, n: int) -> bool:
    return all(regular(completo(x)) for x in range(m, n + 1))

# La comprobación es
#    >>> prop_CompletoRegular(1, 30)
#    True

# ---------------------------------------------------------------------
# Ejercicio 21. Un grafo es k-regular si todos sus vértices son de
# grado k.
#
# Definir la función,
#    regularidad : (Grafo) -> Optional[int]
# tal que regularidad(g) es la regularidad de g. Por ejemplo,
#    regularidad(creaGrafo_(Orientacion.ND, (1,2), [(1,2),(2,3)]) == 1
#    regularidad(creaGrafo_(Orientacion.D, (1,2), [(1,2),(2,3)])  == None
#    regularidad(completo(4))                                     == 3
#    regularidad(completo(5))                                     == 4
#    regularidad(grafoCiclo(4))                                   == 2
#    regularidad(grafoCiclo(5))                                   == 2
# ---------------------------------------------------------------------

def regularidad(g: Grafo) -> Optional[int]:
    if regular(g):
        return grado(g, nodos(g)[0])
    return None

# Verificación
# ============

def test_k_regularidad() -> None:
    g1 = creaGrafo_(Orientacion.ND, (1,2), [(1,2),(2,3)])
    g2 = creaGrafo_(Orientacion.D, (1,2), [(1,2),(2,3)])
    assert regularidad(g1) == 1
    assert regularidad(g2) is None
    assert regularidad(completo(4)) == 3
    assert regularidad(completo(5)) == 4
    assert regularidad(grafoCiclo(4)) == 2
    assert regularidad(grafoCiclo(5)) == 2
    print("Verificado")

# La verificación es
#    >>> test_k_regularidad()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 22. Comprobar que el grafo completo de orden n es
# (n-1)-regular (para n de 1 a 20).
# -----------------------------------------------------------

# La propiedad es
def prop_completoRegular(n: int) -> bool:
    return regularidad(completo(n)) == n - 1

# La comprobación es
#    >>> all(prop_completoRegular(n) for n in range(1, 21))
#    True

# ---------------------------------------------------------------------
# Ejercicio 23. Comprobar que el grafo ciclo de orden n es 2-regular
# (para n de 3 a 20).
# -----------------------------------------------------------

# La propiedad es
def prop_cicloRegular(n: int) -> bool:
    return regularidad(grafoCiclo(n)) == 2

# La comprobación es
#    >>> all(prop_cicloRegular(n) for n in range(3, 21))
#    True

# Verificación
# ============

# La comprobación de las propiedades es
#    src> poetry run pytest -v Problemas_basicos_de_grafos.py
#    test_completo PASSED
#    test_grafoCiclo PASSED
#    test_nVertices PASSED
#    test_incidentes PASSED
#    test_contiguos PASSED
#    test_lazos PASSED
#    test_nLazos PASSED
#    test_nAristas PASSED
#    test_GradoPos PASSED
#    test_GradoNeg PASSED
#    test_sumaGrados PASSED
#    test_grado PASSED
#    test_grado1 PASSED
#    test_apreton PASSED
#    test_numNodosGradoImpar PASSED
#    test_GradoCompleto PASSED
#    test_regular PASSED
#    test_k_regularidad PASSED
#    ====== passed in 1.17s ======
