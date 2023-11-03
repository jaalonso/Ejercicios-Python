# BEE_Mochila.py
# El problema de la mochila (mediante espacio de estados).
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 04-julio-2023
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Introducción
# ---------------------------------------------------------------------

# Se tiene una mochila de capacidad de peso p y una lista de n objetos
# para colocar en la mochila. Cada objeto i tiene un peso w(i) y un
# valor v(i). Considerando la posibilidad de colocar el mismo objeto
# varias veces en la mochila, el problema consiste en determinar la
# forma de colocar los objetos en la mochila sin sobrepasar la
# capacidad de la mochila colocando el máximo valor posible.
#
# En esta relación de ejercicios se resolverá el problema de la mochila
# mediante búsqueda en espacios de estados.

# ---------------------------------------------------------------------
# Importaciones
# ---------------------------------------------------------------------

from src.BusquedaEnProfundidad import buscaProfundidad

# ---------------------------------------------------------------------
# Ejercicio 1. Para solucionar el problema se definen los siguientes
# tipos:
# + Una solución del problema de la mochila es una lista de objetos.
#      Solucion = list[Objeto]
# + Los objetos son pares formado por un peso y un valor
#      Objeto = tuple[Peso, Valor]
# + Los pesos son número enteros
#      Peso = int
# + Los valores son números reales.
#      Valor = float
# + Los estados del problema de la mochila son 5-tupla de la forma
#   (v,p,l,o,s) donde v es el valor de los objetos colocados, p es el
#   peso de los objetos colocados, l es el límite de la capacidad de la
#   mochila, o es la lista de los objetos colocados (ordenados de forma
#   creciente según sus pesos) y s es la solución parcial.
#      Estado = tuple[Valor, Peso, Peso, list[Objeto], Solucion]
#
# Definir los tipos Peso, Valor, Objeto, Solucion, Estado para los tipis
# de los pesos, valores, objetos, soluciones y estados, respectivamente.
# ---------------------------------------------------------------------

Peso = int
Valor = float
Objeto = tuple[Peso, Valor]
Solucion = list[Objeto]
Estado = tuple[Valor, Peso, Peso, list[Objeto], Solucion]

# ---------------------------------------------------------------------
# Ejercicio 2. Definir la función
#    inicial : (list[Objeto], Peso) -> Estado
# tal que inicial(os, l) es el estado inicial del problema de la mochila
# para la lista de objetos os y el límite de capacidad l
# ---------------------------------------------------------------------

def inicial(os: list[Objeto], l: Peso) -> Estado:
    return (0,0,l,sorted(os),[])

# ---------------------------------------------------------------------
# Ejercicio 3. Definir la función
#    sucesores : (Estado) -> list[Estado]
# tal que sucesores(e) es la lista de los sucesores del estado e en el
# problema de la mochila para la lista de objetos os y el límite de
# capacidad l.
# ---------------------------------------------------------------------

def sucesores(n: Estado) -> list[Estado]:
    (v,p,l,os,solp) = n
    return [( v+v1,
              p+p1,
              l,
              [(p2,v2) for (p2,v2) in os if p2 >= p1],
              [(p1,v1)] + solp )
            for (p1,v1) in os if p + p1 <= l]

# ---------------------------------------------------------------------
# Ejercicio 4. Definir la función
#    esObjetivo : (Estado) -> bool
# tal que esObjetivo(e) se verifica si e es un estado final el problema
# de la mochila para la lista de objetos os y el límite de capacidad l.
# ---------------------------------------------------------------------

def esObjetivo(e: Estado) -> bool:
    (_, p, l, os, _) = e
    (p_, _) = os[0]
    return p + p_ > l

# ---------------------------------------------------------------------
# Ejercicio 5. Usando el procedimiento de búsqueda en profundidad,
# definir la función
#    mochila : (list[Objeto], Peso) -> tuple[SolMoch, Valor]
# tal que mochila(os, l) es la solución del problema de la mochila para
# la lista de objetos os y el límite de capacidad l. Por ejemplo,
#    >>> mochila([(2,3),(3,5),(4,6),(5,10)], 8)
#    ([(5, 10), (3, 5)], 15)
#    >>> mochila([(2,3),(3,5),(5,6)], 10)
#    ([(3, 5), (3, 5), (2, 3), (2, 3)], 16)
#    >>> mochila([(8,15),(15,10),(3,6),(6,13), (2,4),(4,8),(5,6),(7,7)], 35)
#    ([(6, 13), (6, 13), (6, 13), (6, 13), (6, 13), (3, 6), (2, 4)], 75)
#    >>> mochila([(2,2.8),(3,4.4),(5,6.1)], 10)
#    ([(3, 4.4), (3, 4.4), (2, 2.8), (2, 2.8)], 14.4)
# ---------------------------------------------------------------------

def mochila(os: list[Objeto], l: Peso) -> tuple[Solucion, Valor]:
    (v,_,_,_,sol) = max(buscaProfundidad(sucesores,
                                         esObjetivo,
                                         inicial(os, l)))
    return (sol, v)

# Verificación
# ============

def test_Mochila() -> None:
    assert mochila([(2,3),(3,5),(4,6),(5,10)], 8) == \
        ([(5,10.0),(3,5.0)],15.0)
    assert mochila([(2,3),(3,5),(5,6)], 10) == \
        ([(3,5.0),(3,5.0),(2,3.0),(2,3.0)],16.0)
    assert mochila([(2,2.8),(3,4.4),(5,6.1)], 10) == \
        ([(3,4.4),(3,4.4),(2,2.8),(2,2.8)],14.4)
    print("Verificado")

# La verificación es
#    >>> test_Mochila()
#    Verificado
