# conjuntoConLibreria.py
# Implementación de los conjuntos mediante listas librería.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 28-enero-2023
# ---------------------------------------------------------------------

# Se define la clase Conj con los siguientes métodos:
#    + inserta(x) añade x al conjunto.
#    + menor() es el menor elemento del conjunto.
#    + elimina(x) elimina las ocurrencias de x en el conjunto.
#    + pertenece(x) se verifica si x pertenece al conjunto.
#    + esVacia() se verifica si la cola es vacía.
# Por ejemplo,
#    >>> c = Conj()
#    >>> c
#    {}
#    >>> c.inserta(5)
#    >>> c.inserta(2)
#    >>> c.inserta(3)
#    >>> c.inserta(4)
#    >>> c.inserta(5)
#    >>> c
#    {2, 3, 4, 5}
#    >>> c.menor()
#    2
#    >>> c.elimina(3)
#    >>> c
#    {2, 4, 5}
#    >>> c.pertenece(4)
#    True
#    >>> c.pertenece(3)
#    False
#    >>> c.esVacio()
#    False
#    >>> c = Conj()
#    >>> c.esVacio()
#    True
#    >>> c = Conj()
#    >>> c.inserta(2)
#    >>> c.inserta(5)
#    >>> d = Conj()
#    >>> d.inserta(5)
#    >>> d.inserta(2)
#    >>> d.inserta(5)
#    >>> c == d
#    True
#
# Además se definen las correspondientes funciones. Por ejemplo,
#    >>> vacio()
#    {}
#    >>> inserta(5, inserta(3, inserta(2, inserta(5, vacio()))))
#    {2, 3, 5}
#    >>> menor(inserta(5, inserta(3, inserta(2, inserta(5, vacio())))))
#    2
#    >>> elimina(5, inserta(5, inserta(3, inserta(2, inserta(5, vacio())))))
#    {2, 3}
#    >>> pertenece(5, inserta(5, inserta(3, inserta(2, inserta(5, vacio())))))
#    True
#    >>> pertenece(1, inserta(5, inserta(3, inserta(2, inserta(5, vacio())))))
#    False
#    >>> esVacio(inserta(5, inserta(3, inserta(2, inserta(5, vacio())))))
#    False
#    >>> esVacio(vacio())
#    True
#    >>> inserta(5, inserta(2, vacio())) == inserta(2, inserta(5, (inserta(2, vacio()))))
#    True
#
# Finalmente, se define un generador aleatorio de conjuntos y se
# comprueba que los conjuntos cumplen las propiedades de su
# especificación.

from __future__ import annotations

__all__ = [
    'Conj',
    'vacio',
    'inserta',
    'menor',
    'elimina',
    'pertenece',
    'esVacio',
    'conjuntoAleatorio'
]

from abc import abstractmethod
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Generic, Protocol, TypeVar

from hypothesis import given
from hypothesis import strategies as st


class Comparable(Protocol):
    @abstractmethod
    def __lt__(self: A, otro: A) -> bool:
        pass

A = TypeVar('A', bound=Comparable)

# Clase de los conjuntos mediante librería
# ========================================

@dataclass
class Conj(Generic[A]):
    _elementos: set[A] = field(default_factory=set)

    def __repr__(self) -> str:
        xs = [str(x) for x in self._elementos]
        return "{" + ", ".join(xs) + "}"

    def inserta(self, x: A) -> None:
        """
        Añade el elemento x al conjunto.
        """
        self._elementos.add(x)

    def menor(self) -> A:
        """
        Devuelve el menor elemento del conjunto
        """
        return min(self._elementos)

    def elimina(self, x: A) -> None:
        """
        Elimina el elemento x del conjunto.
        """
        self._elementos.discard(x)

    def esVacio(self) -> bool:
        """
        Se verifica si el conjunto está vacío.
        """
        return not self._elementos

    def pertenece(self, x: A) -> bool:
        """
        Se verifica si x pertenece al conjunto.
        """
        return x in self._elementos

# Funciones del tipo conjunto
# ===========================

def vacio() -> Conj[A]:
    """
    Crea y devuelve un conjunto vacío de tipo A.
    """
    c: Conj[A] = Conj()
    return c

def inserta(x: A, c: Conj[A]) -> Conj[A]:
    """
    Inserta un elemento x en el conjunto c y devuelve un nuevo comjunto
    con el elemento insertado.
    """
    _aux = deepcopy(c)
    _aux.inserta(x)
    return _aux

def menor(c: Conj[A]) -> A:
    """
    Devuelve el menor elemento del conjunto c.
    """
    return c.menor()

def elimina(x: A, c: Conj[A]) -> Conj[A]:
    """
    Elimina las ocurrencias de c en c y devuelve una copia del conjunto
    resultante.
    """
    _aux = deepcopy(c)
    _aux.elimina(x)
    return _aux

def pertenece(x: A, c: Conj[A]) -> bool:
    """
    Se verifica si x pertenece a c.
    """
    return c.pertenece(x)

def esVacio(c: Conj[A]) -> bool:
    """
    Se verifica si el conjunto está vacío.
    """
    return c.esVacio()

# Generador de conjuntos
# ======================

def conjuntoAleatorio() -> st.SearchStrategy[Conj[int]]:
    """
    Estrategia de búsqueda para generar conjuntos de enteros de forma
    aleatoria.
    """
    return st.builds(Conj, st.lists(st.integers()).map(set))

# Comprobación de las propiedades de los conjuntos
# ================================================

# Las propiedades son
@given(c=conjuntoAleatorio(), x=st.integers(), y=st.integers())
def test_conjuntos(c: Conj[int], x: int, y: int) -> None:
    assert inserta(x, inserta(x, c)) == inserta(x, c)
    assert inserta(x, inserta(y, c)) == inserta(y, inserta(x, c))
    v: Conj[int] = vacio()
    assert not pertenece(x, v)
    assert pertenece(y, inserta(x, c)) == (x == y) or pertenece(y, c)
    assert elimina(x, v) == v

    def relacion(x: int, y: int, c: Conj[int]) -> Conj[int]:
        if x == y:
            return elimina(x, c)
        return inserta(y, elimina(x, c))

    assert elimina(x, inserta(y, c)) == relacion(x, y, c)
    assert esVacio(vacio())
    assert not esVacio(inserta(x, c))

# La comprobación es
#    > poetry run pytest -q conjuntoConLibreria.py
#    1 passed in 0.22s
