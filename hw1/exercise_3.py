from Crypto.Cipher import AES


def get_fixed(x: int, n: int) -> int:
    return (x >> (255 - (n + 1))) & 0b11


def find_kexp_and_fixed_bits(g: int, p: int, n: int, known_pt: int, known_cts: list[int]) -> tuple[list[int], list[tuple[int, int]]]:
    # g has order 4 in p
    g_pow_values = [pow(g, 0, p)]
    while True:
        val = pow(g, len(g_pow_values), p)
        # reached cycle
        if val == 1:
            break
        g_pow_values.append(val)

    assert len(g_pow_values) == 4

    # Since g has order 4, we can take the whole exponent mod 4.
    # This means the `52*r` component disappears.

    # bits of known_pt
    assert known_pt == 0b01_00_11_10

    # so we apply encrypt_key with 2, 3, 0, 1
    # when we unroll encrypt_2bits we see that we compute in order:
    # 1. k_xor1 ^ pow(g, k_exp, p)
    # 2. k_xor2 ^ pow(g, k_exp + 3, p)
    # 3. k_xor3 ^ pow(g, k_exp + 2, p)
    # 4. k_xor4 ^ pow(g, k_exp + 1, p)

    # we can now find k_exp mod 4 by looking for fixed bits
    solutions = []
    for i in range(len(g_pow_values)):
        # k_xori ^ pow(g, k_exp + j, p)
        # we look to eliminate the term pow(g, k_exp + j, p) by finding
        # consecutive g^x values that will result in reducing to k_xori:
        # k_xori ^ pow(g, k_exp + j, p) ^ pow(g, k_exp + j, p) = k_xori
        # We can tell when it has reduced when in all 4 configurations
        # the fixed bits are equal.
        found_bits = None
        for j in range(len(known_cts)):
            # we try different offsets and make sure in all offsets result in same fixed bits
            k_xor = known_cts[j] ^ g_pow_values[(i - j) % len(g_pow_values)]
            fixed = get_fixed(k_xor, n)
            if found_bits == None:
                found_bits = (i, fixed)
            elif fixed != found_bits[1]:
                # we got different fixed bits, its not the correct configuration
                found_bits = None
                break
        if found_bits != None:
            # so k_exp mod 4 = found_bits[0] and fixed bits are found_bits[1]
            solutions.append(found_bits)

    return (g_pow_values, solutions)


def find_possible_keys(solutions: list[tuple[int, int]], cts: list[int], n: int, g_pow_values: list[int]) -> set[int]:
    keys = set()
    for (k_exp_mod, fixed) in solutions:
        key = 0
        for (i, ct) in enumerate(cts):
            already_found = False
            for (j, g_pow) in enumerate(g_pow_values):
                res = ct ^ g_pow
                if get_fixed(res, n) == fixed:
                    if already_found:
                        print('not good, found two possibilities for key part')
                    already_found = True
                    m = (j - k_exp_mod - 2*(i+1)) % len(g_pow_values)
                    key |= m << (i*2)
            if not already_found:
                print('could not find a key part')
        keys.add(key)
    return keys


def decrypt(ciphertext: bytes, tag: bytes, nonce: bytes, key: int) -> str:
    key_bytes = key.to_bytes(16, "big")
    cipher = AES.new(key_bytes, AES.MODE_GCM, nonce)
    pt = cipher.decrypt_and_verify(ciphertext, tag)
    return pt.decode("utf-8")


if __name__ == "__main__":
    n = 8
    p = 65358582236399098140383852530576291366163143046961680710706395821174671515157
    g = 18897172015605387895108229785692294238197575884158182212205468678506383277799
    known_pt = 78
    known_cts = [25373220597102458819118270498896563550551198455596177940508812860813000903724, 25156039730331034105285572226850008645287631890906242586641210467788804245438,
                 73404587414711470727169747545738295046837501786483259720866734845015056695346, 68236171444104079472751058772448037208084314981744779066329988579261111617628]

    ct_aes = b'x*\x03\xe0:8\xf7\\\xf5\xf6\x97\x8d7\x05\xcf\x86p /\xd6\xb4ckJ\x1f\x1b\x06@\xac'
    nonce = b'\xe9\x90e\x0e%\x02aM\x9bs\xda\x98\xcf\xa4[t'
    tag = b'I\xc8o[\xa2\x04\x9b\xbd#\xe2v!:\r+\x89'
    cts = [42651844259866749777652109751852334753810922885302632764540022961785725233744, 38962962675179610804115807065984374761180509438079916581986078744458559693257, 77750489341031480678888953095578656825807333767073118655532280068161365792606, 106967620549405658878225383295861578373516469393508413358788519949916623945054, 12506141260820485600404762368770582063909244428779357866826381425763526436832, 25148217806590379299835348341257145846438548683096687575115750017117621097902, 102507777156686777297837417174833834754567416489715276354224197526867063981928, 78616697905558496615635752454005191443102285830780691256288272333544313919963, 5600820382095032623157470017643040936655469781667637634099375442253073106259, 55348222940337788484391294444076399324275059964935495228344977023212282399728, 111172466735308514608200283280550784245331118423038000802349351274601434566389, 20576659968932318551182823099803814994985229560076441880737612157752208023750, 56590518216139221348281276526715471621925725899880187063880372624361971156177, 103570998927730487297684126319767190430663268955336658905314356495455879757185, 107268655058580009708248553569057239725394104467917298581456240476060755992798, 97691701976957072469431411543555809176208263982984218660940915491958262044517, 111978913761200708782036230521066343314737866440812663976378442507457478385903, 80499667138183572607934852730556006247772515467461341342116161319802120028661, 55901016259262540805795425483831571168147888863107647334959865496041803412676, 98249171174847162481808842657574641191362370882843366426544411572725621419462, 31602848438288708384653391878832839015038225992004325694554244279423990755846, 50678549145642243401205410803190270641257298215603777187499783292551910495225, 38971806832470200247672636648714950731650559778329550268691988354440246648801, 107899332912624998255543336802470495318022491800929814972209705413740935067892, 9278677990579992929977998399793003133082437203684594334368310223960932538624, 18084128757105870583578436086717596346177628732669861680956837543972688988634, 18021639252920892379829256143948251402045811038506371322270115447677396490455, 55678872154836615800975324980714872765992692276983854064526989075861951738862, 36107699814937344651368382749387533746630806902409892669065356728803731031751, 104094214693807614139178886954947703858514194606390149186468991902694670242177, 69479310102569897629255418811027629959170853032480723999006827603549420426020, 14825188720522723724811784155168516659081401079837250575843389769299173749850,
           91433057278383775673350620237310280715796457103226089670393430239121026880576, 24760668353643271331240742655811904264077802581225204921391746770634796617859, 94405910256847421254485748080999320009114943345757581034520986802370809164420, 81950626480114067700197436041328018191067777321946624245317340049488510548197, 86880896754166649308006049111944319146238792138742636570125132509306795279508, 61126208452546052476968254794257617975190816944718696253999628273755292106982, 3958653863148464525415082407086380796768328609035603357571860312439992246879, 102574417013566533457877258196443196337421396490240635040146912223296529040274, 95332603433535495822487827573369568325422704692375813167987310191600552131001, 66459620264525823264320965097822025217518052055863773220457653322169085114355, 44248963285528668211611716969891343457714678959686397061681385257870632660870, 40025243357336507279353542374474619697411100351328800629120286172014256440031, 40004670603583930384094861355011016545229065720941979265713509045154851190557, 91124188767396573809053560940889202677257839204327731835911304264254562590275, 81001154665478878963423949357007594640141261861143780300545418193445016339562, 47424721549492592370392642713217847771365662652350775475313419793317216827445, 55197784401446351930605654621634225453909183586316149823292471041188688702981, 98117631587553802487312972327306493252760790339163890347260195736749276635060, 7127494587023057683296620906137919152883501310199578066497301410373310047506, 63457302921116033759283530306275020803728714270362559729232534680817619134937, 22196296840125815246009103779899047804906144285287929397938120520043956013863, 54163751214483484526460349388383309649993265080898720511422169626468731493349, 111863272472298988352620342634978236815146720518734788813826780643266409900258, 52971622821199567352929844391746792373961645207000843037420318875981181281191, 2354971284486255858463625319614759017595532608866018405947718283249170077091, 105804186003248869157641542881869646659657498347516008116850639298856577148657, 77413691936799751996897710420533278813526143214955170016148266184895645994304, 21235732005162212323539335094754684926790445432545146253508643920962826425717, 49516872687902344016153098438668118367593706275871672094140384572332111585226, 33644970418120195673261389520706270795228090131141372150846435252518308886081, 23302211403542638754247556237438745551707212166223263270391505041982729963290, 87737310234724917408236672113090567909695310379062911979018170111265223089935]

    g_pow_values, solutions = find_kexp_and_fixed_bits(
        g, p, n, known_pt, known_cts)
    known_keys = find_possible_keys(solutions, known_cts, n, g_pow_values)
    assert known_keys == set([known_pt])

    keys = find_possible_keys(solutions, cts, n, g_pow_values)

    for key in keys:
        decrypted = decrypt(ct_aes, tag, nonce, key)
        print(f'Possible answer: {decrypted}')
