from src.funciones_sobre_cadenas import (esSubcadena, esSubcadena3,
                                         esSubcadenaR, mayusculaInicial,
                                         mayusculaInicialRec, posiciones,
                                         posicionesI, posicionesR,
                                         sumaDigitosC, sumaDigitosI,
                                         sumaDigitosR, titulo, tituloRec)


def test_cadenas() -> None:
    assert sumaDigitosC("SE 2431 X") == 10
    assert sumaDigitosR("SE 2431 X") == 10
    assert sumaDigitosI("SE 2431 X") == 10
    assert mayusculaInicial("sEviLLa") == "Sevilla"
    assert mayusculaInicial("") == ""
    assert mayusculaInicialRec("sEviLLa") == "Sevilla"
    assert mayusculaInicialRec("") == ""
    assert titulo(["eL", "arTE", "DE", "La", "proGraMacion"])\
        == ["El", "Arte", "de", "la", "Programacion"]
    assert tituloRec(["eL", "arTE", "DE", "La", "proGraMacion"])\
        == ["El", "Arte", "de", "la", "Programacion"]
    assert posiciones('a', "Salamamca") == [1, 3, 5, 8]
    assert posicionesR('a', "Salamamca") == [1, 3, 5, 8]
    assert posicionesI('a', "Salamamca") == [1, 3, 5, 8]
    assert esSubcadenaR("casa", "escasamente")
    assert not esSubcadenaR("cante", "escasamente")
    assert esSubcadenaR("", "")
    assert esSubcadena("casa", "escasamente")
    assert not esSubcadena("cante", "escasamente")
    assert esSubcadena("", "")
    assert esSubcadena3("casa", "escasamente")
    assert not esSubcadena3("cante", "escasamente")
    assert esSubcadena3("", "")
