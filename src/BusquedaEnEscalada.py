# BusquedaEnEscalada.py
# Búsqueda en escalada.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 4-agosto-2023
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# En la búsqueda en escalada se supone que los estados están ordenados
# mediante una función, la heurística, que es una estimación de su
# coste para llegar a un estado final.
#
# Definir la función
#    buscaEscalada(Callable[[A], list[A]], Callable[[A], bool], A) -> list[A]
# tal que buscaEscalada(s, o, e) es la lista de soluciones del problema de
# espacio de estado definido por la función sucesores s, el objetivo
# o y estado inicial e, obtenidas buscando en escalada.
# ---------------------------------------------------------------------

from __future__ import annotations

from abc import abstractmethod
from functools import reduce
from typing import Callable, Optional, Protocol, TypeVar

from src.TAD.ColaDePrioridad import (CPrioridad, esVacia, inserta, primero,
                                     vacia)


class Comparable(Protocol):
    @abstractmethod
    def __lt__(self: A, otro: A) -> bool:
        pass

A = TypeVar('A', bound=Comparable)

def buscaEscalada(sucesores: Callable[[A], list[A]],
                  esFinal: Callable[[A], bool],
                  inicial: A) -> Optional[A]:
    c: CPrioridad[A] = inserta(inicial, vacia())

    while not esVacia(c):
        x = primero(c)
        if esFinal(x):
            return x

        c = reduce(lambda x, y: inserta(y, x), sucesores(x), vacia())

    return None
