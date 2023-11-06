# Problema_de_suma_cero.py
# Problema de suma cero.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla,  6-noviembre-2023
# ======================================================================

# ---------------------------------------------------------------------
# Introducción
# ---------------------------------------------------------------------

# El problema de suma cero consiste en, dado el conjunto de números
# enteros, encontrar sus subconjuntos no vacío cuyos elementos sumen
# cero. Por ejemplo, la soluciones para [-7,-3,-2,5,8,-1] son
# [-7,-3,-2,-1,5,8], [-7,-1,8] y [-3,-2,5]
#
# El objetivo de esta relación de ejercicios es resolver el problema
# de suma cero mediante búsqueda en espacio de estados, utilizando las
# implementaciones estudiadas en los ejercicios anteriores.

# ---------------------------------------------------------------------
# Importaciones
# ---------------------------------------------------------------------

from src.BusquedaEnProfundidad import buscaProfundidad

# ---------------------------------------------------------------------
# Ejercicio 1. Los estados son ternas formadas por los números
# seleccionados, su suma y los restantes números.
#
# Definir el tipo Estado para los estados.
# ---------------------------------------------------------------------

Estado = tuple[list[int], int, list[int]]

# ---------------------------------------------------------------------
# Ejercicio 2. Definir la función
#    inicial : (list[int]) -> Estado
# tal que inicial(ns) es el estado inicial dell problema de suma cero a
# partir de los números de ns. Por ejemplo,
#    >>> inicial([-7,-3,-2,5,8,-1])
#    ([], 0, [-7, -3, -2, 5, 8, -1])
# ---------------------------------------------------------------------

def inicial(ns: list[int]) -> Estado:
    return ([], 0, ns)

# ---------------------------------------------------------------------
# Ejercicio 3. Definir la función
#    esFinal : (Estado) -> bool
# tal es Final(e) se verifica si e es un estado final. Por ejemplo,
#    >>> esFinal(([-7, -1, 8], 0, [-3, -2, 5]))
#    True
#    >>> esFinal(([-3, 8, -1], 4, [-7, -2, 5]))
#    False
# ---------------------------------------------------------------------

def esFinal(e: Estado) -> bool:
    (xs,s,_) = e
    return xs != [] and s == 0

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    sucesores : (Estado) -> list[Estado]
# tal que sucesores(e) es la lista de los sucesores del estado e. Por
# ejemplo,
#    >>> sucesores(([-2, -3, -7], -12, [5, 8, -1]))
#    [([5, -2, -3, -7], -7,   [8, -1]),
#     ([8, -2, -3, -7], -4,   [5, -1]),
#     ([-1, -2, -3, -7], -13, [5, 8])]
# ---------------------------------------------------------------------

def sucesores(e: Estado) -> list[Estado]:
    (xs, s, ns) = e
    return [([n] + xs, n + s, [m for m in ns if m !=n])
            for n in ns]

# ---------------------------------------------------------------------
# Ejercicio 5. Usando el procedimiento de búsqueda en profundidad,
# definir la función
#    suma0 : (list[int]) -> list[list[int]]
# tal que suma0(ns) es la lista de las soluciones del problema de suma
# cero para ns. Por ejemplo,
#    λ> suma0([-7,-3,-2,5,8])
#    [[-3,-2,5]]
#    λ> suma0([-7,-3,-2,5,8,-1])
#    [[-7,-3,-2,-1,5,8],[-7,-1,8],[-3,-2,5]]
#    λ> suma0([-7,-3,1,5,8])
#    []
# ---------------------------------------------------------------------

def soluciones(ns: list[int]) -> list[Estado]:
    return buscaProfundidad(sucesores, esFinal, inicial(ns))

def suma0(ns: list[int]) -> list[list[int]]:
    xss = [list(sorted(s[0])) for s in soluciones(ns)]
    r = []
    for xs in xss:
        if xs not in r:
            r.append(xs)
    return r

# Verificación
# ============

def test_suma0() -> None:
    assert suma0([-7,-3,-2,5,8]) == \
        [[-3,-2,5]]
    assert suma0([-7,-3,-2,5,8,-1]) == \
        [[-7,-3,-2,-1,5,8],[-7,-1,8],[-3,-2,5]]
    assert not suma0([-7,-3,1,5,8])
    print("Verificado")

# La verificación es
#    >>> test_suma0()
#    Verificado
