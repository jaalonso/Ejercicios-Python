# BEE_El_problema_del_granjero.py
# El problema del granjero mediante búsqueda en espacio de estado.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 14-agosto-2023
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Introducción                                                       --
# ---------------------------------------------------------------------

# Un granjero está parado en un lado del río y con él tiene un lobo,
# una cabra y una repollo. En el río hay un barco pequeño. El granjero
# desea cruzar el río con sus tres posesiones. No hay puentes y en el
# barco hay solamente sitio para el granjero y un artículo. Si deja
# la cabra con la repollo sola en un lado del río la cabra comerá la
# repollo. Si deja el lobo y la cabra en un lado, el lobo se comerá a
# la cabra. ¿Cómo puede cruzar el granjero el río con los tres
# artículos, sin que ninguno se coma al otro?
#
# El objetivo de esta relación de ejercicios es resolver el problema
# del granjero mediante búsqueda en espacio de estados, utilizando las
# implementaciones estudiadas en los ejercicios anteriores.

# ---------------------------------------------------------------------
# Importaciones                                                      --
# ---------------------------------------------------------------------

from enum import Enum

from src.BusquedaEnProfundidad import buscaProfundidad

# ---------------------------------------------------------------------
# Ejercicio 1. Definir el tipo Orilla con dos constructores I y D que
# representan las orillas izquierda y derecha, respectivamente.
# ---------------------------------------------------------------------

class Orilla(Enum):
    I = 0
    D = 1

    def __repr__(self) -> str:
        return self.name

I = Orilla.I
D = Orilla.D

# ---------------------------------------------------------------------
# Ejercicio 2. Definir el tipo Estado como abreviatura de una tupla que
# representan en qué orilla se encuentra cada uno de los elementos
# (granjero, lobo, cabra, repollo). Por ejemplo, (I,D,D,I) representa
# que el granjero está en la izquierda, que el lobo está en la derecha,
# que la cabra está en la derecha y el repollo está en la izquierda.
# ---------------------------------------------------------------------

Estado = tuple[Orilla, Orilla, Orilla, Orilla]

# ---------------------------------------------------------------------
# Ejercicio 3. Definir la función
#    seguro :  (Estado) -> bool
# tal que seguro(e) se verifica si el estado e es seguro; es decir, que
# no puede estar en una orilla el lobo con la cabra sin el granjero ni
# la cabra con el repollo sin el granjero. Por ejemplo,
#    seguro((I,D,D,I))  ==  False
#    seguro((D,D,D,I))  ==  True
#    seguro((D,D,I,I))  ==  False
#    seguro((I,D,I,I))  ==  True
# ---------------------------------------------------------------------

def seguro(e: Estado) -> bool:
    (g,l,c,r) = e
    return not (g != c and c in {l, r})

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    opuesta : (Orilla) -> Orilla
# tal que (opuesta x) es la opuesta de la orilla x. Por ejemplo
#    opuesta(I) == D
# ---------------------------------------------------------------------

def opuesta(o: Orilla) -> Orilla:
    if o == I:
        return D
    return I

# ---------------------------------------------------------------------
# Ejercicio 5. Definir la función
#    sucesoresE(Estado) -> list[Estado]
# tal que sucesoresE(e) es la lista de los sucesores seguros del estado
# e. Por ejemplo,
#    sucesoresE((I,I,I,I))  ==  [(D,I,D,I)]
#    sucesoresE((D,I,D,I))  ==  [(I,I,D,I),(I,I,I,I)]
# ---------------------------------------------------------------------

def sucesoresE(e: Estado) -> list[Estado]:
    def mov(n: int, e: Estado) -> Estado:
        (g,l,c,r) = e
        if n == 1:
            return (opuesta(g), l, c, r)
        if n == 2:
            return (opuesta(g), opuesta(l), c, r)
        if n == 3:
            return (opuesta(g), l, opuesta(c), r)
        return (opuesta(g), l, c, opuesta(r))
    return [mov(n, e) for n in range(1, 5) if seguro(mov(n, e))]

# ---------------------------------------------------------------------
# Ejercicio 6. Nodo es el tipo de los nodos del espacio de búsqueda,
# donde un nodo es una lista de estados
#    [e_n, ..., e_2, e_1]
# tal que e_1 es el estado inicial y para cada i (2 <= i <= n), e_i es un
# sucesor de e_(i-1).
#
# Definir el tipo Nodo.
# ---------------------------------------------------------------------

Nodo = list[Estado]

# ---------------------------------------------------------------------
# Ejercicio 7. Definir
#    inicial: Nodo
# tal que inicial es el nodo inicial en el que todos están en la orilla
# izquierda.
# ---------------------------------------------------------------------

inicial: Nodo = [(I,I,I,I)]

# ---------------------------------------------------------------------
# Ejercicio 8. Definir la función
#    esFinal : (Nodo) -> bool
# tal que esFinal(n) se verifica si n es un nodo final; es decir, su
# primer elemento es el estado final. Por ejemplo,
#    esFinal([(D,D,D,D),(I,I,I,I)])  ==  True
#    esFinal([(I,I,D,I),(I,I,I,I)])  ==  False
# ---------------------------------------------------------------------

def esFinal(n: Nodo) -> bool:
    return n[0] == (D,D,D,D)

# ---------------------------------------------------------------------
# Ejercicio 9. Definir la función
#    sucesores : (Nodo) -> list[Nodo]
# tal que sucesores(n) es la lista de los sucesores del nodo n. Por
# ejemplo,
#    >>> sucesores([(I,I,D,I),(D,I,D,I),(I,I,I,I)])
#    [[(D, D, D, I), (I, I, D, I), (D, I, D, I), (I, I, I, I)],
#     [(D, I, D, D), (I, I, D, I), (D, I, D, I), (I, I, I, I)]]
# ---------------------------------------------------------------------

def sucesores(n: Nodo) -> list[Nodo]:
    e, *es = n
    return [[e1] + n for e1 in sucesoresE(e) if e1 not in es]

# ---------------------------------------------------------------------
# Ejercicio 10. Usando el procedimiento de búsqueda en profundidad,
# definir la función
#    granjero : () -> list[list[Estado]]
# tal que granjero() son las soluciones del problema del granjero
# mediante el patrón de búsqueda en espacio de estados. Por ejemplo,
#    >>> granjero()
#    [[(I,I,I,I),(D,I,D,I),(I,I,D,I),(D,I,D,D),(I,I,I,D),(D,D,I,D),(I,D,I,D),(D,D,D,D)],
#     [(I,I,I,I),(D,I,D,I),(I,I,D,I),(D,D,D,I),(I,D,I,I),(D,D,I,D),(I,D,I,D),(D,D,D,D)]]
# ---------------------------------------------------------------------

def granjero() -> list[list[Estado]]:
    return [list(reversed(es)) for es in buscaProfundidad(sucesores, esFinal, inicial)]

# # Verificación
# # ============

def test_granjero() -> None:
    assert granjero() == \
        [[(I,I,I,I),(D,I,D,I),(I,I,D,I),(D,I,D,D),(I,I,I,D),(D,D,I,D),(I,D,I,D),(D,D,D,D)],
         [(I,I,I,I),(D,I,D,I),(I,I,D,I),(D,D,D,I),(I,D,I,I),(D,D,I,D),(I,D,I,D),(D,D,D,D)]]
    print("Verificado")

# La verificación es
#    >>> test_granjero()
#    Verificado
