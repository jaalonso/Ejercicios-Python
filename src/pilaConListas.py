# pilaConListas.py
# Implementación de las pilas mediante listas.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 20-enero-2023
# ======================================================================

# ---------------------------------------------------------------------
# Una pila es una estructura de datos, caracterizada por ser una
# secuencia de elementos en la que las operaciones de inserción y
# extracción se realizan por el mismo extremo.
#
# Las operaciones que definen a tipo de las pilas (cuyos elementos son
# del tipo a) son las siguientes:
#    vacia    : () -> Pila[A]
#    apila    : (A, Pila[A]) -> Pila[A]
#    cima     : (Pila[A] -> A
#    desapila : (Pila[A] -> Pila[A]
#    esVacia  : (Pila[A] -> bool
# tales que
# + vacia() es la pila vacía.
# + apila(x, p) es la pila obtenida añadiendo x al principio de p.
# + cima(p) es la cima de la pila p.
# + desapila(p) es la pila obtenida suprimiendo la cima de p.
# + esVacia(p) se verifica si p es la pila vacía.
# Por ejemplo,
#    >>> print(vacia())
#    -
#    >>> print(apila(4, apila(3, apila(2, apila(5, vacia())))))
#    4 | 3 | 2 | 5
#    >>> cima(apila(4, apila(3, apila(2, apila(5, vacia())))))
#    4
#    >>> print(desapila(apila(4, apila(3, apila(2, apila(5, vacia()))))))
#    3 | 2 | 5
#    >>> esVacia(apila(4, apila(3, apila(2, apila(5, vacia())))))
#    False
#    >>> esVacia(vacia())
#    True
# Además de las funciones sobre pilas se definirán los métodos sobre
# pilas. Por ejemplo,
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
# Las operaciones tienen que verificar las siguientes propiedades:
# + cima(apila(x, p) == x
# + desapila(apila(x, p)) == p
# + esVacia(vacia)
# + not esVacia(apila(x, p))
#
# El esquema de la definición del tipo de las pilas representadas
# mediante listas es el siguiente:
#    from dataclasses import dataclass, field
#    from copy import deepcopy
#    from typing import Generic, TypeVar
#    from hypothesis import given
#    from hypothesis import strategies as st
#    A = TypeVar('A')
#
#    @dataclass
#    class Pila(Generic[A]):
#        _elementos: list[A] = field(default_factory=list)
#
#        def __str__(self) -> str:
#            if len(self._elementos) == 0:
#                return '-'
#            cadena = ''
#            for x in self._elementos[:-1]:
#                cadena = cadena + str(x) + ' | '
#            return cadena + str(self._elementos[-1])
#
#        def apila(self, x: A) -> None:
#            pass
#
#        def esVacia(self) -> bool:
#            pass
#
#        def cima(self) -> A:
#            pass
#
#        def desapila(self) -> None:
#            pass
#
#    def vacia() -> Pila[A]:
#        pass
#
#    def apila(x: A, p: Pila[A]) -> Pila[A]:
#        pass
#
#    def esVacia(p: Pila[A]) -> bool:
#        pass
#
#    def cima(p: Pila[A]) -> A:
#        pass
#
#    def desapila(p: Pila[A]) -> Pila[A]:
#        pass
#
#    def pilaAleatoria() -> st.SearchStrategy[Pila[int]]:
#        def _build_pila(elementos: list[int]) -> Pila[int]:
#            pila: Pila[int] = vacia()
#            for x in elementos:
#                pila = apila(x, pila)
#            return pila
#        return st.builds(_build_pila, st.lists(st.integers()))
#
#    @given(p=pilaAleatoria(), x=st.integers())
#    def test_pila(p: Pila[int], x: int) -> None:
#        pass
#
# Completar el código anterior definiendo
# + Los métodos de la clase Pila; es decir, apila, esVacia, cima y apila.
# + Las funciones sobre pila: vacia, apila, esVacia, cima y apila.
# + La función test_pila para comprobar las propiedades de las pilas.
# ---------------------------------------------------------------------

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
    _elementos: list[A] = field(default_factory=list)

    def __str__(self) -> str:
        if len(self._elementos) == 0:
            return '-'
        cadena = ''
        for x in self._elementos[:-1]:
            cadena = cadena + str(x) + ' | '
        return cadena + str(self._elementos[-1])

    def apila(self, x: A) -> None:
        self._elementos.insert(0, x)

    def esVacia(self) -> bool:
        return len(self._elementos) == 0

    def cima(self) -> A:
        return self._elementos[0]

    def desapila(self) -> None:
        self._elementos.pop(0)

# Funciones del tipo de las listas
# ================================

def vacia() -> Pila[A]:
    p: Pila[A] = Pila()
    return p

def apila(x: A, p: Pila[A]) -> Pila[A]:
    aux = deepcopy(p)
    aux.apila(x)
    return aux

def esVacia(p: Pila[A]) -> bool:
    return p.esVacia()

def cima(p: Pila[A]) -> A:
    return p.cima()

def desapila(p: Pila[A]) -> Pila[A]:
    aux = deepcopy(p)
    aux.desapila()
    return aux

# Generador de pilas
# ==================

def pilaAleatoria() -> st.SearchStrategy[Pila[int]]:
    def _build_pila(elementos: list[int]) -> Pila[int]:
        pila: Pila[int] = vacia()
        for x in elementos:
            pila = apila(x, pila)
        return pila
    return st.builds(_build_pila, st.lists(st.integers()))

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
#    > poetry run pytest -q pilaConListas.py
#    1 passed in 0.25s
