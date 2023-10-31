# PolRepDispersa.hs
# Implementación de polinomios mediante listas dispersas.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 17-abril-2023
# ---------------------------------------------------------------------

# Representaremos un polinomio mediante una lista de pares (grado,coef),
# ordenados en orden decreciente según el grado. Por ejemplo, el
# polinomio
#    6x^4 -5x^2 + 4x -7
# se representa por
#    [(4,6),(2,-5),(1,4),(0,-7)].
#
# En la representación se supone que los primeros elementos de los
# pares forman una sucesión estrictamente decreciente y que los
# segundos elementos son distintos de cero.
#
# Se define la clase Polinomio con los siguientes métodos:
#    + esPolCero() se verifica si es el polinomio cero.
#    + consPol(n, b) es el polinomio obtenido añadiendo el térmiono bx^n
#    + grado() es el grado del polinomio.
#    + coefLider() es el coeficiente líder del polinomio.
#    + restoPol() es el resto del polinomio.
# Por ejemplo,
#    >>> Polinomio()
#    0
#    >>> ejPol1 = Polinomio().consPol(0,3).consPol(2,-5).consPol(4,3)
#    >>> ejPol1
#    3*x^4 + -5*x^2 + 3
#    >>> ejPol2 = Polinomio().consPol(1,4).consPol(2,5).consPol(5,1)
#    >>> ejPol2
#    x^5 + 5*x^2 + 4*x
#    >>> ejPol3 = Polinomio().consPol(1,2).consPol(4,6)
#    >>> ejPol3
#    6*x^4 + 2*x
#    >>> Polinomio().esPolCero()
#    True
#    >>> ejPol1.esPolCero()
#    False
#    >>> ejPol2
#    x^5 + 5*x^2 + 4*x
#    >>> ejPol2.consPol(3,0)
#    x^5 + 5*x^2 + 4*x
#    >>> Polinomio().consPol(3,2)
#    2*x^3
#    >>> ejPol2.consPol(6,7)
#    7*x^6 + x^5 + 5*x^2 + 4*x
#    >>> ejPol2.consPol(4,7)
#    x^5 + 7*x^4 + 5*x^2 + 4*x
#    >>> ejPol2.consPol(5,7)
#    8*x^5 + 5*x^2 + 4*x
#    >>> ejPol3
#    6*x^4 + 2*x
#    >>> ejPol3.grado()
#    4
#    >>> ejPol3.restoPol()
#    2*x
#    >>> ejPol2
#    x^5 + 5*x^2 + 4*x
#    >>> ejPol2.restoPol()
#    5*x^2 + 4*x
#
# Además se definen las correspondientes funciones. Por ejemplo,
#    >>> polCero()
#    0
#    >>> ejPol1a = consPol(4,3,consPol(2,-5,consPol(0,3,polCero())))
#    >>> ejPol1a
#    3*x^4 + -5*x^2 + 3
#    >>> ejPol2a = consPol(5,1,consPol(2,5,consPol(1,4,polCero())))
#    >>> ejPol2a
#    x^5 + 5*x^2 + 4*x
#    >>> ejPol3a = consPol(4,6,consPol(1,2,polCero()))
#    >>> ejPol3a
#    6*x^4 + 2*x
#    >>> esPolCero(polCero())
#    True
#    >>> esPolCero(ejPol1a)
#    False
#    >>> ejPol2a
#    x^5 + 5*x^2 + 4*x
#    >>> consPol(3,9,ejPol2a)
#    x^5 + 9*x^3 + 5*x^2 + 4*x
#    >>> consPol(3,2,polCero())
#    2*x^3
#    >>> consPol(6,7,ejPol2a)
#    7*x^6 + x^5 + 5*x^2 + 4*x
#    >>> consPol(4,7,ejPol2a)
#    x^5 + 7*x^4 + 5*x^2 + 4*x
#    >>> consPol(5,7,ejPol2a)
#    8*x^5 + 5*x^2 + 4*x
#    >>> ejPol3a
#    6*x^4 + 2*x
#    >>> grado(ejPol3a)
#    4
#    >>> restoPol(ejPol3a)
#    2*x
#    >>> ejPol2a
#    x^5 + 5*x^2 + 4*x
#    >>> restoPol(ejPol2a)
#    5*x^2 + 4*x
#
# Finalmente, se define un generador aleatorio de polinomios y se
# comprueba que los polinomios cumplen las propiedades de su
# especificación.

from __future__ import annotations

__all__ = [
    'Polinomio',
    'polCero',
    'esPolCero',
    'consPol',
    'grado',
    'coefLider',
    'restoPol',
    'polinomioAleatorio'
]

from dataclasses import dataclass, field
from typing import Generic, TypeVar

from hypothesis import assume, given
from hypothesis import strategies as st

A = TypeVar('A', int, float, complex)

# Clase de los polinomios mediante listas densas
# ==============================================

@dataclass
class Polinomio(Generic[A]):
    _terminos: list[tuple[int, A]] = field(default_factory=list)

    def esPolCero(self) -> bool:
        return not self._terminos

    def grado(self) -> int:
        if self.esPolCero():
            return 0
        return self._terminos[0][0]

    def coefLider(self) -> A:
        if self.esPolCero():
            return 0
        return self._terminos[0][1]

    def restoPol(self) -> Polinomio[A]:
        xs = self._terminos
        if len(xs) <= 1:
            return Polinomio([])
        return Polinomio(xs[1:])

    def consPol(self, n: int, b: A) -> Polinomio[A]:
        m = self.grado()
        c = self.coefLider()
        xs = self._terminos
        if b == 0:
            return self
        if self.esPolCero():
            return Polinomio([(n, b)])
        if n > m:
            return Polinomio([(n, b)] + xs)
        if n < m:
            return Polinomio(xs[1:]).consPol(n, b).consPol(m, c)
        if b + c == 0:
            return Polinomio(xs[1:])
        return Polinomio([(n, b + c)] + xs[1:])

    def __repr__(self) -> str:
        n = self.grado()
        a = self.coefLider()
        p = self.restoPol()
        if self.esPolCero():
            return "0"
        if n == 0 and p.esPolCero():
            return str(a)
        if n == 0:
            return str(a) + " + " + str(p)
        if n == 1 and p.esPolCero():
            return str(a) + "*x"
        if n == 1:
            return str(a) + "*x + " + str(p)
        if a == 1 and p.esPolCero():
            return "x^" + str(n)
        if p.esPolCero():
            return str(a) + "*x^" + str(n)
        if a == 1:
            return "x^" + str(n) + " + " + str(p)
        return str(a) + "*x^" + str(n) + " + " + str(p)

# Funciones del tipo polinomio
# ============================

def polCero() -> Polinomio[A]:
    return Polinomio([])

def esPolCero(p: Polinomio[A]) -> bool:
    return p.esPolCero()

def grado(p: Polinomio[A]) -> int:
    return p.grado()

def coefLider(p: Polinomio[A]) -> A:
    return p.coefLider()

def restoPol(p: Polinomio[A]) -> Polinomio[A]:
    return p.restoPol()

def consPol(n: int, b: A, p: Polinomio[A]) -> Polinomio[A]:
    return p.consPol(n, b)

# Generador de polinomios
# =======================

# normal(ps) es la representación dispersa de un polinomio.
def normal(ps: list[tuple[int, A]]) -> list[tuple[int, A]]:
    xs = sorted(list({p[0] for p in ps}), reverse=True)
    ys = [p[1] for p in ps]
    return [(x, y) for (x, y) in zip(xs, ys) if y != 0]

# polinomioAleatorio() genera polinomios aleatorios. Por ejemplo,
#    >>> polinomioAleatorio().example()
#    -4*x^8 + -5*x^7 + -4*x^6 + -4*x^5 + -8*x^3
#    >>> polinomioAleatorio().example()
#    -7*x^9 + -8*x^6 + -8*x^3 + 2*x^2 + -1*x + 4
def polinomioAleatorio() -> st.SearchStrategy[Polinomio[int]]:
    return st.lists(st.tuples(st.integers(min_value=0, max_value=9),
                              st.integers(min_value=-9, max_value=9)))\
             .map(lambda ps: normal(ps))\
             .map(Polinomio)

# Comprobación de las propiedades de los polinomios
# =================================================

# Las propiedades son
def test_esPolCero1() -> None:
    assert esPolCero(polCero())

@given(p=polinomioAleatorio(),
       n=st.integers(min_value=0, max_value=10),
       b=st.integers())
def test_esPolCero2(p: Polinomio[int], n: int, b: int) -> None:
    assume(n > grado(p) and b != 0)
    assert not esPolCero(consPol(n, b, p))

@given(p=polinomioAleatorio())
def test_consPol(p: Polinomio[int]) -> None:
    assume(not esPolCero(p))
    assert consPol(grado(p), coefLider(p), restoPol(p)) == p

@given(p=polinomioAleatorio(),
       n=st.integers(min_value=0, max_value=10),
       b=st.integers())
def test_grado(p: Polinomio[int], n: int, b: int) -> None:
    assume(n > grado(p) and b != 0)
    assert grado(consPol(n, b, p)) == n

@given(p=polinomioAleatorio(),
       n=st.integers(min_value=0, max_value=10),
       b=st.integers())
def test_coefLider(p: Polinomio[int], n: int, b: int) -> None:
    assume(n > grado(p) and b != 0)
    assert coefLider(consPol(n, b, p)) == b

@given(p=polinomioAleatorio(),
       n=st.integers(min_value=0, max_value=10),
       b=st.integers())
def test_restoPol(p: Polinomio[int], n: int, b: int) -> None:
    assume(n > grado(p) and b != 0)
    assert restoPol(consPol(n, b, p)) == p

# La comprobación es
#    > poetry run pytest -v PolRepDispersa.py
#
#    PolRepDispersa.py::test_esPolCero1 PASSED
#    PolRepDispersa.py::test_esPolCero2 PASSED
#    PolRepDispersa.py::test_consPol PASSED
#    PolRepDispersa.py::test_grado PASSED
#    PolRepDispersa.py::test_coefLider PASSED
#    PolRepDispersa.py::test_restoPol PASSED
#
#    === 6 passed in 1.74s ===
