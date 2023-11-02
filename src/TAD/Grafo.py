# Grafo.py
# El tipo abstracto de datos de los grafos.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 15-mayo-2023
# ---------------------------------------------------------------------

# Un grafo es una estructura que consta de un conjunto de vértices y un
# conjunto de aristas que conectan los vértices entre sí. Cada vértice
# representa una entidad o un elemento, y cada arista representa una
# relación o conexión entre dos vértices.
#
# Por ejemplo,
#
#          12
#     1 -------- 2
#     | \78     /|
#     |  \   32/ |
#     |   \   /  |
#   34|     5    |55
#     |   /   \  |
#     |  /44   \ |
#     | /     93\|
#     3 -------- 4
#          61
#
# representa un grafo no dirigido, lo que significa que las aristas no
# tienen una dirección específica. Cada arista tiene un peso asociado,
# que puede representar una medida o una valoración de la relación
# entre los vértices que conecta.
#
# El grafo consta de cinco vértices numerados del 1 al 5. Las aristas
# especificadas en la lista indican las conexiones entre los vértices y
# sus respectivos pesos. Por ejemplo, la arista (1,2,12) indica que
# existe una conexión entre el vértice 1 y el vértice 2 con un peso de
# 12.
#
# En el grafo representado, se pueden observar las conexiones entre los
# vértices de la siguiente manera:
# + El vértice 1 está conectado con el vértice 2 (peso 12), el vértice
#   3 (peso 34) y el vértice 5 (peso 78).
# + El vértice 2 está conectado con el vértice 4 (peso 55) y el vértice
#   5 (peso 32).
# + El vértice 3 está conectado con el vértice 4 (peso 61) y el vértice
#   5 (peso 44).
# + El vértice 4 está conectado con el vértice 5 (peso 93).
#
# Las operaciones del tipo abstracto de datos (TAD) de los grafos son
#    creaGrafo
#    creaGrafo_
#    dirigido
#    adyacentes
#    nodos
#    aristas
#    aristaEn
#    peso
# tales que
#    + creaGrafo(o, cs, as) es un grafo (dirigido o no, según el valor
#       de o), con el par de cotas cs y listas de aristas as (cada
#       arista es un trío formado por los dos vértices y su peso). Ver
#       un ejemplo en el siguiente apartado.
#    + creaGrafo_ es la versión de creaGrafo para los grafos sin pesos.
#    + dirigido(g) se verifica si g es dirigido.
#    + nodos(g) es la lista de todos los nodos del grafo g.
#    + aristas(g) es la lista de las aristas del grafo g.
#    + adyacentes(g, v) es la lista de los vértices adyacentes al nodo
#      v en el grafo g.
#    + aristaEn(g, a) se verifica si a es una arista del grafo g.
#    + peso(v1, v2, g) es el peso de la arista que une los vértices v1 y
#      v2 en el grafo g.
#
# Usando el TAD de los grafos, el grafo anterior se puede definir por
#    creaGrafo ND (1,5) [(1,2,12),(1,3,34),(1,5,78),
#                        (2,4,55),(2,5,32),
#                        (3,4,61),(3,5,44),
#                        (4,5,93)]
# con los siguientes argumentos:
#    + ND: Es un parámetro de tipo Orientacion que indica si el grafo
#      es dirigido o no. En este caso, se utiliza ND, lo que significa
#      "no dirigido". Por lo tanto, el grafo creado será no dirigido,
#      lo que implica que las aristas no tienen una dirección
#      específica.
#    + (1,5): Es el par de cotas que define los vértices del grafo. En
#      este caso, el grafo tiene vértices numerados desde 1 hasta 5.
#    + [(1,2,12),(1,3,34),(1,5,78),(2,4,55),(2,5,32),(3,4,61),(3,5,44),(4,5,93)]:
#      Es una lista de aristas, donde cada arista está representada por
#      un trío de valores. Cada trío contiene los dos vértices que
#      están conectados por la arista y el peso de dicha arista.
#
# Para usar el TAD hay que usar una implementación concreta. En
# principio, consideraremos sólo la siguiente:
#    + mediante lista de adyacencia.

# pylint: disable=unused-import

__all__ = [
    'Orientacion',
    'Grafo',
    'Vertice',
    'Peso',
    'creaGrafo',
    'creaGrafo_',
    'dirigido',
    'adyacentes',
    'nodos',
    'aristas',
    'aristaEn',
    'peso'
    ]

from src.TAD.GrafoConListaDeAdyacencia import (Arista, Cotas, Grafo,
                                               Orientacion, Peso, Vertice,
                                               adyacentes, aristaEn, aristas,
                                               creaGrafo, creaGrafo_, dirigido,
                                               nodos, peso)
