# conjunto.py
# El tipo abstracto de datos de los conjuntos.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 28-febrero-2023
# ---------------------------------------------------------------------

# Un conjunto es una estructura de datos, caracterizada por ser una
# colección de elementos en la que no importe ni el orden ni la
# repetición de elementos.
#
# Las operaciones que definen al tipo abstracto de datos (TAD) de los
# conjuntos (cuyos elementos son del tipo a) son las siguientes:
#    vacio      :: Conj a
#    inserta    :: Ord a => a -> Conj a -> Conj a
#    menor      :: Ord a => Conj a -> a
#    elimina    :: Ord a => a -> Conj a -> Conj a
#    pertenece  :: Ord a => a -> Conj a -> Bool
#    esVacio    :: Conj a -> Bool
# tales que
#    + vacio es el conjunto vacío.
#    + (inserta x c) es el conjunto obtenido añadiendo el elemento x al
#      conjunto c.
#    + (menor c) es el menor elemento del conjunto c.
#    + (elimina x c) es el conjunto obtenido eliminando el elemento x
#      del conjunto c.
#    + (pertenece x c) se verifica si x pertenece al conjunto c.
#    + (esVacio c) se verifica si c es el conjunto vacío.
#
# Las operaciones tienen que verificar las siguientes propiedades:
#    + inserta x (inserta x c) == inserta x c
#    + inserta x (inserta y c) == inserta y (inserta x c)
#    + not (pertenece x vacio)
#    + pertenece y (inserta x c) == (x==y) || pertenece y c
#    + elimina x vacio == vacio
#    + Si x == y, entonces
#      elimina x (inserta y c) == elimina x c
#    + Si x /= y, entonces
#      elimina x (inserta y c) == inserta y (elimina x c)
#    + esVacio vacio
#    + not (esVacio (inserta x c))
#
# Para usar el TAD hay que usar una implementación concreta. En
# principio, consideraremos las siguientes:
#    + mediante listas no ordenadas con duplicados,
#    + mediante listas no ordenadas sin duplicados,
#    + mediante listas ordenadas sin duplicados y
#    + mediante la librería Data.Set.
# Hay que elegir la que se desee utilizar, descomentándola y comentando
# las otras.

__all__ = [
    'Conj',
    'vacio',
    'inserta',
    'menor',
    'elimina',
    'pertenece',
    'esVacio',
    'conjuntoAleatorio'
]

# from src.TAD.conjuntoConListasNoOrdenadasConDuplicados import (
#     Conj, conjuntoAleatorio, elimina, esVacio, inserta,
#     menor, pertenece, vacio)

# from src.TAD.conjuntoConListasNoOrdenadasSinDuplicados import (
#     Conj, conjuntoAleatorio, elimina, esVacio, inserta, menor, pertenece,
#     vacio)

from src.TAD.conjuntoConListasOrdenadasSinDuplicados import (Conj,
                                                             conjuntoAleatorio,
                                                             elimina, esVacio,
                                                             inserta, menor,
                                                             pertenece, vacio)

# from src.TAD.conjuntoConLibreria import (
#     Conj, conjuntoAleatorio, elimina, esVacio, inserta, menor, pertenece,
#     vacio)
