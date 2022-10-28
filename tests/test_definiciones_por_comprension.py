from src.definiciones_por_comprension import \
    suma1, \
    suma2, \
    sumaDeCuadrados1, \
    sumaDeCuadrados2, \
    euler6a, \
    euler6b, \
    replica, \
    linea1, \
    linea2, \
    linea3, \
    triangulo1, \
    triangulo2, \
    triangulo3, \
    perfectos, \
    numeroAbundante, \
    numerosAbundantesMenores, \
    todosPares, \
    euler1, \
    circulo1, \
    circulo2, \
    circulo3, \
    circulo4, \
    aproxE, \
    errorAproxE, \
    aproxLimSeno, \
    errorLimSeno, \
    calculaPi, \
    errorPi, \
    pitagoricas1, \
    pitagoricas2, \
    pitagoricas3, \
    numeroDePares, \
    conjetura, \
    ternasPitagoricas1, \
    ternasPitagoricas2, \
    ternasPitagoricas3, \
    productoEscalar, \
    sumaConsecutivos, \
    densa, \
    personas, \
    nombres, \
    musicos, \
    seleccion, \
    musicos2, \
    vivas

def test_comprension1() -> None:
    assert suma1(3) == 6
    assert suma2(3) == 6
    assert sumaDeCuadrados1(3) == 14
    assert sumaDeCuadrados2(3) == 14
    assert euler6a(10) == 2640
    assert euler6b(10) == 2640
    assert replica(4, 7) == [7, 7, 7, 7]
    assert replica(3, True) == [True, True, True]
    assert linea1(4) == [7, 8, 9, 10]
    assert linea1(5) == [11, 12, 13, 14, 15]
    assert linea2(4) == [7, 8, 9, 10]
    assert linea2(5) == [11, 12, 13, 14, 15]
    assert linea3(4) == [7, 8, 9, 10]
    assert linea3(5) == [11, 12, 13, 14, 15]
    assert triangulo1(3) == [[1], [2, 3], [4, 5, 6]]
    assert triangulo1(4) == [[1], [2, 3], [4, 5, 6], [7, 8, 9, 10]]
    assert triangulo2(3) == [[1], [2, 3], [4, 5, 6]]
    assert triangulo2(4) == [[1], [2, 3], [4, 5, 6], [7, 8, 9, 10]]
    assert triangulo3(3) == [[1], [2, 3], [4, 5, 6]]
    assert triangulo3(4) == [[1], [2, 3], [4, 5, 6], [7, 8, 9, 10]]
    assert perfectos(500) == [6, 28, 496]
    assert numeroAbundante(5) is False
    assert numeroAbundante(12) is True
    assert numeroAbundante(28) is False
    assert numeroAbundante(30) is True
    assert numerosAbundantesMenores(50) == [12, 18, 20, 24, 30, 36, 40, 42, 48]
    assert numerosAbundantesMenores(48) == [12, 18, 20, 24, 30, 36, 40, 42, 48]
    assert todosPares(10) is True
    assert todosPares(100) is True
    assert todosPares(1000) is False
    assert euler1(10) == 23

def test_comprension2() -> None:
    assert circulo1(1) == 3
    assert circulo1(2) == 6
    assert circulo1(3) == 11
    assert circulo1(4) == 17
    assert circulo2(1) == 3
    assert circulo2(2) == 6
    assert circulo2(3) == 11
    assert circulo2(4) == 17
    assert circulo3(1) == 3
    assert circulo3(2) == 6
    assert circulo3(3) == 11
    assert circulo3(4) == 17
    assert circulo4(1) == 3
    assert circulo4(2) == 6
    assert circulo4(3) == 11
    assert circulo4(4) == 17
    assert aproxE(4) == [2.0, 2.25, 2.37037037037037, 2.44140625]
    assert errorAproxE(0.1) == 13
    assert errorAproxE(0.01) == 135
    assert errorAproxE(0.001) == 1359
    assert aproxLimSeno(1) == [0.8414709848078965]
    assert aproxLimSeno(2) == [0.8414709848078965, 0.958851077208406]
    assert errorLimSeno(0.1) == 2
    assert errorLimSeno(0.01) == 5
    assert errorLimSeno(0.001) == 13
    assert errorLimSeno(0.0001) == 41
    assert calculaPi(3) == 2.8952380952380956
    assert calculaPi(300) == 3.1449149035588526
    assert errorPi(0.1) == 9
    assert errorPi(0.01) == 99
    assert errorPi(0.001) == 999
    assert pitagoricas1(10) == [(3, 4, 5), (6, 8, 10)]
    assert pitagoricas1(15) == \
        [(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15)]
    assert pitagoricas2(10) == [(3, 4, 5), (6, 8, 10)]
    assert pitagoricas2(15) == \
        [(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15)]
    assert pitagoricas3(10) == [(3, 4, 5), (6, 8, 10)]
    assert pitagoricas3(15) == \
        [(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15)]
    assert numeroDePares(3, 5, 7) == 0
    assert numeroDePares(3, 6, 7) == 1
    assert numeroDePares(3, 6, 4) == 2
    assert numeroDePares(4, 6, 4) == 3
    assert conjetura(10) is True
    assert ternasPitagoricas1(12) == [(3, 4, 5)]
    assert ternasPitagoricas1(60) == [(10, 24, 26), (15, 20, 25)]
    assert ternasPitagoricas2(12) == [(3, 4, 5)]
    assert ternasPitagoricas2(60) == [(10, 24, 26), (15, 20, 25)]
    assert ternasPitagoricas3(12) == [(3, 4, 5)]
    assert ternasPitagoricas3(60) == [(15, 20, 25), (10, 24, 26)]
    assert productoEscalar([1, 2, 3], [4, 5, 6]) == 32

def test_comprension3() -> None:
    assert sumaConsecutivos([3, 1, 5, 2]) == [4, 6, 7]
    assert sumaConsecutivos([3]) == []
    assert densa([6, 0, -5, 4, -7]) == [(4, 6), (2, -5), (1, 4), (0, -7)]
    assert densa([6, 0, 0, 3, 0, 4]) == [(5, 6), (2, 3), (0, 4)]
    assert densa([0]) == [(0, 0)]
    assert nombres(personas) == ['Cervantes', 'Velazquez', 'Picasso',
                                 'Beethoven', 'Poincare', 'Quevedo',
                                 'Goya', 'Einstein', 'Mozart',
                                 'Botticelli', 'Borromini', 'Bach']
    assert musicos(personas) == ['Beethoven', 'Mozart', 'Bach']
    assert seleccion(personas, 'Pintura') == \
        ['Velazquez', 'Picasso', 'Goya', 'Botticelli']
    assert seleccion(personas, 'Musica') == ['Beethoven', 'Mozart', 'Bach']
    assert musicos2(personas) == ['Beethoven', 'Mozart', 'Bach']
    assert vivas(personas, 1600) == \
        ['Cervantes', 'Velazquez', 'Quevedo', 'Borromini']
