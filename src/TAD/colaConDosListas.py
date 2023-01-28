# colaConDosListas.py
# Implementación de las colas mediante dos listas.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 2-enero-2023
# ======================================================================

# Se define la clase Cola con los siguientes métodos:
#    + inserta(x) añade x al final de la cola.
#    + primero() es el primero de la cola.
#    + resto() elimina el primero de la cola.
#    + esVacia() se verifica si la cola es vacía.
# Por ejemplo,
#    >>> c = Cola()
#    >>> print(c)
#    -
#    >>> c.inserta(5)
#    >>> c.inserta(2)
#    >>> c.inserta(3)
#    >>> c.inserta(4)
#    >>> print(c)
#    5 | 2 | 3 | 4
#    >>> c.primero()
#    5
#    >>> c.resto()
#    >>> print(c)
#    2 | 3 | 4
#    >>> c.esVacia()
#    False
#    >>> c = Cola()
#    >>> c.esVacia()
#    True
#
# Además se definen las correspondientes funciones. Por ejemplo,
#    >>> print(vacia())
#    -
#    >>> print(inserta(4, inserta(3, inserta(2, inserta(5, vacia())))))
#    5 | 2 | 3 | 4
#    >>> primero(inserta(4, inserta(3, inserta(2, inserta(5, vacia())))))
#    5
#    >>> print(resto(inserta(4, inserta(3, inserta(2, inserta(5, vacia()))))))
#    2 | 3 | 4
#    >>> esVacia(inserta(4, inserta(3, inserta(2, inserta(5, vacia())))))
#    False
#    >>> esVacia(vacia())
#    True
#
# Finalmente, se define un generador aleatorio de colas y se comprueba
# que las colas cumplen las propiedades de su especificación.

__all__ = [
    'Cola',
    'vacia',
    'inserta',
    'primero',
    'resto',
    'esVacia',
    'colaAleatoria'
]

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from hypothesis import assume, given
from hypothesis import strategies as st

A = TypeVar('A')

# Clase de las colas mediante listas
# ==================================

@dataclass
class Cola(Generic[A]):
    _primera: list[A] = field(default_factory=list)
    _segunda: list[A] = field(default_factory=list)

    def _elementos(self) -> list[A]:
        """
        Devuelve una lista con los elementos de la cola en orden.
        """
        return self._primera + self._segunda[::-1]

    def __str__(self) -> str:
        """
        Devuelve una cadena con los elementos de la cola separados por " | ".
        Si la cola está vacía, devuelve "-".
        """
        elementos = self._elementos()
        if not elementos:
            return "-"
        return " | ".join(map(str, elementos))

    def __eq__(self, c: Any) -> bool:
        """
        Comprueba si la cola actual es igual a otra cola.
        Se considera que dos colas son iguales si tienen los mismos
        elementos en el mismo orden.

        Parámetro:
        - c (Cola): La cola con la que se va a comparar.

        Devuelve True si las dos colas son iguales, False en caso
        contrario.
        """
        return self._elementos() == c._elementos()

    def inserta(self, y: A) -> None:
        """
        Inserta el elemento y en la cola.
        """
        xs = self._primera
        ys = self._segunda
        # Si no hay elementos en la primera lista, se inserta en la segunda
        if not xs:
            ys.insert(0, y)
            # Se invierte la segunda lista y se asigna a la primera
            self._primera = ys[::-1]
            self._segunda = []
        else:
            # Si hay elementos en la primera lista, se inserta en la segunda
            ys.insert(0, y)

    def esVacia(self) -> bool:
        """
        Devuelve si la cola está vacía.
        """
        return not self._primera

    def primero(self) -> A:
        """
        Devuelve el primer elemento de la cola.
        """
        return self._primera[0]

    def resto(self) -> None:
        """
        Elimina el primer elemento de la cola.
        """
        xs = self._primera
        ys = self._segunda
        del xs[0]
        if not xs:
            self._primera = ys[::-1]
            self._segunda = []

# Funciones del tipo de las listas
# ================================

def vacia() -> Cola[A]:
    """
    Crea y devuelve una cola vacía de tipo A.
    """
    c: Cola[A] = Cola()
    return c

def inserta(x: A, c: Cola[A]) -> Cola[A]:
    """
    Inserta un elemento x en la cola c y devuelve una nueva cola con
    el elemento insertado.
    """
    _aux = deepcopy(c)
    _aux.inserta(x)
    return _aux

def esVacia(c: Cola[A]) -> bool:
    """
    Devuelve True si la cola está vacía, False si no lo está.
    """
    return c.esVacia()

def primero(c: Cola[A]) -> A:
    """
    Devuelve el primer elemento de la cola c.
    """
    return c.primero()

def resto(c: Cola[A]) -> Cola[A]:
    """
    Elimina el primer elemento de la cola c y devuelve una copia de la
    cola resultante.
    """
    _aux = deepcopy(c)
    _aux.resto()
    return _aux

# Generador de colas
# ==================

def colaAleatoria() -> st.SearchStrategy[Cola[int]]:
    """
    Genera una estrategia de búsqueda para generar colas de enteros de
    forma aleatoria.

    Utiliza la librería Hypothesis para generar una lista de enteros y
    luego se convierte en una instancia de la clase cola.
    """
    return st.lists(st.integers()).map(Cola)

# Comprobación de las propiedades de las colas
# ============================================

# Las propiedades son
@given(c=colaAleatoria(), x=st.integers())
def test_cola1(c: Cola[int], x: int) -> None:
    assert primero(inserta(x, vacia())) == x
    assert resto(inserta(x, vacia())) == vacia()
    assert esVacia(vacia())
    assert not esVacia(inserta(x, c))

@given(c=colaAleatoria(), x=st.integers())
def test_cola2(c: Cola[int], x: int) -> None:
    assume(not esVacia(c))
    assert primero(inserta(x, c)) == primero(c)
    assert resto(inserta(x, c)) == inserta(x, resto(c))

# La comprobación es
#    > poetry run pytest -q colaConListas.py
#    2 passed in 0.40s
