from src.operaciones_con_conjuntos import (algunos, algunos2, algunos3,
                                           algunos4, cardinal, cardinal2,
                                           cardinal3, cardinal4,
                                           conjuntoAlista, conjuntoAlista2,
                                           conjuntoAlista3, diferencia,
                                           diferencia2, diferencia3,
                                           diferencia4, diferenciaSimetrica,
                                           diferenciaSimetrica2,
                                           diferenciaSimetrica3, disjuntos,
                                           disjuntos2, disjuntos3, disjuntos4,
                                           disjuntos5, divide, divide2,
                                           divide3, divide4, filtra, filtra2,
                                           filtra3, filtra4, inserta,
                                           interseccion, interseccion2,
                                           interseccion3, interseccion4,
                                           interseccionG, interseccionG2,
                                           interseccionG3, listaAconjunto,
                                           listaAconjunto2, listaAconjunto3,
                                           mapC, mapC2, mapC3, mapC4,
                                           particion, particion2, particion3,
                                           productoC, productoC2, productoC3,
                                           productoC4, productoC5, subconjunto,
                                           subconjunto2, subconjunto3,
                                           subconjunto4, subconjunto5,
                                           subconjuntoPropio, todos, todos2,
                                           todos3, todos4, union, union2,
                                           union3, union4, unionG, unionG2,
                                           unionG3, unitario, vacio)


def test_operaciones_con_conjuntos() -> None:
    for listaAconjunto_ in [listaAconjunto, listaAconjunto2,
                            listaAconjunto3]:
        assert str(listaAconjunto_([3, 2, 5])) == "{2, 3, 5}"
    for conjuntoAlista_ in [conjuntoAlista, conjuntoAlista2,
                            conjuntoAlista3]:
        assert conjuntoAlista_(inserta(5, inserta(2, inserta(3, vacio()))))\
            == [2, 3, 5]
    ej4_1 = inserta(5, inserta(2, vacio()))
    ej4_2 = inserta(3, inserta(2, inserta(5, vacio())))
    ej4_3 = inserta(3, inserta(4, inserta(5, vacio())))
    for subconjunto_ in [subconjunto, subconjunto2, subconjunto3,
                         subconjunto4, subconjunto5]:
        assert subconjunto_(ej4_1, ej4_2)
        assert not subconjunto_(ej4_1, ej4_3)
    ej5_1 = inserta(5, inserta(2, vacio()))
    ej5_2 = inserta(3, inserta(2, inserta(5, vacio())))
    ej5_3 = inserta(3, inserta(4, inserta(5, vacio())))
    ej5_4 = inserta(2, inserta(5, vacio()))
    assert subconjuntoPropio(ej5_1, ej5_2)
    assert not subconjuntoPropio(ej5_1, ej5_3)
    assert not subconjuntoPropio(ej5_1, ej5_4)
    assert str(unitario(5)) == "{5}"
    for cardinal_ in [cardinal, cardinal2, cardinal3, cardinal4]:
        assert cardinal_(inserta(4, inserta(5, vacio()))) == 2
        assert cardinal_(inserta(4, inserta(5, inserta(4, vacio())))) == 2
    ej8_1 = inserta(3, inserta(5, vacio()))
    ej8_2 = inserta(4, inserta(3, vacio()))
    for union_ in [union, union2, union3, union4]:
        assert str(union_(ej8_1, ej8_2)) == "{3, 4, 5}"
    ej9_1 = inserta(3, inserta(5, vacio()))
    ej9_2 = inserta(5, inserta(6, vacio()))
    ej9_3 = inserta(3, inserta(6, vacio()))
    for unionG_ in [unionG, unionG2, unionG3]:
        assert str(unionG_([ej9_1, ej9_2, ej9_3])) == "{3, 5, 6}"
    ej10_1 = inserta(3, inserta(5, inserta(2, vacio())))
    ej10_2 = inserta(2, inserta(4, inserta(3, vacio())))
    for interseccion_ in [interseccion, interseccion2, interseccion3,
                          interseccion4]:
        assert str(interseccion_(ej10_1, ej10_2)) == "{2, 3}"
    ej11_1 = inserta(2, inserta(3, inserta(5, vacio())))
    ej11_2 = inserta(5, inserta(2, inserta(7, vacio())))
    ej11_3 = inserta(3, inserta(2, inserta(5, vacio())))
    for interseccionG_ in [interseccionG, interseccionG2,
                           interseccionG3]:
        assert str(interseccionG_([ej11_1, ej11_2, ej11_3])) == "{2, 5}"
    ej12_1 = inserta(2, inserta(5, vacio()))
    ej12_2 = inserta(4, inserta(3, vacio()))
    ej12_3 = inserta(5, inserta(3, vacio()))
    for disjuntos_ in [disjuntos, disjuntos2, disjuntos3, disjuntos4,
                       disjuntos5]:
        assert disjuntos_(ej12_1, ej12_2)
        assert not disjuntos_(ej12_1, ej12_3)
    ej13_1 = inserta(5, inserta(3, inserta(2, inserta(7, vacio()))))
    ej13_2 = inserta(7, inserta(4, inserta(3, vacio())))
    for diferencia_ in [diferencia, diferencia2, diferencia3,
                        diferencia4]:
        assert str(diferencia_(ej13_1, ej13_2)) == "{2, 5}"
        assert str(diferencia_(ej13_2, ej13_1)) == "{4}"
        assert str(diferencia_(ej13_1, ej13_1)) == "{}"
    ej14_1 = inserta(5, inserta(3, inserta(2, inserta(7, vacio()))))
    ej14_2 = inserta(7, inserta(4, inserta(3, vacio())))
    for diferenciaSimetrica_ in [diferenciaSimetrica,
                                 diferenciaSimetrica2,
                                 diferenciaSimetrica3]:
        assert str(diferenciaSimetrica_(ej14_1, ej14_2)) == "{2, 4, 5}"
    ej15 = inserta(5, inserta(4, inserta(7, inserta(2, vacio()))))
    for filtra_ in [filtra, filtra2, filtra3, filtra4]:
        assert str(filtra_(lambda x: x % 2 == 0, ej15)) == "{2, 4}"
        assert str(filtra_(lambda x: x % 2 == 1, ej15)) == "{5, 7}"
    ej16 = inserta(5, inserta(4, inserta(7, inserta(2, vacio()))))
    for particion_ in [particion, particion2, particion3]:
        assert str(particion_(lambda x: x % 2 == 0, ej16)) == "({2, 4}, {5, 7})"
    for divide_ in [divide, divide2, divide3, divide4]:
        assert str(divide(5, inserta(7, inserta(2, inserta(8, vacio())))))\
            == "({2}, {7, 8})"
    for mapC_ in [mapC, mapC2, mapC3, mapC4]:
        assert str(mapC_(lambda x: 2 * x, inserta(3, inserta(1, vacio()))))\
            == "{2, 6}"
    for todos_ in [todos, todos2, todos3, todos4]:
        assert todos_(lambda x: x % 2 == 0, inserta(4, inserta(6, vacio())))
        assert not todos_(lambda x: x % 2 == 0, inserta(4, inserta(7, vacio())))
    for algunos_ in [algunos, algunos2, algunos3, algunos4]:
        assert algunos_(lambda x: x % 2 == 0, inserta(4, inserta(7, vacio())))
        assert not algunos_(lambda x: x % 2 == 0, inserta(3, inserta(7, vacio())))
    ej21_1 = inserta(2, inserta(5, vacio()))
    ej21_2 = inserta(9, inserta(4, inserta(3, vacio())))
    for productoC_ in [productoC, productoC2, productoC3, productoC4,
                       productoC5]:
        assert str(productoC_(ej21_1, ej21_2))\
            == "{(2, 3), (2, 4), (2, 9), (5, 3), (5, 4), (5, 9)}"
