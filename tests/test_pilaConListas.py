from src.pilaConListas import Pila, apila, cima, desapila, esVacia, vacia


def test_pila() -> None:
    assert str(vacia()) == '-'
    assert str(apila(4, apila(3, apila(2, apila(5, vacia())))))\
        == '4 | 3 | 2 | 5'
    assert cima(apila(4, apila(3, apila(2, apila(5, vacia())))))\
        == 4
    assert str(desapila(apila(4, apila(3, apila(2, apila(5, vacia()))))))\
        == '3 | 2 | 5'
    assert not esVacia(apila(4, apila(3, apila(2, apila(5, vacia())))))
    assert esVacia(vacia())
    p: Pila[int] = Pila()
    assert str(p) == '-'
    p.apila(5)
    p.apila(2)
    p.apila(3)
    p.apila(4)
    assert str(p) == '4 | 3 | 2 | 5'
    assert p.cima() == 4
    p.desapila()
    assert str(p) == '3 | 2 | 5'
    assert not p.esVacia()
    q: Pila[int] = Pila()
    assert q.esVacia()
