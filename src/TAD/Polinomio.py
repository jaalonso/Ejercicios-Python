# Polinomio.py
# El tipo abstracto de datos de los polinomios.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 17-abril-2023
# ---------------------------------------------------------------------

# Un polinomio es una expresión matemática compuesta por una suma de
# términos, donde cada término es el producto de un coeficiente y una
# variable elevada a una potencia. Por ejemplo, el polinomio 3x^2+2x-1
# tiene un término de segundo grado (3x^2), un término de primer grado
# (2x) y un término constante (-1).
#
# Las operaciones que definen al tipo abstracto de datos (TAD) de los
# polinomios (cuyos coeficientes son del tipo a) son las siguientes:
#    polCero   :: Polinomio a
#    esPolCero :: Polinomio a -> Bool
#    consPol   :: (Num a, Eq a) => Int -> a -> Polinomio a -> Polinomio a
#    grado     :: Polinomio a -> Int
#    coefLider :: Num a => Polinomio a -> a
#    restoPol  :: (Num a, Eq a) => Polinomio a -> Polinomio a
# tales que
#    + polCero es el polinomio cero.
#    + (esPolCero p) se verifica si p es el polinomio cero.
#    + (consPol n b p) es el polinomio bx^n+p
#    + (grado p) es el grado del polinomio p.
#    + (coefLider p) es el coeficiente líder del polinomio p.
#    + (restoPol p) es el resto del polinomio p.
#
# Por ejemplo, el polinomio
#    3*x^4 + -5*x^2 + 3
# se representa por
#    consPol 4 3 (consPol 2 (-5) (consPol 0 3 polCero))
#
# Las operaciones tienen que verificar las siguientes propiedades:
#    + esPolCero polCero
#    + n > grado p && b /= 0 ==> not (esPolCero (consPol n b p))
#    + consPol (grado p) (coefLider p) (restoPol p) == p
#    + n > grado p && b /= 0 ==> grado (consPol n b p) == n
#    + n > grado p && b /= 0 ==> coefLider (consPol n b p) == b
#    + n > grado p && b /= 0 ==> restoPol (consPol n b p) == p
#
# Para usar el TAD hay que usar una implementación concreta. En
# principio, consideraremos las siguientes:
#    + mediante tipo de dato algebraico,
#    + mediante listas densas y
#    + mediante listas dispersas.
# Hay que elegir la que se desee utilizar, descomentándola y comentando
# las otras.

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

from src.TAD.PolRepDensa import (Polinomio, coefLider, consPol, esPolCero,
                                 grado, polCero, polinomioAleatorio, restoPol)

# from src.TAD.PolRepDispersa import (Polinomio, polCero, esPolCero,
#                                     consPol, grado, coefLider,
#                                     restoPol, polinomioAleatorio)
