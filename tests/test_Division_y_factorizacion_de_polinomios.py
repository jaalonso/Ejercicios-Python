from src.Division_y_factorizacion_de_polinomios import (cocienteRuffini,
                                                        esRaizRuffini,
                                                        factorizacion,
                                                        raicesRuffini,
                                                        restoRuffini,
                                                        ruffiniDensa,
                                                        terminoIndep)
from src.TAD.Polinomio import consPol, polCero


def test_division_polinomios() -> None:
    ejPol1 = consPol(4, 3, consPol(2, 5, consPol(0, 3, polCero())))
    ejPol2 = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
    assert terminoIndep(ejPol1) == 3
    assert terminoIndep(ejPol2) == 0
    ejPol1 = consPol(4, 3, consPol(2, -5, consPol(0, 3, polCero())))
    assert ruffiniDensa(2, [1, 2, -1, -2]) == [1, 4, 7, 12]
    assert ruffiniDensa(1, [1, 2, -1, -2]) == [1, 3, 2, 0]
    ejPol = consPol(3, 1, consPol(2, 2, consPol(1, -1, consPol(0, -2, polCero()))))
    assert str(cocienteRuffini(2, ejPol)) == "x^2 + 4*x + 7"
    assert str(cocienteRuffini(-2, ejPol)) == "x^2 + -1"
    assert str(cocienteRuffini(3, ejPol)) == "x^2 + 5*x + 14"
    assert restoRuffini(2, ejPol) == 12
    assert restoRuffini(-2, ejPol) == 0
    assert restoRuffini(3, ejPol) == 40
    ejPol = consPol(4, 6, consPol(1, 2, polCero()))
    assert esRaizRuffini(0, ejPol)
    assert not esRaizRuffini(1, ejPol)

    assert raicesRuffini(ejPol1) == []
    ejPol2 = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
    assert raicesRuffini(ejPol2) == [0, -1]
    ejPol3 = consPol(4, 6, consPol(1, 2, polCero()))
    assert raicesRuffini(ejPol3) == [0]
    ejPol4 = consPol(3, 1, consPol(2, 2, consPol(1, -1, consPol(0, -2, polCero()))))
    assert raicesRuffini(ejPol4) == [1, -1, -2]
    ejPol1 = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
    assert list(map(str, factorizacion(ejPol1))) \
        == ["1*x", "1*x + 1", "x^3 + -1*x^2 + 1*x + 4"]
    ejPol2 = consPol(3, 1, consPol(2, 2, consPol(1, -1, consPol(0, -2, polCero()))))
    assert list(map(str, factorizacion(ejPol2))) \
        == ["1*x + -1", "1*x + 1", "1*x + 2", "1"]
