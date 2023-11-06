# El_problema_del_calendario_mediante_busqueda_en_espacio_de_estado.py
# El problema del calendario mediante búsqueda en espacio de estado.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla,  6-noviembre-2023
# ======================================================================

# ---------------------------------------------------------------------
# Introducción
# ---------------------------------------------------------------------

# El problema del calendario, para una competición deportiva en la que
# se enfrentan n participantes, consiste en elaborar un calendario de
# forma que:
#    + el campeonato dure n-1 días,
#    + cada participante juegue exactamente un partido diario y
#    + cada participante juegue exactamente una vez con cada adversario.
# Por ejemplo, con 8 participantes una posible solución es
#      | 1 2 3 4 5 6 7
#    --+--------------
#    1 | 2 3 4 5 6 7 8
#    2 | 1 4 3 6 5 8 7
#    3 | 4 1 2 7 8 5 6
#    4 | 3 2 1 8 7 6 5
#    5 | 6 7 8 1 2 3 4
#    6 | 5 8 7 2 1 4 3
#    7 | 8 5 6 3 4 1 2
#    8 | 7 6 5 4 3 2 1
# donde las filas indican los jugadores y las columnas los días; es
# decir, el elemento (i,j) indica el adversario del jugador i el día j;
# por ejemplo, el adversario del jugador 2 el 4ª día es el jugador 6.
#
# El objetivo de esta relación de ejercicios es resolver el problema
# del calendario mediante búsqueda en espacio de estados, utilizando las
# implementaciones estudiadas en los ejercicios anteriores.

# ---------------------------------------------------------------------
# Importaciones
# ---------------------------------------------------------------------

from copy import deepcopy
from typing import Optional

import numpy as np
import numpy.typing as npt

from src.BusquedaEnProfundidad import buscaProfundidad

# ---------------------------------------------------------------------
# Ejercicio 1. Definir el tipo Calendario como matrices de enteros.
# ---------------------------------------------------------------------

Calendario = npt.NDArray[np.int_]

# ---------------------------------------------------------------------
# Ejercicio 2. Definir la función
#    inicial : (int) -> Calendario
# tal que inicial(n) es el estado inicial para el problema del
# calendario con n participantes; es decir, una matriz de n fila y n-1
# columnas con todos sus elementos iguales a 0. Por ejemplo,
#    >>> inicial(4)
#    array([[0, 0, 0],
#           [0, 0, 0],
#           [0, 0, 0],
#           [0, 0, 0]])
# ---------------------------------------------------------------------

def inicial(n: int) -> Calendario:
    return np.zeros((n, n - 1), dtype=int)

# ---------------------------------------------------------------------
# Ejercicio 3. Definir la función
#    primerHueco : (Calendario) -> tuple[int, int]
# primerHueco(c) es la posición del primer elemento cuyo valor es 0. Si
# todos los valores son distintos de 0, devuelve (-1,-1). Por ejemplo,
#    primerHueco(np.array([[1,2,3],[4,5,0],[7,0,0]])) == (1, 2)
#    primerHueco(np.array([[1,2,3],[4,5,6],[7,8,0]])) == (2, 2)
#    primerHueco(np.array([[1,2,3],[4,5,6],[7,8,9]])) == (-1, -1)
# ---------------------------------------------------------------------

def primerHueco(c: Calendario) -> tuple[int, int]:
    (n, m) = c.shape
    for i in range(0, n):
        for j in range(0, m):
            if c[i,j] == 0:
                return (i, j)
    return (-1, -1)

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    libres : (Calendario, int, int) -> list[int]
# tal que libres(c, i, j) es la lista de valores que que pueden poner en
# la posición (i,j) del calendario c. Por ejemplo,
#    libres(np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0]]),0,0) == [2, 3, 4]
#    libres(np.array([[2,0,0],[1,0,0],[0,0,0],[0,0,0]]),0,1) == [3, 4]
#    libres(np.array([[2,3,0],[1,0,0],[0,1,0],[0,0,0]]),0,2) == [4]
#    libres(np.array([[2,3,4],[1,0,0],[0,1,0],[0,0,1]]),1,1) == [4]
#    libres(np.array([[2,3,4],[1,4,0],[0,1,0],[0,2,1]]),1,2) == [3]
# ---------------------------------------------------------------------

def libres(c: Calendario, i: int, j: int) -> list[int]:
    n = c.shape[0]
    return list(set(range(1, n + 1))
                - {i + 1}
                - set(c[i])
                - set(c[:,j]))

# ---------------------------------------------------------------------
# Ejercicio 5. Definir la función
#    setElem : (int, int, int, Calendario) -> Calendario
# setElem(k, i, j, c) es el calendario obtenido colocando en c el valor
# k en la posición (i,j).
#    >>> setElem(7,1,2,np.array([[1,2,3],[4,5,0],[0,0,0]]))
#    array([[1, 2, 3],
#           [4, 5, 7],
#           [0, 0, 0]])
# ---------------------------------------------------------------------

def setElem(k: int, i: int, j: int, c: Calendario) -> Calendario:
    _c = deepcopy(c)
    _c[i, j] = k
    return _c

# ---------------------------------------------------------------------
# Ejercicio 6. Definir la función
#    sucesores : (Calendario) -> list[Calendario]
# tal que sucesores(c) es la lista de calendarios obtenidos poniendo en
# el lugar del primer elemento nulo de c uno de los posibles jugadores
# de forma que se cumplan las condiciones del problema. Por ejemplo,
#    >>> sucesores(np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0]]))
#    [array([[2,0,0], [1,0,0], [0,0,0], [0,0,0]]),
#     array([[3,0,0], [0,0,0], [1,0,0], [0,0,0]]),
#     array([[4,0,0], [0,0,0], [0,0,0], [1,0,0]])]
#    >>> sucesores(np.array([[2,0,0],[1,0,0],[0,0,0],[0,0,0]]))
#    [array([[2,3,0], [1,0,0], [0,1,0], [0,0,0]]),
#     array([[2,4,0], [1,0,0], [0,0,0], [0,1,0]])]
#    >>> sucesores(np.array([[2,3,0],[1,0,0],[0,1,0],[0,0,0]]))
#    [array([[2,3,4], [1,0,0], [0,1,0], [0,0,1]])]
#    >>> sucesores(np.array([[2,3,4],[1,0,0],[0,1,0],[0,0,1]]))
#    [array([[2,3,4], [1,4,0], [0,1,0], [0,2,1]])]
#    >>> sucesores(np.array([[2,3,4],[1,4,0],[0,1,0],[0,2,1]]))
#    [array([[2,3,4], [1,4,3], [0,1,2], [0,2,1]])]
#    >>> sucesores(np.array([[2,3,4],[1,4,3],[0,1,2],[0,2,1]]))
#    [array([[2,3,4], [1,4,3], [4,1,2], [3,2,1]])]
#    >>> sucesores(np.array([[2,3,4],[1,4,3],[4,1,2],[3,2,1]]))
#    []
# ---------------------------------------------------------------------

def sucesores(c: Calendario) -> list[Calendario]:
    n = c.shape[0]
    (i, j) = primerHueco(c)
    return [setElem(i+1, k-1, j, setElem(k, i, j, c))
            for k in libres(c, i, j)]

# ---------------------------------------------------------------------
# Ejercicio 7. Definir la función
#    esFinal : (Calendario) -> bool
# esFinal(c) se verifica si c un estado final para el problema
# del calendario con n participantes; es decir, no queda en c ningún
# elemento igual a 0. Por ejemplo,
#    >>> esFinal(np.array([[2,3,4],[1,4,3],[4,1,2],[3,2,1]]))
#    True
#    >>> esFinal(np.array([[2,3,4],[1,4,3],[4,1,2],[3,2,0]]))
#    False
# ---------------------------------------------------------------------

def esFinal(c: Calendario) -> bool:
    return primerHueco(c) == (-1, -1)

# ---------------------------------------------------------------------
# Ejercicio 7. Usando el procedimiento de búsqueda en profundidad,
# definir la función
#    calendario : (int) -> [Calendario]
# tal que calendario(n) son las soluciones del problema del calendario,
# con n participantes, mediante el patrón de búsqueda em
# profundidad. Por ejemplo,
#    >>> calendario(6)[0]
#    array([[6, 5, 4, 3, 2],
#           [5, 4, 3, 6, 1],
#           [4, 6, 2, 1, 5],
#           [3, 2, 1, 5, 6],
#           [2, 1, 6, 4, 3],
#           [1, 3, 5, 2, 4]])
#    >>> len(calendario(6))
#    720
#    >>> len(calendario(5))
#    0
# ---------------------------------------------------------------------

def calendario(n: int) -> list[Calendario]:
    return buscaProfundidad(sucesores, esFinal, inicial(n))

# Verificación
# ============

def test_calendario() -> None:
    def filas(p: Calendario) -> list[list[int]]:
        return p.tolist()

    assert filas(calendario(6)[0]) == \
        [[6, 5, 4, 3, 2],
         [5, 4, 3, 6, 1],
         [4, 6, 2, 1, 5],
         [3, 2, 1, 5, 6],
         [2, 1, 6, 4, 3],
         [1, 3, 5, 2, 4]]
    assert len(calendario(6)) == 720
    assert len(calendario(5)) == 0
    print("Verificado")
