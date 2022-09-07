from src.condicionales_guardas_y_patrones import \
    divisionSegura1, \
    divisionSegura2, \
    xor1, \
    xor2, \
    xor3, \
    xor4, \
    xor5, \
    mayorRectangulo, \
    intercambia, \
    distancia, \
    ciclo, \
    numeroMayor1, \
    numeroMayor2, \
    numeroDeRaices, \
    raices, \
    area, \
    interseccion, \
    formaReducida, \
    sumaRacional, \
    productoRacional, \
    igualdadRacional

def test_condicionales():
    assert divisionSegura1(7, 2) == 3.5
    assert divisionSegura1(7, 0) == 9999.0
    assert divisionSegura2(7, 2) == 3.5
    assert divisionSegura2(7, 0) == 9999.0
    assert xor1(True, True) is False
    assert xor1(True, False) is True
    assert xor1(False, True) is True
    assert xor1(False, False) is False
    assert xor2(True, True) is False
    assert xor2(True, False) is True
    assert xor2(False, True) is True
    assert xor2(False, False) is False
    assert xor3(True, True) is False
    assert xor3(True, False) is True
    assert xor3(False, True) is True
    assert xor3(False, False) is False
    assert xor4(True, True) is False
    assert xor4(True, False) is True
    assert xor4(False, True) is True
    assert xor4(False, False) is False
    assert xor5(True, True) is False
    assert xor5(True, False) is True
    assert xor5(False, True) is True
    assert xor5(False, False) is False
    assert mayorRectangulo((4, 6), (3, 7)) == (4, 6)
    assert mayorRectangulo((4, 6), (3, 8)) == (4, 6)
    assert mayorRectangulo((4, 6), (3, 9)) == (3, 9)
    assert intercambia((2, 5)) == (5, 2)
    assert intercambia((5, 2)) == (2, 5)
    assert distancia((1, 2), (4, 6)) == 5.0
    assert ciclo([2, 5, 7, 9]) == [9, 2, 5, 7]
    assert not ciclo([])
    assert ciclo([2]) == [2]
    assert numeroMayor1(2, 5) == 52
    assert numeroMayor1(5, 2) == 52
    assert numeroMayor2(2, 5) == 52
    assert numeroMayor2(5, 2) == 52
    assert numeroDeRaices(2, 0, 3) == 0
    assert numeroDeRaices(4, 4, 1) == 1
    assert numeroDeRaices(5, 23, 12) == 2
    assert raices(1, 3, 2) == [-1.0, -2.0]
    assert raices(1, (-2), 1) == [1.0, 1.0]
    assert not raices(1, 0, 1)
    assert area(3, 4, 5) == 6.0

def test_condicionales2():
    assert not interseccion([], [3, 5])
    assert not interseccion([3, 5], [])
    assert not interseccion([2, 4], [6, 9])
    assert interseccion([2, 6], [6, 9]) == [6, 6]
    assert interseccion([2, 6], [0, 9]) == [2, 6]
    assert interseccion([2, 6], [0, 4]) == [2, 4]
    assert interseccion([4, 6], [0, 4]) == [4, 4]
    assert not interseccion([5, 6], [0, 4])
    assert formaReducida((4, 10)) == (2, 5)
    assert formaReducida((0, 5)) == (0, 1)
    assert sumaRacional((2, 3), (5, 6)) == (3, 2)
    assert sumaRacional((3, 5), (-3, 5)) == (0, 1)
    assert productoRacional((2, 3), (5, 6)) == (5, 9)
    assert igualdadRacional((6, 9), (10, 15)) is True
    assert igualdadRacional((6, 9), (11, 15)) is False
    assert igualdadRacional((0, 2), (0, -5)) is True
