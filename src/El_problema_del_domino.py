# El_problema_del_domino.py
# El problema del dominó mediante búsqueda en espacio de estados.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla,  6-noviembre-2023
# ======================================================================

# ---------------------------------------------------------------------
# Introducción
# ---------------------------------------------------------------------

# Las fichas del dominó se pueden representar por pares de números
# enteros. El problema del dominó consiste en colocar todas las fichas
# de una lista dada de forma que el segundo número de cada ficha
# coincida con el primero de la siguiente.
#
# El objetivo de esta relación de ejercicios es resolver el problema
# del dominó mediante búsqueda en espacio de estados, utilizando las
# implementaciones estudiadas en los ejercicios anteriores.

# ---------------------------------------------------------------------
# Importaciones
# ---------------------------------------------------------------------

from src.BusquedaEnProfundidad import buscaProfundidad

# ---------------------------------------------------------------------
# Ejercicio 1. Las fichas son pares de números enteros.
#
# Definir el tipo Ficha para las fichas.
# ---------------------------------------------------------------------

Ficha  = tuple[int, int]

# ---------------------------------------------------------------------
# Ejercicio 2. Un problema está definido por la lista de fichas que hay
# que colocar.
#
# Definir el tipo Problema para los problemas.
# ---------------------------------------------------------------------

Problema = list[Ficha]

# ---------------------------------------------------------------------
# Ejercicio 3. Los estados son los pares formados por la listas sin
# colocar y las colocadas.
#
# Definir el tipo Estado para los estados.
# ---------------------------------------------------------------------

Estado = tuple[list[Ficha], list[Ficha]]

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    inicial : (Problema) -> Estado
# tal que inicial(p) es el estado inicial del problema p. Por ejemplo,
#    >>> inicial([(1,2),(2,3),(1,4)])
#    ([(1, 2), (2, 3), (1, 4)], [])
# ---------------------------------------------------------------------

def inicial(p: Problema) -> Estado:
    return (p, [])

# ---------------------------------------------------------------------
# Ejercicio 5. Definir la función
#    esFinal : (Estado) -> bool
# tal que esFinal(e) se verifica si e es un estado final. Por ejemplo,
#    >>> esFinal(([], [(4,1),(1,2),(2,3)]))
#    True
#    >>> esFinal(([(2,3)], [(4,1),(1,2)]))
#    False
# ---------------------------------------------------------------------

def esFinal(e: Estado) -> bool:
    return not e[0]

# ---------------------------------------------------------------------
# Ejercicio 6. Definir la función
#    elimina : (Ficha, list[Ficha]) -> list[Ficha]
# tal que elimina(f, fs) es la lista obtenida eliminando la ficha f de
# la lista fs. Por ejemplo,
#    >>> elimina((1,2),[(4,1),(1,2),(2,3)])
#    [(4, 1), (2, 3)]
# ---------------------------------------------------------------------

def elimina(f: Ficha, fs: list[Ficha]) -> list[Ficha]:
    return [g for g in fs if g != f]

# ---------------------------------------------------------------------
# Ejercicio 7. Definir la función
#    sucesores : (Estado) -> list[Estado]
# tal que sucesores(e) es la lista de los sucesores del estado e. Por
# ejemplo,
#    >>> sucesores(([(1,2),(2,3),(1,4)],[]))
#    [([(2,3),(1,4)],[(1,2)]),
#     ([(1,2),(1,4)],[(2,3)]),
#     ([(1,2),(2,3)],[(1,4)]),
#     ([(2,3),(1,4)],[(2,1)]),
#     ([(1,2),(1,4)],[(3,2)]),
#     ([(1,2),(2,3)],[(4,1)])]
#    >>> sucesores(([(2,3),(1,4)],[(1,2)]))
#    [([(2,3)],[(4,1),(1,2)])]
#    >>> sucesores(([(2,3),(1,4)],[(2,1)]))
#    [([(1,4)],[(3,2),(2,1)])]
# ---------------------------------------------------------------------

def sucesores(e: Estado) -> list[Estado]:
    if not e[1]:
        return [(elimina((a,b), e[0]), [(a,b)]) for (a,b) in e[0] if a != b] + \
               [(elimina((a,b), e[0]), [(b,a)]) for (a,b) in e[0]]
    return [(elimina((u,v),e[0]),[(u,v)]+e[1]) for (u,v) in e[0] if u != v and v == e[1][0][0]] +\
           [(elimina((u,v),e[0]),[(v,u)]+e[1]) for (u,v) in e[0] if u != v and u == e[1][0][0]] +\
           [(elimina((u,v),e[0]),[(u,v)]+e[1]) for (u,v) in e[0] if u == v and u == e[1][0][0]]

# ---------------------------------------------------------------------
# Ejercicio 8. Definir, mediante búsqueda en espacio de estados, la
# función
#    soluciones : (Problema) -> list[Estado]
# tal que soluciones(p) es la lista de las soluciones del problema
# p. Por ejemplo,
#    >>> soluciones([(1,2),(2,3),(1,4)])
#    [([], [(3, 2), (2, 1), (1, 4)]), ([], [(4, 1), (1, 2), (2, 3)])]
# ---------------------------------------------------------------------

def soluciones(p: Problema) -> list[Estado]:
    return buscaProfundidad(sucesores, esFinal, inicial(p))

# ---------------------------------------------------------------------
# Ejercicio 9. Definir la función
#    domino : (Problema) -> list[list[Ficha]]
# tal que domino(fs) es la lista de las soluciones del problema del
# dominó correspondiente a las fichas fs. Por ejemplo,
#    >>> domino([(1,2),(2,3),(1,4)])
#    [[(3, 2), (2, 1), (1, 4)], [(4, 1), (1, 2), (2, 3)]]
#    >>> domino([(1,2),(1,1),(1,4)])
#    [[(2, 1), (1, 1), (1, 4)], [(4, 1), (1, 1), (1, 2)]]
#    >>> domino([(1,2),(3,4),(2,3)])
#    [[(4, 3), (3, 2), (2, 1)], [(1, 2), (2, 3), (3, 4)]]
#    >>> domino([(1,2),(2,3),(5,4)])
#    []
# ---------------------------------------------------------------------

def domino(p: Problema) -> list[list[Ficha]]:
    return [s[1] for s in soluciones(p)]

# # Verificación
# # ============

def test_domino() -> None:
    assert domino([(1,2),(2,3),(1,4)]) == \
        [[(3, 2), (2, 1), (1, 4)], [(4, 1), (1, 2), (2, 3)]]
    assert domino([(1,2),(1,1),(1,4)]) == \
        [[(2, 1), (1, 1), (1, 4)], [(4, 1), (1, 1), (1, 2)]]
    assert domino([(1,2),(3,4),(2,3)]) == \
        [[(4, 3), (3, 2), (2, 1)], [(1, 2), (2, 3), (3, 4)]]
    assert domino([(1,2),(2,3),(5,4)]) == \
        []
    print("Verificado")

# La verificación es
#    >>> test_domino()
#    Verificado
