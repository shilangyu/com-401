def prepare_key(k) -> list[list[str]]:
    """
    Checks the validity of a key. And normalize.
    """
    # has 5 rows
    if len(k) != 5:
        raise RuntimeError("Key does not have exactly 5 rows")
    # each row has 5 columns
    if not all(len(r) == 5 for r in k):
        raise RuntimeError("Key does not have exactly 5 columns")
    # each cell has one character
    if not all(all(len(c) == 1 for c in r) for r in k):
        raise RuntimeError("Key does not store a single charecter in each cell")

    # normalize:
    # - replace J with I
    # - lowercase
    key = [["i" if c.lower() == "j" else c.lower() for c in r] for r in k]

    # matrix has the whole alphabet
    if set(c for r in key for c in r) != set("abcdefghiklmnopqrstuvwxyz"):
        raise RuntimeError("Key does not have the full alphabet")

    return key


def _pairs(s: str) -> list[(str, str)]:
    """
    Returns the sliding window of size 2 of the characters of a string.
    The string has to have an even length.
    """
    assert len(s) % 2 == 0
    return [(s[i], s[i + 1]) for i in range(0, len(s), 2)]


def prepare_message(m: str) -> list[(str, str)]:
    """
    Prepares a plain text message to be encrypted.
    """
    # normalize:
    # - turn all j's into i's
    # - lowercase
    # - remove special characters (FIXME)
    m = "".join(c for c in m.replace("j", "i").lower() if c.isalpha())

    res = ""
    for i in range(len(m)):
        res += m[i]
        # if two consequitive characters are equal, separate them with an 'x'
        if i != len(m) - 1 and m[i] == m[i + 1]:
            # this will produce two consequitive 'x', this breaks encryption rules
            if m[i] == "x":
                raise RuntimeError("Unsupported message")
            res += "x"

    # if a string has odd length, pad it with an extra 'x'
    if len(res) % 2 == 1:
        if res[-1] == "x":
            # this will produce two consequitive 'x', this breaks encryption rules
            raise RuntimeError("Unsupported message")
        res += "x"

    return _pairs(res)


def _index_dict(k) -> dict[str, (int, int)]:
    """
    Creates an index dictionairy to efficiently get indices of characters.
    """
    return dict((c, (i, j)) for i in range(len(k)) for (j, c) in enumerate(k[i]))


def encrypt(k: list[list[str]], m: str) -> str:
    k = prepare_key(k)

    pairs = prepare_message(m)

    k_index = _index_dict(k)

    encrypted = ""
    for m1, m2 in pairs:
        (r1, c1) = k_index[m1]
        (r2, c2) = k_index[m2]

        if r1 == r2:
            # shift to the right with wrapping
            encrypted += k[r1][(c1 + 1) % 5] + k[r2][(c2 + 1) % 5]
        elif c1 == c2:
            # shift down with wrapping
            encrypted += k[(r1 + 1) % 5][c1] + k[(r2 + 1) % 5][c2]
        else:
            # swap coordinates
            encrypted += k[r1][c2] + k[r2][c1]

    return encrypted


def decrypt(k: list[list[str]], encrypted: str) -> str:
    k = prepare_key(k)

    k_index = _index_dict(k)

    m = ""
    for m1, m2 in _pairs(encrypted):
        (r1, c1) = k_index[m1]
        (r2, c2) = k_index[m2]

        if r1 == r2:
            # shift to the left with wrapping
            m += k[r1][(c1 - 1) % 5] + k[r2][(c2 - 1) % 5]
        elif c1 == c2:
            # shift up with wrapping
            m += k[(r1 - 1) % 5][c1] + k[(r2 - 1) % 5][c2]
        else:
            # swap coordinates
            m += k[r1][c2] + k[r2][c1]

    return m


if __name__ == "__main__":
    ek = [
        ["l", "y", "n", "b", "e"],
        ["z", "m", "v", "r", "h"],
        ["i", "g", "u", "q", "a"],
        ["c", "t", "o", "s", "w"],
        ["d", "k", "x", "p", "f"],
    ]
    m = "To speak of Don Quixote as if it were merely a humorous book would be a manifest misdescription. Cervantes at times makes it a kind of commonplace book for occasional essays and criticisms, or for the observations and reflections and gathered wisdom of a long and stirring life. It is a mine of shrewd observation on mankind and human nature. Among modern novels there may be, here and there, more elaborate studies of character, but there is no book richer in individualised character. What Coleridge said of Shakespeare in minimis is true of Cervantes; he never, even for the most temporary purpose, puts forward a lay figure. There is life and individuality in all his characters, however little they may have to do, or however short a time they may be before the reader. Samson Carrasco, the curate, Teresa Panza, Altisidora, even the two students met on the road to the cave of Montesinos, all live and move and have their being; and it is characteristic of the broad humanity of Cervantes that there is not a hateful one among them all. Even poor Maritornes, with her deplorable morals, has a kind heart of her own and some faint and distant resemblance to a Christian about her; and as for Sancho, though on dissection we fail to find a lovable trait in him, unless it be a sort of dog-like affection for his master, who is there that in his heart does not love him?"

    dk = [
        ["i", "m", "t", "p", "r"],
        ["y", "w", "b", "s", "f"],
        ["v", "q", "h", "x", "n"],
        ["l", "o", "k", "a", "g"],
        ["u", "c", "e", "z", "d"],
    ]
    encrypted = "mkxszkaknrgqvcpvkmzkypyrmbdtctdtukslvewcmgzywkqaoblcguhtopgxryzbptpyuzwzimrpmlqddtxlhrzbkphpmtzbpoetyppkltgrgwmcpqwcxrogezwkqagbgmcmqzzxmlxgkuxaxzwfgxueimpmumwpwafngmbkcksfdtxlpmgqxzgrtdygzepmgqxzgrlgbkdtzuymfzcwgwgogqlggrbpminprvloryutpmxztmhdgwbxtdfckwbzinkpmlqgqrgxltgrgxencigxnvkpdizkwcgdwcuzfgnvlqukbpkttdpowstkdtzkgrbkdtctgmzhukksgmkpzbieurzbgweqgpozbttfeihpkttdpyqgwkqagtmuktimvrgrylruzluybzuexkpgemdtbqkpmckuimrdzblpcgyfxketxszktdrvtmvrtmypbpidckwddtxlhrzbkthdhutdhugngmbkctawphbttrgmgpsidimabzizpbwgmfgpzgogwyrlditbkttdpyuybdgxurgrylruzluyibrvgovavtwzxkpgemdtbxcquhdtuyphiktbktwilsxkhumkcgqatncquhdtbxgmpkpmtcbkubpowsthdbgmtbkttdgzdtxzpwgqzopnpgwzkmktecpgbtbttdxzszxdzagopmypcgpguhdhbktbqcbpcudhpbtcmkhrktmggzmkbkzelxckwrgqbtypqgxzavavuyhugxcrlqzkgrxkhubkuttfutgdgxurpmwzxkpgemdtpypmmcbrktftkgencigxmpwlwddtxlhrzbbkkphpkttdpyqgpkxkbtydokhdopgqkrktpoavkuhuxraqgmpoimmkfgzbymbknxdtuziagmkskuwcpgayxkxzltgrktgpmkbndtcqxggrwatcsgrvpkgrnzpypkhrtdbztwogqdtbkgeqimbpplxgwkeiktpggrzxwgpfgxeqkmqkdlqkgrpyaxzepmgqbcsgyumkyrgrgolqkskupilppmvxmtdvkuxaypbhzkwaipgwcglotlzksnbdemmlgngmvtwpzxbtmfqkpybkdttbxkpmvxpyktgprekcfxkmokhuvtpq"

    print(f"Question 1.1: {encrypt(ek, m)}")
    print(f"Question 1.2: {decrypt(dk, encrypted)}")
