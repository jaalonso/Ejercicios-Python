from src.el_TAD_de_las_colas import (agrupaColas1, agrupaColas2,
                                     algunoVerifica1, algunoVerifica2,
                                     algunoVerifica3, algunoVerifica4,
                                     algunoVerifica5, colaAlista, colaAlista2,
                                     colaAlista3, contenidaCola1,
                                     contenidaCola2, contenidaCola3,
                                     contenidaCola4, extiendeCola,
                                     extiendeCola2, extiendeCola3,
                                     extiendeCola4, extiendeCola5, inserta,
                                     intercalaColas, intercalaColas2,
                                     intercalaColas3, intercalaColas4,
                                     intercalaColas5, listaAcola, listaAcola2,
                                     longitudCola1, longitudCola2,
                                     longitudCola3, longitudCola4,
                                     longitudCola5, maxCola1, maxCola2,
                                     maxCola3, maxCola4, ordenadaCola,
                                     ordenadaCola2, ordenadaCola3,
                                     ordenadaCola4, perteneceCola,
                                     perteneceCola2, perteneceCola3,
                                     perteneceCola4, prefijoCola, prefijoCola2,
                                     prefijoCola3, prefijoCola4, subCola1,
                                     subCola2, subCola3, todosVerifican1,
                                     todosVerifican2, todosVerifican3,
                                     todosVerifican4, todosVerifican5,
                                     ultimoCola, ultimoCola2, ultimoCola3,
                                     ultimoCola4, ultimoCola5, vacia)


def test_colas() -> None:
    assert str(listaAcola([3, 2, 5])) == "3 | 2 | 5"
    assert str(listaAcola2([3, 2, 5])) == "3 | 2 | 5"
    ej1 = inserta(5, inserta(2, inserta(3, vacia())))
    assert colaAlista(ej1) == [3, 2, 5]
    assert colaAlista2(ej1) == [3, 2, 5]
    assert colaAlista3(ej1) == [3, 2, 5]
    assert str(ej1) == "3 | 2 | 5"
    for ultimoCola_ in [ultimoCola, ultimoCola2, ultimoCola3,
                        ultimoCola4, ultimoCola5]:
        assert ultimoCola_(inserta(3, inserta(5, inserta(2, vacia())))) == 3
        assert ultimoCola_(inserta(2, vacia())) == 2
    for longitudCola in [longitudCola1, longitudCola2, longitudCola3,
                         longitudCola4, longitudCola5]:
        assert longitudCola(inserta(4, inserta(2, inserta(5, vacia()))))\
            == 3
    for todosVerifican in [todosVerifican1, todosVerifican2,
                           todosVerifican3, todosVerifican4,
                           todosVerifican5]:
        assert todosVerifican(lambda x: x > 0, inserta(3, inserta(2, vacia())))
        assert not todosVerifican(lambda x: x > 0, inserta(3, inserta(-2, vacia())))
    for algunoVerifica in [algunoVerifica1, algunoVerifica2,
                           algunoVerifica3, algunoVerifica4,
                           algunoVerifica5]:
        assert algunoVerifica(lambda x: x > 0, inserta(-3, inserta(2, vacia())))
        assert not algunoVerifica(lambda x: x > 0, inserta(-3, inserta(-2, vacia())))
    ej3 = inserta(3, inserta(2, vacia()))
    ej4 = inserta(5, inserta(3, inserta(4, vacia())))
    for extiendeCola_ in [extiendeCola, extiendeCola2, extiendeCola3,
                          extiendeCola4, extiendeCola5]:
        assert str(extiendeCola_(ej3, ej4)) == "2 | 3 | 4 | 3 | 5"
        assert str(extiendeCola_(ej4, ej3)) == "4 | 3 | 5 | 2 | 3"
    ej_7_1 = inserta(3, inserta(5, vacia()))
    ej_7_2 = inserta(0, inserta(7, inserta(4, inserta(9, vacia()))))
    for intercalaColas_ in [intercalaColas, intercalaColas2,
                            intercalaColas3, intercalaColas4,
                            intercalaColas5]:
        assert str(intercalaColas_(ej_7_1, ej_7_2)) == "5 | 9 | 3 | 4 | 7 | 0"
        assert str(intercalaColas_(ej_7_2, ej_7_1)) == "9 | 5 | 4 | 3 | 7 | 0"
    ej_8_1 = inserta(2, inserta(5, vacia()))
    ej_8_2 = inserta(3, inserta(7, inserta(4, vacia())))
    ej_8_3 = inserta(9, inserta(0, inserta(1, inserta(6, vacia()))))
    for agrupaColas in [agrupaColas1, agrupaColas2]:
        assert str(agrupaColas([ej_8_1])) == "5 | 2"
        assert str(agrupaColas([ej_8_1, ej_8_2])) == "5 | 4 | 2 | 7 | 3"
        assert str(agrupaColas([ej_8_1, ej_8_2, ej_8_3]))\
            == "5 | 6 | 4 | 1 | 2 | 0 | 7 | 9 | 3"
    for perteneceCola_ in [perteneceCola, perteneceCola2,
                           perteneceCola3, perteneceCola4]:
        assert perteneceCola_(2, inserta(5, inserta(2, inserta(3, vacia()))))
        assert not perteneceCola_(4, inserta(5, inserta(2, inserta(3, vacia()))))
    ej_9_1 = inserta(3, inserta(2, vacia()))
    ej_9_2 = inserta(3, inserta(4, vacia()))
    ej_9_3 = inserta(5, inserta(2, inserta(3, vacia())))
    for contenidaCola in [contenidaCola1, contenidaCola2,
                          contenidaCola3, contenidaCola4]:
        assert contenidaCola(ej_9_1, ej_9_3)
        assert not contenidaCola(ej_9_2, ej_9_3)
    ej_11_1 = inserta(4, inserta(2, vacia()))
    ej_11_2 = inserta(5, inserta(4, inserta(2, vacia())))
    ej_11_3 = inserta(5, inserta(2, inserta(4, vacia())))
    for prefijoCola_ in [prefijoCola, prefijoCola2, prefijoCola3,
                         prefijoCola4]:
        assert prefijoCola_(ej_11_1, ej_11_2)
        assert not prefijoCola_(ej_11_1, ej_11_3)
    ej_12_1 = inserta(2, inserta(3, vacia()))
    ej_12_2 = inserta(7, inserta(2, inserta(3, inserta(5, vacia()))))
    ej_12_3 = inserta(2, inserta(7, inserta(3, inserta(5, vacia()))))
    for subCola in [subCola1, subCola2, subCola3]:
        assert subCola(ej_12_1, ej_12_2)
        assert not subCola(ej_12_1, ej_12_3)
    for ordenadaCola_ in [ordenadaCola, ordenadaCola2, ordenadaCola3,
                          ordenadaCola4]:
        assert ordenadaCola(inserta(6, inserta(5, inserta(1, vacia()))))
        assert not ordenadaCola(inserta(1, inserta(0, inserta(6, vacia()))))
    for maxCola in [maxCola1, maxCola2, maxCola3, maxCola4]:
        assert maxCola(inserta(3, inserta(5, inserta(1, vacia())))) == 5
