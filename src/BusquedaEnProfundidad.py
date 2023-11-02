# BusquedaEnProfundidad.py
# Búsqueda en espacios de estados por profundidad.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 2-noviembre-2023
# ======================================================================

# ---------------------------------------------------------------------
# Las características de los problemas de espacios de estados son:
# + un conjunto de las posibles situaciones o nodos que constituye el
#   espacio de estados (estos son las potenciales soluciones que se
#   necesitan explorar),
# + un conjunto de movimientos de un nodo a otros nodos, llamados los
#   sucesores del nodo,
# + un nodo inicial y
# + un nodo objetivo que es la solución.
#
# Definir las funciones
#    buscaProfundidad(Callable[[A], list[A]], Callable[[A], bool], A) -> list[A]
#    buscaProfundidad1(Callable[[A], list[A]], Callable[[A], bool], A) -> Optional[A]
# tales que
# + buscaProfundidad(s, o, e) es la lista de soluciones del
#   problema de espacio de estado definido por la función sucesores s,
#   el objetivo o y estado inicial e obtenidas mediante búsqueda en
#   profundidad.
# + buscaProfundidad1(s, o, e) es la primera solución del
#   problema de espacio de estado definido por la función sucesores s,
#   el objetivo o y estado inicial e obtenidas mediante búsqueda en
#   profundidad.
# ---------------------------------------------------------------------

from functools import reduce
from sys import setrecursionlimit
from typing import Callable, Optional, TypeVar

from src.TAD.pila import Pila, apila, cima, desapila, esVacia, vacia

A = TypeVar('A')

setrecursionlimit(10**6)

def buscaProfundidad(sucesores: Callable[[A], list[A]],
                     esFinal: Callable[[A], bool],
                     inicial: A) -> list[A]:
    def aux(p: Pila[A]) -> list[A]:
        if esVacia(p):
            return []
        if esFinal(cima(p)):
            return [cima(p)] + aux(desapila(p))
        return aux(reduce(lambda x, y: apila(y, x),
                          sucesores(cima(p)),
                          desapila(p)))

    return aux(apila(inicial, vacia()))

def buscaProfundidad1(sucesores: Callable[[A], list[A]],
                      esFinal: Callable[[A], bool],
                      inicial: A) -> Optional[A]:
    p: Pila[A] = apila(inicial, vacia())

    while not esVacia(p):
        cp = cima(p)
        if esFinal(cp):
            return cp

        es = sucesores(cp)
        p = reduce(lambda x, y: apila(y, x), es, desapila(p))

    return None
