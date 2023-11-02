# GrafoConListaDeAdyacencia.py
# Implementación del TAD de los grafos mediante listas.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 16-mayo-2023
# ======================================================================

# Se define la clase Grafo con los siguientes métodos:
#    + dirigido() se verifica si el grafo es dirigido.
#    + nodos() es la lista de todos los nodos del grafo.
#    + aristas() es la lista de las aristas del grafo.
#    + adyacentes(v) es la lista de los vértices adyacentes al vértice
#      v en el grafo.
#    + aristaEn(a) se verifica si a es una arista del grafo.
#    + peso(v1, v2) es el peso de la arista que une los vértices v1 y
#      v2 en el grafo.
# Por ejemplo,
#    >>> Grafo(Orientacion.D, (1,3), [((1,2),0),((3,2),0),((2,2),0)])
#    G D ([1, 2, 3], [(1, 2), (2, 2), (3, 2)])
#    >>> Grafo(Orientacion.ND, (1,3), [((1,2),0),((3,2),0),((2,2),0)])
#    G ND ([1, 2, 3], [(1, 2), (2, 2), (2, 3)])
#    >>> Grafo(Orientacion.ND, (1,3), [((1,2),0),((3,2),5),((2,2),0)])
#    G ND ([1, 2, 3], [((1, 2), 0), ((2, 2), 0), ((2, 3), 5)])
#    >>> Grafo(Orientacion.D, (1,3), [((1,2),0),((3,2),5),((2,2),0)])
#    G D ([1, 2, 3], [((1, 2), 0), ((2, 2), 0), ((3, 2), 5)])
#    >>> ejGrafoND: Grafo = Grafo(Orientacion.ND,
#                                 (1, 5),
#                                 [((1, 2), 12), ((1, 3), 34), ((1, 5), 78),
#                                  ((2, 4), 55), ((2, 5), 32),
#                                  ((3, 4), 61), ((3, 5), 44),
#                                  ((4, 5), 93)])
#    >>> ejGrafoND
#    G ND ([1, 2, 3, 4, 5],
#          [((1, 2), 12), ((1, 3), 34), ((1, 5), 78),
#           ((2, 4), 55), ((2, 5), 32),
#           ((3, 4), 61), ((3, 5), 44),
#           ((4, 5), 93)])
#    >> ejGrafoD: Grafo = Grafo(Orientacion.D,
#                               (1,5),
#                               [((1, 2), 12), ((1, 3), 34), ((1, 5), 78),
#                                ((2, 4), 55), ((2, 5), 32),
#                                ((3, 4), 61), ((3, 5), 44),
#                                ((4, 5), 93)])
#    >>> ejGrafoD
#    G D ([1, 2, 3, 4, 5],
#         [((1, 2), 12), ((1, 3), 34), ((1, 5), 78),
#          ((2, 4), 55), ((2, 5), 32),
#          ((3, 4), 61), ((3, 5), 44),
#          ((4, 5), 93)])
#    >>> ejGrafoD.dirigido()
#    True
#    >>> ejGrafoND.dirigido()
#    False
#    >>> ejGrafoND.nodos()
#    [1, 2, 3, 4, 5]
#    >>> ejGrafoD.nodos()
#    [1, 2, 3, 4, 5]
#    >>> ejGrafoND.adyacentes(4)
#    [2, 3, 5]
#    >>> ejGrafoD.adyacentes(4)
#    [5]
#    >>> ejGrafoND.aristaEn((5, 1))
#    True
#    >>> ejGrafoND.aristaEn((4, 1))
#    False
#    >>> ejGrafoD.aristaEn((5, 1))
#    False
#    >>> ejGrafoD.aristaEn((1, 5))
#    True
#    >>> ejGrafoND.peso(1, 5)
#    78
#    >>> ejGrafoD.peso(1, 5)
#    78
#    >>> ejGrafoD._aristas
#    [((1, 2), 12), ((1, 3), 34), ((1, 5), 78),
#     ((2, 4), 55), ((2, 5), 32),
#     ((3, 4), 61), ((3, 5), 44),
#     ((4, 5), 93)]
#    >>> ejGrafoND._aristas
#    [((1, 2), 12), ((1, 3), 34), ((1, 5), 78),
#     ((2, 1), 12), ((2, 4), 55), ((2, 5), 32),
#     ((3, 1), 34), ((3, 4), 61), ((3, 5), 44),
#     ((4, 2), 55), ((4, 3), 61), ((4, 5), 93),
#     ((5, 1), 78), ((5, 2), 32), ((5, 3), 44),
#     ((5, 4), 93)]
#
# Además se definen las correspondientes funciones. Por ejemplo,
#    >>> creaGrafo(Orientacion.ND, (1,3), [((1,2),12),((1,3),34)])
#    G ND ([1, 2, 3], [((1, 2), 12), ((1, 3), 34), ((2, 1), 12), ((3, 1), 34)])
#    >>> creaGrafo(Orientacion.D, (1,3), [((1,2),12),((1,3),34)])
#    G D ([1, 2, 3], [((1, 2), 12), ((1, 3), 34)])
#    >>> creaGrafo(Orientacion.D, (1,4), [((1,2),12),((1,3),34)])
#    G D ([1, 2, 3, 4], [((1, 2), 12), ((1, 3), 34)])
#    >>> ejGrafoND2: Grafo = creaGrafo(Orientacion.ND,
#                                      (1,5),
#                                      [((1,2),12),((1,3),34),((1,5),78),
#                                       ((2,4),55),((2,5),32),
#                                       ((3,4),61),((3,5),44),
#                                       ((4,5),93)])
#    >>> ejGrafoND2
#    G ND ([1, 2, 3, 4, 5],
#          [((1, 2), 12), ((1, 3), 34), ((1, 5), 78),
#           ((2, 4), 55), ((2, 5), 32),
#           ((3, 4), 61), ((3, 5), 44),
#           ((4, 5), 93)])
#    >>> ejGrafoD2: Grafo = creaGrafo(Orientacion.D,
#                                     (1,5),
#                                     [((1,2),12),((1,3),34),((1,5),78),
#                                      ((2,4),55),((2,5),32),
#                                      ((3,4),61),((3,5),44),
#                                      ((4,5),93)])
#    >>> ejGrafoD2
#    G D ([1, 2, 3, 4, 5],
#         [((1, 2), 12), ((1, 3), 34), ((1, 5), 78),
#          ((2, 4), 55), ((2, 5), 32),
#          ((3, 4), 61), ((3, 5), 44),
#          ((4, 5), 93)])
#    >>> creaGrafo_(Orientacion.D, (1,3), [(2, 1), (1, 3)])
#    G D ([1, 2, 3], [(1, 3), (2, 1)])
#    >>> creaGrafo_(Orientacion.ND, (1,3), [(2, 1), (1, 3)])
#    G ND ([1, 2, 3], [(1, 2), (1, 3)])
#    >>> dirigido(ejGrafoD2)
#    True
#    >>> dirigido(ejGrafoND2)
#    False
#    >>> nodos(ejGrafoND2)
#    [1, 2, 3, 4, 5]
#    >>> nodos(ejGrafoD2)
#    [1, 2, 3, 4, 5]
#    >>> adyacentes(ejGrafoND2, 4)
#    [2, 3, 5]
#    >>> adyacentes(ejGrafoD2, 4)
#    [5]
#    >>> aristaEn(ejGrafoND2, (5,1))
#    True
#    >>> aristaEn(ejGrafoND2, (4,1))
#    False
#    >>> aristaEn(ejGrafoD2, (5,1))
#    False
#    >>> aristaEn(ejGrafoD2, (1,5))
#    True
#    >>> peso(1, 5, ejGrafoND2)
#    78
#    >>> peso(1, 5, ejGrafoD2)
#    78
#    >>> aristas(ejGrafoD2)
#    [((1, 2), 12), ((1, 3), 34), ((1, 5), 78),
#     ((2, 4), 55), ((2, 5), 32),
#     ((3, 4), 61), ((3, 5), 44),
#     ((4, 5), 93)]
#    >>> aristas(ejGrafoND2)
#    [((1, 2), 12), ((1, 3), 34), ((1, 5), 78),
#     ((2, 1), 12), ((2, 4), 55), ((2, 5), 32),
#     ((3, 1), 34), ((3, 4), 61), ((3, 5), 44),
#     ((4, 2), 55), ((4, 3), 61), ((4, 5), 93),
#     ((5, 1), 78), ((5, 2), 32), ((5, 3), 44), ((5, 4), 93)]

# pylint: disable=protected-access

from enum import Enum

Orientacion = Enum('Orientacion', ['D', 'ND'])

Vertice = int
Cotas = tuple[Vertice, Vertice]
Peso = float
Arista = tuple[tuple[Vertice, Vertice], Peso]

class Grafo:
    def __init__(self,
                 _orientacion: Orientacion,
                 _cotas: Cotas,
                 _aristas: list[Arista]):
        self._orientacion = _orientacion
        self._cotas = _cotas
        if _orientacion == Orientacion.ND:
            simetricas = [((v2, v1), p) for ((v1, v2), p)
                          in _aristas
                          if v1 != v2]
            self._aristas = sorted(_aristas + simetricas)
        else:
            self._aristas = sorted(_aristas)

    def nodos(self) -> list[Vertice]:
        (x, y) = self._cotas
        return list(range(x, 1 + y))

    def __repr__(self) -> str:
        o = self._orientacion
        vs = nodos(self)
        ns = self._aristas
        escribeOrientacion = "D" if o == Orientacion.D else "ND"
        ponderado = {p for ((_, _), p) in ns} != {0}
        aristasReducidas = ns if o == Orientacion.D \
            else [((x, y), p)
                  for ((x, y), p) in ns
                  if x <= y]
        escribeAristas = str(aristasReducidas) if ponderado \
            else str([a for (a, _) in aristasReducidas])
        return f"G {escribeOrientacion} ({vs}, {escribeAristas})"

    def dirigido(self) -> bool:
        return self._orientacion == Orientacion.D

    def adyacentes(self, v: int) -> list[int]:
        return list(set(u for ((w, u), _)
                        in self._aristas
                        if w == v))

    def aristaEn(self, a: tuple[Vertice, Vertice]) -> bool:
        (x, y) = a
        return y in self.adyacentes(x)

    def peso(self, v1: Vertice, v2: Vertice) -> Peso:
        return [p for ((x1, x2), p)
                in self._aristas
                if (x1, x2) == (v1, v2)][0]

def creaGrafo(o: Orientacion,
              cs: Cotas,
              as_: list[Arista]) -> Grafo:
    return Grafo(o, cs, as_)

def creaGrafo_(o: Orientacion,
              cs: Cotas,
              as_: list[tuple[Vertice, Vertice]]) -> Grafo:
    return Grafo(o, cs, [((v1, v2), 0) for (v1, v2) in as_])

def dirigido(g: Grafo) -> bool:
    return g.dirigido()

def nodos(g: Grafo) -> list[Vertice]:
    return g.nodos()

def adyacentes(g: Grafo, v: Vertice) -> list[Vertice]:
    return g.adyacentes(v)

def aristaEn(g: Grafo, a: tuple[Vertice, Vertice]) -> bool:
    return g.aristaEn(a)

def peso(v1: Vertice, v2: Vertice, g: Grafo) -> Peso:
    return g.peso(v1, v2)

def aristas(g: Grafo) -> list[Arista]:
    return g._aristas

# En los ejemplos se usarán los grafos (no dirigido y dirigido)
# correspondientes a
#             12
#        1 -------- 2
#        | \78     /|
#        |  \   32/ |
#        |   \   /  |
#      34|     5    |55
#        |   /   \  |
#        |  /44   \ |
#        | /     93\|
#        3 -------- 4
#             61
# definidos por
ejGrafoND: Grafo = Grafo(Orientacion.ND,
                         (1, 5),
                         [((1, 2), 12), ((1, 3), 34), ((1, 5), 78),
                          ((2, 4), 55), ((2, 5), 32),
                          ((3, 4), 61), ((3, 5), 44),
                          ((4, 5), 93)])
ejGrafoD: Grafo = Grafo(Orientacion.D,
                        (1,5),
                        [((1, 2), 12), ((1, 3), 34), ((1, 5), 78),
                         ((2, 4), 55), ((2, 5), 32),
                         ((3, 4), 61), ((3, 5), 44),
                         ((4, 5), 93)])

ejGrafoND2: Grafo = creaGrafo(Orientacion.ND,
                              (1,5),
                              [((1,2),12),((1,3),34),((1,5),78),
                               ((2,4),55),((2,5),32),
                               ((3,4),61),((3,5),44),
                               ((4,5),93)])

ejGrafoD2: Grafo = creaGrafo(Orientacion.D,
                             (1,5),
                             [((1,2),12),((1,3),34),((1,5),78),
                              ((2,4),55),((2,5),32),
                              ((3,4),61),((3,5),44),
                              ((4,5),93)])
