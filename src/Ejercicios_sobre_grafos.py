# Ejercicios_sobre_grafos.py
# Ejercicios sobre grafos.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 1-noviembre-2023
# ======================================================================

# ----------------------------------------------------------------------
# Introducción                                                        --
# ----------------------------------------------------------------------

# En esta relación se presenta una recopilación de ejercicios sobre
# grafos propuestos en exámenes.

# ----------------------------------------------------------------------
# Librerías auxiliares                                                --
# ----------------------------------------------------------------------

from enum import Enum
from itertools import permutations
from typing import TypeVar

from src.Algoritmos_sobre_grafos import recorridoEnAnchura
from src.Problemas_basicos_de_grafos import grafoCiclo, incidentes
from src.TAD.Grafo import (Grafo, Orientacion, Vertice, adyacentes, aristas,
                           creaGrafo_, nodos)

A = TypeVar('A')

# ---------------------------------------------------------------------
# Ejercicio 1. Definir la función
#    recorridos : (list[A]) -> list[list[A]]
# tal que recorridos(xs) es la lista de todos los posibles recorridos
# por el grafo cuyo conjunto de vértices es xs y cada vértice se
# encuentra conectado con todos los otros y los recorridos pasan por
# todos los vértices una vez y terminan en el vértice inicial. Por
# ejemplo,
#    >>> recorridos([2, 5, 3])
#    [[2, 5, 3, 2], [2, 3, 5, 2], [5, 2, 3, 5], [5, 3, 2, 5],
#     [3, 2, 5, 3], [3, 5, 2, 3]]
# ---------------------------------------------------------------------

def recorridos(xs: list[A]) -> list[list[A]]:
    return [(list(y) + [y[0]]) for y in permutations(xs)]

# Verificación
# ============

def test_recorridos() -> None:
    assert recorridos([2, 5, 3]) \
        == [[2, 5, 3, 2], [2, 3, 5, 2], [5, 2, 3, 5], [5, 3, 2, 5],
            [3, 2, 5, 3], [3, 5, 2, 3]]
    print("Verificado")

# La verificación es
#    >>> test_recorridos()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 2.1. En un grafo, la anchura de un nodo es el máximo de los
# valores absolutos de la diferencia entre el valor del nodo y los de
# sus adyacentes; y la anchura del grafo es la máxima anchura de sus
# nodos. Por ejemplo, en el grafo
#    grafo1: Grafo = creaGrafo_(Orientacion.D, (1,5), [(1,2),(1,3),(1,5),
#                                                      (2,4),(2,5),
#                                                      (3,4),(3,5),
#                                                      (4,5)])
# su anchura es 4 y el nodo de máxima anchura es el 5.
#
# Definir la función,
#    anchura : (Grafo) -> int
# tal que anchuraG(g) es la anchura del grafo g. Por ejemplo,
#    anchura(grafo1)  ==  4
# ---------------------------------------------------------------------

grafo1: Grafo = creaGrafo_(Orientacion.D, (1,5), [(1,2),(1,3),(1,5),
                                                  (2,4),(2,5),
                                                  (3,4),(3,5),
                                                  (4,5)])

# 1ª solución
# ===========

def anchura(g: Grafo) -> int:
    return max(anchuraN(g, x) for x in nodos(g))

# (anchuraN g x) es la anchura del nodo x en el grafo g. Por ejemplo,
#    anchuraN g 1  ==  4
#    anchuraN g 2  ==  3
#    anchuraN g 4  ==  2
#    anchuraN g 5  ==  4
def anchuraN(g: Grafo, x: Vertice) -> int:
    return max([0] + [abs (x - v) for v in adyacentes(g, x)])

# 2ª solución
# ===========

def anchura2(g: Grafo) -> int:
    return max(abs (x-y) for ((x,y),_) in aristas(g))

# Verificación
# ============

def test_anchura() -> None:
    g2 = creaGrafo_(Orientacion.ND, (1,3), [(1,2),(1,3),(2,3),(3,3)])
    assert anchura(grafo1) == 4
    assert anchura(g2) == 2
    print("Verificado")

# La verificación es
#    >>> test_anchura()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 2.2. Comprobar experimentalmente que la anchura del grafo
# ciclo de orden n es n-1.
# ---------------------------------------------------------------------

# La conjetura
def conjetura(n: int) -> bool:
    return anchura(grafoCiclo(n)) == n - 1

# La comprobación es
#    >>> all(conjetura(n) for n in range(2, 11))
#    True

# ---------------------------------------------------------------------
# Ejercicio 3. Un grafo no dirigido G se dice conexo, si para cualquier
# par de vértices u y v en G, existe al menos una trayectoria (una
# sucesión de vértices adyacentes) de u a v.
#
# Definir la función,
#    conexo :: (Grafo) -> bool
# tal que (conexo g) se verifica si el grafo g es conexo. Por ejemplo,
#    conexo (creaGrafo_(Orientacion.ND, (1,3), [(1,2),(3,2)]))       == True
#    conexo (creaGrafo_(Orientacion.ND, (1,4), [(1,2),(3,2),(4,1)])) == True
#    conexo (creaGrafo_(Orientacion.ND, (1,4), [(1,2),(3,4)]))       == False
# ---------------------------------------------------------------------

def conexo(g: Grafo) -> bool:
    xs = nodos(g)
    i = xs[0]
    n = len(xs)
    return len(recorridoEnAnchura(i, g)) == n

# Verificación
# ============

def test_conexo() -> None:
    g1 = creaGrafo_(Orientacion.ND, (1,3), [(1,2),(3,2)])
    g2 = creaGrafo_(Orientacion.ND, (1,4), [(1,2),(3,2),(4,1)])
    g3 = creaGrafo_(Orientacion.ND, (1,4), [(1,2),(3,4)])
    assert conexo(g1)
    assert conexo(g2)
    assert not conexo(g3)
    print("Verificado")

# La verificación es
#    >>> test_conexo()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 4. Un mapa se puede representar mediante un grafo donde los
# vértices son las regiones del mapa y hay una arista entre dos
# vértices si las correspondientes regiones son vecinas. Por ejemplo,
# el mapa siguiente
#    +----------+----------+
#    |    1     |     2    |
#    +----+-----+-----+----+
#    |    |           |    |
#    | 3  |     4     | 5  |
#    |    |           |    |
#    +----+-----+-----+----+
#    |    6     |     7    |
#    +----------+----------+
# se pueden representar por
#    mapa: Grafo = creaGrafo_(Orientacion.ND,
#                             (1,7),
#                             [(1,2),(1,3),(1,4),(2,4),(2,5),(3,4),
#                              (3,6),(4,5),(4,6),(4,7),(5,7),(6,7)])
#
# Para colorear el mapa se dispone de 4 colores definidos por
#    Color = Enum('Color', ['A', 'B', 'C', 'E'])
#
# Usando el [tipo abstracto de datos de los grafos](https://bit.ly/45cQ3Fo),
# definir la función,
#    correcta : (list[tuple[int, Color]], Grafo) -> bool
# tal que (correcta ncs m) se verifica si ncs es una coloración del
# mapa m tal que todos las regiones vecinas tienen colores distintos.
# Por ejemplo,
#    correcta [(1,A),(2,B),(3,B),(4,C),(5,A),(6,A),(7,B)] mapa == True
#    correcta [(1,A),(2,B),(3,A),(4,C),(5,A),(6,A),(7,B)] mapa == False
# ---------------------------------------------------------------------

mapa: Grafo = creaGrafo_(Orientacion.ND,
                         (1,7),
                         [(1,2),(1,3),(1,4),(2,4),(2,5),(3,4),
                          (3,6),(4,5),(4,6),(4,7),(5,7),(6,7)])

Color = Enum('Color', ['A', 'B', 'C', 'E'])

def correcta(ncs: list[tuple[int, Color]], g: Grafo) -> bool:
    def color(x: int) -> Color:
        return [c for (y, c) in ncs if y == x][0]
    return all(color(x) != color(y) for ((x, y), _) in aristas(g))

# Verificación
# ============

def test_correcta() -> None:
    assert correcta([(1,Color.A),
                     (2,Color.B),
                     (3,Color.B),
                     (4,Color.C),
                     (5,Color.A),
                     (6,Color.A),
                     (7,Color.B)],
                    mapa)
    assert not correcta([(1,Color.A),
                         (2,Color.B),
                         (3,Color.A),
                         (4,Color.C),
                         (5,Color.A),
                         (6,Color.A),
                         (7,Color.B)],
                        mapa)
    print("Verificado")

# La verificación es
#    >>> test_correcta()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 5. Dado un grafo dirigido G, diremos que un nodo está
# aislado si o bien de dicho nodo no sale ninguna arista o bien no
# llega al nodo ninguna arista. Por ejemplo, en el siguiente grafo
#    grafo7: Grafo = creaGrafo_(Orientacion.D,
#                               (1,6),
#                               [(1,2),(1,3),(1,4),(3,6),(5,4),(6,2),(6,5)])
# podemos ver que del nodo 1 salen 3 aristas pero no llega ninguna, por
# lo que lo consideramos aislado. Así mismo, a los nodos 2 y 4 llegan
# aristas pero no sale ninguna, por tanto también estarán aislados.
#
# Definir la función,
#    aislados :: (Ix v, Num p) => Grafo v p -> [v]
# tal que (aislados g) es la lista de nodos aislados del grafo g. Por
# ejemplo,
#    aislados grafo7 == [1,2,4]
# ---------------------------------------------------------------------

grafo7: Grafo = creaGrafo_(Orientacion.D,
                           (1,6),
                           [(1,2),(1,3),(1,4),(3,6),(5,4),(6,2),(6,5)])

def aislados(g: Grafo) -> list[Vertice]:
    return [n for n in nodos(g)
            if not adyacentes(g, n) or not incidentes(g, n)]

# Verificación
# ============

def test_aislados() -> None:
    assert aislados(grafo7) == [1, 2, 4]
    print("Verificado")

# La verificación es
#    >>> test_aislados()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 6. Definir la función,
#    conectados : (Grafo, Vertice, Vertice) -> bool
# tal que conectados(g, v1, v2) se verifica si los vértices v1 y v2
# están conectados en el grafo g. Por ejemplo, si grafo1 es el grafo
# definido por
#    grafo8 = creaGrafo_(Orientacion.D,
#                        (1,6),
#                        [(1,3),(1,5),(3,5),(5,1),(5,50),
#                         (2,4),(2,6),(4,6),(4,4),(6,4)])
# entonces,
#    conectados grafo8 1 3  ==  True
#    conectados grafo8 1 4  ==  False
#    conectados grafo8 6 2  ==  False
#    conectados grafo8 3 1  ==  True
# ----------------------------------------------------------------------------

def unionV(xs: list[Vertice], ys: list[Vertice]) -> list[Vertice]:
    return list(set(xs) | set(ys))

def conectadosAux(g: Grafo, vs: list[Vertice], ws: list[Vertice]) -> list[Vertice]:
    if not ws:
        return vs
    w, *ws = ws
    if w in vs:
        return conectadosAux(g, vs, ws)
    return conectadosAux(g, unionV([w], vs), unionV(ws, adyacentes(g, w)))

def conectados(g: Grafo, v1: Vertice, v2: Vertice) -> bool:
    return v2 in conectadosAux(g, [], [v1])


# Verificación
# ============

def test_conectados() -> None:
    grafo8 = creaGrafo_(Orientacion.D,
                        (1,6),
                        [(1,3),(1,5),(3,5),(5,1),(5,50),
                         (2,4),(2,6),(4,6),(4,4),(6,4)])
    grafo8b = creaGrafo_(Orientacion.ND,
                        (1,6),
                        [(1,3),(1,5),(3,5),(5,1),(5,50),
                         (2,4),(2,6),(4,6),(4,4),(6,4)])
    assert conectados(grafo8, 1, 3)
    assert not conectados(grafo8, 1, 4)
    assert not conectados(grafo8, 6, 2)
    assert conectados(grafo8, 3, 1)
    assert conectados(grafo8b, 1, 3)
    assert not conectados(grafo8b, 1, 4)
    assert conectados(grafo8b, 6, 2)
    assert conectados(grafo8b, 3, 1)
    print("Verificado")

# La verificación es
#    >>> test_conectados()
#    Verificado

# Verificación
# ============

# La verificación es
#    src> poetry run pytest -v Ejercicios_sobre_grafos.py
#    test_recorridos PASSED
#    test_anchura PASSED
#    test_conexo PASSED
#    test_correcta PASSED
#    test_aislados PASSED
#    test_conectados PASSED
#    ====== 6 passed in 0.14s ======
