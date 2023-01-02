from src.tipos_de_datos_algebraicos_Arboles_binarios import (H, N, espejo,
                                                             mapArbol, nHojas,
                                                             nNodos, postorden,
                                                             preorden,
                                                             profundidad,
                                                             replicateArbol,
                                                             takeArbol)


def test_arboles_binarios() -> None:
    assert nHojas(N(9, N(3, H(2), H(4)), H(7))) == 3
    assert nNodos(N(9, N(3, H(2), H(4)), H(7))) == 2
    assert profundidad(N(9, N(3, H(2), H(4)), H(7))) == 2
    assert profundidad(N(9, N(3, H(2), N(1, H(4), H(5))), H(7))) == 3
    assert profundidad(N(4, N(5, H(4), H(2)), N(3, H(7), H(4)))) == 2
    assert preorden(N(9, N(3, H(2), H(4)), H(7)))\
        == [9, 3, 2, 4, 7]
    assert postorden(N(9, N(3, H(2), H(4)), H(7)))\
        == [2, 4, 3, 7, 9]
    assert espejo(N(9, N(3, H(2), H(4)), H(7))) == N(9, H(7), N(3, H(4), H(2)))
    assert takeArbol(0, N(9, N(3, H(2), H(4)), H(7)))\
        == H(9)
    assert takeArbol(1, N(9, N(3, H(2), H(4)), H(7)))\
        == N(9, H(3), H(7))
    assert takeArbol(2, N(9, N(3, H(2), H(4)), H(7)))\
        == N(9, N(3, H(2), H(4)), H(7))
    assert takeArbol(3, N(9, N(3, H(2), H(4)), H(7)))\
        == N(9, N(3, H(2), H(4)), H(7))
    assert replicateArbol(0, 5)\
        == H(5)
    assert replicateArbol(1, 5)\
        == N(5, H(5), H(5))
    assert replicateArbol(2, 5)\
        == N(5, N(5, H(5), H(5)), N(5, H(5), H(5)))
    assert mapArbol(lambda x: 2 * x, N(9, N(3, H(2), H(4)), H(7)))\
        == N(18, N(6, H(4), H(8)), H(14))
