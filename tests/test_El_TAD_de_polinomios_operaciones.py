from src.El_TAD_de_polinomios_operaciones import (cociente, coeficiente,
                                                  creaTermino, creaTermino2,
                                                  densaAdispersa,
                                                  densaAdispersa2,
                                                  densaAdispersa3,
                                                  densaApolinomio,
                                                  densaApolinomio2, derivada,
                                                  dispersaAdensa,
                                                  dispersaAdensa2,
                                                  dispersaAdensa3,
                                                  dispersaApolinomio,
                                                  dispersaApolinomio2,
                                                  divisiblePol, esRaiz, horner,
                                                  horner2, integral,
                                                  integralDef, multEscalar,
                                                  multPol, polinomioAdensa,
                                                  polinomioAdensa2,
                                                  polinomioAdispersa, potencia,
                                                  potencia2, potencia3,
                                                  restaPol, resto, sumaPol,
                                                  sumaPol2, termLider,
                                                  termLider2, valor)
from src.TAD.Polinomio import Polinomio, consPol, polCero


def test_TAD_polinomios_1() -> None:
    for densaAdispersa_ in [densaAdispersa, densaAdispersa2,
                            densaAdispersa3]:
        assert densaAdispersa_([9, 0, 0, 5, 0, 4, 7])\
            == [(6, 9), (3, 5), (1, 4), (0, 7)]
    for dispersaAdensa_ in [dispersaAdensa, dispersaAdensa2,
                            dispersaAdensa3]:
        assert dispersaAdensa_([(6,9),(3,5),(1,4),(0,7)])\
            == [9, 0, 0, 5, 0, 4, 7]
    for dispersaApolinomio_ in [dispersaApolinomio,
                                dispersaApolinomio2]:
        assert str(dispersaApolinomio_([(6, 9), (3, 5), (1, 4), (0, 7)]))\
            == "9*x^6 + 5*x^3 + 4*x + 7"
    ejPol = consPol(6, 9, consPol(3, 5, consPol(1, 4, consPol(0, 7, polCero()))))
    assert polinomioAdispersa(ejPol) == [(6, 9), (3, 5), (1, 4), (0, 7)]
    ejPol = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
    assert coeficiente(2, ejPol) == 5
    assert coeficiente(3, ejPol) == 0
    assert str(densaApolinomio([9, 0, 0, 5, 0, 4, 7]))\
        == "9*x^6 + 5*x^3 + 4*x + 7"
    assert str(densaApolinomio2([9, 0, 0, 5, 0, 4, 7]))\
        == "9*x^6 + 5*x^3 + 4*x + 7"
    ejPol = consPol(6, 9, consPol(3, 5, consPol(1, 4, consPol(0, 7, polCero()))))
    assert polinomioAdensa(ejPol) == [9, 0, 0, 5, 0, 4, 7]
    assert polinomioAdensa2(ejPol) == [9, 0, 0, 5, 0, 4, 7]
    assert str(creaTermino(2, 5)) == "5*x^2"
    assert str(creaTermino2(2, 5)) == "5*x^2"
    ejPol = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
    assert str(termLider(ejPol)) == "x^5"
    assert str(termLider2(ejPol)) == "x^5"
    ejPol1 = consPol(4, 3, consPol(2, -5, consPol(0, 3, polCero())))
    ejPol2 = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
    assert str(sumaPol(ejPol1, ejPol2)) == "x^5 + 3*x^4 + 4*x + 3"
    assert str(sumaPol2(ejPol1, ejPol2)) == "x^5 + 3*x^4 + 4*x + 3"
    ejPol1 = consPol(4, 3, consPol(2, -5, consPol(0, 3, polCero())))
    ejPol2 = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
    assert str(multPol(ejPol1, ejPol2)) ==\
        "3*x^9 + -5*x^7 + 15*x^6 + 15*x^5 + -25*x^4 + -20*x^3 + 15*x^2 + 12*x"
    ejPol = consPol(4, 3, consPol(2, -5, consPol(0, 3, polCero())))
    assert valor(ejPol, 0) == 3
    assert valor(ejPol, 1) == 1
    assert valor(ejPol, -2) == 31
    ejPol = consPol(4, 6, consPol(1, 2, polCero()))
    assert esRaiz(0, ejPol)
    assert not esRaiz(1, ejPol)
    ejPol = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
    assert str(derivada(ejPol)) == "5*x^4 + 10*x + 4"
    ejPol1 = consPol(5,1,consPol(4,5,consPol(2,5,consPol(0,9,polCero()))))
    ejPol2 = consPol(4,3,consPol(2,5,consPol(0,3,polCero())))
    assert str(restaPol(ejPol1, ejPol2)) == "x^5 + 2*x^4 + 6"
    ejPol = consPol(1, 2, consPol(0, 3, polCero()))
    for potencia_ in [potencia, potencia2, potencia3]:
        assert str(potencia_(ejPol, 2)) == "4*x^2 + 12*x + 9"
        assert str(potencia_(ejPol, 3)) == "8*x^3 + 36*x^2 + 54*x + 27"
    ejPol4: Polinomio[float] = consPol(7, 2, consPol(4, 5, consPol(2, 5, polCero())))
    assert str(integral(ejPol4)) == "0.25*x^8 + x^5 + 1.6666666666666667*x^3"
    ejPol5: Polinomio[float] = consPol(7, 2, consPol(4, 5, consPol(2, 5, polCero())))
    assert integralDef(ejPol5, 0, 1) == 2.916666666666667
    ejPol = consPol(1, 2, consPol(0, 3, polCero()))
    assert str(multEscalar(4, ejPol)) == "8*x + 12"

def test_TAD_polinomios_2() -> None:
    pol1: Polinomio[float] = consPol(3, 2, consPol(2, 9, consPol(1, 10, consPol(0, 4, polCero()))))
    pol2: Polinomio[float] = consPol(2, 1, consPol(1, 3, polCero()))
    assert str(cociente(pol1, pol2)) == "2.0*x + 3.0"
    assert str(resto(pol1, pol2)) == "1.0*x + 4"
    pol1a: Polinomio[float] = consPol(2, 8, consPol(1, 14, consPol(0, 3, polCero())))
    pol2a: Polinomio[float] = consPol(1, 2, consPol(0, 3, polCero()))
    pol3a: Polinomio[float] = consPol(2, 6, consPol(1, 2, polCero()))
    assert divisiblePol(pol1a, pol2a)
    assert not divisiblePol(pol1a, pol3a)
    pol1b: Polinomio[float] = consPol(5, 1, consPol(2, 5, consPol(1, 4, polCero())))
    for horner_ in [horner, horner2]:
        assert horner_(pol1b, 0) == 0
        assert horner_(pol1b, 1) == 10
        assert horner_(pol1b, 1.5) == 24.84375
