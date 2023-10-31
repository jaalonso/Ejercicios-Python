# El_TAD_de_polinomios_operaciones.py
# Operaciones con el tipo abstracto de datos de los polinomios.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 31-octubre-2023
# ======================================================================

# ---------------------------------------------------------------------
# Introducción                                                       --
# ---------------------------------------------------------------------

# El objetivo de esta relación es ampliar el conjunto de operaciones
# sobre polinomios definidas utilizando las implementaciones de los
# ejercicios anteriores-

# ---------------------------------------------------------------------
# Importación de librerías                                           --
# ---------------------------------------------------------------------

from functools import reduce
from itertools import dropwhile
from sys import setrecursionlimit
from typing import TypeVar

from hypothesis import given
from hypothesis import strategies as st

from src.TAD.Polinomio import (Polinomio, coefLider, consPol, esPolCero, grado,
                               polCero, polinomioAleatorio, restoPol)

setrecursionlimit(10**6)

A = TypeVar('A', int, float, complex)

# ---------------------------------------------------------------------
# Ejercicio 1. Definir la función
#    densaAdispersa : (list[A]) -> list[tuple[int, A]]
# tal que densaAdispersa(xs) es la representación dispersa del polinomio
# cuya representación densa es xs. Por ejemplo,
#    >>> densaAdispersa([9, 0, 0, 5, 0, 4, 7])
#    [(6, 9), (3, 5), (1, 4), (0, 7)]
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def densaAdispersa(xs: list[A]) -> list[tuple[int, A]]:
    n = len(xs)
    return [(m, a) for (m, a) in zip(range(n-1, -1, -1),  xs) if a != 0]

# 2ª solución
# ===========

def densaAdispersa2(xs: list[A]) -> list[tuple[int, A]]:
    def aux(xs: list[A], n: int) -> list[tuple[int, A]]:
        if not xs:
            return []
        if xs[0] == 0:
            return aux(xs[1:], n + 1)
        return [(n, xs[0])] + aux(xs[1:], n + 1)

    return list(reversed(aux(list(reversed(xs)), 0)))

# 3ª solución
# ===========

def densaAdispersa3(xs: list[A]) -> list[tuple[int, A]]:
    r = []
    n = len(xs) - 1
    for x in xs:
        if x != 0:
            r.append((n, x))
        n -= 1
    return r

# Comprobación de equivalencia
# ============================

# normalDensa(ps) es la representación dispersa de un polinomio.
def normalDensa(xs: list[A]) -> list[A]:
    return list(dropwhile(lambda x: x == 0, xs))

# densaAleatoria() genera representaciones densas de polinomios
# aleatorios. Por ejemplo,
#    >>> densaAleatoria().example()
#    [-5, 9, -6, -5, 7, -5, -1, 9]
#    >>> densaAleatoria().example()
#    [-4, 9, -3, -3, -5, 0, 6, -8, 8, 6, 0, -9]
#    >>> densaAleatoria().example()
#    [-3, -1, 2, 0, -9]
def densaAleatoria() -> st.SearchStrategy[list[int]]:
    return st.lists(st.integers(min_value=-9, max_value=9))\
             .map(normalDensa)

# La propiedad es
@given(xs=densaAleatoria())
def test_densaADispersa(xs: list[int]) -> None:
    r = densaAdispersa(xs)
    assert densaAdispersa2(xs) == r
    assert densaAdispersa3(xs) == r

# La comprobación es
#    >>> test_densaADispersa()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 2. Definir la función
#    dispersaAdensa : (list[tuple[int, A]]) -> list[A]
# tal que dispersaAdensa(ps) es la representación densa del polinomio
# cuya representación dispersa es ps. Por ejemplo,
#    >>> dispersaAdensa([(6,9),(3,5),(1,4),(0,7)])
#    [9, 0, 0, 5, 0, 4, 7]
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def dispersaAdensa(ps: list[tuple[int, A]]) -> list[A]:
    if not ps:
        return []
    if len(ps) == 1:
        return [ps[0][1]] + [0] * ps[0][0]
    (n, a) = ps[0]
    (m, _) = ps[1]
    return [a] + [0] * (n-m-1) + dispersaAdensa(ps[1:])

# 2ª solución
# ===========

# coeficienteDensa(ps, n) es el coeficiente del término de grado n en el
# polinomio cuya representación densa es ps. Por ejemplo,
#    coeficienteDensa([(6, 9), (3, 5), (1, 4), (0, 7)], 3)  ==  5
#    coeficienteDensa([(6, 9), (3, 5), (1, 4), (0, 7)], 4)  ==  0
def coeficienteDensa(ps: list[tuple[int, A]], n: int) -> A:
    if not ps:
        return 0
    (m, a) = ps[0]
    if n > m:
        return 0
    if n == m:
        return a
    return coeficienteDensa(ps[1:], n)

def dispersaAdensa2(ps: list[tuple[int, A]]) -> list[A]:
    if not ps:
        return []
    n = ps[0][0]
    return [coeficienteDensa(ps, m) for m in range(n, -1, -1)]

# 3ª solución
# ===========

def dispersaAdensa3(ps: list[tuple[int, A]]) -> list[A]:
    if not ps:
        return []
    n = ps[0][0]
    r: list[A] = [0] * (n + 1)
    for (m, a) in ps:
        r[n-m] = a
    return r

# Comprobación de equivalencia
# ============================

# normalDispersa(ps) es la representación dispersa de un polinomio.
def normalDispersa(ps: list[tuple[int, A]]) -> list[tuple[int, A]]:
    xs = sorted(list({p[0] for p in ps}), reverse=True)
    ys = [p[1] for p in ps]
    return [(x, y) for (x, y) in zip(xs, ys) if y != 0]

# dispersaAleatoria() genera representaciones densas de polinomios
# aleatorios. Por ejemplo,
#    >>> dispersaAleatoria().example()
#    [(5, -6), (2, -1), (0, 2)]
#    >>> dispersaAleatoria().example()
#    [(6, -7)]
#    >>> dispersaAleatoria().example()
#    [(7, 2), (4, 9), (3, 3), (0, -2)]
def dispersaAleatoria() -> st.SearchStrategy[list[tuple[int, int]]]:
    return st.lists(st.tuples(st.integers(min_value=0, max_value=9),
                              st.integers(min_value=-9, max_value=9)))\
             .map(normalDispersa)

# La propiedad es
@given(ps=dispersaAleatoria())
def test_dispersaAdensa(ps: list[tuple[int, int]]) -> None:
    r = dispersaAdensa(ps)
    assert dispersaAdensa2(ps) == r
    assert dispersaAdensa3(ps) == r

# La comprobación es
#    >>> test_dispersaAdensa()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 3. Comprobar con Hypothesis que las funciones densaAdispersa
# y dispersaAdensa son inversas.
# ---------------------------------------------------------------------

# La primera propiedad es
@given(xs=densaAleatoria())
def test_dispersaAdensa_densaAdispersa(xs: list[int]) -> None:
    assert dispersaAdensa(densaAdispersa(xs)) == xs

# La comprobación es
#    >>> test_dispersaAdensa_densaAdispersa()
#    >>>

# La segunda propiedad es
@given(ps=dispersaAleatoria())
def test_densaAdispersa_dispersaAdensa(ps: list[tuple[int, int]]) -> None:
    assert densaAdispersa(dispersaAdensa(ps)) == ps

# La comprobación es
#    >>> test_densaAdispersa_dispersaAdensa()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    dispersaApolinomio : (list[tuple[int, A]]) -> Polinomio[A]
# tal que dispersaApolinomio(ps) es el polinomiocuya representación
# dispersa es ps. Por ejemplo,
#    >>> dispersaApolinomio([(6, 9), (3, 5), (1, 4), (0, 7)])
#    9*x^6 + 5*x^3 + 4*x + 7
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def dispersaApolinomio(ps: list[tuple[int, A]]) -> Polinomio[A]:
    if not ps:
        return polCero()
    (n, a) = ps[0]
    return consPol(n, a, dispersaApolinomio(ps[1:]))

# 2ª solución
# ===========

def dispersaApolinomio2(ps: list[tuple[int, A]]) -> Polinomio[A]:
    r: Polinomio[A] = polCero()
    for (n, a) in reversed(ps):
        r = consPol(n, a, r)
    return r

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(ps=dispersaAleatoria())
def test_dispersaApolinomio(ps: list[tuple[int, int]]) -> None:
    assert dispersaApolinomio(ps) == dispersaApolinomio2(ps)

# La comprobación es
#    >>> test_dispersaApolinomio()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 5. Definir la función
#    polinomioAdispersa : (Polinomio[A]) -> list[tuple[int, A]]
# tal polinomioAdispersa(p) es la representación dispersa del polinomio
# p. Por ejemplo,
#    >>> ejPol1 = consPol(3, 5, consPol(1, 4, consPol(0, 7, polCero())))
#    >>> ejPol = consPol(6, 9, ejPol1)
#    >>> ejPol
#    9*x^6 + 5*x^3 + 4*x + 7
#    >>> polinomioAdispersa(ejPol)
#    [(6, 9), (3, 5), (1, 4), (0, 7)]
# ---------------------------------------------------------------------

def polinomioAdispersa(p: Polinomio[A]) -> list[tuple[int, A]]:
    if esPolCero(p):
        return []
    return [(grado(p), coefLider(p))] + polinomioAdispersa(restoPol(p))

# ---------------------------------------------------------------------
# Ejercicio 6. Comprobar con Hypothesis que ambas funciones son
# inversas.
# ---------------------------------------------------------------------

# La primera propiedad es
@given(ps=dispersaAleatoria())
def test_polinomioAdispersa_dispersaApolinomio(ps: list[tuple[int,
                                                              int]]) -> None:
    assert polinomioAdispersa(dispersaApolinomio(ps)) == ps

# La comprobación es
#    >>> test_polinomioAdispersa_dispersaApolinomio()
#    >>>

# La segunda propiedad es
@given(p=polinomioAleatorio())
def test_dispersaApolinomio_polinomioAdispersa(p: Polinomio[int]) -> None:
    assert dispersaApolinomio(polinomioAdispersa(p)) == p

# La comprobación es
#    >>> test_dispersaApolinomio_polinomioAdispersa()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 7. Definir la función
#    coeficiente : (int, Polinomio[A]) -> A
# tal que coeficiente(k, p) es el coeficiente del término de grado k
# del polinomio p. Por ejemplo,
#    >>> ejPol = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
#    >>> ejPol
#    x^5 + 5*x^2 + 4*x
#    >>> coeficiente(2, ejPol)
#    5
#    >>> coeficiente(3, ejPol)
#    0
# ---------------------------------------------------------------------

def coeficiente(k: int, p: Polinomio[A]) -> A:
    if k == grado(p):
        return coefLider(p)
    if k > grado(restoPol(p)):
        return 0
    return coeficiente(k, restoPol(p))

# ---------------------------------------------------------------------
# Ejercicio 8. Definir la función
#    densaApolinomio : (list[A]) -> Polinomio[A]
# tal que densaApolinomio(xs) es el polinomio cuya representación densa es
# xs. Por ejemplo,
#    >>> densaApolinomio([9, 0, 0, 5, 0, 4, 7])
#    9*x^6 + 5*x^3 + 4*x + 7
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def densaApolinomio(xs: list[A]) -> Polinomio[A]:
    if not xs:
        return polCero()
    return consPol(len(xs[1:]), xs[0], densaApolinomio(xs[1:]))

# 2ª solución
# ===========

def densaApolinomio2(xs: list[A]) -> Polinomio[A]:
    return dispersaApolinomio(densaAdispersa(xs))

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(xs=densaAleatoria())
def test_densaApolinomio(xs: list[int]) -> None:
    assert densaApolinomio(xs) == densaApolinomio2(xs)

# La comprobación es
#    >>> test_densaApolinomio()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 9. Definir la función
#    polinomioAdensa : (Polinomio[A]) -> list[A]
# tal que polinomioAdensa(c) es la representación densa del polinomio
# p. Por ejemplo,
#    >>> ejPol = consPol(6, 9, consPol(3, 5, consPol(1, 4, consPol(0, 7, polCero()))))
#    >>> ejPol
#    9*x^6 + 5*x^3 + 4*x + 7
#    >>> polinomioAdensa(ejPol)
#    [9, 0, 0, 5, 0, 4, 7]
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def polinomioAdensa(p: Polinomio[A]) -> list[A]:
    if esPolCero(p):
        return []
    n = grado(p)
    return [coeficiente(k, p) for k in range(n, -1, -1)]

# 2ª solución
# ===========

def polinomioAdensa2(p: Polinomio[A]) -> list[A]:
    return dispersaAdensa(polinomioAdispersa(p))

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(p=polinomioAleatorio())
def test_polinomioAdensa(p: Polinomio[int]) -> None:
    assert polinomioAdensa(p) == polinomioAdensa2(p)

# La comprobación es
#    >>> test_polinomioAdensa()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 10. Comprobar con Hypothesis que ambas funciones son
# inversas.
# ---------------------------------------------------------------------

# La primera propiedad es
@given(xs=densaAleatoria())
def test_polinomioAdensa_densaApolinomio(xs: list[int]) -> None:
    assert polinomioAdensa(densaApolinomio(xs)) == xs

# La comprobacion es
#    >>> test_polinomioAdensa_densaApolinomio()
#    >>>

# La segunda propiedad es
@given(p=polinomioAleatorio())
def test_densaApolinomio_polinomioAdensa(p: Polinomio[int]) -> None:
    assert densaApolinomio(polinomioAdensa(p)) == p

# La comprobación es
#    >>> test_densaApolinomio_polinomioAdensa()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 11. Definir la función
#    creaTermino : (int, A) -> Polinomio[A]
# tal que creaTermino(n, a) es el término a*x^n. Por ejemplo,
#    >>> creaTermino(2, 5)
#    5*x^2
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def creaTermino(n: int, a: A) -> Polinomio[A]:
    return consPol(n, a, polCero())

# 2ª solución
# ===========

def creaTermino2(n: int, a: A) -> Polinomio[A]:
    r: Polinomio[A] = polCero()
    return r.consPol(n, a)

# Equivalencia de las definiciones
# ================================

# La propiedad es
@given(st.integers(min_value=0, max_value=9),
       st.integers(min_value=-9, max_value=9))
def test_creaTermino(n: int, a: int) -> None:
    assert creaTermino(n, a) == creaTermino2(n, a)

# La comprobación es
#    >>> test_creaTermino()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 12. Definir la función
#    termLider : (Polinomio[A]) -> Polinomio[A]
# tal que termLider(p) es el término líder del polinomio p. Por
# ejemplo,
#    >>> ejPol = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
#    >>> ejPol
#    x^5 + 5*x^2 + 4*x
#    >>> termLider(ejPol)
#    x^5
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def termLider(p: Polinomio[A]) -> Polinomio[A]:
    return creaTermino(grado(p), coefLider(p))

# 2ª solución
# ===========

def termLider2(p: Polinomio[A]) -> Polinomio[A]:
    return creaTermino(p.grado(), p.coefLider())

# Equivalencia de las definiciones
# ================================

# La propiedad es
@given(p=polinomioAleatorio())
def test_termLider(p: Polinomio[int]) -> None:
    assert termLider(p) == termLider2(p)

# La comprobación es
#    >>> test_termLider()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 13. Definir la función
#    sumaPol : (Polinomio[A], Polinomio[A]) -> Polinomio[A]
# tal que sumaPol(p, q) es la suma de los polinomios p y q. Por ejemplo,
#    >>> ejPol1 = consPol(4, 3, consPol(2, -5, consPol(0, 3, polCero())))
#    >>> ejPol2 = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
#    >>> ejPol1
#    3*x^4 + -5*x^2 + 3
#    >>> ejPol2
#    x^5 + 5*x^2 + 4*x
#    >>> sumaPol(ejPol1, ejPol2)
#    x^5 + 3*x^4 + 4*x + 3
#
# Comprobar con Hypothesis las siguientes propiedades:
# + polCero es el elemento neutro de la suma.
# + la suma es conmutativa.
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def sumaPol(p: Polinomio[A], q: Polinomio[A]) -> Polinomio[A]:
    if esPolCero(p):
        return q
    if esPolCero(q):
        return p
    n1, a1, r1 = grado(p), coefLider(p), restoPol(p)
    n2, a2, r2 = grado(q), coefLider(q), restoPol(q)
    if n1 > n2:
        return consPol(n1, a1, sumaPol(r1, q))
    if n1 < n2:
        return consPol(n2, a2, sumaPol(p, r2))
    return consPol(n1, a1 + a2, sumaPol(r1, r2))

# 2ª solución
# ===========

def sumaPol2(p: Polinomio[A], q: Polinomio[A]) -> Polinomio[A]:
    if p.esPolCero():
        return q
    if q.esPolCero():
        return p
    n1, a1, r1 = p.grado(), p.coefLider(), p.restoPol()
    n2, a2, r2 = q.grado(), q.coefLider(), q.restoPol()
    if n1 > n2:
        return sumaPol(r1, q).consPol(n1, a1)
    if n1 < n2:
        return sumaPol(p, r2).consPol(n2, a2)
    return sumaPol(r1, r2).consPol(n1, a1 + a2)

# Equivalencia de las definiciones
# ================================

# La propiedad es
@given(p=polinomioAleatorio(), q=polinomioAleatorio())
def test_sumaPol(p: Polinomio[int], q: Polinomio[int]) -> None:
    assert sumaPol(p, q) == sumaPol2(p,q)

# La comprobación es
#    >>> test_sumaPol()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 14. Comprobar con Hypothesis las siguientes propiedades:
# + polCero es el elemento neutro de la suma.
# + la suma es conmutativa.
# ---------------------------------------------------------------------

# El polinomio cero es el elemento neutro de la suma.
@given(p=polinomioAleatorio())
def test_neutroSumaPol(p: Polinomio[int]) -> None:
    assert sumaPol(polCero(), p) == p
    assert sumaPol(p, polCero()) == p

# La comprobación es
#    >>> test_neutroSumaPol()
#    >>>

# La suma es conmutativa.
@given(p=polinomioAleatorio(), q=polinomioAleatorio())
def test_conmutativaSuma(p: Polinomio[int], q: Polinomio[int]) -> None:
    p1 = p
    q1 = q
    assert sumaPol(p, q) == sumaPol(q1, p1)

# La comprobación es
#    >>> test_conmutativaSuma()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 15. Definir la función
#    multPol : (Polinomio[A], Polinomio[A]) -> Polinomio[A]
# tal que multPol(p, q) es el producto de los polinomios p y q. Por
# ejemplo,
#    >>> ejPol1 = consPol(4, 3, consPol(2, -5, consPol(0, 3, polCero())))
#    >>> ejPol2 = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
#    >>> ejPol1
#    3*x^4 + -5*x^2 + 3
#    >>> ejPol2
#    x^5 + 5*x^2 + 4*x
#    >>> multPol(ejPol1, ejPol2)
#    3*x^9 + -5*x^7 + 15*x^6 + 15*x^5 + -25*x^4 + -20*x^3 + 15*x^2 + 12*x
# ---------------------------------------------------------------------

# multPorTerm(t, p) es el producto del término t por el polinomio
# p. Por ejemplo,
#    ejTerm                     ==  4*x
#    ejPol2                     ==  x^5 + 5*x^2 + 4*x
#    multPorTerm ejTerm ejPol2  ==  4*x^6 + 20*x^3 + 16*x^2
def multPorTerm(term: Polinomio[A], pol: Polinomio[A]) -> Polinomio[A]:
    n = grado(term)
    a = coefLider(term)
    m = grado(pol)
    b = coefLider(pol)
    r = restoPol(pol)
    if esPolCero(pol):
        return polCero()
    return consPol(n + m, a * b, multPorTerm(term, r))

def multPol(p: Polinomio[A], q: Polinomio[A]) -> Polinomio[A]:
    if esPolCero(p):
        return polCero()
    return sumaPol(multPorTerm(termLider(p), q),
                   multPol(restoPol(p), q))

# ---------------------------------------------------------------------
# Ejercicio 16. Comprobar con Hypothesis las siguientes propiedades
# + El producto de polinomios es conmutativo.
# + El producto es distributivo respecto de la suma.
# ---------------------------------------------------------------------

# El producto de polinomios es conmutativo.
@given(p=polinomioAleatorio(),
       q=polinomioAleatorio())
def test_conmutativaProducto(p: Polinomio[int], q: Polinomio[int]) -> None:
    p1 = p
    q1 = q
    assert multPol(p, q) == multPol(q1, p1)

# La comprobación es
#    >>> test_conmutativaProducto()
#    >>>

# El producto es distributivo respecto de la suma.
@given(p=polinomioAleatorio(),
       q=polinomioAleatorio(),
       r=polinomioAleatorio())
def test_distributivaProductoSuma(p: Polinomio[int],
                                  q: Polinomio[int],
                                  r: Polinomio[int]) -> None:
    assert multPol(p, sumaPol(q, r)) == sumaPol(multPol(p, q), multPol(p, r))

# La comprobación es
#    >>> test_distributivaProductoSuma()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 17. Definir la función
#    valor : (Polinomio[A], A) -> A
# tal que valor(p, c) es el valor del polinomio p al sustituir su
# variable por c. Por ejemplo,
#    >>> ejPol = consPol(4, 3, consPol(2, -5, consPol(0, 3, polCero())))
#    >>> ejPol
#    3*x^4 + -5*x^2 + 3
#    >>> valor(ejPol, 0)
#    3
#    >>> valor(ejPol, 1)
#    1
#    >>> valor(ejPol, -2)
#    31
# --------------------------------------------------------------------

def valor(p: Polinomio[A], c: A) -> A:
    if esPolCero(p):
        return 0
    n = grado(p)
    b = coefLider(p)
    r = restoPol(p)
    return b*c**n + valor(r, c)

# ---------------------------------------------------------------------
# Ejercicio 18. Definir la función
#    esRaiz(A, Polinomio[A]) -> bool
# tal que esRaiz(c, p) se verifica si c es una raiz del polinomio p. Por
# ejemplo,
#    >>> ejPol = consPol(4, 6, consPol(1, 2, polCero()))
#    >>> ejPol
#    6*x^4 + 2*x
#    >>> esRaiz(0, ejPol)
#    True
#    >>> esRaiz(1, ejPol)
#    False
# ---------------------------------------------------------------------

def esRaiz(c: A, p: Polinomio[A]) -> bool:
    return valor(p, c) == 0

# ---------------------------------------------------------------------
# Ejercicio 19. Definir la función
#    derivada :: (Eq a, Num a) => Polinomio a -> Polinomio a
# tal que (derivada p) es la derivada del polinomio p. Por ejemplo,
#    >>> ejPol = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
#    >>> ejPol
#    x^5 + 5*x^2 + 4*x
#    >>> derivada(ejPol)
#    5*x^4 + 10*x + 4
# ---------------------------------------------------------------------

def derivada(p: Polinomio[A]) -> Polinomio[A]:
    n = grado(p)
    if n == 0:
        return polCero()
    b = coefLider(p)
    r = restoPol(p)
    return consPol(n - 1, b * n, derivada(r))

# ---------------------------------------------------------------------
# Ejercicio 20. Comprobar con Hypothesis que la derivada de la suma es
# la suma de las derivadas.
# ---------------------------------------------------------------------

# La propiedad es
@given(p=polinomioAleatorio(), q=polinomioAleatorio())
def test_derivada(p: Polinomio[int], q: Polinomio[int]) -> None:
    assert derivada(sumaPol(p, q)) == sumaPol(derivada(p), derivada(q))

# La comprobación es
#    >>> test_derivada()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 21. Definir la función
#    restaPol : (Polinomio[A], Polinomio[A]) -> Polinomio[A]
# tal que restaPol(p, q) es el polinomio obtenido restándole a p el q. Por
# ejemplo,
#    >>> ejPol1 = consPol(5,1,consPol(4,5,consPol(2,5,consPol(0,9,polCero()))))
#    >>> ejPol2 = consPol(4,3,consPol(2,5,consPol(0,3,polCero())))
#    >>> ejPol1
#    x^5 + 5*x^4 + 5*x^2 + 9
#    >>> ejPol2
#    3*x^4 + 5*x^2 + 3
#    >>> restaPol(ejPol1, ejPol2)
#    x^5 + 2*x^4 + 6
# ---------------------------------------------------------------------

def restaPol(p: Polinomio[A], q: Polinomio[A]) -> Polinomio[A]:
    return sumaPol(p, multPorTerm(creaTermino(0, -1), q))

# ---------------------------------------------------------------------
# Ejercicio 22. Definir la función
#    potencia : (Polinomio[A], int) -> Polinomio[A]
# tal que potencia(p, n) es la potencia n-ésima del polinomio p. Por
# ejemplo,
#    >>> ejPol = consPol(1, 2, consPol(0, 3, polCero()))
#    >>> ejPol
#    2*x + 3
#    >>> potencia(ejPol, 2)
#    4*x^2 + 12*x + 9
#    >>> potencia(ejPol, 3)
#    8*x^3 + 36*x^2 + 54*x + 27
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def potencia(p: Polinomio[A], n: int) -> Polinomio[A]:
    if n == 0:
        return consPol(0, 1, polCero())
    return multPol(p, potencia(p, n - 1))

# 2ª solución
# ===========

def potencia2(p: Polinomio[A], n: int) -> Polinomio[A]:
    if n == 0:
        return consPol(0, 1, polCero())
    if n % 2 == 0:
        return potencia2(multPol(p, p), n // 2)
    return multPol(p, potencia2(multPol(p, p), (n - 1) // 2))

# 3ª solución
# ===========

def potencia3(p: Polinomio[A], n: int) -> Polinomio[A]:
    r: Polinomio[A] = consPol(0, 1, polCero())
    for _ in range(0, n):
        r = multPol(p, r)
    return r

# Comprobación de equivalencia
# ============================

# La propiedad es
@given(p=polinomioAleatorio(),
       n=st.integers(min_value=1, max_value=10))
def test_potencia(p: Polinomio[int], n: int) -> None:
    r = potencia(p, n)
    assert potencia2(p, n) == r
    assert potencia3(p, n) == r

# La comprobación es
#    >>> test_potencia()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 23. Definir la función
#    integral : (Polinomio[float]) -> Polinomio[float]
# tal que integral(p) es la integral del polinomio p cuyos coefientes
# son números decimales. Por ejemplo,
#    >>> ejPol = consPol(7, 2, consPol(4, 5, consPol(2, 5, polCero())))
#    >>> ejPol
#    2*x^7 + 5*x^4 + 5*x^2
#    >>> integral(ejPol)
#    0.25*x^8 + x^5 + 1.6666666666666667*x^3
# ---------------------------------------------------------------------

def integral(p: Polinomio[float]) -> Polinomio[float]:
    if esPolCero(p):
        return  polCero()
    n = grado(p)
    b = coefLider(p)
    r = restoPol(p)
    return consPol(n + 1, b / (n + 1), integral(r))

# ---------------------------------------------------------------------
# Ejercicio 24. Definir la función
#    integralDef : (Polinomio[float], float, float) -> float
# tal que integralDef(p, a, b) es la integral definida del polinomio p
# entre a y b. Por ejemplo,
#    >>> ejPol = consPol(7, 2, consPol(4, 5, consPol(2, 5, polCero())))
#    >>> ejPol
#    2*x^7 + 5*x^4 + 5*x^2
#    >>> integralDef(ejPol, 0, 1)
#    2.916666666666667
# ---------------------------------------------------------------------

def integralDef(p: Polinomio[float], a: float, b: float) -> float:
    q = integral(p)
    return valor(q, b) - valor(q, a)

# ---------------------------------------------------------------------
# Ejercicio 25. Definir la función
#    multEscalar : (A, Polinomio[A]) -> Polinomio[A]
# tal que multEscalar(c, p) es el polinomio obtenido multiplicando el
# número c por el polinomio p. Por ejemplo,
#    >>> ejPol = consPol(1, 2, consPol(0, 3, polCero()))
#    >>> ejPol
#    2*x + 3
#    >>> multEscalar(4, ejPol)
#    8*x + 12
#    >>> from fractions import Fraction
#    >>> multEscalar(Fraction('1/4'), ejPol)
#    1/2*x + 3/4
# ---------------------------------------------------------------------

def multEscalar(c: A, p: Polinomio[A]) -> Polinomio[A]:
    if esPolCero(p):
        return polCero()
    n = grado(p)
    b = coefLider(p)
    r = restoPol(p)
    return consPol(n, c * b, multEscalar(c, r))

# ---------------------------------------------------------------------
# Ejercicio 26. Definir la función
#    cociente : (Polinomio[float], Polinomio[float]) -> Polinomio[float]
# tal que cociente(p, q) es el cociente de la división de p entre q. Por
# ejemplo,
#    >>> pol1 = consPol(3, 2, consPol(2, 9, consPol(1, 10, consPol(0, 4, polCero()))))
#    >>> pol1
#    2*x^3 + 9*x^2 + 10*x + 4
#    >>> pol2 = consPol(2, 1, consPol(1, 3, polCero()))
#    >>> pol2
#    x^2 + 3*x
#    >>> cociente(pol1, pol2)
#    2.0*x + 3.0
# ---------------------------------------------------------------------

def cociente(p: Polinomio[float], q: Polinomio[float]) -> Polinomio[float]:
    n1 = grado(p)
    a1 = coefLider(p)
    n2 = grado(q)
    a2 = coefLider(q)
    n3 = n1 - n2
    a3 = a1 / a2
    p3 = restaPol(p, multPorTerm(creaTermino(n3, a3), q))
    if n2 == 0:
        return multEscalar(1 / a2, p)
    if n1 < n2:
        return polCero()
    return consPol(n3, a3, cociente(p3, q))

# ---------------------------------------------------------------------
# Ejercicio 27. Definir la función
#    resto : (Polinomio[float], Polinomio[float]) -> Polinomio[float]
# tal que resto(p, q) es el resto de la división de p entre q. Por ejemplo,
#    >>> resto(pol1, pol2)
#    1.0*x + 4
# ---------------------------------------------------------------------

def resto(p: Polinomio[float], q: Polinomio[float]) -> Polinomio[float]:
    return restaPol(p, multPol(cociente(p, q), q))

# ---------------------------------------------------------------------
# Ejercicio 28. Definir la función
#    divisiblePol : (Polinomio[float], Polinomio[float]) -> bool
# tal que divisiblePol(p, q) se verifica si el polinomio p es divisible
# por el polinomio q. Por ejemplo,
#    >>> pol1 = consPol(2, 8, consPol(1, 14, consPol(0, 3, polCero())))
#    >>> pol1
#    8*x^2 + 14*x + 3
#    >>> pol2 = consPol(1, 2, consPol(0, 3, polCero()))
#    >>> pol2
#    2*x + 3
#    >>> pol3 = consPol(2, 6, consPol(1, 2, polCero()))
#    >>> pol3
#    6*x^2 + 2*x
#    >>> divisiblePol(pol1, pol2)
#    True
#    >>> divisiblePol(pol1, pol3)
#    False
# ---------------------------------------------------------------------

def divisiblePol(p: Polinomio[float], q: Polinomio[float]) -> bool:
    return esPolCero(resto(p, q))

# ---------------------------------------------------------------------
# Ejercicio 29. El método de Horner para calcular el valor de un
# polinomio se basa en representarlo de una forma forma alernativa. Por
# ejemplo, para calcular el valor de
#    a*x^5 + b*x^4 + c*x^3 + d*x^2 + e*x + f
# se representa como
#   (((((0 * x + a) * x + b) * x + c) * x + d) * x + e) * x + f
# y se evalúa de dentro hacia afuera; es decir,
#   v(0) = 0
#   v(1) = v(0)*x+a = 0*x+a = a
#   v(2) = v(1)*x+b = a*x+b
#   v(3) = v(2)*x+c = (a*x+b)*x+c = a*x^2+b*x+c
#   v(4) = v(3)*x+d = (a*x^2+b*x+c)*x+d = a*x^3+b*x^2+c*x+d
#   v(5) = v(4)*x+e = (a*x^3+b*x^2+c*x+d)*x+e = a*x^4+b*x^3+c*x^2+d*x+e
#   v(6) = v(5)*x+f = (a*x^4+b*x^3+c*x^2+d*x+e)*x+f = a*x^5+b*x^4+c*x^3+d*x^2+e*x+f
#
# Usando el [tipo abstracto de los polinomios](https://bit.ly/3KwqXYu),
# definir la función
#    horner : (Polinomio[float], float) -> float
# tal que horner(p, x) es el valor del polinomio p al sustituir su
# variable por el número x. Por ejemplo,
#    >>> pol1 = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
#    >>> pol1
#    x^5 + 5*x^2 + 4*x
#    >>> horner(pol1, 0)
#    0
#    >>> horner(pol1, 1)
#    10
#    >>> horner(pol1, 1.5)
#    24.84375
#    >>> from fractions import Fraction
#    >>> horner(pol1, Fraction('3/2'))
#    Fraction(795, 32)
# ---------------------------------------------------------------------

# 1ª solución
# ===========

def horner(p: Polinomio[float], x: float) -> float:
    def hornerAux(ys: list[float], v: float) -> float:
        if not ys:
            return v
        return hornerAux(ys[1:], v * x + ys[0])

    return hornerAux(polinomioAdensa(p), 0)

# El cálculo de horner(pol1, 2) es el siguiente
#    horner pol1 2
#    = hornerAux [1,0,0,5,4,0] 0
#    = hornerAux   [0,0,5,4,0] ( 0*2+1) = hornerAux   [0,0,5,4,0] 1
#    = hornerAux     [0,5,4,0] ( 1*2+0) = hornerAux     [0,5,4,0] 2
#    = hornerAux       [5,4,0] ( 2*2+0) = hornerAux       [5,4,0] 4
#    = hornerAux         [4,0] ( 4*2+5) = hornerAux         [4,0] 13
#    = hornerAux           [0] (13*2+4) = hornerAux           [0] 30
#    = hornerAux            [] (30*2+0) = hornerAux            [] 60

# 2ª solución
# ===========

def horner2(p: Polinomio[float], x: float) -> float:
    return reduce(lambda a, b: a * x + b, polinomioAdensa(p) , 0.0)

# Comprobación de propiedades
# ===========================

# La comprobación es
#    > poetry run pytest El_TAD_de_polinomios_operaciones.py
#    ======= 20 passed in 5.51s =======
