from src.el_TAD_de_las_pilas import (apila, contenidaPila1, contenidaPila2,
                                     contenidaPila3, contenidaPila4,
                                     filtraPila1, filtraPila2, filtraPila3,
                                     filtraPila4, listaApila, listaApila2,
                                     mapPila1, mapPila2, mapPila3, mapPila4,
                                     maxPila1, maxPila2, maxPila3, maxPila4,
                                     nubPila1, nubPila2, nubPila3,
                                     ordenadaPila, ordenadaPila4,
                                     ordenaInserPila1, ordenaInserPila2,
                                     ordenaInserPila3, pertenecePila,
                                     pertenecePila2, pertenecePila3,
                                     pertenecePila4, pilaAlista, pilaAlista2,
                                     pilaAlista3, prefijoPila, prefijoPila2,
                                     prefijoPila3, prefijoPila4, subPila1,
                                     subPila2, subPila3, vacia)


def test_el_TAD_de_las_pilas () -> None:
    assert str(listaApila([3, 2, 5])) == "5 | 2 | 3"
    assert str(listaApila2([3, 2, 5])) == "5 | 2 | 3"
    ej1 = apila(5, apila(2, apila(3, vacia())))
    assert pilaAlista(ej1) == [3, 2, 5]
    assert pilaAlista2(ej1) == [3, 2, 5]
    assert pilaAlista3(ej1) == [3, 2, 5]
    assert str(ej1) == "5 | 2 | 3"
    ej2 = apila(3, apila(4, apila(6, apila(5, vacia()))))
    for filtraPila in [filtraPila1, filtraPila2, filtraPila3,
                       filtraPila4]:
        assert str(filtraPila1(lambda x: x % 2 == 0, ej2)) == "4 | 6"
        assert str(filtraPila1(lambda x: x % 2 == 1, ej2)) == "3 | 5"
        assert str(ej2) == "3 | 4 | 6 | 5"
    ej3 = apila(5, apila(2, apila(7, vacia())))
    for mapPila in [mapPila1, mapPila2, mapPila3, mapPila4]:
        assert str(mapPila(lambda x: x + 1, ej3)) == "6 | 3 | 8"
        assert str(ej3) == "5 | 2 | 7"
    for pertenecePila_ in [pertenecePila, pertenecePila2,
                           pertenecePila3, pertenecePila4]:
        assert pertenecePila_(2, apila(5, apila(2, apila(3, vacia()))))
        assert not pertenecePila_(4, apila(5, apila(2, apila(3, vacia()))))
    ej1a = apila(3, apila(2, vacia()))
    ej2a = apila(3, apila(4, vacia()))
    ej3a = apila(5, apila(2, apila(3, vacia())))
    for contenidaPila in [contenidaPila1, contenidaPila2,
                          contenidaPila3, contenidaPila4]:
        assert contenidaPila(ej1a, ej3a)
        assert not contenidaPila(ej2a, ej3a)
    ej1b = apila(4, apila(2, vacia()))
    ej2b = apila(4, apila(2, apila(5, vacia())))
    ej3b = apila(5, apila(4, apila(2, vacia())))
    for prefijoPila_ in [prefijoPila, prefijoPila2, prefijoPila3,
                         prefijoPila4]:
        assert prefijoPila_(ej1b, ej2b)
        assert not prefijoPila_(ej1b, ej3b)
    ej1c = apila(2, apila(3, vacia()))
    ej2c = apila(7, apila(2, apila(3, apila(5, vacia()))))
    ej3c = apila(2, apila(7, apila(3, apila(5, vacia()))))
    for subPila in [subPila1, subPila2, subPila3]:
        assert subPila(ej1c, ej2c)
        assert not subPila(ej1c, ej3c)
    for ordenadaPila_ in [ordenadaPila, ordenaInserPila2,
                          ordenaInserPila3, ordenadaPila4]:
        assert ordenadaPila(apila(1, apila(5, apila(6, vacia()))))
        assert not ordenadaPila(apila(1, apila(0, apila(6, vacia()))))
    for ordenaInserPila in [ordenaInserPila1, ordenaInserPila2,
                            ordenaInserPila3]:
        assert str(ordenaInserPila(apila(4, apila(1, apila(3, vacia())))))\
            == "1 | 3 | 4"
    ej4 = apila(3, apila(1, apila(3, apila(5, vacia()))))
    for nubPila in [nubPila1, nubPila2, nubPila3]:
        assert str(ej4) == "3 | 1 | 3 | 5"
        assert str(nubPila1(ej4)) == "1 | 3 | 5"
        assert str(ej4) == "3 | 1 | 3 | 5"
    for maxPila in [maxPila1, maxPila2, maxPila3, maxPila4]:
        assert maxPila(apila(3, apila(5, apila(1, vacia())))) == 5
