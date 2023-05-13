from src.relaciones_binarias_homogeneas import (Rel, antisimetrica,
                                                antisimetrica2, antisimetrica3,
                                                antisimetrica4, antisimetrica5,
                                                clausuraReflexiva,
                                                clausuraSimetrica,
                                                clausuraTransitiva,
                                                clausuraTransitiva2,
                                                composicion, composicion2,
                                                composicion3, esEquivalencia,
                                                esRelacionBinaria,
                                                esRelacionBinaria2,
                                                esRelacionBinaria3, grafo,
                                                irreflexiva, irreflexiva2,
                                                irreflexiva3, reflexiva,
                                                reflexiva2, reflexiva3,
                                                simetrica, simetrica2,
                                                simetrica3, subconjunto,
                                                subconjunto1, subconjunto2,
                                                subconjunto3, subconjunto4,
                                                total, transitiva, transitiva1,
                                                transitiva2, transitiva3,
                                                universo)


def test_relacionesNinarias() -> None:
    for esRelacionBinaria_ in [esRelacionBinaria, esRelacionBinaria2,
                               esRelacionBinaria3]:
        assert esRelacionBinaria_(([1, 3], [(3, 1), (3, 3)]))
        assert not esRelacionBinaria_(([1, 3], [(3, 1), (3, 2)]))
    assert universo(([3, 2, 5], [(2, 3), (3, 5)])) == [3, 2, 5]
    assert grafo(([3, 2, 5], [(2, 3), (3, 5)])) == [(2, 3), (3, 5)]
    for reflexiva_ in [reflexiva, reflexiva2, reflexiva3]:
        assert reflexiva_(([1, 3], [(1, 1),(1, 3),(3, 3)]))
        assert not reflexiva_(([1, 2, 3], [(1, 1),(1, 3),(3, 3)]))
    for simetrica_ in [simetrica, simetrica2, simetrica3]:
        assert simetrica_(([1, 3], [(1, 1), (1, 3), (3, 1)]))
        assert not simetrica_(([1, 3], [(1, 1), (1, 3), (3, 2)]))
        assert simetrica_(([1, 3], []))
    for subconjunto_ in [subconjunto, subconjunto1, subconjunto2,
                         subconjunto3, subconjunto4]:
        assert subconjunto_([3, 2, 3], [2, 5, 3, 5])
        assert not subconjunto_([3, 2, 3], [2, 5, 6, 5])
    for composicion_ in [composicion, composicion2, composicion3]:
        assert composicion_(([1,2],[(1,2),(2,2)]), ([1,2],[(2,1)])) \
            == ([1, 2], [(1, 1), (2, 1)])
    for transitiva_ in [transitiva, transitiva1, transitiva2,
                        transitiva3]:
        assert transitiva_(([1, 3, 5], [(1, 1), (1, 3), (3, 1), (3, 3), (5, 5)]))
        assert not transitiva_(([1, 3, 5], [(1, 1), (1, 3), (3, 1), (5,
                                                                     5)]))
    assert esEquivalencia (([1,3,5],[(1,1),(1,3),(3,1),(3,3),(5,5)]))
    assert not esEquivalencia (([1,2,3,5],[(1,1),(1,3),(3,1),(3,3),(5,5)]))
    assert not esEquivalencia (([1,3,5],[(1,1),(1,3),(3,3),(5,5)]))
    for irreflexiva_ in [irreflexiva, irreflexiva2, irreflexiva3]:
        assert irreflexiva_(([1, 2, 3], [(1, 2), (2, 1), (2, 3)]))
        assert not irreflexiva_(([1, 2, 3], [(1, 2), (2, 1), (3, 3)]))
    for antisimetrica_ in [antisimetrica, antisimetrica2,
                           antisimetrica3, antisimetrica4,
                           antisimetrica5]:
        assert antisimetrica_(([1,2],[(1,2)]))
        assert not antisimetrica_(([1,2],[(1,2),(2,1)]))
        assert antisimetrica_(([1,2],[(1,1),(2,1)]))
    assert total (([1,3],[(1,1),(3,1),(3,3)]))
    assert not total (([1,3],[(1,1),(3,1)]))
    assert not total (([1,3],[(1,1),(3,3)]))
    assert clausuraReflexiva (([1,3],[(1,1),(3,1)])) \
        == ([1, 3], [(3, 1), (1, 1), (3, 3)])
    assert clausuraSimetrica(([1, 3, 5], [(1, 1), (3, 1), (1, 5)])) \
        == ([1, 3, 5], [(1, 5), (3, 1), (1, 1), (1, 3), (5, 1)])
    for clausuraTransitiva_ in [clausuraTransitiva,
                                clausuraTransitiva2]:
        assert clausuraTransitiva_(([1, 2, 3, 4, 5, 6], [(1, 2), (2, 5), (5, 6)])) \
            == ([1, 2, 3, 4, 5, 6], [(1, 2), (2, 5), (5, 6), (2, 6), (1, 5), (1, 6)])
