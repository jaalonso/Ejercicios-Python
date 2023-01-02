from src.tipos_de_datos_algebraicos_Expresiones import (C1, C2, C3, C4, C5, E4,
                                                        P1, P2, P3, P4, R4, S1,
                                                        S2, S3, S4, V3, Ap,
                                                        Mul, Op, Sum, Vec, X,
                                                        Y, aplica, maximo,
                                                        numVars, reducible,
                                                        sumas, sustitucion,
                                                        valor, valor3, valorE,
                                                        valorEG, valorEV1,
                                                        valorEV2)


def test_expresiones() -> None:
    assert valor(P1(C1(2), S1(C1(3), C1(7)))) == 20
    assert aplica(lambda x: 2 + x, S1(P1(C1(3), C1(5)), P1(C1(6), C1(7))))\
        == S1(P1(C1(5), C1(7)), P1(C1(8), C1(9)))
    assert aplica(lambda x: 2 * x, S1(P1(C1(3), C1(5)), P1(C1(6), C1(7))))\
        == S1(P1(C1(6), C1(10)), P1(C1(12), C1(14)))
    assert valorE(P2(X(), S2(C2(13), X())), 2) == 30
    assert numVars(C2(3)) == 0
    assert numVars(X()) == 1
    assert numVars(P2(X(), S2(C2(13), X()))) == 2
    assert valor3(P3(C3(2), S3(V3('a'), V3('b'))), [('a', 2), ('b', 5)]) == 14
    assert sumas(P3(V3('z'), S3(C3(3), V3('x')))) == 1
    assert sumas(S3(V3('z'), S3(C3(3), V3('x')))) == 2
    assert sumas(P3(V3('z'), P3(C3(3), V3('x')))) == 0
    assert sustitucion(P3(V3('z'), S3(C3(3), V3('x'))), [('x', 7), ('z', 9)])\
        == P3(C3(9), S3(C3(3), C3(7)))
    assert sustitucion(P3(V3('z'), S3(C3(3), V3('y'))), [('x', 7), ('z', 9)])\
        == P3(C3(9), S3(C3(3), V3('y')))
    assert reducible(S3(C3(3), C3(4))) is True
    assert reducible(S3(C3(3), V3('x'))) is False
    assert reducible(S3(C3(3), P3(C3(4), C3(5)))) is True
    assert reducible(S3(V3('x'), P3(C3(4), C3(5)))) is True
    assert reducible(S3(C3(3), P3(V3('x'), C3(5)))) is False
    assert reducible(C3(3)) is False
    assert reducible(V3('x')) is False
    assert maximo(E4(S4(C4(10), P4(R4(C4(1), Y()), Y())), 2), list(range(-3, 4)))\
        == (100, [0, 1])
    assert valorEG(Ap(Op.S, Ap(Op.R, C5(7), C5(3)), Ap(Op.M, C5(2), C5(5))))\
        == 14
    assert valorEG(Ap(Op.M, Ap(Op.R, C5(7), C5(3)), Ap(Op.S, C5(2), C5(5))))\
        == 28
    for valorEV in [valorEV1, valorEV2]:
        assert valorEV(Vec(1, 2)) == (1, 2)
        assert valorEV(Sum(Vec(1, 2), Vec(3, 4))) == (4, 6)
        assert valorEV(Mul(2, Vec(3, 4))) == (6, 8)
        assert valorEV(Mul(2, Sum(Vec(1, 2), Vec(3, 4)))) == (8, 12)
        assert valorEV(Sum(Mul(2, Vec(1, 2)), Mul(2, Vec(3, 4)))) == (8, 12)
