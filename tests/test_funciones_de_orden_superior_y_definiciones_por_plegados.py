from src.funciones_de_orden_superior_y_definiciones_por_plegados import (
    agrupa1, agrupa2, agrupa3, agrupa4, agrupa5, concC, concP, concR,
    filtraAplicaC, filtraAplicaI, filtraAplicaMF, filtraAplicaP, filtraAplicaR,
    maximo1, maximo2, maximo3, relacionadosC, relacionadosR, segmentos1,
    segmentos2)


def test_orden_superior() -> None:
    for segmentos in [segmentos1, segmentos2]:
        assert segmentos((lambda x: x % 2 == 0),
                         [1, 2, 0, 4, 9, 6, 4, 5, 7, 2])\
            == [[2, 0, 4], [6, 4], [2]]
        assert segmentos((lambda x: x % 2 == 1),
                         [1, 2, 0, 4, 9, 6, 4, 5, 7, 2])\
            == [[1], [9], [5, 7]]
    assert relacionadosC(lambda x, y: x < y, [2, 3, 7, 9])
    assert not relacionadosC(lambda x, y: x < y, [2, 3, 1, 9])
    assert relacionadosR(lambda x, y: x < y, [2, 3, 7, 9])
    assert not relacionadosR(lambda x, y: x < y, [2, 3, 1, 9])
    for agrupa in [agrupa1, agrupa2, agrupa3, agrupa4, agrupa5]:
        assert agrupa([[1, 6], [7, 8, 9], [3, 4, 5]])\
            == [[1, 7, 3], [6, 8, 4]]
    assert concC([[1, 3], [2, 4, 6], [1, 9]]) == [1, 3, 2, 4, 6, 1, 9]
    assert concR([[1, 3], [2, 4, 6], [1, 9]]) == [1, 3, 2, 4, 6, 1, 9]
    assert concP([[1, 3], [2, 4, 6], [1, 9]]) == [1, 3, 2, 4, 6, 1, 9]
    assert filtraAplicaC(lambda x: x + 4, lambda x: x < 3, list(range(1, 7)))\
        == [5, 6]
    assert filtraAplicaMF(lambda x: x + 4, lambda x: x < 3, list(range(1, 7)))\
        == [5, 6]
    assert filtraAplicaR(lambda x: x + 4, lambda x: x < 3, list(range(1, 7)))\
        == [5, 6]
    assert filtraAplicaP(lambda x: x + 4, lambda x: x < 3, list(range(1, 7)))\
        == [5, 6]
    assert filtraAplicaI(lambda x: x + 4, lambda x: x < 3, list(range(1, 7)))\
        == [5, 6]
    for maximo in [maximo1, maximo2, maximo3]:
        assert maximo([3, 7, 2, 5]) == 7
        assert maximo(["todo", "es", "falso"]) == "todo"
        assert maximo(["menos", "alguna", "cosa"]) == "menos"
