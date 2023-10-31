from src.TAD.PolRepDispersa import (Polinomio, coefLider, consPol, esPolCero,
                                    grado, polCero, polinomioAleatorio,
                                    restoPol)


def test_PolRepDispersa() -> None:
    assert str(Polinomio()) == "0"
    ejPol1 = Polinomio().consPol(0, 3).consPol(2, -5).consPol(4, 3)
    assert str(ejPol1) == "3*x^4 + -5*x^2 + 3"
    ejPol2 = Polinomio().consPol(1, 4).consPol(2, 5).consPol(5, 1)
    assert str(ejPol2) == "x^5 + 5*x^2 + 4*x"
    ejPol3 = Polinomio().consPol(1, 2).consPol(4, 6)
    assert str(ejPol3) == "6*x^4 + 2*x"
    assert Polinomio().esPolCero()
    assert not ejPol1.esPolCero()
    assert str(ejPol2.consPol(3, 0)) == "x^5 + 5*x^2 + 4*x"
    assert str(Polinomio().consPol(3, 2)) == "2*x^3"
    assert str(ejPol2.consPol(6, 7)) == "7*x^6 + x^5 + 5*x^2 + 4*x"
    assert str(ejPol2.consPol(4, 7)) == "x^5 + 7*x^4 + 5*x^2 + 4*x"
    assert str(ejPol2.consPol(5, 7)) == "8*x^5 + 5*x^2 + 4*x"
    assert ejPol3.grado() == 4
    assert str(ejPol3.restoPol()) == "2*x"
    assert str(ejPol2.restoPol()) == "5*x^2 + 4*x"
    assert str(polCero()) == "0"
    ejPol1a = consPol(4, 3, consPol(2, -5, consPol(0, 3, polCero())))
    assert str(ejPol1a) == "3*x^4 + -5*x^2 + 3"
    ejPol2a = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
    assert str(ejPol2a) == "x^5 + 5*x^2 + 4*x"
    ejPol3a = consPol(4, 6, consPol(1, 2, polCero()))
    assert str(ejPol3a) == "6*x^4 + 2*x"
    assert esPolCero(polCero())
    assert not esPolCero(ejPol1a)
    assert str(consPol(3, 9, ejPol2a)) == "x^5 + 9*x^3 + 5*x^2 + 4*x"
    assert str(consPol(3, 2, polCero())) == "2*x^3"
    assert str(consPol(6, 7, ejPol2a)) == "7*x^6 + x^5 + 5*x^2 + 4*x"
    assert str(consPol(4, 7, ejPol2a)) == "x^5 + 7*x^4 + 5*x^2 + 4*x"
    assert str(consPol(5, 7, ejPol2a)) == "8*x^5 + 5*x^2 + 4*x"
    assert grado(ejPol3a) == 4
    assert str(restoPol(ejPol3a)) == "2*x"
    assert str(restoPol(ejPol2a)) == "5*x^2 + 4*x"
