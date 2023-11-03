# BPM_8Puzzle.py
# El problema del 8 puzzle.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 3-noviembre-2023
# ======================================================================

# ---------------------------------------------------------------------
# Introducción
# ---------------------------------------------------------------------

# Para el 8-puzzle se usa un cajón cuadrado en el que hay situados 8
# bloques cuadrados. El cuadrado restante está sin rellenar. Cada
# bloque tiene un número. Un bloque adyacente al hueco puede deslizarse
# hacia él. El juego consiste en transformar la posición inicial en la
# posición final mediante el deslizamiento de los bloques. En
# particular, consideramos el estado inicial y final siguientes:
#
#    +---+---+---+                   +---+---+---+
#    |   | 1 | 3 |                   | 1 | 2 | 3 |
#    +---+---+---+                   +---+---+---+
#    | 8 | 2 | 4 |                   | 8 |   | 4 |
#    +---+---+---+                   +---+---+---+
#    | 7 | 5 | 5 |                   | 7 | 6 | 5 |
#    +---+---+---+                   +---+---+---+
#    Estado inicial                  Estado final
#
# En esta relación de ejercicios resolveremos el problema del 8-puzzle
# mediante búsqueda por primero el mejor.

# ---------------------------------------------------------------------
# Importaciones
# ---------------------------------------------------------------------

from copy import deepcopy
from typing import Optional

from src.BusquedaPrimeroElMejor import buscaPM

# ---------------------------------------------------------------------
# Ejercicio 1. Para solucionar el problema se usará el tipo Tablero que
# son listas de listas de números enteros (que representan las piezas en
# cada posición y el 0 representa el hueco).
#
# Definir el tipo Tablero.
# ---------------------------------------------------------------------

Tablero = list[list[int]]

# ---------------------------------------------------------------------
# Ejercicio 2. Definir la constante tableroFinalpara representar el
# tablero final del 8 puzzle.
# ---------------------------------------------------------------------

tableroFinal: Tablero = [[1,2,3],
                         [8,0,4],
                         [7,6,5]]

# ---------------------------------------------------------------------
# Ejercicio 3. Una posición es un par de enteros.
#
# Definir el tipo Posicion para representar posiciones.
# ---------------------------------------------------------------------

Posicion = tuple[int,int]

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    distancia : (Posicion, Posicion) -> int
# tal que distancia(p1, p2) es la distancia Manhatan entre las posiciones p1 y
# p2. Por ejemplo,
#    >>> distancia((2,7), (4,1))
#    8
# ---------------------------------------------------------------------

def distancia(p1: Posicion, p2: Posicion) -> int:
    (x1, y1) = p1
    (x2, y2) = p2
    return abs(x1-x2) + abs (y1-y2)

# ---------------------------------------------------------------------
# Ejercicio 5. Definir la función
#    posicionElemento : (Tablero, int) -> Posicion
# tal que posicionElemento(t, a) es la posición de elemento a en el tablero
# t. Por ejemplo,
#    λ> posicionElemento([[2,1,3],[8,0,4],[7,6,5]], 4)
#    (1, 2)
# ---------------------------------------------------------------------

def posicionElemento(t: Tablero, a: int) -> Posicion:
    for i in range(0, 3):
        for j in range(0, 3):
            if t[i][j] == a:
                return (i, j)
    return (4, 4)

# ---------------------------------------------------------------------
# Ejercicio 6. Definir la función
#    posicionHueco : (Tablero) -> Posicion
# posicionHueco(t) es la posición del hueco en el tablero t. Por
# ejemplo,
#    >>> posicionHueco([[2,1,3],[8,0,4],[7,6,5]])
#    (1, 1)
# ---------------------------------------------------------------------

def posicionHueco(t: Tablero) -> Posicion:
    return posicionElemento(t, 0)

# ---------------------------------------------------------------------
# Ejercicio 7. Definir la función
#    heuristica : (Tablero) -> int
# tal que heuristica(t) es la suma de la distancia Manhatan desde la
# posición de cada objeto del tablero a su posición en el tablero
# final. Por ejemplo,
#    >>> heuristica([[0,1,3],[8,2,4],[7,6,5]])
#    4
# ---------------------------------------------------------------------

def heuristica(t: Tablero) -> int:
    return sum((distancia(posicionElemento(t, i),
                          posicionElemento(tableroFinal, i))
                for i in range(0, 10)))

# ---------------------------------------------------------------------
# Ejercicio 8. Un estado es una tupla (h, n, ts), donde ts es una listas
# de tableros [t_n,...,t_1] tal que t_i es un sucesor de t_(i-1) y h es
# la heurística de t_n.
#
# Definir el tipo Estado para representar los estados.
# ---------------------------------------------------------------------

Estado = tuple[int, int, list[Tablero]]

# ---------------------------------------------------------------------
# Ejercicio 9. Definir la función
#    inicial (Tablero) -> Estado
# tal que inicial(t) es el estado inicial del problema del 8 puzzle a
# partir del tablero t.
# ---------------------------------------------------------------------

def inicial(t: Tablero) -> Estado:
    return (heuristica(t), 1, [t])

# ---------------------------------------------------------------------
# Ejercicio 10. Definir la función
#    esFinal : (Estado) -> bool
# tal que esFinal(e) se verifica si e es un estado final.
# ---------------------------------------------------------------------

def esFinal(e: Estado) -> bool:
    (_, _, ts) = e
    return ts[0] == tableroFinal

# ---------------------------------------------------------------------
# Ejercicio 11. Definir la función
#    posicionesVecinas : (Posicion) -> list[Posicion]
# tal que posicionesVecinas(p) son las posiciones de la matriz cuadrada
# de dimensión 3 que se encuentran encima, abajo, a la izquierda y a la
# derecha de los posición p. Por ejemplo,
#    >>> posicionesVecinas((1,1))
#    [(0, 1), (2, 1), (1, 0), (1, 2)]
#    >>> posicionesVecinas((0,1))
#    [(1, 1), (0, 0), (0, 2)]
#    >>> posicionesVecinas((0,0))
#    [(1, 0), (0, 1)]
# ---------------------------------------------------------------------

def posicionesVecinas(p: Posicion) -> list[Posicion]:
    (i, j) = p
    vecinas = []
    if i > 0:
        vecinas.append((i - 1, j))
    if i < 2:
        vecinas.append((i + 1, j))
    if j > 0:
        vecinas.append((i, j - 1))
    if j < 2:
        vecinas.append((i, j + 1))
    return vecinas

# ---------------------------------------------------------------------
# Ejercicio 12. Definir la función
#    intercambia : (Tablero, Posicion, Posicion) -> Tablero
# tal que intercambia(t,p1, p2) es el tablero obtenido intercambiando en
# t los elementos que se encuentran en las posiciones p1 y p2. Por
# ejemplo,
#    >>> intercambia([[2,1,3],[8,0,4],[7,6,5]], (0,1), (1,1))
#    [[2, 0, 3], [8, 1, 4], [7, 6, 5]]
# ---------------------------------------------------------------------

def intercambia(t: Tablero, p1: Posicion, p2: Posicion) -> Tablero:
    (i1, j1) = p1
    (i2, j2) = p2
    t1 = deepcopy(t)
    a1 = t1[i1][j1]
    a2 = t1[i2][j2]
    t1[i1][j1] = a2
    t1[i2][j2] = a1
    return t1

# ---------------------------------------------------------------------
# Ejercicio 13. Definir la función
#    tablerosSucesores : (Tablero) -> list[Tablero]
# tal que tablerosSucesores(t) es la lista de los tablrtos sucesores del
# tablero t. Por ejemplo,
#    >>> tablerosSucesores([[2,1,3],[8,0,4],[7,6,5]])
#    [[[2, 0, 3], [8, 1, 4], [7, 6, 5]],
#     [[2, 1, 3], [8, 6, 4], [7, 0, 5]],
#     [[2, 1, 3], [0, 8, 4], [7, 6, 5]],
#     [[2, 1, 3], [8, 4, 0], [7, 6, 5]]]
# ---------------------------------------------------------------------

def tablerosSucesores(t: Tablero) -> list[Tablero]:
    p = posicionHueco(t)
    return [intercambia(t, p, q) for q in posicionesVecinas(p)]

# ---------------------------------------------------------------------
# Ejercicio 14. Definir la función
#    sucesores : (Estado) -> list[Estado]
# tal que (sucesores e) es la lista de sucesores del estado e. Por
# ejemplo,
#    >>> t1 = [[0,1,3],[8,2,4],[7,6,5]]
#    >>> es = sucesores((heuristica(t1), 1, [t1]))
#    >>> es
#    [(4, 2, [[[8, 1, 3],
#              [0, 2, 4],
#              [7, 6, 5]],
#             [[0, 1, 3],
#              [8, 2, 4],
#              [7, 6, 5]]]),
#     (2, 2, [[[1, 0, 3],
#              [8, 2, 4],
#              [7, 6, 5]],
#             [[0, 1, 3],
#              [8, 2, 4],
#              [7, 6, 5]]])]
#    >>> sucesores(es[1])
#    [(0, 3, [[[1, 2, 3],
#              [8, 0, 4],
#              [7, 6, 5]],
#             [[1, 0, 3],
#              [8, 2, 4],
#              [7, 6, 5]],
#             [[0, 1, 3],
#              [8, 2, 4],
#              [7, 6, 5]]]),
#     (4, 3, [[[1, 3, 0],
#              [8, 2, 4],
#              [7, 6, 5]],
#             [[1, 0, 3],
#              [8, 2, 4],
#              [7, 6, 5]],
#             [[0, 1, 3],
#              [8, 2, 4],
#              [7, 6, 5]]])]
# ---------------------------------------------------------------------

def sucesores(e: Estado) -> list[Estado]:
    (_, n, ts) = e
    return [(heuristica(t1), n+1, [t1] + ts)
            for t1 in tablerosSucesores(ts[0])
            if t1 not in ts]

# ---------------------------------------------------------------------
# Ejercicio 15. Usando el procedimiento de búsqueda por primero el
# mejor, definir la función
#    solucion_8puzzle : (Tablero) -> Tablero
# tal que solucion_8puzzle(t) es la solución del problema del problema
# del 8 puzzle a partir del tablero t. Por ejemplo,
#    >>> solucion_8puzzle([[0,1,3],[8,2,4],[7,6,5]])
#    [[[0, 1, 3],
#      [8, 2, 4],
#      [7, 6, 5]],
#     [[1, 0, 3],
#      [8, 2, 4],
#      [7, 6, 5]],
#     [[1, 2, 3],
#      [8, 0, 4],
#      [7, 6, 5]]]
#    >>> solucion_8puzzle([[8,1,3],[0,2,4],[7,6,5]])
#    [[[8, 1, 3],
#      [0, 2, 4],
#      [7, 6, 5]],
#     [[0, 1, 3],
#      [8, 2, 4],
#      [7, 6, 5]],
#     [[1, 0, 3],
#      [8, 2, 4],
#      [7, 6, 5]],
#     [[1, 2, 3],
#      [8, 0, 4],
#      [7, 6, 5]]]
#    >>> len(solucion_8puzzle([[2,6,3],[5,0,4],[1,7,8]]))
#    21
# ---------------------------------------------------------------------

def solucion_8puzzle(t: Tablero) -> Optional[list[Tablero]]:
    r = buscaPM(sucesores, esFinal, inicial(t))
    if r is None:
        return None
    (_, _, ts) = r
    ts.reverse()
    return ts

# Verificación
# ============

def test_8puzzle() -> None:
    assert solucion_8puzzle([[8,1,3],[0,2,4],[7,6,5]]) == \
        [[[8, 1, 3], [0, 2, 4], [7, 6, 5]],
         [[0, 1, 3], [8, 2, 4], [7, 6, 5]],
         [[1, 0, 3], [8, 2, 4], [7, 6, 5]],
         [[1, 2, 3], [8, 0, 4], [7, 6, 5]]]
    print("Verificado")

# La verificación es
#    >>> test_8puzzle()
#    Verificado
