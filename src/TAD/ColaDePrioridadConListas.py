# ColaDePrioridadConListas.py
# El tipo de datos de las colas de prioridad mediante listas.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 5-julio-2023
# ---------------------------------------------------------------------

# Se define la clase CPrioridad con los siguientes métodos:
#    + inserta(x) añade x a la cola.
#    + primero() es el primero de la cola.
#    + resto() elimina el primero de la cola.
#    + esVacia() se verifica si la cola es vacía.
# Por ejemplo,
#    >>> c = CPrioridad()
#    >>> c
#    -
#    >>> c.inserta(5)
#    >>> c.inserta(2)
#    >>> c.inserta(3)
#    >>> c.inserta(4)
#    >>> c
#    2 | 3 | 4 | 5
#    >>> c.primero()
#    2
#    >>> c.resto()
#    >>> c
#    3 | 4 | 5
#    >>> c.esVacia()
#    False
#    >>> c = CPrioridad()
#    >>> c.esVacia()
#    True
#
# Además se definen las correspondientes funciones. Por ejemplo,
#    >>> vacia()
#    -
#    >>> inserta(4, inserta(3, inserta(2, inserta(5, vacia()))))
#    2 | 3 | 4 | 5
#    >>> primero (inserta(4, inserta(3, inserta(2, inserta(5, vacia())))))
#    2
#    >>> resto (inserta(4, inserta(3, inserta(2, inserta(5, vacia())))))
#    3 | 4 | 5
#    >>> esVacia(inserta(4, inserta(3, inserta(2, inserta(5, vacia())))))
#    False
#    >>> esVacia(vacia())
#    True
#
# Finalmente, se define un generador aleatorio de colas de prioridad y
# se comprueba que las colas de prioridad cumplen las propiedades de su
# especificación.

from __future__ import annotations

__all__ = [
   'CPrioridad',
   'vacia',
   'inserta',
   'primero',
   'resto',
   'esVacia',
]

from abc import abstractmethod
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Generic, Protocol, TypeVar

from hypothesis import assume, given
from hypothesis import strategies as st


class Comparable(Protocol):
    @abstractmethod
    def __lt__(self: A, otro: A) -> bool:
        pass

A = TypeVar('A', bound=Comparable)

# Clase de las colas de prioridad mediante listas
# ===============================================

@dataclass
class CPrioridad(Generic[A]):
    _elementos: list[A] = field(default_factory=list)

    def __repr__(self) -> str:
        """
        Devuelve una cadena con los elementos de la cola separados por " | ".
        Si la cola está vacía, devuelve "-".
        """
        if not self._elementos:
            return '-'
        return ' | '.join(str(x) for x in self._elementos)

    def esVacia(self) -> bool:
        """
        Comprueba si la cola está vacía.

        Devuelve True si la cola está vacía, False en caso contrario.
        """
        return not self._elementos

    def inserta(self, x: A) -> None:
        """
        Inserta el elemento x en la cola de prioridad.
        """
        self._elementos.append(x)
        self._elementos.sort()

    def primero(self) -> A:
        """
        Devuelve el primer elemento de la cola.
        """
        return self._elementos[0]

    def resto(self) -> None:
        """
        Elimina el primer elemento de la cola
        """
        self._elementos.pop(0)

# Funciones del tipo de las listas
# ================================

def vacia() -> CPrioridad[A]:
    """
    Crea y devuelve una cola vacía de tipo A.
    """
    c: CPrioridad[A] = CPrioridad()
    return c

def inserta(x: A, c: CPrioridad[A]) -> CPrioridad[A]:
    """
    Inserta un elemento x en la cola c y devuelve una nueva cola con
    el elemento insertado.
    """
    _aux = deepcopy(c)
    _aux.inserta(x)
    return _aux

def esVacia(c: CPrioridad[A]) -> bool:
    """
    Devuelve True si la cola está vacía, False si no lo está.
    """
    return c.esVacia()

def primero(c: CPrioridad[A]) -> A:
    """
    Devuelve el primer elemento de la cola c.
    """
    return c.primero()

def resto(c: CPrioridad[A]) -> CPrioridad[A]:
    """
    Elimina el primer elemento de la cola c y devuelve una copia de la
    cola resultante.
    """
    _aux = deepcopy(c)
    _aux.resto()
    return _aux

# Generador de colas de prioridad
# ===============================

def colaAleatoria() -> st.SearchStrategy[CPrioridad[int]]:
    """
    Genera una estrategia de búsqueda para generar colas de enteros de
    forma aleatoria.

    Utiliza la librería Hypothesis para generar una lista de enteros y
    luego se convierte en una instancia de la clase cola.
    """
    return st.lists(st.integers()).map(CPrioridad)

# Comprobación de las propiedades de las colas
# ============================================

# Las propiedades son
@given(c=colaAleatoria(), x=st.integers(), y=st.integers())
def test_cola1(c: CPrioridad[int], x: int, y: int) -> None:
    assert inserta(x, inserta(y, c)) == inserta(y, inserta(x, c))
    assert primero(inserta(x, vacia())) == x
    assert resto(inserta(x, vacia())) == vacia()
    assert esVacia(vacia())
    assert not esVacia(inserta(x, c))

@given(c=colaAleatoria(), x=st.integers(), y=st.integers())
def test_cola2(c: CPrioridad[int], x: int, y: int) -> None:
    assume(not y < x)
    assert primero(inserta(y, (inserta(x, c)))) == \
        primero(inserta(x,c))
    assert resto(inserta(y, (inserta(x, c)))) == \
        inserta(y, resto(inserta(x, c)))

# La comprobación es
#    > poetry run pytest -q ColaDePrioridadConListas.py
#    2 passed in 0.54s
