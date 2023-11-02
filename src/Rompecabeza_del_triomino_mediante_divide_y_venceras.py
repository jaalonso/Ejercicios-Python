# Rompecabeza_del_triomino_mediante_divide_y_venceras.py
# Rompecabeza del triominó_mediante divide y vencerás.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 2-noviembre-2023
# ======================================================================

# ---------------------------------------------------------------------
# Introducción
# ---------------------------------------------------------------------

# Un poliominó es una figura geométrica plana formada conectando dos o
# más cuadrados por alguno de sus lados. Los cuadrados se conectan lado
# con lado, pero no se pueden conectar ni por sus vértices, ni juntando
# solo parte de un lado de un cuadrado con parte de un lado de otro. Si
# unimos dos cuadrados se obtiene un dominó, si se juntan tres
# cuadrados se construye un triominó.
#
# Sólo existen dos triominós, el I-triomino (por tener forma de I) y el
# L-triominó (por su forma de L) como se observa en las siguientes
# figuras
#
#    X
#-   X     X
#    X     XX
#
# El rompecabeza del triominó consiste en cubrir un tablero cuadrado
# con 2^n filas y 2^n columnas, en el que se ha eliminado una casilla,
# con L-triominós de formas que cubran todas las casillas excepto la
# eliminada y los triominós no se solapen.
#
# La casilla eliminada se representará con -1 y los L-triominós con
# sucesiones de tres números consecutivos en forma de L. Con esta
# representación una solución del rompecabeza del triominó con 4 filas
# y la fila eliminada en la posición (4,4) es
#    (  3  3  2  2 )
#    (  3  1  1  2 )
#    (  4  1  5  5 )
#    (  4  4  5 -1 )
#
# Con divideVenceras(ind, resuelve, divide, combina pbInicial) se
# resuelve el problema pbInicial mediante la técnica de divide y
# vencerás, donde
# + ind(pb) se verifica si el problema pb es indivisible
# + resuelve(pb) es la solución del problema indivisible pb
# + divide(pb) es la lista de subproblemas de pb
# + combina(pb, ss) es la combinación de las soluciones ss de los
#   subproblemas del problema pb.
# + pbInicial es el problema inicial
#
# En los distintos apartados de esta relación se irán definiendo las
# anteriores funciones.

# ---------------------------------------------------------------------
# Librerías auxiliares
# ---------------------------------------------------------------------

import numpy as np
import numpy.typing as npt

from src.DivideVenceras import divideVenceras

# ---------------------------------------------------------------------
# Tipos
# ---------------------------------------------------------------------

# Los tableros son matrices de números enteros donde -1 representa el
# hueco, 0 las posiciones sin rellenar y los números mayores que 0
# representan los triominós.
Tablero = npt.NDArray[np.int_]

# Los problemas se representarán mediante pares formados por un número
# natural mayor que 0 (que indica el número con el que se formará el
# siguiente triominó que se coloque) y un tablero.
Problema = tuple[int, Tablero]

# Las posiciones son pares de números enteros
Posicion = tuple[int, int]

# ---------------------------------------------------------------------
# Problema inicial
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 1. Definir la función
#    tablero(int, Posicion) -> Tablero
# tal que tablero(n, p) es el tablero inicial del problema del triominó
# en un cuadrado nxn en el que se ha eliminado la casilla de la
# posición p. Por ejemplo,
#    >>> tablero(4, (3,4))
#    array([[ 0,  0,  0,  0],
#           [ 0,  0,  0,  0],
#           [ 0,  0,  0, -1],
#           [ 0,  0,  0,  0]])
# ---------------------------------------------------------------------
def tablero(n: int, p: Posicion) -> Tablero:
    (i, j) = p
    q = np.zeros((n, n), dtype=int)
    q[i - 1, j - 1] = -1
    return q

# ---------------------------------------------------------------------
# Ejercicio 2. Definir la función
#    pbInicial(int, Posicion) -> Problema
# tal que pbInicial(n, p) es el problema inicial del rompecabeza del
# triominó en un cuadrado nxn en el que se ha eliminado la casilla de la
# posición p. Por ejemplo,
#    >>> pbInicial(4, (4,4))
#    (1, array([[ 0,  0,  0,  0],
#           [ 0,  0,  0,  0],
#           [ 0,  0,  0,  0],
#           [ 0,  0,  0, -1]]))
def pbInicial(n: int, p: Posicion) -> Problema:
    return 1, tablero(n, p)

# ---------------------------------------------------------------------
# Problemas indivisibles
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 3. Definir la función
#    ind :: (Problema) -> bool
# ind(pb) se verifica si el problema pb es indivisible. Por ejemplo,
#    ind(pbInicial(2, (1,2)))  ==  True
#    ind(pbInicial(4, (1,2)))  ==  False
# ---------------------------------------------------------------------

def ind(pb: Problema) -> bool:
    _, p = pb
    return p.shape[1] == 2

# ---------------------------------------------------------------------
# Resolución de problemas indivisibles
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    posicionHueco(Tablero) -> Posicion
# posicionHueco(t) es la posición del hueco en el tablero t. Por
# ejemplo,
#    posicionHueco(tablero(8, (5,2)))  ==  (5,2)
# ---------------------------------------------------------------------

def posicionHueco(t: Tablero) -> Posicion:
    indices = np.argwhere(t != 0)
    (i, j) =  tuple(indices[0])
    return (i + 1, j + 1)

# ---------------------------------------------------------------------
# Ejercicio 5. Definir la función
#    cuadranteHueco(t: Tablero) -> int
# cuadranteHueco(p) es el cuadrante donde se encuentra el hueco del
# tablero t (donde la numeración de los cuadrantes es 1 el superior
# izquierdo, 2 el inferior izquierdo, 3 el superior derecho y 4 el
# inferior derecho). Por ejemplo,
#    cuadranteHueco(tablero(8, (4,4)))  ==  1
#    cuadranteHueco(tablero(8, (5,2)))  ==  2
#    cuadranteHueco(tablero(8, (3,6)))  ==  3
#    cuadranteHueco(tablero(8, (6,6)))  ==  4
# ---------------------------------------------------------------------

def cuadranteHueco(t: Tablero) -> int:
    i, j = posicionHueco(t)
    x = t.shape[0] // 2
    if j <= x:
        if i <= x:
            return 1
        return 2
    if i <= x:
        return 3
    return 4

# ---------------------------------------------------------------------
# Ejercicio 6. Definir la función
#    centralHueco :: (Tablero) -> Posicion
# tal que centralHueco(t) es la casilla central del cuadrante del
# tablero t donde se encuentra el hueco. Por ejemplo,
#    centralHueco(tablero(8, (5,2)))  ==  (5,4)
#    centralHueco(tablero(8, (4,4)))  ==  (4,4)
#    centralHueco(tablero(8, (3,6)))  ==  (4,5)
#    centralHueco(tablero(8, (6,6)))  ==  (5,5)
# ---------------------------------------------------------------------

def centralHueco(t: Tablero) -> Posicion:
    x = t.shape[0] // 2
    cuadrante = cuadranteHueco(t)
    if cuadrante == 1:
        return (x, x)
    if cuadrante == 2:
        return (x+1, x)
    if cuadrante == 3:
        return (x, x+1)
    return (x+1, x+1)

# ---------------------------------------------------------------------
# Ejercicio 7. Definir la función
#    centralesSinHueco : (Tablero) -> [Posicion]
# tal que centralesSinHueco(t) son las posiciones centrales del tablero
# t de los cuadrantes sin hueco. Por ejemplo,
#    centralesSinHueco(tablero(8, (5,2)))  ==  [(4,4),(4,5),(5,5)]
# ---------------------------------------------------------------------

def centralesSinHueco(t: Tablero) -> list[Posicion]:
    x = t.shape[0] // 2
    i, j = centralHueco(t)
    ps = [(x, x), (x+1, x), (x, x+1), (x+1, x+1)]
    return [p for p in ps if p != (i, j)]

# ---------------------------------------------------------------------
# Ejercicio 8. Definir la función
#    actualiza : (Tablero, list[tuple[Posicion, int]]) -> Tablero
# actualiza(t, ps) es la matriz obtenida cambiando en t los valores del
# las posiciones indicadas en ps por sus correspondientes valores. Por
# ejemplo,
#    >>> actualiza(np.identity(3, dtype=int), [((1,2),4),((3,1),5)])
#    array([[1, 4, 0],
#           [0, 1, 0],
#           [5, 0, 1]])
# ---------------------------------------------------------------------

def actualiza(p: Tablero, ps: list[tuple[Posicion, int]]) -> Tablero:
    for (i, j), x in ps:
        p[i - 1, j - 1] = x
    return p

# ---------------------------------------------------------------------
# Ejercicio 9. Definir la función
#    triominoCentral : (Problema) -> Tablero
# tal que triominoCentral(n,t) es el tablero obtenido colocando el
# triominó formado por el número n en las posiciones centrales de los 3
# cuadrantes que no contienen el hueco. Por ejemplo,
#    >>> triominoCentral((7, tablero(4, (4,4))))
#    array([[ 0,  0,  0,  0],
#           [ 0,  7,  7,  0],
#           [ 0,  7,  0,  0],
#           [ 0,  0,  0, -1]])
# ---------------------------------------------------------------------

def triominoCentral(p: Problema) -> Tablero:
    n, t = p
    return actualiza(t, [((i,j),n) for (i,j) in centralesSinHueco(t)])

# ---------------------------------------------------------------------
# Ejercicio 10. Definir la función
#    resuelve :: (Problema) -> Tablero
# tal que resuelve(p) es la solución del problema indivisible p. Por
# ejemplo,
#    >>> tablero(2, (2,2))
#    array([[ 0,  0],
#           [ 0, -1]])
#    >>> resuelve((5,tablero(2, (2,2))))
#    array([[ 5,  5],
#           [ 5, -1]])
# ---------------------------------------------------------------------

def resuelve(p: Problema) -> Tablero:
    return triominoCentral(p)

# ---------------------------------------------------------------------
# División en subproblemas
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 11. Definir la función
#    divide : (Problema) -> list[Problema]
# tal que divide(n,t) es la lista de de los problemas obtenidos
# colocando el triominó n en las casillas centrales de t que no
# contienen el hueco y dividir el tablero en sus cuatros cuadrantes y
# aumentar en uno el número del correspondiente triominó. Por ejemplo,
#    >>> divide((3,tablero(4, (4,4))))
#    [(4, array([[0, 0],
#                [3, 0]])),
#     (5, array([[0, 0],
#                [0, 3]])),
#     (6, array([[0, 3],
#                [0, 0]])),
#     (7, array([[ 0,  0],
#                [ 0, -1]]))]
# ---------------------------------------------------------------------

def divide(p: Problema) -> list[Problema]:
    q = triominoCentral(p)
    n, t = p
    m = t.shape[0]
    x = m // 2
    subproblemas = [
        (n+1, q[0:x, x:m]),
        (n+2, q[0:x, 0:x]),
        (n+3, q[x:m, 0:x]),
        (n+4, q[x:m, x:m])
    ]
    return subproblemas

# ---------------------------------------------------------------------
# Combinación de soluciones
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 12. Definir la función
#    combina : (Problema, list[Tablero]) -> Tablero
# combina(p, ts) es la combinación de las soluciones ts de los
# subproblemas del problema p. Por ejemplo,
#    >>> inicial = (1, tablero(4, (4, 4)))
#    >>> p1, p2, p3, p4 = divide(inicial)
#    >>> s1, s2, s3, s4 = map(resuelve, [p1, p2, p3, p4])
#    >>> combina(inicial, [s1, s2, s3, s4])
#    array([[ 3,  3,  2,  2],
#           [ 3,  1,  1,  2],
#           [ 4,  1,  5,  5],
#           [ 4,  4,  5, -1]])
# ---------------------------------------------------------------------

def combina(_: Problema, ts: list[Tablero]) -> Tablero:
    s1, s2, s3, s4 = ts
    combined = np.block([[s2, s1], [s3, s4]])
    return combined

# ---------------------------------------------------------------------
# Solución mediante divide y vencerás
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 13. Definir la función
#    triomino : (int, Posicion) -> Tablero
# tal que triomino(n, p) es la solución, mediante divide y vencerás,
# del rompecabeza del triominó en un cuadrado nxn en el que se ha
# eliminado la casilla de la posición p. Por ejemplo,
#    >>> triomino(4, (4,4))
#    array([[ 3,  3,  2,  2],
#           [ 3,  1,  1,  2],
#           [ 4,  1,  5,  5],
#           [ 4,  4,  5, -1]])
#    >>> triomino(4, (2,3))
#    array([[ 3,  3,  2,  2],
#           [ 3,  1, -1,  2],
#           [ 4,  1,  1,  5],
#           [ 4,  4,  5,  5]])
#    >>> triomino(16, (5,6))
#    array([[ 7,  7,  6,  6,  6,  6,  5,  5,  6,  6,  5,  5,  5,  5,  4,  4],
#           [ 7,  5,  5,  6,  6,  4,  4,  5,  6,  4,  4,  5,  5,  3,  3,  4],
#           [ 8,  5,  9,  9,  7,  7,  4,  8,  7,  4,  8,  8,  6,  6,  3,  7],
#           [ 8,  8,  9,  3,  3,  7,  8,  8,  7,  7,  8,  2,  2,  6,  7,  7],
#           [ 8,  8,  7,  3,  9, -1,  8,  8,  7,  7,  6,  6,  2,  8,  7,  7],
#           [ 8,  6,  7,  7,  9,  9,  7,  8,  7,  5,  5,  6,  8,  8,  6,  7],
#           [ 9,  6,  6, 10, 10,  7,  7, 11,  8,  8,  5,  9,  9,  6,  6, 10],
#           [ 9,  9, 10, 10, 10, 10, 11, 11,  1,  8,  9,  9,  9,  9, 10, 10],
#           [ 8,  8,  7,  7,  7,  7,  6,  1,  1,  9,  8,  8,  8,  8,  7,  7],
#           [ 8,  6,  6,  7,  7,  5,  6,  6,  9,  9,  7,  8,  8,  6,  6,  7],
#           [ 9,  6, 10, 10,  8,  5,  5,  9, 10,  7,  7, 11,  9,  9,  6, 10],
#           [ 9,  9, 10,  4,  8,  8,  9,  9, 10, 10, 11, 11,  5,  9, 10, 10],
#           [ 9,  9,  8,  4,  4, 10,  9,  9, 10, 10,  9,  5,  5, 11, 10, 10],
#           [ 9,  7,  8,  8, 10, 10,  8,  9, 10,  8,  9,  9, 11, 11,  9, 10],
#           [10,  7,  7, 11, 11,  8,  8, 12, 11,  8,  8, 12, 12,  9,  9, 13],
#           [10, 10, 11, 11, 11, 11, 12, 12, 11, 11, 12, 12, 12, 12, 13, 13]])
# ---------------------------------------------------------------------

def triomino(n: int, p: Posicion) -> Tablero:
    return divideVenceras(ind, resuelve, divide, combina, pbInicial(n, p))

# Verificación
# ============

def test_triomino() -> None:
    def filas(p: Tablero) -> list[list[int]]:
        return p.tolist()

    assert filas(triomino(4, (4,4))) == \
        [[3,3,2,2],[3,1,1,2],[4,1,5,5],[4,4,5,-1]]
    assert filas(triomino(4, (2,3))) == \
        [[3,3,2,2],[3,1,-1,2],[4,1,1,5],[4,4,5,5]]
    assert filas(triomino(16, (5,6))) == \
        [[7,7,6,6,6,6,5,5,6,6,5,5,5,5,4,4],
         [7,5,5,6,6,4,4,5,6,4,4,5,5,3,3,4],
         [8,5,9,9,7,7,4,8,7,4,8,8,6,6,3,7],
         [8,8,9,3,3,7,8,8,7,7,8,2,2,6,7,7],
         [8,8,7,3,9,-1,8,8,7,7,6,6,2,8,7,7],
         [8,6,7,7,9,9,7,8,7,5,5,6,8,8,6,7],
         [9,6,6,10,10,7,7,11,8,8,5,9,9,6,6,10],
         [9,9,10,10,10,10,11,11,1,8,9,9,9,9,10,10],
         [8,8,7,7,7,7,6,1,1,9,8,8,8,8,7,7],
         [8,6,6,7,7,5,6,6,9,9,7,8,8,6,6,7],
         [9,6,10,10,8,5,5,9,10,7,7,11,9,9,6,10],
         [9,9,10,4,8,8,9,9,10,10,11,11,5,9,10,10],
         [9,9,8,4,4,10,9,9,10,10,9,5,5,11,10,10],
         [9,7,8,8,10,10,8,9,10,8,9,9,11,11,9,10],
         [10,7,7,11,11,8,8,12,11,8,8,12,12,9,9,13],
         [10,10,11,11,11,11,12,12,11,11,12,12,12,12,13,13]]
    print("Verificado")

# La verificación es
#    >>> test_triomino()
#    Verificado

# ---------------------------------------------------------------------
# Referencias
# ---------------------------------------------------------------------

# + Raúl Ibáñez "Embaldosando con L-triominós (Un ejemplo de
#   demostración por inducción)" http://bit.ly/1DKPBbt
# + "Algorithmic puzzles" pp. 10.
