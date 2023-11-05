# BEE_El_problema_de_las_fichas.py
# El problema de las fichas mediante búsqueda en espacio de estado.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 5-noviembre-2023
# ======================================================================

# ---------------------------------------------------------------------
# Introducción
# ---------------------------------------------------------------------

# Para el problema de las fichas de orden (m,n) se considera un tablero
# con m+n+1 cuadrados consecutivos.
#
# Inicialmente, en cada uno de los m primeros cuadrados hay una ficha
# blanca, a continuación un hueco y  en cada uno de los n últimos
# cuadrados hay una ficha verde. El objetivo consiste en tener las
# fichas verdes al principio y las blancas al final.
#
# Por ejemplo, en el problema de las fichas de orden (3,3) el tablero
# inicial es
#       +---+---+---+---+---+---+---+
#       | B | B | B |   | V | V | V |
#       +---+---+---+---+---+---+---+
# y el final es
#       +---+---+---+---+---+---+---+
#       | V | V | V |   | B | B | B |
#       +---+---+---+---+---+---+---+
#
# Los movimientos permitidos consisten en desplazar una ficha al hueco
# saltando, como máximo, sobre otras dos.
#
# Además, se considera la heurística que para cada tablero vale la suma
# de piezas blancas situadas a la izquierda de cada una de las piezas
# verdes. Por  ejemplo, para el estado
#       +---+---+---+---+---+---+---+
#       | B | V | B |   | V | V | B |
#       +---+---+---+---+---+---+---+
# su valor es 1+2+2 = 5. La heurística de un estado es la del primero
# de sus tableros.
#
# El objetivo de esta relación de ejercicios es resolver el problema
# de las fichas mediante búsqueda en espacio de estados, utilizando las
# implementaciones estudiadas en los ejercicios anteriores.

# ---------------------------------------------------------------------
# Importaciones
# ---------------------------------------------------------------------

from enum import Enum
from functools import partial
from typing import Callable, Optional

from src.BusquedaEnAnchura import buscaAnchura1
from src.BusquedaEnEscalada import buscaEscalada
from src.BusquedaEnProfundidad import buscaProfundidad1
from src.BusquedaPrimeroElMejor import buscaPM

# Representación del problema
# ===========================

# ---------------------------------------------------------------------
# Ejercicio 1. Definir el tipo Ficha con tres constructores B, V y H que
# representan las fichas blanca, verde y hueco, respectivamente.
# ---------------------------------------------------------------------

class Ficha(Enum):
    B = 0
    V = 1
    H = 2

    def __repr__(self) -> str:
        return self.name

B = Ficha.B
V = Ficha.V
H = Ficha.H

# ---------------------------------------------------------------------
# Ejercicio 2. Definir el tipo Tablero como una lista de fichas que
# representa las fichas colocadas en el tablero.
# ---------------------------------------------------------------------

Tablero = list[Ficha]

# ---------------------------------------------------------------------
# Ejercicio 3. Definir la función
#    tableroInicial : (int, int) -> Tablero
# tal que tableroInicial(m, n) representa el tablero inicial del
# problema de las fichas de orden (m,n). Por ejemplo,
#    tableroInicial(2, 3)  ==  [B,B,H,V,V,V]
#    tableroInicial(3, 2)  ==  [B,B,B,H,V,V]
# ---------------------------------------------------------------------

def tableroInicial(m: int, n: int) -> Tablero:
    return [B]*m + [H] + [V]*n

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    tableroFinal : (int, int) -> Tablero
# tal que tableroFinal(m, n) representa el tablero final del problema de
# las fichas de orden (m,n). Por ejemplo,
#    tableroFinal(2, 3)  ==  [V,V,V,H,B,B]
#    tableroFinal(3, 2)  ==  [V,V,H,B,B,B]
# ---------------------------------------------------------------------

def tableroFinal(m: int, n: int) -> Tablero:
    return [V]*n + [H] + [B]*m

# ---------------------------------------------------------------------
# Ejercicio 5. Definir la función
#    posicionHueco : (Tablero) -> int
# tal que posicionHueco(t) es la posición del hueco en el tablero t. Por
# ejemplo,
#    posicionHueco(tableroInicial(3, 2))  ==  3
# ---------------------------------------------------------------------

def posicionHueco(t: Tablero) -> int:
    return t.index(H)

# intercambia(xs, i, j) es la lista obtenida intercambiando los
# elementos de xs en las posiciones i y j. Por ejemplo,
#    intercambia(1, 3, tableroInicial(3, 2))  ==  [B, H, B, B, V, V]
def intercambia(i: int, j: int, t: Tablero) -> Tablero:
    t1 = t.copy()
    t1[i], t1[j] = t1[j], t1[i]
    return t1

# ---------------------------------------------------------------------
# Ejercicio 6. Definir la función
#    tablerosSucesores : (Tablero) -> list[Tablero]
# tal que tablerosSucesores(t) es la lista de los sucesores del tablero
# t. Por ejemplo,
#    >>> tablerosSucesores([V,B,H,V,V,B])
#    [[V,H,B,V,V,B],[H,B,V,V,V,B],[V,B,V,H,V,B],[V,B,V,V,H,B],
#     [V,B,B,V,V,H]]
#    >>> tablerosSucesores([B,B,B,H,V,V,V])
#    [[B,B,H,B,V,V,V],[B,H,B,B,V,V,V],[H,B,B,B,V,V,V],
#     [B,B,B,V,H,V,V],[B,B,B,V,V,H,V],[B,B,B,V,V,V,H]]
# ---------------------------------------------------------------------

def tablerosSucesores(t: Tablero) -> list[Tablero]:
    j = posicionHueco(t)
    n = len(t)
    return [intercambia(i, j, t)
            for i in [j-1,j-2,j-3,j+1,j+2,j+3]
            if 0 <= i < n]

# Heurística
# ==========

# ---------------------------------------------------------------------
# Ejercicio 7. Definir la función
#    heuristicaT : (Tablero) -> int
# tal que heuristicaT(t) es la heurística del tablero t. Por ejemplo,
#    heuristicaT([B,V,B,H,V,V,B]) == 5
# ---------------------------------------------------------------------

def heuristicaT(t: Tablero) -> int:
    if not t:
        return 0
    f, *fs = t
    if f in {V, H}:
        return heuristicaT(fs)
    return heuristicaT(fs) + len([x for x in fs if x == V])

# ---------------------------------------------------------------------
# Ejercicio 8. La clase Estado representa los estados del espacio de
# búsqueda, donde un estado es una lista de tableros [t_n,...,t_2,t_1]
# tal que t_1 es el tablero inicial y para cada i (2 <= i <= n), t_i es
# un sucesor de t_(i-1).
#
# Definir la clase Estado.
# ---------------------------------------------------------------------

class Estado(list[Tablero]):
    def __lt__(self, e: list[Tablero]) -> bool:
        return heuristicaT(self[0]) < heuristicaT(e[0])

# ---------------------------------------------------------------------
# Ejercicio 9. Definir la función
#    inicial : (int, int) -> Estado
# tal que inicial(m, n) representa el estado inicial del problema de las
# fichas de orden (m,n). Por ejemplo,
#    inicial(2, 3)  ==  [[B,B,H,V,V,V]]
#    inicial(3, 2)  ==  [[B,B,B,H,V,V]]
# ---------------------------------------------------------------------

def inicial(m: int, n: int) -> Estado:
    return Estado([tableroInicial(m, n)])

# ---------------------------------------------------------------------
# Ejercicio 10. Definir la función
#    esFinal(int, int, Estado) -> bool
# tal que esFinal(m, n, e) se verifica si e es un estado final del
# problema de las fichas de orden (m,n). Por ejemplo,
#    >>> esFinal(2, 1, [[V,H,B,B],[V,B,B,H],[H,B,B,V],[B,B,H,V]])
#    True
#    >>> esFinal(2, 1, [[V,B,B,H],[H,B,B,V],[B,B,H,V]])
#    False
# ---------------------------------------------------------------------

def esFinal(m: int, n: int, e: Estado) -> bool:
    return e[0] == tableroFinal(m, n)

# ---------------------------------------------------------------------
# Ejercicio 11. Definir la función
#    sucesores : (Estado) -> list[Estado]
# tal que sucesores(n) es la lista de los sucesores del estado n. Por
# ejemplo,
#    >>> sucesores([[H,B,B,V],[B,B,H,V]])
#    [[[B,H,B,V],[H,B,B,V],[B,B,H,V]],
#     [[V,B,B,H],[H,B,B,V],[B,B,H,V]]]
#    >>> sucesores([[B,H,B,V],[H,B,B,V],[B,B,H,V]])
#    [[[B,V,B,H],[B,H,B,V],[H,B,B,V],[B,B,H,V]]]
# ---------------------------------------------------------------------

def sucesores(e: Estado) -> list[Estado]:
    t, *ts = e
    return [Estado([t1] + e) for t1 in tablerosSucesores(t) if t1 not in ts]

# Solución por búsqueda
# =====================

# ---------------------------------------------------------------------
# Ejercicio 12. Definir el tipo Busqueda par representar los
# procedimientos de búsqueda.
# ---------------------------------------------------------------------

Busqueda = Callable[[Callable[[Estado], list[Estado]],
                     Callable[[Estado], bool],
                     Estado],
                    Optional[Estado]]

# ---------------------------------------------------------------------
# Ejercicio 13. Usando los métodos de búsqueda estudiado en los
# ejercicios anteriores, definir la función
#    fichas :: Busqueda -> Int -> Int -> [[Tablero]]
# tal que fichas(b, m, n) es la lista de las soluciones del problema de
# las fichas de orden (m,n) obtenidas mediante el procedimiento de
# búsqueda b. Por ejemplo,
#    >>> fichas(buscaProfundidad1, 2, 2)
#    [[B,B,H,V,V],[H,B,B,V,V],[B,H,B,V,V],[B,V,B,H,V],[H,V,B,B,V].
#     [B,V,H,B,V],[B,V,V,B,H],[B,H,V,B,V],[B,B,V,H,V],[H,B,V,B,V],
#     [V,B,H,B,V],[V,B,V,B,H],[V,H,V,B,B],[V,B,V,H,B],[H,B,V,V,B],
#     [B,H,V,V,B],[B,V,V,H,B],[H,V,V,B,B],[V,V,H,B,B]]
#    >>> fichas(buscaAnchura1, 2, 2)
#    [[B,B,H,V,V],[H,B,B,V,V],[V,B,B,H,V],[V,H,B,B,V],[V,V,B,B,H],
#     [V,V,H,B,B]]
#    >>> fichas(buscaPM, 2, 2)
#    [[B,B,H,V,V],[H,B,B,V,V],[V,B,B,H,V],[V,B,B,V,H],[V,H,B,V,B],
#     [V,V,B,H,B],[V,V,H,B,B]]
#    >>> fichas(buscaEscalada, 2, 2)
#    [[B,B,H,V,V],[B,H,B,V,V],[H,B,B,V,V],[V,B,B,H,V],[V,B,B,V,H],
#     [V,H,B,V,B],[V,V,B,H,B],[V,V,H,B,B]]
# ---------------------------------------------------------------------

def fichas(b: Busqueda, m: int, n: int) -> Optional[list[Tablero]]:
    r = partial(b, sucesores, lambda e: esFinal(m, n, e), inicial(m, n))()
    if r is None:
        return None
    return [list(reversed(es)) for es in r]

# Verificación
# ============

def test_fichas() -> None:
    assert fichas(buscaProfundidad1, 1, 2) == \
        [[B, H, V, V], [B, V, V, H], [H, V, V, B], [V, V, H, B]]
    assert fichas(buscaAnchura1, 1, 2) == \
        [[B, H, V, V], [B, V, V, H], [H, V, V, B], [V, V, H, B]]
    assert fichas(buscaPM, 1, 2) == \
        [[B, H, V, V], [B, V, H, V], [H, V, B, V], [V, V, B, H],
         [V, V, H, B]]
    assert fichas(buscaEscalada, 1, 2) == \
        [[B, H, V, V], [H, B, V, V], [V, B, H, V], [V, H, B, V],
         [V, V, B, H], [V, V, H, B]]
    print("Verificado")

# La verificación es
#    >>> test_fichas()
#    Verificado
