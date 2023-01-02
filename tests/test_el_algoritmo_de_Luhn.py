from src.el_algoritmo_de_Luhn import (digitosInv, doblePosImpar, luhn,
                                      sumaDigitos, ultimoDigito)


def test_luhn() -> None:
    assert digitosInv(320274) == [4, 7, 2, 0, 2, 3]
    assert doblePosImpar([4, 9, 5, 5]) == [4, 18, 5, 10]
    assert doblePosImpar([4, 9, 5, 5, 7]) == [4, 18, 5, 10, 7]
    assert sumaDigitos([10, 5, 18, 4]) == 19
    assert ultimoDigito(123) == 3
    assert ultimoDigito(0) == 0
    assert luhn(5594589764218858)
    assert not luhn(1234567898765432)
