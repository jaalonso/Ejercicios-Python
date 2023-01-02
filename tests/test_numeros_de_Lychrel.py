from itertools import islice

from src.numeros_de_Lychrel import (busquedaDeCapicua, capicuaFinal, esCapicua,
                                    inverso, menorDeOrdenMayor,
                                    menoresdDeOrdenMayor, orden, ordenEntre,
                                    ordenMayor, siguiente)


def test_lychrel() -> None:
    assert esCapicua(252)
    assert not esCapicua(253)
    assert inverso(253) == 352
    assert siguiente(253) == 605
    assert busquedaDeCapicua(253) == [253, 605, 1111]
    assert capicuaFinal(253) == 1111
    assert orden(253) == 2
    assert ordenMayor(1186060307891929990, 2)
    assert list(islice(ordenEntre(10, 11), 5))\
        == [829, 928, 9059, 9149, 9239]
    assert menorDeOrdenMayor(2) == 19
    assert menorDeOrdenMayor(20) == 89
    assert menoresdDeOrdenMayor(5)\
        == [(1, 10), (2, 19), (3, 59), (4, 69), (5, 79)]
