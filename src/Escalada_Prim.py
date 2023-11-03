# Escalada_Prim.py
# El algoritmo de Prim del árbol de expansión mínimo por escalada.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 3-noviembre-2023
# ======================================================================

# ---------------------------------------------------------------------
# Introducción
# ---------------------------------------------------------------------

# El [algoritmo de Prim](https://bit.ly/466fwRe) calcula un árbol
# recubridor mínimo en un grafo conexo y ponderado. Es decir, busca un
# subconjunto de aristas que, formando un árbol, incluyen todos los
# vértices y donde el valor de la suma de todas las aristas del árbol
# es el mínimo.
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
# En esta relación de ejercicios implementaremos el algoritmo de Prim
# mediante búsqueda en escalada usando el tipo abstracto de los grafos.

# ---------------------------------------------------------------------
# Importaciones
# ---------------------------------------------------------------------

from typing import Optional

from src.BusquedaEnEscalada import buscaEscalada
from src.TAD.Grafo import (Grafo, Orientacion, Peso, Vertice, aristaEn,
                           creaGrafo, nodos, peso)

# ---------------------------------------------------------------------
# Nota. En los ejemplos de los ejercicios usaremos los grafos definidos
# a continuación.
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

# ---------------------------------------------------------------------
# Ejercicio 1. Las aristas son pares de la forma ((v1, v2), p) donde v1
# es el vértice origen, v2 es el vértice destino y p es el peso de la
# arista.
#
# Definir el tipo Arista para las aristas.
# ---------------------------------------------------------------------

Arista = tuple[tuple[Vertice, Vertice], Peso]

# ---------------------------------------------------------------------
# Ejercicio 2. Un estado es una tupla de la forma (p,t,r,aem) donde p es
# el peso de la última arista añadida el árbol de expansión mínimo
# (aem), t es la lista de nodos del grafo que están en el aem y r es la
# lista de nodos del grafo que no están en el aem.
#
# Definir el tipo Estado para los estados.
# ---------------------------------------------------------------------

Estado = tuple[Peso, list[Vertice], list[Vertice], list[Arista]]

# ---------------------------------------------------------------------
# Ejercicio 3. Definir la función
#    inicial : (Grafo) -> Estado
# tal que inicial(g) es el estado inicial correspondiente al grafo g.
# ---------------------------------------------------------------------

def inicial(g: Grafo) -> Estado:
    n, *ns = nodos(g)
    return (0, [n], ns, [])

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    esFinal : (Estado) -> bool
# esFinal(e) se verifica si e es un estado final; es decir, si no
# queda ningún elemento en la lista de nodos sin colocar en el árbol de
# expansión mínimo.
# ---------------------------------------------------------------------

def esFinal(e: Estado) -> bool:
    return e[2] == []

# ---------------------------------------------------------------------
# Ejercicio 5. Definir la función
#    sucesores : (Grafo, Estado) -> list[Estado]
# sucesores(g, e) es la lista de los sucesores del estado e en el
# grafo g. Por ejemplo,
#    λ> sucesores(g1, (0,[1],[2,3,4,5],[]))
#    [(12,[2,1],[3,4,5],[(1,2,12)]),
#     (34,[3,1],[2,4,5],[(1,3,34)]),
#     (78,[5,1],[2,3,4],[(1,5,78)])]
# ---------------------------------------------------------------------

def sucesores(g: Grafo, e: Estado) -> list[Estado]:
    (_,t,r,aem) = e
    return [(peso(x, y, g),
             [y] + t,
             [x for x in r if x != y],
             [((x,y),peso(x, y, g))] + aem)
            for x in t for y in r if aristaEn(g, (x, y))]

# ---------------------------------------------------------------------
# Ejercicio 6. Usando la búsqueda en escalada, definir la función
#    prim : (Grafo) -> list[tuple[Peso, Vertice, Vertice]]
# tal que prim(g) es el árbol de expansión mínimo del grafo g
# calculado mediante el algoritmo de Prim con bñusqueda en
# escalada. Por ejemplo, si g1, g2, g3 y g4 son los grafos definidos
# por
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
#    prim(g1) == [((2,4),55),((1,3),34),((2,5),32),((1,2),12)]
#    prim(g2) == [((2,5),32),((2,4),12),((1,2),13),((1,3),11)]
#    prim(g3) == [((5,7),9),((2,3),7),((5,4),5),((6,5),3),((1,6),6),((1,2),5)]
#    prim(g4) == [((5,7),9),((5,4),5),((5,3),1),((6,5),3),((1,6),6),((1,2),5)]
# ---------------------------------------------------------------------

def prim(g: Grafo) -> Optional[list[Arista]]:
    r = buscaEscalada(lambda e: sucesores(g, e), esFinal, inicial(g))
    if r is None:
        return None
    return r[3]

# Verificación
# ============

def test_prim() -> None:
    assert prim(g1) == [((2,4),55),((1,3),34),((2,5),32),((1,2),12)]
    assert prim(g2) == [((2,5),32),((2,4),12),((1,2),13),((1,3),11)]
    assert prim(g3) == [((5,7),9),((2,3),7),((5,4),5),((6,5),3),((1,6),6),((1,2),5)]
    assert prim(g4) == [((5,7),9),((5,4),5),((5,3),1),((6,5),3),((1,6),6),((1,2),5)]
    print("Verificado")

# La verificación es
#    >>> test_prim()
#    Verificado
