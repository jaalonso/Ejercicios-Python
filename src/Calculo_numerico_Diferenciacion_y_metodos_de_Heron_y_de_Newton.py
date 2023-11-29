# Calculo_numerico_Diferenciacion_y_metodos_de_Heron_y_de_Newton.py
# Cálculo numérico: Diferenciación y métodos de Herón y de Newton.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 29-noviembre-2023
# ======================================================================

# ---------------------------------------------------------------------
# Introducción                                                       --
# ---------------------------------------------------------------------

# En esta relación se definen funciones para resolver los siguientes
# problemas de cálculo numérico:
# + diferenciación numérica,
# + cálculo de la raíz cuadrada mediante el método de Herón,
# + cálculo de los ceros de una función por el método de Newton y
# + cálculo de funciones inversas.

# ----------------------------------------------------------------------
# Librerías auxiliares                                                --
# ----------------------------------------------------------------------

from functools import partial
from math import cos, pi, sin
from typing import Callable

from hypothesis import given
from hypothesis import strategies as st

# ---------------------------------------------------------------------
# Diferenciación numérica                                            --
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 1.1. Definir la función
#    derivada : (float, Callable[[float], float], float) -> float
# tal que derivada(a, f, x) es el valor de la derivada de la función f
# en el punto x con aproximación a. Por ejemplo,
#    derivada(0.001, sin, pi)  ==  -0.9999998333332315
#    derivada(0.001, cos, pi)  ==  4.999999583255033e-4
# ---------------------------------------------------------------------

def derivada(a: float, f: Callable[[float], float], x: float) -> float:
    return (f(x+a) - f(x)) / a

# Verificación
# ============

def test_derivada() -> None:
    assert derivada(0.001, sin, pi) == -0.9999998333332315
    assert derivada(0.001, cos, pi) == 4.999999583255033e-4
    print("Verificado")

# La comprobación es
#    >>> test_derivada()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 1.2. Definir las funciones
#    derivadaBurda : Callable[[Callable[[float], float], float], float]
#    derivadaFina  : Callable[[Callable[[float], float], float], float]
#    derivadaSuper : Callable[[Callable[[float], float], float], float]
# tales que
#    * derivadaBurda(f, x) es el valor de la derivada de la función f
#      en el punto x con aproximación 0.01,
#    * (derivadaFina(f, x) es el valor de la derivada de la función f
#      en el punto x con aproximación 0.0001.
#    * (derivadaSuper(f, x) es el valor de la derivada de la función f
#      en el punto x con aproximación 0.000001.
# Por ejemplo,
#    derivadaBurda(cos, pi)  ==  0.004999958333473664
#    derivadaFina(cos, pi)   ==  4.999999969612645e-05
#    derivadaSuper(cos, pi)  ==  5.000444502911705e-07
# ---------------------------------------------------------------------

derivadaBurda: Callable[[Callable[[float], float], float], float] =\
    partial(derivada, 0.01)

derivadaFina: Callable[[Callable[[float], float], float], float] =\
    partial(derivada, 0.0001)

derivadaSuper: Callable[[Callable[[float], float], float], float] =\
    partial(derivada, 0.000001)

# Verificación
# ============

def test_derivadas() -> None:
    assert derivadaBurda(cos, pi) == 0.004999958333473664
    assert derivadaFina(cos, pi) == 4.999999969612645e-05
    assert derivadaSuper(cos, pi) == 5.000444502911705e-07
    print("Verificado")

# La comprobación es
#    >>> test_derivadas()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 1.3. Definir la función
#    derivadaFinaDelSeno : Callable[[float], float]
# tal que derivadaFinaDelSeno(x) es el valor de la derivada fina del
# seno en x. Por ejemplo,
#    derivadaFinaDelSeno(pi) == -0.9999999983354435
# ---------------------------------------------------------------------

derivadaFinaDelSeno: Callable[[float], float] =\
    partial(derivadaFina, sin)

# Verificación
# ============

def test_derivadaFinaSeno() -> None:
    assert derivadaFinaDelSeno(pi) == -0.9999999983354435
    print("Verificado")

# La comprobación es
#    >>> test_derivadaFinaSeno()
#    Verificado

# ---------------------------------------------------------------------
# Cálculo de la raíz cuadrada                                        --
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 2.1. En los siguientes apartados de este ejercicio se va a
# calcular la raíz cuadrada de un número basándose en las siguientes
# propiedades:
# + Si y es una aproximación de la raíz cuadrada de x, entonces
#   (y+x/y)/2 es una aproximación mejor.
# + El límite de la sucesión definida por
#       x_0     = 1
#       x_{n+1} = (x_n+x/x_n)/2
#   es la raíz cuadrada de x.
#
# Definir, por recursión, la función
#    raiz : (float) -> float
# tal que raiz(x) es la raíz cuadrada de x calculada usando la
# propiedad anterior con una aproximación de 0.00001 y tomando como
# valor inicial 1. Por ejemplo,
#    raiz(9) == 3.000000001396984
# ---------------------------------------------------------------------

def raiz(x : float) -> float:
    def aceptable(y: float) -> bool:
        return abs(y*y-x) < 0.00001
    def mejora(y: float) -> float:
        return 0.5*(y+x/y)
    def raizAux(y: float) -> float:
        if aceptable(y):
            return y
        return raizAux(mejora(y))
    return raizAux(1)

# Verificación
# ============

def test_raiz() -> None:
    assert raiz(9) == 3.000000001396984
    print("Verificado")

# La comprobación es
#    >>> test_raiz()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 3.2. Definir el operador
#    casiIgual : (float, float) -> bool
# tal que casiIgual(x, y) si |x-y| < 0.001. Por ejemplo,
#    casiIgual(3.05, 3.07)        == False
#    casiIgual(3.00005, 3.00007)  == True
# ---------------------------------------------------------------------

def casiIgual(x: float, y: float) -> bool:
    return abs(x - y) < 0.001

# Verificación
# ============

def test_casiIgual() -> None:
    assert not casiIgual(3.05, 3.07)
    assert casiIgual(3.00005, 3.00007)
    print("Verificado")

# La comprobación es
#    >>> test_casiIgual()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 3.3. Comprobar con Hypothesis que si x es positivo,
# entonces
#    casiIgual(raiz(x)**2, x)
# ---------------------------------------------------------------------

# La propiedad es
@given(st.floats(min_value=0, max_value=100))
def test_cuadradro_de_raiz(x):
    assert casiIgual(raiz(x)**2, x)

# La comprobación es
#    >>> test_cuadradro_de_raiz()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 3.4. Definir, por iteración, la función
#    raizI : (float) -> float
# tal que raizI(x) es la raíz cuadrada de x calculada usando la
# propiedad anterior. Por ejemplo,
#    raizI(9)  ==  3.000000001396984
# ---------------------------------------------------------------------

def raizI(x: float) -> float:
    def aceptable(y: float) -> bool:
        return abs(y*y-x) < 0.00001
    def mejora(y: float) -> float:
        return 0.5*(y+x/y)
    y = 1.0
    while not aceptable(y):
        y = mejora(y)
    return y

# Verificación
# ============

def test_raizI() -> None:
    assert raizI(9) == 3.000000001396984
    print("Verificado")

# La comprobación es
#    >>> test_raizI()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 3.5. Comprobar con Hypothesis que si x es positivo,
# entonces
#    casiIgual(raizI(x)**2, x)
# ---------------------------------------------------------------------

# La propiedad es
@given(st.floats(min_value=0, max_value=100))
def test_cuadrado_de_raizI(x):
    assert casiIgual(raizI(x)**2, x)

# La comprobación es
#    >>> test_cuadrado_de_raizI()
#    >>>

# ---------------------------------------------------------------------
# Ceros de una función                                               --
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 4. Los ceros de una función pueden calcularse mediante el
# método de Newton basándose en las siguientes propiedades:
# + Si b es una aproximación para el punto cero de f, entonces
#   b-f(b)/f'(b) es una mejor aproximación.
# + el límite de la sucesión x_n definida por
#      x_0     = 1
#      x_{n+1} = x_n-f(x_n)/f'(x_n)
#   es un cero de f.
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 4.1. Definir, por recursión, la función
#    puntoCero : (Callable[[float], float]) -> float
# tal que puntoCero(f) es un cero de la función f calculado usando la
# propiedad anterior. Por ejemplo,
#    puntoCero(cos)  ==  1.5707963267949576
# ---------------------------------------------------------------------

def puntoCero(f: Callable[[float], float]) -> float:
    def aceptable(b: float) -> bool:
        return abs(f(b)) < 0.00001
    def mejora(b: float) -> float:
        return b - f(b) / derivadaFina(f, b)
    def aux(g: Callable[[float], float], x: float) -> float:
        if aceptable(x):
            return x
        return aux(g, mejora(x))
    return aux(f, 1)

# Verificación
# ============

def test_puntoCero () -> None:
    assert puntoCero(cos) == 1.5707963267949576
    assert puntoCero(cos) - pi/2 == 6.106226635438361e-14
    assert puntoCero(sin) == -5.8094940533562345e-15
    print("Verificado")

# La comprobación es
#    >>> test_puntoCero()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 4.2. Definir, por iteración, la función
#    puntoCeroI : (Callable[[float], float]) -> float
# tal que puntoCeroI(f) es un cero de la función f calculado usando la
# propiedad anterior. Por ejemplo,
#    puntoCeroI(cos)  ==  1.5707963267949576
# ---------------------------------------------------------------------

def puntoCeroI(f: Callable[[float], float]) -> float:
    def aceptable(b: float) -> bool:
        return abs(f(b)) < 0.00001
    def mejora(b: float) -> float:
        return b - f(b) / derivadaFina(f, b)
    y = 1.0
    while not aceptable(y):
        y = mejora(y)
    return y

# Verificación
# ============

def test_puntoCeroI() -> None:
    assert puntoCeroI(cos) == 1.5707963267949576
    assert puntoCeroI(cos) - pi/2 == 6.106226635438361e-14
    assert puntoCeroI(sin) == -5.8094940533562345e-15
    print("Verificado")

# La comprobación es
#    >>> test_puntoCeroI()
#    Verificado

# ---------------------------------------------------------------------
# Funciones inversas                                                 --
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 5. En este ejercicio se usará la función puntoCero para
# definir la inversa de distintas funciones.
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Ejercicio 5.1. Definir, usando puntoCero, la función
#    raizCuadrada : (float) -> float
# tal que raizCuadrada(x) es la raíz cuadrada de x. Por ejemplo,
#    raizCuadrada(9)  ==  3.000000002941184
# ---------------------------------------------------------------------

def raizCuadrada(a: float) -> float:
    return puntoCero(lambda x : x*x-a)

# Verificación
# ============

def test_raizCuadrada() -> None:
    assert raizCuadrada(9) == 3.000000002941184
    print("Verificado")

# La comprobación es
#    >>> test_raizCuadrada()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 5.2. Comprobar con Hypothesis que si x es positivo,
# entonces
#    casiIgual(raizCuadrada(x)**2, x)
# ---------------------------------------------------------------------

# La propiedad es
@given(st.floats(min_value=0, max_value=100))
def test_cuadrado_de_raizCuadrada(x):
    assert casiIgual(raizCuadrada(x)**2, x)

# La comprobación es
#    >>> test_cuadrado_de_raizCuadrada()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 5.3. Definir, usando puntoCero, la función
#    raizCubica : (float) -> float
# tal que raizCubica(x) es la raíz cúbica de x. Por ejemplo,
#    raizCubica(27) == 3.0000000000196048
# ---------------------------------------------------------------------

def raizCubica(a: float) -> float:
    return puntoCero(lambda x : x*x*x-a)

# Verificación
# ============

def test_raizCubica() -> None:
    assert raizCubica(27) == 3.0000000000196048
    print("Verificado")

# La comprobación es
#    >>> test_raizCubica()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 5.4. Comprobar con Hypothesis que si x es positivo,
# entonces
#    casiIgual(raizCubica(x)**3, x)
# ---------------------------------------------------------------------

# La propiedad es
@given(st.floats(min_value=0, max_value=100))
def test_cubo_de_raizCubica(x):
    assert casiIgual(raizCubica(x)**3, x)

# La comprobación es
#    >>> test_cubo_de_raizCubica()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 5.5. Definir, usando puntoCero, la función
#    arcoseno : (float) -> float
# tal que arcoseno(x) es el arcoseno de x. Por ejemplo,
#    arcoseno(1) == 1.5665489428306574
# ---------------------------------------------------------------------

def arcoseno(a: float) -> float:
    return puntoCero(lambda x : sin(x) - a)

# Verificación
# ============

def test_arcoseno() -> None:
    assert arcoseno(1) == 1.5665489428306574
    print("Verificado")

# La comprobación es
#    >>> test_arcoseno()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 5.6. Comprobar con Hypothesis que si x está entre 0 y 1,
# entonces
#    casiIgual(sin(arcoseno(x)), x)
# ---------------------------------------------------------------------

# La propiedad es
@given(st.floats(min_value=0, max_value=1))
def test_seno_de_arcoseno(x):
    assert casiIgual(sin(arcoseno(x)), x)

# La comprobación es
#    >>> test_seno_de_arcoseno()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 5.7. Definir, usando puntoCero, la función
#    arcocoseno : (float) -> float
# tal que arcoseno(x) es el arcoseno de x. Por ejemplo,
#    arcocoseno(0) == 1.5707963267949576
# ---------------------------------------------------------------------

def arcocoseno(a: float) -> float:
    return puntoCero(lambda x : cos(x) - a)

# Verificación
# ============

def test_arcocoseno() -> None:
    assert arcocoseno(0) == 1.5707963267949576
    print("Verificado")

# La comprobación es
#    >>> test_arcocoseno()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 5.8. Comprobar con Hypothesis que si x está entre 0 y 1,
# entonces
#    casiIgual(cos(arcocoseno(x)), x)
# ---------------------------------------------------------------------

# La propiedad es
@given(st.floats(min_value=0, max_value=1))
def test_coseno_de_arcocoseno(x):
    assert casiIgual(cos(arcocoseno(x)), x)

# La comprobación es
#    >>> test_coseno_de_arcocoseno()
#    >>>

# ---------------------------------------------------------------------
# Ejercicio 5.7. Definir, usando puntoCero, la función
#    inversa : (Callable[[float],float], float) -> float
# tal que inversa(g, x) es el valor de la inversa de g en x. Por
# ejemplo,
#    inversa(lambda x: x**2, 9)  ==  3.000000002941184
# ---------------------------------------------------------------------

def inversa(g: Callable[[float],float], a: float) -> float:
    return puntoCero(lambda x: g(x) - a)

# Verificación
# ============

def test_inversa() -> None:
    assert inversa(lambda x: x**2, 9) == 3.000000002941184
    print("Verificado")

# La comprobación es
#    >>> test_inversa()
#    Verificado

# ---------------------------------------------------------------------
# Ejercicio 5.8. Redefinir, usando inversa, las funciones raizCuadrada,
# raizCubica, arcoseno y arcocoseno.
# ---------------------------------------------------------------------

raizCuadrada2 = partial(inversa, lambda x : x**2)
raizCubica2   = partial(inversa, lambda x : x**3)
arcoseno2     = partial(inversa, sin)
arcocoseno2   = partial(inversa, cos)

# Verificación
# ============

def test_inversas() -> None:
    assert raizCuadrada2(9) == 3.000000002941184
    assert raizCubica2(27) == 3.0000000000196048
    assert arcoseno2(1) == 1.5665489428306574
    assert arcocoseno2(0) == 1.5707963267949576
    print("Verificado")

# La comprobación es
#    >>> test_inversas()
#    Verificado

# Verificación de todo
# ====================

# La comprobación es
#    src> poetry run pytest Calculo_numerico_Diferenciacion_y_metodos_de_Heron_y_de_Newton.py
#    ===== 20 passed in 0.88s =====
