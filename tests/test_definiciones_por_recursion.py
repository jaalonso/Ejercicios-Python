from src.definiciones_por_recursion import (coge, concatenaListas, digitosC,
                                            digitosR, listaNumeroC,
                                            listaNumeroR, mayorExponenteC,
                                            mayorExponenteR, mcd, pertenece,
                                            potencia, sumaDeCuadradosC,
                                            sumaDeCuadradosR, sumaDigitosNR,
                                            sumaDigitosR)


def test_recursion() -> None:
    assert potencia(2, 3) == 8
    assert mcd(30, 45) == 15
    assert mcd(45, 30) == 15
    assert pertenece(3, [2, 3, 5]) is True
    assert pertenece(4, [2, 3, 5]) is False
    assert concatenaListas([[1, 3], [5], [2, 4, 6]]) == [1, 3, 5, 2, 4, 6]
    assert coge(3, list(range(4, 12))) == [4, 5, 6]
    assert sumaDeCuadradosR(3) == 14
    assert sumaDeCuadradosR(100) == 338350
    assert sumaDeCuadradosC(3) == 14
    assert sumaDeCuadradosC(100) == 338350
    assert digitosR(320274) == [3, 2, 0, 2, 7, 4]
    assert digitosC(320274) == [3, 2, 0, 2, 7, 4]
    assert sumaDigitosR(3) == 3
    assert sumaDigitosR(2454) == 15
    assert sumaDigitosR(20045) == 11
    assert sumaDigitosNR(3) == 3
    assert sumaDigitosNR(2454) == 15
    assert sumaDigitosNR(20045) == 11
    assert listaNumeroR([5]) == 5
    assert listaNumeroR([1, 3, 4, 7]) == 1347
    assert listaNumeroR([0, 0, 1]) == 1
    assert listaNumeroC([5]) == 5
    assert listaNumeroC([1, 3, 4, 7]) == 1347
    assert listaNumeroC([0, 0, 1]) == 1
    assert mayorExponenteR(2, 8) == 3
    assert mayorExponenteR(2, 9) == 0
    assert mayorExponenteR(5, 100) == 2
    assert mayorExponenteR(2, 60) == 2
    assert mayorExponenteC(2, 8) == 3
    assert mayorExponenteC(2, 9) == 0
    assert mayorExponenteC(5, 100) == 2
    assert mayorExponenteC(2, 60) == 2
