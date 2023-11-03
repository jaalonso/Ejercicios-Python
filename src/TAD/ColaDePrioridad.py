# ColaDePrioridad.py
# El tipo abstracto de datos de las colas de prioridad
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 5-julio-2023
# ---------------------------------------------------------------------

# Una cola de prioridad es una cola en la que cada elemento tiene
# asociada una prioridad. La operación de extracción siempre elige el
# elemento de menor prioridad.
#
# Las operaciones que definen a tipo abstracto de datos (TAD) de las
# colas de prioridad (cuyos elementos son del tipo a) son las
# siguientes:
#    vacia   :: Ord a => CPrioridad a
#    inserta :: Ord a => a -> CPrioridad a -> CPrioridad a
#    primero :: Ord a => CPrioridad a -> a
#    resto   :: Ord a => CPrioridad a -> CPrioridad a
#    esVacia :: Ord a => CPrioridad a -> Bool
# tales que
# + vacia es la cola de prioridad vacía.
# + (inserta x c) añade el elemento x a la cola de prioridad c.
# + (primero c) es el primer elemento de la cola de prioridad c.
# + (resto c) es el resto de la cola de prioridad c.
# + (esVacia c) se verifica si la cola de prioridad c es vacía.
#
# Las operaciones tienen que verificar las siguientes propiedades:
# + inserta x (inserta y c) == inserta y (inserta x c)
# + primero (inserta x vacia) == x
# + Si x <= y, entonces primero (inserta y (inserta x c)) == primero (inserta x c)
# + resto (inserta x vacia) == vacia
# + Si x <= y, entonces resto (inserta y (inserta x c)) == inserta y (resto (inserta x c))
# + esVacia vacia
# + not (esVacia (inserta x c))
#
# Para usar el TAD hay que usar una implementación concreta. En
# principio, consideraremos su representación mediante listas.

__all__ = [
   'CPrioridad',
   'vacia',
   'inserta',
   'primero',
   'resto',
   'esVacia',
    ]

from src.TAD.ColaDePrioridadConListas import (CPrioridad, esVacia, inserta,
                                              primero, resto, vacia)
