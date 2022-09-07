from src.definiciones_por_composicion import \
    media3, \
    sumaMonedas, \
    volumenEsfera, \
    areaDeCoronaCircular, \
    ultimoDigito, \
    maxTres, \
    rota1a, \
    rota1b, \
    rota1c, \
    rota, \
    rango, \
    palindromo, \
    interior1, \
    interior2, \
    finales1, \
    finales2, \
    finales3, \
    segmento1, \
    segmento2, \
    extremos, \
    mediano, \
    tresIguales1, \
    tresIguales2, \
    tresDiferentes, \
    cuatroIguales1, \
    cuatroIguales2

def test_definiciones_por_composicion():
    assert media3(1, 3, 8) == 4.0
    assert media3(-1, 0, 7) == 2.0
    assert media3(-3, 0, 3) == 0.0
    assert sumaMonedas(0, 0, 0, 0, 1) == 20
    assert sumaMonedas(0, 0, 8, 0, 3) == 100
    assert sumaMonedas(1, 1, 1, 1, 1) == 38
    assert volumenEsfera(10) == 4188.790204786391
    assert areaDeCoronaCircular(1, 2) == 9.42477796076938
    assert areaDeCoronaCircular(2, 5) == 65.97344572538566
    assert areaDeCoronaCircular(3, 5) == 50.26548245743669
    assert ultimoDigito(325) == 5
    assert maxTres(6, 2, 4) == 6
    assert maxTres(6, 7, 4) == 7
    assert maxTres(6, 7, 9) == 9
    assert rota1a([3, 2, 5, 7]) == [2, 5, 7, 3]
    assert rota1a(['a', 'b', 'c']) == ['b', 'c', 'a']
    assert rota1b([3, 2, 5, 7]) == [2, 5, 7, 3]
    assert rota1b(['a', 'b', 'c']) == ['b', 'c', 'a']
    assert rota1c([3, 2, 5, 7]) == [2, 5, 7, 3]
    assert rota1c(['a', 'b', 'c']) == ['b', 'c', 'a']
    assert rota(1, [3, 2, 5, 7]) == [2, 5, 7, 3]
    assert rota(2, [3, 2, 5, 7]) == [5, 7, 3, 2]
    assert rota(3, [3, 2, 5, 7]) == [7, 3, 2, 5]
    assert rango([3, 2, 7, 5]) == [2, 7]
    assert palindromo([3, 2, 5, 2, 3]) is True
    assert palindromo([3, 2, 5, 6, 2, 3]) is False
    assert interior1([2, 5, 3, 7, 3]) == [5, 3, 7]
    assert interior2([2, 5, 3, 7, 3]) == [5, 3, 7]
    assert finales1(3, [2, 5, 4, 7, 9, 6]) == [7, 9, 6]
    assert finales2(3, [2, 5, 4, 7, 9, 6]) == [7, 9, 6]
    assert finales3(3, [2, 5, 4, 7, 9, 6]) == [7, 9, 6]
    assert segmento1(3, 4, [3, 4, 1, 2, 7, 9, 0]) == [1, 2]
    assert segmento1(3, 5, [3, 4, 1, 2, 7, 9, 0]) == [1, 2, 7]
    assert not segmento1(5, 3, [3, 4, 1, 2, 7, 9, 0])
    assert segmento2(3, 4, [3, 4, 1, 2, 7, 9, 0]) == [1, 2]
    assert segmento2(3, 5, [3, 4, 1, 2, 7, 9, 0]) == [1, 2, 7]
    assert not segmento2(5, 3, [3, 4, 1, 2, 7, 9, 0])
    assert extremos(3, [2, 6, 7, 1, 2, 4, 5, 8, 9, 2, 3]) == [2, 6, 7, 9, 2, 3]
    assert mediano(3, 2, 5) == 3
    assert mediano(2, 4, 5) == 4
    assert mediano(2, 6, 5) == 5
    assert mediano(2, 6, 6) == 6
    assert tresIguales1(4, 4, 4) is True
    assert tresIguales1(4, 3, 4) is False
    assert tresIguales2(4, 4, 4) is True
    assert tresIguales2(4, 3, 4) is False
    assert tresDiferentes(3, 5, 2) is True
    assert tresDiferentes(3, 5, 3) is False

def test_definiciones_por_composicion2():
    assert cuatroIguales1(5, 5, 5, 5) is True
    assert cuatroIguales1(5, 5, 4, 5) is False
    assert cuatroIguales2(5, 5, 5, 5) is True
    assert cuatroIguales2(5, 5, 4, 5) is False
