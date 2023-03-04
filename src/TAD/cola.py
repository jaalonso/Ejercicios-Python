# cola.py
# El TAD de las colas.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 18-enero-2023
# ======================================================================

# Una cola es una estructura de datos, caracterizada por ser una
# secuencia de elementos en la que la operación de inserción se realiza
# por un extremo (el posterior o final) y la operación de extracción
# por el otro (el anterior o frente).
#
# Las operaciones que definen a tipo abstracto de datos (TAD) de las
# colas (cuyos elementos son del tipo a) son las siguientes:
#    vacia   :: Cola a
#    inserta :: a -> Cola a -> Cola a
#    primero :: Cola a -> a
#    resto   :: Cola a -> Cola a
#    esVacia :: Cola a -> Bool
# tales que
#    + vacia es la cola vacía.
#    + (inserta x c) es la cola obtenida añadiendo x al final de c.
#    + (primero c) es el primero de la cola c.
#    + (resto c) es la cola obtenida eliminando el primero de c.
#    + (esVacia c) se verifica si c es la cola vacía.
#
# Las operaciones tienen que verificar las siguientes propiedades:
#    + primero (inserta x vacia) == x
#    + Si c es una cola no vacía, entonces primero (inserta x c) == primero c,
#    + resto (inserta x vacia) == vacia
#    + Si c es una cola no vacía, entonces resto (inserta x c) == inserta x (resto c)
#    + esVacia vacia
#    + not (esVacia (inserta x c))
#
# Para usar el TAD hay que usar una implementación concreta. En
# principio, consideraremos dos: una usando listas y otra usando
# sucesiones. Hay que elegir la que se desee utilizar, descomentándola
# y comentando las otras.

__all__ = [
    'Cola',
    'vacia',
    'inserta',
    'primero',
    'resto',
    'esVacia',
    'colaAleatoria'
]

# from src.TAD.colaConListas import (Cola, colaAleatoria, esVacia, inserta,
#                                    primero, resto, vacia)
# from src.TAD.colaConDosListas import (Cola, colaAleatoria, esVacia, inserta,
#                                       primero, resto, vacia)
from src.TAD.colaConDeque import (Cola, colaAleatoria, esVacia, inserta,
                                  primero, resto, vacia)
