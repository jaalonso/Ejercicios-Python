from src.TAD.ColaDePrioridadConListas import (CPrioridad, esVacia, inserta,
                                              primero, resto, vacia)


def test_CPrioridad() -> None:
    c: CPrioridad[int] = CPrioridad()
    assert str(c) == "-"
    c.inserta(5)
    c.inserta(2)
    c.inserta(3)
    c.inserta(4)
    assert str(c) == "2 | 3 | 4 | 5"
    assert c.primero() == 2
    c.resto()
    assert str(c) == "3 | 4 | 5"
    assert not c.esVacia()
    c = CPrioridad()
    assert c.esVacia()
    assert str(vacia()) == "-"
    assert str(inserta(4, inserta(3, inserta(2, inserta(5, vacia()))))) \
        == "2 | 3 | 4 | 5"
    assert primero(inserta(4, inserta(3, inserta(2, inserta(5, vacia()))))) \
        == 2
    assert str(resto(inserta(4, inserta(3, inserta(2, inserta(5, vacia()))))))\
        == "3 | 4 | 5"
    assert not esVacia(inserta(4, inserta(3, inserta(2, inserta(5, vacia())))))
    assert esVacia(vacia())
