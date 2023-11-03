# BusquedaPrimeroElMejor.py
# Búsqueda por primero el mejor.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 6-julio-2023
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# En la búsqueda por primero el mejos se supone que los estados están
# ordenados mediante una función, la heurística, que es una rstimación
# de su coste para llegar a un estado final.
#
# Definir la función
#    buscaPM : (Callable[[A], list[A]], Callable[[A], bool], A) -> Optional[A]
# tal que buscaPM(s, o, e) es la primera de las soluciones del problema de
# espacio de estado definido por la función sucesores s, el objetivo
# o y estado inicial e, obtenidas buscando por primero el mejor.
# ---------------------------------------------------------------------

from __future__ import annotations

from abc import abstractmethod
from functools import reduce
from typing import Callable, Optional, Protocol, TypeVar

from src.TAD.ColaDePrioridad import (CPrioridad, esVacia, inserta, primero,
                                     resto, vacia)


class Comparable(Protocol):
    @abstractmethod
    def __lt__(self: A, otro: A) -> bool:
        pass

A = TypeVar('A', bound=Comparable)

def buscaPM(sucesores: Callable[[A], list[A]],
            esFinal: Callable[[A], bool],
            inicial: A) -> Optional[A]:
    c: CPrioridad[A] = inserta(inicial, vacia())

    while not esVacia(c):
        if esFinal(primero(c)):
            return primero(c)

        es = sucesores(primero(c))
        c = reduce(lambda x, y: inserta(y, x), es, resto(c))

    return None
