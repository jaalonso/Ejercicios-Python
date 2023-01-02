from src.tipos_de_datos_algebraicos_Arboles import (H1, H3, N1, N3, NG,
                                                    algunoArbol, arbol1,
                                                    arbol2, arbol3, arbol4,
                                                    arbolFactorizacion1,
                                                    arbolFactorizacion2,
                                                    balanceado, ej1, ej2,
                                                    ej3arbol1, ej3arbol2,
                                                    ej3arbol3, ej3arbol4, ejG1,
                                                    igualBorde,
                                                    igualEstructura, mapArbol,
                                                    nivel, ramaIzquierda,
                                                    ramifica, sumaArbol,
                                                    valorB)


def test_TDA_Arboles() -> None:
    assert sumaArbol(N1(2,
                        N1(5, N1(3, H1(), H1()), N1(7, H1(), H1())),
                        N1(4, H1(), H1()))) == 21
    assert mapArbol(lambda x: 1 + x,
                    N1(2,
                       N1(5, N1(3, H1(), H1()), N1(7, H1(), H1())),
                       N1(4, H1(), H1()))) == \
        N1(3, N1(6, N1(4, H1(), H1()), N1(8, H1(), H1())), N1(5, H1(), H1()))
    assert ramaIzquierda(N1(2,
                            N1(5, N1(3, H1(), H1()), N1(7, H1(), H1())),
                            N1(4, H1(), H1()))) == [2, 5, 3]
    assert balanceado(N1(5, H1(), N1(3, H1(), H1()))) is True
    assert balanceado(N1(4,
                         N1(3, N1(2, H1(), H1()), H1()),
                         N1(5, H1(), N1(6, H1(), N1(7, H1(), H1()))))) is False
    assert igualBorde(arbol1, arbol2) is True
    assert igualBorde(arbol1, arbol3) is False
    assert igualBorde(arbol1, arbol4) is False
    assert igualEstructura(ej3arbol1, ej3arbol2) is True
    assert igualEstructura(ej3arbol1, ej3arbol3) is False
    assert igualEstructura(ej3arbol1, ej3arbol4) is False
    assert algunoArbol(N3(5, N3(3, H3(1), H3(4)), H3(2)), lambda x: x > 4)
    assert not algunoArbol(N3(5, N3(3, H3(1), H3(4)), H3(2)), lambda x: x > 7)
    assert nivel(0, N3(7, N3(2, H3(5), H3(4)), H3(9))) == [7]
    assert nivel(1, N3(7, N3(2, H3(5), H3(4)), H3(9))) == [2, 9]
    assert nivel(2, N3(7, N3(2, H3(5), H3(4)), H3(9))) == [5, 4]
    assert not nivel(3, N3(7, N3(2, H3(5), H3(4)), H3(9)))
    for arbolFactorizacion in [arbolFactorizacion1, arbolFactorizacion2]:
        assert arbolFactorizacion(60) == N3(60,
                                            N3(6, H3(2), H3(3)),
                                            N3(10, H3(2), H3(5)))
        assert arbolFactorizacion(45) == N3(45, H3(5), N3(9, H3(3), H3(3)))
        assert arbolFactorizacion(7) == H3(7)
        assert arbolFactorizacion(9) == N3(9, H3(3), H3(3))
        assert arbolFactorizacion(14) == N3(14, H3(2), H3(7))
        assert arbolFactorizacion(28) == N3(28, N3(4, H3(2), H3(2)), H3(7))
        assert arbolFactorizacion(84) == N3(84,
                                            H3(7),
                                            N3(12, H3(3), N3(4, H3(2), H3(2))))
    assert valorB(ej1)
    assert not valorB(ej2)
    assert ramifica(ejG1, NG(8, []), lambda x: x > 4) == \
        NG(1, [NG(2, []), NG(3, [NG(4, [])])])
    assert ramifica(ejG1, NG(8, []), lambda x: x > 3) == \
        NG(1, [NG(2, []), NG(3, [NG(4, [NG(8, [])])])])
    assert ramifica(ejG1, NG(8, []), lambda x: x > 2) == \
        NG(1, [NG(2, []), NG(3, [NG(4, [NG(8, [])]), NG(8, [])])])
    assert ramifica(ejG1, NG(8, []), lambda x: x > 1) == \
        NG(1, [NG(2, [NG(8, [])]), NG(3, [NG(4, [NG(8, [])]), NG(8, [])])])
    assert ramifica(ejG1, NG(8, []), lambda x: x > 0) == \
        NG(1, [NG(2, [NG(8, [])]),
               NG(3, [NG(4, [NG(8, [])]), NG(8, [])]),
               NG(8, [])])
