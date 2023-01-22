# pilaConDeque.py
# Implementación de las pilas mediante deque.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 2-enero-2023
# ======================================================================

# Se define la clase Pila con los siguientes métodos:
#    + apila(x) añade x al principio de la pila.
#    + cima() devuelve la cima de la pila.
#    + desapila() elimina la cima de la pila.
#    + esVacia() se verifica si la pila es vacía.
# Por ejemplo,
#    >>> p = Pila()
#    >>> print(p)
#    -
#    >>> p.apila(5)
#    >>> p.apila(2)
#    >>> p.apila(3)
#    >>> p.apila(4)
#    >>> print(p)
#    4 | 3 | 2 | 5
#    >>> p.cima()
#    4
#    >>> p.desapila()
#    >>> print(p)
#    3 | 2 | 5
#    >>> p.esVacia()
#    False
#    >>> p = Pila()
#    >>> p.esVacia()
#    True
#
# Además se definen las correspondientes funciones. Por ejemplo,
#    >>> print(vacia())
#    -
#    >>> print(apila(4, apila(3, apila(2, apila(5, vacia())))))
#    4 | 3 | 2 | 5
#    >>> print(cima(apila(4, apila(3, apila(2, apila(5, vacia()))))))
#    4
#    >>> print(desapila(apila(4, apila(3, apila(2, apila(5, vacia()))))))
#    3 | 2 | 5
#    >>> print(esVacia(apila(4, apila(3, apila(2, apila(5, vacia()))))))
#    False
#    >>> print(esVacia(vacia()))
#    True
#
# Finalmente, se define un generador aleatorio de pilas y se comprueba
# que las pilas cumplen las propiedades de su especificación.

__all__ = [
    'Pila',
    'vacia',
    'apila',
    'esVacia',
    'cima',
    'desapila',
    'pilaAleatoria'
]

from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from hypothesis import given
from hypothesis import strategies as st

A = TypeVar('A')

# Clase de las pilas mediante Listas
# ==================================

@dataclass
class Pila(Generic[A]):
    _elementos: deque[A] = field(default_factory=deque)

    def __str__(self) -> str:
        """
        Devuelve una cadena con los elementos de la pila separados por " | ".
        Si la pila está vacía, devuelve "-".
        """
        if len(self._elementos) == 0:
            return '-'
        return ' | '.join(str(x) for x in self._elementos)

    def apila(self, x: A) -> None:
        """
        Agrega el elemento x al inicio de la pila.
        """
        self._elementos.appendleft(x)

    def esVacia(self) -> bool:
        """
        Verifica si la pila está vacía.

        Devuelve True si la pila está vacía, False en caso contrario.
        """
        return len(self._elementos) == 0

    def cima(self) -> A:
        """
        Devuelve el elemento en la cima de la pila.
        """
        return self._elementos[0]

    def desapila(self) -> None:
        """
        Elimina el elemento en la cima de la pila.
        """
        self._elementos.popleft()

# Funciones del tipo de las listas
# ================================

def vacia() -> Pila[A]:
    """
    Crea y devuelve una pila vacía de tipo A.
    """
    p: Pila[A] = Pila()
    return p

def apila(x: A, p: Pila[A]) -> Pila[A]:
    """
    Añade un elemento x al tope de la pila p y devuelve una copia de la
    pila modificada.
    """
    _aux = deepcopy(p)
    _aux.apila(x)
    return _aux

def esVacia(p: Pila[A]) -> bool:
    """
    Devuelve True si la pila está vacía, False si no lo está.
    """
    return p.esVacia()

def cima(p: Pila[A]) -> A:
    """
    Devuelve el elemento en la cima de la pila p.
    """
    return p.cima()

def desapila(p: Pila[A]) -> Pila[A]:
    """
    Elimina el elemento en la cima de la pilla p y devuelve una copia de la
    pila resultante.
    """
    _aux = deepcopy(p)
    _aux.desapila()
    return _aux

# Generador de pilas
# ==================

def pilaAleatoria() -> st.SearchStrategy[Pila[int]]:
    """
    Genera una estrategia de búsqueda para generar pilas de enteros de
    forma aleatoria.

    Utiliza la librería Hypothesis para generar una lista de enteros y
    luego se convierte en una instancia de la clase pila.
    """
    def _creaPila(elementos: list[int]) -> Pila[int]:
        pila: Pila[int] = vacia()
        pila._elementos.extendleft(elementos)
        return pila
    return st.builds(_creaPila, st.lists(st.integers()))

# Comprobación de las propiedades de las pilas
# ============================================

# Las propiedades son
@given(p=pilaAleatoria(), x=st.integers())
def test_pila(p: Pila[int], x: int) -> None:
    assert cima(apila(x, p)) == x
    assert desapila(apila(x, p)) == p
    assert esVacia(vacia())
    assert not esVacia(apila(x, p))

# La comprobación es
#    > poetry run pytest -q pilaConQueue.py
#    1 passed in 0.25s
