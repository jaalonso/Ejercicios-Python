# DivideVenceras.py
# Algoritmo divide y vencerás.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 2-noviembre-2023
# ======================================================================

# ----------------------------------------------------------------------
# Introducción                                                        --
# ----------------------------------------------------------------------

# La técnica [divide y vencerás](https://bit.ly/46afaca) consta de
# los siguientes pasos:
# + Dividir el problema en subproblemas menores.
# + Resolver por separado cada uno de los subproblemas:
#   + si los subproblemas son complejos, usar la misma técnica recursivamente;
#   + si son simples, resolverlos directamente.
# + Combinar todas las soluciones de los subproblemas en una solución simple.

# ----------------------------------------------------------------------
# Librerías auxiliares                                                --
# ----------------------------------------------------------------------

from typing import Callable, TypeVar

P = TypeVar('P')
S = TypeVar('S')

# ---------------------------------------------------------------------
# Definir la función
#    divideVenceras(Callable[[P], bool],
#                   Callable[[P], S],
#                   Callable[[P], list[P]],
#                   Callable[[P, list[S]], S],
#                   P) -> S:
# tal que divideVenceras(ind, resuelve, divide, combina, pbInicial)
# resuelve el problema pbInicial mediante la técnica de divide y
# vencerás, donde
# + ind(pb) se verifica si el problema pb es indivisible
# + resuelve(pb) es la solución del problema indivisible pb
# + divide(pb) es la lista de subproblemas de pb
# + combina(pb, ss) es la combinación de las soluciones ss de los
#   subproblemas del problema pb.
# + pbInicial es el problema inicial
#
# Usando la función DivideVenceras definir las funciones
#    ordenaPorMezcla : (list[int]) -> list[int]
#    ordenaRapida    : (list[int]) -> list[int]
# tales que
# + ordenaPorMezcla(xs) es la lista obtenida ordenando xs por el
#   procedimiento de ordenación por mezcla. Por ejemplo,
#      >>> ordenaPorMezcla([3,1,4,1,5,9,2,8])
#      [1, 1, 2, 3, 4, 5, 8, 9]
# + ordenaRapida(xs) es la lista obtenida ordenando xs por el
#   procedimiento de ordenación rápida. Por ejemplo,
#      λ> ordenaRapida([3,1,4,1,5,9,2,8])
#      [1, 1, 2, 3, 4, 5, 8, 9]
# ---------------------------------------------------------------------

def divideVenceras(ind: Callable[[P], bool],
                   resuelve: Callable[[P], S],
                   divide: Callable[[P], list[P]],
                   combina: Callable[[P, list[S]], S],
                   p: P) -> S:
    def dv(pb: P) -> S:
        if ind(pb):
            return resuelve(pb)
        return combina(pb, [dv(sp) for sp in divide(pb)])
    return dv(p)

def ordenaPorMezcla(xs: list[int]) -> list[int]:
    def ind(xs: list[int]) -> bool:
        return len(xs) <= 1

    def divide(xs: list[int]) -> list[list[int]]:
        n = len(xs) // 2
        return [xs[:n], xs[n:]]

    def combina(_: list[int], xs: list[list[int]]) -> list[int]:
        return mezcla(xs[0], xs[1])

    return divideVenceras(ind, lambda x: x, divide, combina, xs)

# (mezcla xs ys) es la lista obtenida mezclando xs e ys. Por ejemplo,
#    mezcla([1,3], [2,4,6]) == [1,2,3,4,6]
def mezcla(a: list[int], b: list[int]) -> list[int]:
    if not a:
        return b
    if not b:
        return a
    if a[0] <= b[0]:
        return [a[0]] + mezcla(a[1:], b)
    return [b[0]] + mezcla(a, b[1:])

def ordenaRapida(xs: list[int]) -> list[int]:
    def ind(xs: list[int]) -> bool:
        return len(xs) <= 1

    def divide(xs: list[int]) -> list[list[int]]:
        x, *xs = xs
        return [[y for y in xs if y <= x],
                [y for y in xs if y > x]]

    def combina(xs: list[int], ys: list[list[int]]) -> list[int]:
        x = xs[0]
        return ys[0] + [x] + ys[1]

    return divideVenceras(ind, lambda x: x, divide, combina, xs)

# Verificación
# ============

def test_divideVenceras() -> None:
    assert ordenaPorMezcla([3,1,4,1,5,9,2,8]) == [1,1,2,3,4,5,8,9]
    assert ordenaRapida([3,1,4,1,5,9,2,8]) == [1,1,2,3,4,5,8,9]
    print("Verificado")

# La verificación es
#    >>> test_divideVenceras()
#    Verificado
