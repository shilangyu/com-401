def embedding_degree(E: EllipticCurve) -> int:
    """
    Bruteforce looking for the embedding degree.
    """
    M = E.order()
    for k in range(1, 10000):
        if (E.base_field().characteristic() ^ k - 1) % M == 0:
            return k
    raise RuntimeError("Could not find embedding")


def lemma1(E: EllipticCurve, P: "EllipticCurvePoint", Q: "EllipticCurvePoint") -> bool:
    """
    Assets conditions of lemma 1. If true is returned, then there exists an n such that Q = nP.
    """
    assert P in E and Q in E

    if E.base_field().characteristic() != E.base_field().order():
        return False

    N = P.order()

    if gcd(E.base_field().characteristic(), N) != 1:
        return False

    if not ((N * Q).order() == 1 and P.weil_pairing(Q, N) == 1):
        return False

    return True


def MOV(params: list[int], p: int, P: tuple[int, int], Q: tuple[int, int]) -> int:
    """
    Solves Q = nP for n. From https://crypto.stanford.edu/pbc/notes/elliptic/movattack.html
    """
    E = EllipticCurve(GF(p), params)
    k = embedding_degree(E)
    F.<y> = GF((p, k))
    Ek = EllipticCurve(F, params)


    P = E(*P)
    Q = E(*Q)
    assert lemma1(E, P, Q) # otherwise the discrete log does not exist

    N = P.order()
    # we want such an R of order N that there does not exist an n such that R = nP. We use the lemma to see if such n exists.
    R = None
    m = E.order()
    n = Ek.order()
    for _ in range(1, 1000000):
        temp = Ek.random_point()
        if True or not temp in E:
            S = (n / m) * temp
            # print(temp)
            # print(S)
            if S.order() != 1:
                R = S
                break
    print('found R')
    if R == None:
        raise RuntimeError('Could not find a point for MOV') 
        
    assert not lemma1(E, P, R)
    
    u = P.weil_pairing(R, N)
    v = Q.weil_pairing(R, N)

    n = discrete_log(v, u)

    assert n * P == Q

    return n


if __name__ == "__main__":
    Q1_param=[-35, 98]
    Q1_p=434252269029337012720086440207
    Q1_P=(16378704336066569231287640165, 377857010369614774097663166640)
    Q1_Q=(429232528000613182403739134488, 373273367618177537099469237857)

    E = EllipticCurve(GF(Q1_p), Q1_param)
    k = embedding_degree(E)

    print(f'Question 1.1: {k}')

    F.<y> = GF((Q1_p, k))
    Ek = EllipticCurve(F, Q1_param)

    Q1b_S1=(16378704336066569231287640165, 377857010369614774097663166640)
    Q1b_S2=(70537032201908735903640201134*y + 112916464356536482203722151790, 61270675842937552626945489624*y + 261740183693532755354980023566)

    S1 = Ek(*Q1b_S1)
    S2 = Ek(*Q1b_S2)

    # for _ in range(1, 10000):
    #     try:
    #         print(Ek.random_point() in E)
    #     except:
    #         pass
        
    # exit(0)

    # Ek is finite, we need an N such that N.S1 = N.S2 = 0, trivially we can set N to the order of Ek
    weil = S1.weil_pairing(S2, Ek.order())
    print(f'Question 1.2: {weil}')

    n = MOV(Q1_param, Q1_p, Q1_P, Q1_Q)
    print(f'Question 1.3: {n}')
