# tipos_de_datos_algebraicos_Expresiones.py
# Tipos de datos algebraicos: Expresiones.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 1-enero-2023
# ======================================================================

# ---------------------------------------------------------------------
# Introducción                                                       --
# ---------------------------------------------------------------------

# En esta relación se continúan con ejercicios sobre distintos tipos de
# datos algebraicos de la relación anterior. Concretamente,
# + Expresiones aritméticas
#   + Expresiones aritméticas básicas.
#   + Expresiones aritméticas con una variable.
#   + Expresiones aritméticas con varias variables.
#   + Expresiones aritméticas generales.
#   + Expresiones aritméticas con tipo de operaciones.
# + Expresiones vectoriales
#
# Los ejercicios corresponden al tema 9 que se encuentran en
#    https://jaalonso.github.io/cursos/i1m/temas/tema-9.html

# ---------------------------------------------------------------------
# Librerías auxiliares
# ---------------------------------------------------------------------

from dataclasses import dataclass
from enum import Enum
from typing import Callable, TypeVar

A = TypeVar("A")
B = TypeVar("B")

# ---------------------------------------------------------------------
# Ejercicio 6.1. Las expresiones aritméticas básicas pueden
# representarse usando el siguiente tipo de datos
#    @dataclass
#    class Expr1:
#        pass
#
#    @dataclass
#    class C1(Expr1):
#        x: int
#
#    @dataclass
#    class S1(Expr1):
#        x: Expr1
#        y: Expr1
#
#    @dataclass
#    class P1(Expr1):
#        x: Expr1
#        y: Expr1
# Por ejemplo, la expresión 2*(3+7) se representa por
#    P1(C1(2), S1(C1(3), C1(7)))
#
# Definir la función
#    valor : (Expr1) -> int:
# tal que valor(e) es el valor de la expresión aritmética e. Por
# ejemplo,
#    valor(P1(C1(2), S1(C1(3), C1(7))))  ==  20
# ---------------------------------------------------------------------

@dataclass
class Expr1:
    pass

@dataclass
class C1(Expr1):
    x: int

@dataclass
class S1(Expr1):
    x: Expr1
    y: Expr1

@dataclass
class P1(Expr1):
    x: Expr1
    y: Expr1

def valor(e: Expr1) -> int:
    match e:
        case C1(x):
            return x
        case S1(x, y):
            return valor(x) + valor(y)
        case P1(x, y):
            return valor(x) * valor(y)
    assert False

# ---------------------------------------------------------------------
# Ejercicio 6.2. Definir la función
#    aplica : (Callable[[int], int], Expr1) -> Expr1
# tal que aplica(f, e) es la expresión obtenida aplicando la función f
# a cada uno de los números de la expresión e. Por ejemplo,
#    >>> aplica(lambda x: 2 + x, S1(P1(C1(3), C1(5)), P1(C1(6), C1(7))))
#    S1(P1(C1(5), C1(7)), P1(C1(8), C1(9)))
#    >>> aplica(lambda x: 2 * x, S1(P1(C1(3), C1(5)), P1(C1(6), C1(7))))
#    S1(P1(C1(6), C1(10)), P1(C1(12), C1(14)))
# ---------------------------------------------------------------------

def aplica(f: Callable[[int], int], e: Expr1) -> Expr1:
    match e:
        case C1(x):
            return C1(f(x))
        case S1(x, y):
            return S1(aplica(f, x), aplica(f, y))
        case P1(x, y):
            return P1(aplica(f, x), aplica(f, y))
    assert False

# ---------------------------------------------------------------------
# Ejercicio 7.1. Las expresiones aritméticas construidas con una
# variable (denotada por X), los números enteros y las operaciones de
# sumar y multiplicar se pueden representar mediante el tipo de datos
# Expr2 definido por
#    @dataclass
#    class Expr2:
#        pass
#
#    @dataclass
#    class X(Expr2):
#        pass
#
#    @dataclass
#    class C2(Expr2):
#        x: int
#
#    @dataclass
#    class S2(Expr2):
#        x: Expr2
#        y: Expr2
#
#    @dataclass
#    class P2(Expr2):
#        x: Expr2
#        y: Expr2
# Por ejemplo, la expresión X*(13+X) se representa por
#    P2(X(), S2(C2(13), X()))
#
# Definir la función
#    valorE : (Expr2, int) -> int
# tal que valorE(e, n) es el valor de la expresión e cuando se
# sustituye su variable por n. Por ejemplo,
#    valorE(P2(X(), S2(C2(13), X())), 2)  ==  30
# ---------------------------------------------------------------------

@dataclass
class Expr2:
    pass

@dataclass
class X(Expr2):
    pass

@dataclass
class C2(Expr2):
    x: int

@dataclass
class S2(Expr2):
    x: Expr2
    y: Expr2

@dataclass
class P2(Expr2):
    x: Expr2
    y: Expr2

def valorE(e: Expr2, n: int) -> int:
    match e:
        case X():
            return n
        case C2(a):
            return a
        case S2(e1, e2):
            return valorE(e1, n) + valorE(e2, n)
        case P2(e1, e2):
            return valorE(e1, n) * valorE(e2, n)
    assert False

# ---------------------------------------------------------------------
# Ejercicio 7.2. Definir la función
#    numVars : (Expr2) -> int
# tal que numVars(e) es el número de variables en la expresión e. Por
# ejemplo,
#    numVars(C2(3))                     ==  0
#    numVars(X())                       ==  1
#    numVars(P2(X(), S2(C2(13), X())))  ==  2
# ---------------------------------------------------------------------

def numVars(e: Expr2) -> int:
    match e:
        case X():
            return 1
        case C2(_):
            return 0
        case S2(e1, e2):
            return numVars(e1) + numVars(e2)
        case P2(e1, e2):
            return numVars(e1) + numVars(e2)
    assert False


# ---------------------------------------------------------------------
# Ejercicio 8.1. Las expresiones aritméticas con variables pueden
# representarse usando el siguiente tipo de datos
#    @dataclass
#    class Expr3:
#        pass
#
#    @dataclass
#    class C3(Expr3):
#        x: int
#
#    @dataclass
#    class V3(Expr3):
#        x: str
#
#    @dataclass
#    class S3(Expr3):
#        x: Expr3
#        y: Expr3
#
#    @dataclass
#    class P3(Expr3):
#        x: Expr3
#        y: Expr3
#
# Por ejemplo, la expresión 2*(a+5) se representa por
#    P3(C3(2), S3(V3('a'), C3(5)))
#
# Definir la función
#    valor3 : (Expr3, list[tuple[str, int]]) -> int
# tal que valor3(x, e) es el valor de la expresión x en el entorno e (es
# decir, el valor de la expresión donde las variables de x se sustituyen
# por los valores según se indican en el entorno e). Por ejemplo,
#    λ> valor3(P3(C3(2), S3(V3('a'), V3('b'))), [('a', 2), ('b', 5)])
#    14
# ---------------------------------------------------------------------

@dataclass
class Expr3:
    pass

@dataclass
class C3(Expr3):
    x: int

@dataclass
class V3(Expr3):
    x: str

@dataclass
class S3(Expr3):
    x: Expr3
    y: Expr3

@dataclass
class P3(Expr3):
    x: Expr3
    y: Expr3

def valor3(e: Expr3, xs: list[tuple[str, int]]) -> int:
    match e:
        case C3(a):
            return a
        case V3(x):
            return [y for (z, y) in xs if z == x][0]
        case S3(e1, e2):
            return valor3(e1, xs) + valor3(e2, xs)
        case P3(e1, e2):
            return valor3(e1, xs) * valor3(e2, xs)
    assert False

# ---------------------------------------------------------------------
# Ejercicio 8.2. Definir la función
#    sumas : (Expr3) -> int
# tal que sumas(e) es el número de sumas en la expresión e. Por
# ejemplo,
#    sumas(P3(V3('z'), S3(C3(3), V3('x')))) == 1
#    sumas(S3(V3('z'), S3(C3(3), V3('x')))) == 2
#    sumas(P3(V3('z'), P3(C3(3), V3('x')))) == 0
# ---------------------------------------------------------------------

def sumas(e: Expr3) -> int:
    match e:
        case C3(_):
            return 0
        case V3(_):
            return 0
        case S3(e1, e2):
            return 1 + sumas(e1) + sumas(e2)
        case P3(e1, e2):
            return sumas(e1) + sumas(e2)
    assert False

# ---------------------------------------------------------------------
# Ejercicio 8.3. Definir la función
#    sustitucion : (Expr3, list[tuple[str, int]]) -> Expr3
# tal que sustitucion(e s) es la expresión obtenida sustituyendo las
# variables de la expresión e según se indica en la sustitución s. Por
# ejemplo,
#    >>> sustitucion(P3(V3('z'), S3(C3(3), V3('x'))), [('x', 7), ('z', 9)])
#    P3(C3(9), S3(C3(3), C3(7)))
#    >>> sustitucion(P3(V3('z'), S3(C3(3), V3('y'))), [('x', 7), ('z', 9)])
#    P3(C3(9), S3(C3(3), V3('y')))
# ---------------------------------------------------------------------

def sustitucion(e: Expr3, ps: list[tuple[str, int]]) -> Expr3:
    match (e, ps):
        case(e, []):
            return e
        case (V3(c), ps):
            if c == ps[0][0]:
                return C3(ps[0][1])
            return sustitucion(V3(c), ps[1:])
        case (C3(n), _):
            return C3(n)
        case (S3(e1, e2), ps):
            return S3(sustitucion(e1, ps), sustitucion(e2, ps))
        case (P3(e1, e2), ps):
            return P3(sustitucion(e1, ps), sustitucion(e2, ps))
    assert False

# ---------------------------------------------------------------------
# Ejercicio 8.4. Definir la función
#    reducible : (Expr3) -> bool
# tal que reducible(a) se verifica si a es una expresión reducible; es
# decir, contiene una operación en la que los dos operandos son números.
# Por ejemplo,
#    reducible(S3(C3(3), C3(4)))              == True
#    reducible(S3(C3(3), V3('x')))            == False
#    reducible(S3(C3(3), P3(C3(4), C3(5))))   == True
#    reducible(S3(V3('x'), P3(C3(4), C3(5)))) == True
#    reducible(S3(C3(3), P3(V3('x'), C3(5)))) == False
#    reducible(C3(3))                         == False
#    reducible(V3('x'))                       == False
# ---------------------------------------------------------------------

def reducible(e: Expr3) -> bool:
    match e:
        case C3(_):
            return False
        case V3(_):
            return False
        case S3(C3(_), C3(_)):
            return True
        case S3(a, b):
            return reducible(a) or reducible(b)
        case P3(C3(_), C3(_)):
            return True
        case P3(a, b):
            return reducible(a) or reducible(b)
    assert False

# ---------------------------------------------------------------------
# Ejercicio 9. Las expresiones aritméticas generales se pueden definir
# usando el siguiente tipo de datos
#    @dataclass
#    class Expr4:
#        pass
#
#    @dataclass
#    class C4(Expr4):
#        x: int
#
#    @dataclass
#    class Y(Expr4):
#        pass
#
#    @dataclass
#    class S4(Expr4):
#        x: Expr4
#        y: Expr4
#
#    @dataclass
#    class R4(Expr4):
#        x: Expr4
#        y: Expr4
#
#    @dataclass
#    class P4(Expr4):
#        x: Expr4
#        y: Expr4
#
#    @dataclass
#    class E4(Expr4):
#        x: Expr4
#        y: int
# Por ejemplo, la expresión
#    3*y - (y+2)^7
# se puede definir por
#    R4(P4(C4(3), Y()), E4(S4(Y(), C4(2)), 7))
#
# Definir la función
#    maximo : (Expr4, list[int]) -> tuple[int, list[int]]
# tal que maximo(e, xs) es el par formado por el máximo valor de la
# expresión e para los puntos de xs y en qué puntos alcanza el
# máximo. Por ejemplo,
#    >>> maximo(E4(S4(C4(10), P4(R4(C4(1), Y()), Y())), 2), list(range(-3, 4)))
#    (100, [0, 1])
# ---------------------------------------------------------------------

@dataclass
class Expr4:
    pass

@dataclass
class C4(Expr4):
    x: int

@dataclass
class Y(Expr4):
    pass

@dataclass
class S4(Expr4):
    x: Expr4
    y: Expr4

@dataclass
class R4(Expr4):
    x: Expr4
    y: Expr4

@dataclass
class P4(Expr4):
    x: Expr4
    y: Expr4

@dataclass
class E4(Expr4):
    x: Expr4
    y: int

def valor4(e: Expr4, n: int) -> int:
    match e:
        case C4(a):
            return a
        case Y():
            return n
        case S4(e1, e2):
            return valor4(e1, n) + valor4(e2, n)
        case R4(e1, e2):
            return valor4(e1, n) - valor4(e2, n)
        case P4(e1, e2):
            return valor4(e1, n) * valor4(e2, n)
        case E4(e1, m):
            return valor4(e1, n) ** m
    assert False

def maximo(e: Expr4, ns: list[int]) -> tuple[int, list[int]]:
    m = max((valor4(e, n) for n in ns))
    return (m, [n for n in ns if valor4(e, n) == m])

# ---------------------------------------------------------------------
# Ejercicio 10. Las operaciones de suma, resta y  multiplicación se
# pueden representar mediante el siguiente tipo de datos
#    Op = Enum('Op', ['S', 'R', 'M'])
# La expresiones aritméticas con dichas operaciones se pueden
# representar mediante el siguiente tipo de dato algebraico
#    @dataclass
#    class Expr5:
#        pass
#
#    @dataclass
#    class C5(Expr5):
#        x: int
#
#    @dataclass
#    class Ap(Expr5):
#        o: Op
#        x: Expr5
#        y: Expr5
# Por ejemplo, la expresión
#    (7-3)+(2*5)
# se representa por
#    Ap(Op.S, Ap(Op.R, C5(7), C5(3)), Ap(Op.M, C5(2), C5(5)))
#
# Definir la función
#    valorEG : (Expr5) -> int
# tal que valorEG(e) es el valor de la expresión e. Por ejemplo,
#    >>> valorEG(Ap(Op.S, Ap(Op.R, C5(7), C5(3)), Ap(Op.M, C5(2), C5(5))))
#    14
#    >>> valorEG(Ap(Op.M, Ap(Op.R, C5(7), C5(3)), Ap(Op.S, C5(2), C5(5))))
#    28
# ---------------------------------------------------------------------

Op = Enum('Op', ['S', 'R', 'M'])

@dataclass
class Expr5:
    pass

@dataclass
class C5(Expr5):
    x: int

@dataclass
class Ap(Expr5):
    o: Op
    x: Expr5
    y: Expr5

def aplica5(o: Op, x: int, y: int) -> int:
    match o:
        case Op.S:
            return x + y
        case Op.R:
            return x - y
        case Op.M:
            return x * y
    assert False

def valorEG(e: Expr5) -> int:
    match e:
        case C5(x):
            return x
        case Ap(o, e1, e2):
            return aplica5(o, valorEG(e1), valorEG(e2))
    assert False

# ---------------------------------------------------------------------
# Ejercicio 11. Se consideran las expresiones vectoriales formadas por
# un vector, la suma de dos expresiones vectoriales o el producto de un
# entero por una expresión vectorial. El siguiente tipo de dato define
# las expresiones vectoriales
#    @dataclass
#    class ExpV:
#        pass
#
#    @dataclass
#    class Vec(ExpV):
#        x: int
#        y: int
#
#    @dataclass
#    class Sum(ExpV):
#        x: ExpV
#        y: ExpV
#
#    @dataclass
#    class Mul(ExpV):
#        x: int
#        y: ExpV
#
# Definir la función
#    valorEV : (ExpV) -> tuple[int, int]
# tal que valorEV(e) es el valorEV de la expresión vectorial c. Por
# ejemplo,
#    valorEV(Vec(1, 2))                                  ==  (1,2)
#    valorEV(Sum(Vec(1, 2), Vec(3, 4)))                  ==  (4,6)
#    valorEV(Mul(2, Vec(3, 4)))                          ==  (6,8)
#    valorEV(Mul(2, Sum(Vec(1, 2), Vec(3, 4))))          ==  (8,12)
#    valorEV(Sum(Mul(2, Vec(1, 2)), Mul(2, Vec(3, 4))))  ==  (8,12)
# ---------------------------------------------------------------------

@dataclass
class ExpV:
    pass

@dataclass
class Vec(ExpV):
    x: int
    y: int

@dataclass
class Sum(ExpV):
    x: ExpV
    y: ExpV

@dataclass
class Mul(ExpV):
    x: int
    y: ExpV

# 1ª solución
# ===========

def valorEV1(e: ExpV) -> tuple[int, int]:
    match e:
        case Vec(x, y):
            return (x, y)
        case Sum(e1, e2):
            x1, y1 = valorEV1(e1)
            x2, y2 = valorEV1(e2)
            return (x1 + x2, y1 + y2)
        case Mul(n, e):
            x, y = valorEV1(e)
            return (n * x, n * y)
    assert False

# 2ª solución
# ===========

def suma(p: tuple[int, int], q: tuple[int, int]) -> tuple[int, int]:
    a, b = p
    c, d = q
    return (a + c, b + d)

def multiplica(n: int, p: tuple[int, int]) -> tuple[int, int]:
    a, b = p
    return (n * a, n * b)

def valorEV2(e: ExpV) -> tuple[int, int]:
    match e:
        case Vec(x, y):
            return (x, y)
        case Sum(e1, e2):
            return suma(valorEV2(e1), valorEV2(e2))
        case Mul(n, e):
            return multiplica(n, valorEV2(e))
    assert False
