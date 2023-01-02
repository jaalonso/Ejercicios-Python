# funciones_sobre_cadenas.py
# Funciones sobre cadenas.
# José A. Alonso Jiménez <https://jaalonso.github.io>
# Sevilla, 22-diciembre-2022
# ======================================================================

# ---------------------------------------------------------------------
# Importación de librerías auxiliares                                --
# ---------------------------------------------------------------------

from sys import setrecursionlimit

from hypothesis import given
from hypothesis import strategies as st

setrecursionlimit(10**6)

# ---------------------------------------------------------------------
# Ejercicio 1.1. Definir, por comprensión, la función
#    sumaDigitosC : (str) -> int
# tal que sumaDigitosC(xs) es la suma de los dígitos de la cadena
# xs. Por ejemplo,
#    sumaDigitosC("SE 2431 X")  ==  10
# ---------------------------------------------------------------------

def sumaDigitosC(xs: str) -> int:
    return sum((int(x) for x in xs if x.isdigit()))

# ---------------------------------------------------------------------
# Ejercicio 1.2. Definir, por recursión, la función
#    sumaDigitosR : (str) -> int
# tal que sumaDigitosR(xs) es la suma de los dígitos de la cadena
# xs. Por ejemplo,
#    sumaDigitosR("SE 2431 X")  ==  10
# ---------------------------------------------------------------------

def sumaDigitosR(xs: str) -> int:
    if xs:
        if xs[0].isdigit():
            return int(xs[0]) + sumaDigitosR(xs[1:])
        return sumaDigitosR(xs[1:])
    return 0

# ---------------------------------------------------------------------
# Ejercicio 1.3. Definir, por iteración, la función
#    sumaDigitosI : (str) -> int
# tal que sumaDigitosI(xs) es la suma de los dígitos de la cadena
# xs. Por ejemplo,
#    sumaDigitosI("SE 2431 X")  ==  10
# ---------------------------------------------------------------------

def sumaDigitosI(xs: str) -> int:
    r = 0
    for x in xs:
        if x.isdigit():
            r = r + int(x)
    return r

# ---------------------------------------------------------------------
# Ejercicio 1.4. Comprobar con QuickCheck que las tres definiciones son
# equivalentes.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.text(alphabet=st.characters(min_codepoint=32, max_codepoint=127)))
def test_sumaDigitos(xs: str) -> None:
    r = sumaDigitosC(xs)
    assert sumaDigitosR(xs) == r
    assert sumaDigitosI(xs) == r

# ---------------------------------------------------------------------
# Ejercicio 2.1. Definir, por comprensión, la función
#    mayusculaInicial : (str) -> str
# tal que mayusculaInicial(xs) es la palabra xs con la letra inicial
# en mayúscula y las restantes en minúsculas. Por ejemplo,
#    mayusculaInicial("sEviLLa")  ==  "Sevilla"
#    mayusculaInicial("")         ==  ""
# ---------------------------------------------------------------------

def mayusculaInicial(xs: str) -> str:
    if xs:
        return "".join([xs[0].upper()] + [y.lower() for y in xs[1:]])
    return ""

# ---------------------------------------------------------------------
# Ejercicio 2.2. Definir, por recursión, la función
#    mayusculaInicialRec : (str) -> str
# tal que mayusculaInicialRec(xs) es la palabra xs con la letra inicial
# en mayúscula y las restantes en minúsculas. Por ejemplo,
#    mayusculaInicialRec("sEviLLa")  ==  "Sevilla"
#    mayusculaInicialRec("")         ==  ""
# ---------------------------------------------------------------------

def mayusculaInicialRec(xs: str) -> str:
    def aux(ys: str) -> str:
        if ys:
            return ys[0].lower() + aux(ys[1:])
        return ""
    if xs:
        return "".join(xs[0].upper() + aux(xs[1:]))
    return ""

# ---------------------------------------------------------------------
# Ejercicio 2.3. Comprobar con Hypothesis que ambas definiciones son
# equivalentes.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.text())
def test_mayusculaInicial(xs: str) -> None:
    assert mayusculaInicial(xs) == mayusculaInicialRec(xs)

# ---------------------------------------------------------------------
# Ejercicio 3.1. Se consideran las siguientes reglas de mayúsculas
# iniciales para los títulos:
#    * la primera palabra comienza en mayúscula y
#    * todas las palabras que tienen 4 letras como mínimo empiezan
#      con mayúsculas
#
# Definir, por comprensión, la función
#    titulo : (list[str]) -> list[str]
# tal que titulo(ps) es la lista de las palabras de ps con
# las reglas de mayúsculas iniciales de los títulos. Por ejemplo,
#    >>> titulo(["eL", "arTE", "DE", "La", "proGraMacion"])
#    ["El", "Arte", "de", "la", "Programacion"]
# ---------------------------------------------------------------------


# (minuscula xs) es la palabra xs en minúscula.
def minuscula(xs: str) -> str:
    return xs.lower()

# (transforma p) es la palabra p con mayúscula inicial si su longitud
# es mayor o igual que 4 y es p en minúscula en caso contrario
def transforma(p: str) -> str:
    if len(p) >= 4:
        return mayusculaInicial(p)
    return minuscula(p)

def titulo(ps: list[str]) -> list[str]:
    if ps:
        return [mayusculaInicial(ps[0])] + [transforma(q) for q in ps[1:]]
    return []

# ---------------------------------------------------------------------
# Ejercicio 3.2. Definir, por recursión, la función
#    tituloRec : (list[str]) -> list[str]
# tal que tituloRec(ps) es la lista de las palabras de ps con
# las reglas de mayúsculas iniciales de los títulos. Por ejemplo,
#    >>> tituloRec(["eL", "arTE", "DE", "La", "proGraMacion"])
#    ["El", "Arte", "de", "la", "Programacion"]
# ---------------------------------------------------------------------

def tituloRec(ps: list[str]) -> list[str]:
    def aux(qs: list[str]) -> list[str]:
        if qs:
            return [transforma(qs[0])] + aux(qs[1:])
        return []
    if ps:
        return [mayusculaInicial(ps[0])] + aux(ps[1:])
    return []

# ---------------------------------------------------------------------
# Ejercicio 3.3. Comprobar con Hypothesis que ambas definiciones son
# equivalentes.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.lists(st.text()))
def test_titulo(ps: list[str]) -> None:
    assert titulo(ps) == tituloRec(ps)

# ---------------------------------------------------------------------
# Ejercicio 4.1. Definir, por comprensión, la función
#    posiciones : (str, str) -> list[int]
# tal que posiciones(x, ys) es la lista de la posiciones del carácter x
# en la cadena ys. Por ejemplo,
#    posiciones('a', "Salamamca")   ==  [1,3,5,8]
# ---------------------------------------------------------------------

def posiciones(x: str, ys: str) -> list[int]:
    return [n for (n, y) in enumerate(ys) if y == x]

# ---------------------------------------------------------------------
# Ejercicio 4.2. Definir, por recursión, la función
#    posicionesR : (str, str) -> list[int]
# tal que posicionesR(x, ys) es la lista de la posiciones del carácter x
# en la cadena ys. Por ejemplo,
#    posicionesR('a', "Salamamca")   ==  [1,3,5,8]
# ---------------------------------------------------------------------

def posicionesR(x: str, ys: str) -> list[int]:
    def aux(a: str, bs: str, n: int) -> list[int]:
        if bs:
            if a == bs[0]:
                return [n] + aux(a, bs[1:], n + 1)
            return aux(a, bs[1:], n + 1)
        return []
    return aux(x, ys, 0)

# ---------------------------------------------------------------------
# Ejercicio 4.3. Definir, por iteración, la función
#    posicionesI : (str, str) -> list[int]
# tal que posicionesI(x ,ys) es la lista de la posiciones del carácter x
# en la cadena ys. Por ejemplo,
#    posicionesI('a', "Salamamca")   ==  [1,3,5,8]
# ---------------------------------------------------------------------

def posicionesI(x: str, ys: str) -> list[int]:
    r = []
    for n, y in enumerate(ys):
        if x == y:
            r.append(n)
    return r

# ---------------------------------------------------------------------
# Ejercicio 4.3. Comprobar con Hypothesis que las tres definiciones son
# equivalentes.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.text(), st.text())
def test_posiciones(x: str, ys: str) -> None:
    r = posiciones(x, ys)
    assert posicionesR(x, ys) == r
    assert posicionesI(x, ys) == r

# ---------------------------------------------------------------------
# Ejercicio 5.1. Definir, por recursión, la función
#    esSubcadenaR : (str, str) -> bool
# tal que esSubcadenaR(xs ys) se verifica si xs es una subcadena de ys.
# Por ejemplo,
#    esSubcadenaR("casa", "escasamente")   ==  True
#    esSubcadenaR("cante", "escasamente")  ==  False
#    esSubcadenaR("", "")                  ==  True
# ---------------------------------------------------------------------

def esSubcadenaR(xs: str, ys: str) -> bool:
    if not xs:
        return True
    if not ys:
        return False
    return ys.startswith(xs) or esSubcadenaR(xs, ys[1:])

# ---------------------------------------------------------------------
# Ejercicio 5.2. Definir, por comprensión, la función
#    esSubcadena : (str, str) -> bool
# tal que esSubcadena(xs ys) se verifica si xs es una subcadena de ys.
# Por ejemplo,
#    esSubcadena("casa", "escasamente")   ==  True
#    esSubcadena("cante", "escasamente")  ==  False
#    esSubcadena("", "")                  ==  True
# ---------------------------------------------------------------------

# sufijos(xs) es la lista de sufijos de xs. Por ejemplo,
#    sufijos("abc")  ==  ['abc', 'bc', 'c', '']
def sufijos(xs: str) -> list[str]:
    return [xs[i:] for i in range(len(xs) + 1)]

def esSubcadena(xs: str, ys: str) -> bool:
    return any(zs.startswith(xs) for zs in sufijos(ys))

# Se puede definir por
def esSubcadena3(xs: str, ys: str) -> bool:
    return xs in ys

# ---------------------------------------------------------------------
# Ejercicio 5.3. Comprobar con Hypothesis que las tres definiciones son
# equivalentes.
# ---------------------------------------------------------------------

# La propiedad es
@given(st.text(), st.text())
def test_esSubcadena(xs: str, ys: str) -> None:
    r = esSubcadenaR(xs, ys)
    assert esSubcadena(xs, ys) == r
    assert esSubcadena3(xs, ys) == r

# ---------------------------------------------------------------------
# Comprobación de las propiedades
# ---------------------------------------------------------------------

# La comprobación es
#    src> poetry run pytest -q funciones_sobre_cadenas.py
#    1 passed in 0.41s
