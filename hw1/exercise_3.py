from Crypto.Cipher import AES
import random

Q3_n=8
Q3_p=65358582236399098140383852530576291366163143046961680710706395821174671515157
Q3_g=18897172015605387895108229785692294238197575884158182212205468678506383277799

def decrypt(Q3_ct_aes, Q3_tag, Q3_nonce, rec_k_aes):
    # rec_k_aes is assumed to be an int
    rec_k_aes_bytes = rec_k_aes.to_bytes(16, "big")
    cipher = AES.new(rec_k_aes_bytes, AES.MODE_GCM, Q3_nonce)
    Q3_pt = cipher.decrypt_and_verify(Q3_ct_aes, Q3_tag)
    return Q3_pt

def faulty_keygen() -> int:
    b = int.from_bytes(random.randbytes(32), "big")
    b = b | (0x3 << (32 - Q3_n))    # make 11 at correct position
    return b


def encrypt_2bits(k_exp, m, j) -> int:
    k_xor = faulty_keygen()
    r = random.randint(0, Q3_p)
    c = k_xor ^ pow(Q3_g, k_exp + 52*r + m+ 2*(j+1), Q3_p)
    return c

def encrypt_key(k_exp, k_aes):
    j = 0
    cts = []
    while k_aes > 0 :
        m = k_aes & 0x0b11
        c = encrypt_2bits(k_exp, m, j)
        cts += c
        j += 1
        k_aes = k_aes >> 2
    return cts

# def find_k_aes():



# L = ["candidate1", "candidate2"]
# L_bytes = bytes()
# for item in L:
#     L_bytes += bytes(item, "utf-8")


###### Exercise 3
Q3_known_pt=78
Q3_known_cts=[78827043567212480155170140646673037362912267749303007185181943742797255118007, 100799022190225447015927611342260995812725000665589698629426462534627779522085, 95970175372447404503883762799694438821752264171363111731695755941226725968218, 37779024407629451623659794763654507713152606641711826908444541448262497395545]
Q3_ct_aes=b'0\x02p\x91\xaf\xb1\x8dB\xe7\x85\x8e\xe4uti\x1eq\xb9\x01t\x9e\x93\xdc\xc4\xc6\x0c\xac\xce\x8b'
Q3_nonce=b'\x80\xc6\xb8\xcbZ\xa1yl\x16\xa8k\xbd\xcf\xe4\xf7\xca'
Q3_tag=b'\xd7\x80RC\x95A)\xfa\xf1\xe4\x10\x03>V\xb1\x01'
Q3_cts=[99892985083459113959731261981400346071271994247048836649362803331478863186103, 63176309604312519887769171060930416854728506671863234646380619240853332829124, 87223692380444382801634452242198947562425809988625644344457872734715704502900, 46339852118750263564298993487172770263339264037215307760864277194669876622223, 102856064718134552534699044942752923203380588394184287206749094412322343640163, 98539371571930860434030724002762156538048979106040262937157081384192199900380, 106252905354670441615210734301199437700542874286868948148845980521559842082484, 74204644518803893989207188126303407392967114451897948127204474259499939749249, 101364160715491256991097859871073342150280460766961993339605376397450061573222, 88114256988821266452652135702491997256347627180011602728479615881656179441596, 18954054751576961097445936314008334472753142917970226204328972661471975533800, 94100724353634631853579244934838236306734264938489204810569081282560833516248, 10258914934692375192468470695677916565583096414672677458485801899026037631416, 71688617322759009390219093154054003523558383881140074826100405554017863735525, 10038239651903885316368049198179020014997456533058177054193478923578720606145, 51984280955868691915917740161765637188588877606049180929807135636509426585160, 34385897477682436659495426192639307395806705254182014846272681325526650219303, 93109567834524675304975971418982421159206879072254405061050755033632975507372, 42168343776750307549256226088840484699112882105669121046979217528929990906808, 92526450439575859261682826326889794450991086913107491734180599222629732705222, 105225868180714542367179295564887973013910770958756618697576857153870281651814, 8494481733489552930234956111163666758556786973935473811753241518289684966723, 11712986018821819975958911563954563554912620567676476788998980273214894320026, 17284702173434216246417477567790928557286113330415911200964893361576253662109, 61049235630014060233543387586107974285122162692646579480153527314955735806034, 522985065371574769336721058648386212532270620987464647197154782310897355964, 32814684335483412368358979184383727551932904528688786805461524130376628253874, 94920139772324900767801319000081627829232791789514847552870848762404550418192, 92669897295261666138457538566191446022077898276332932102730348952579710090385, 18632267171728552323419047355458251509176473616214609190074225445689030331198, 26297407467677788613766105933722223070076395583397554903659752357697901724646, 36846726841251819704236822727158183296044412081546306951720765041973074383545, 21856185468472132523256317641836235929257264433345941725953252645980974597379, 100932665262562598669377595988151452285729555810326969292654400458955420859778, 70501077514136179880681005486610668202034983853066880648501471028818604079231, 55039574102949361364971571017278684723147481189404794782208666883184626855356, 58755014553841844297161371697146917547863802088852058575359476447818604452979, 40758061529582293432847504142809848810454403184372628074904799497162422454011, 50347667076682058135210587273571053793078689487862986400057263387231614609172, 89095592227924646199738917933224379068272468529123755714624306471264759506057, 20845252502656514500211441989753587056927097411055285410525675263053011864849, 41714692170363488143146642190622621993752992803786354118310135621795934253180, 23971408135624632416849467980300027404418225882443246534457491915969038052394, 80620602889102634592192986644173813882145225427660012106022204230196486927168, 44306503914562386607144409419904917712917787441700944262538878799964314306973, 19206108254660968461186394863657138424337972080846370344972655116311360519105, 85728256212886925757422529675562411214188783883603842622588106168470368594737, 63895493953824731121437050509856611005761982955332702830124387549813413330729, 74944630416337999639037509945455763225639841055018917700422029012063665165138, 81250174966732978335741271954013316184974459263589707898282228153920048202800, 39831059454908839416357485934414397126397404773955685164766785345887151973334, 67673751005623647405176437601869311832475966705950531160063266357682898717726, 14148175142567331723538527904598060307723539452730565362071310308117755446659, 52202705551418532386427349295293741704502299050369110513789762711013147251173, 4084627050828730368086254052647812766845236166531240888859751503571156735589, 37835534835006366868018656563139407452766617671881395308574479416064416035504, 98283741177706721116046056044843924391442062841984950351935577633459017853289, 53049081786288216212689555966719942291439093837880165072723648397885265462588, 85736874592967876333127742583499658630744334896257772857274270755785221210221, 99896247360373958541472492270454147223992127806244186154578125638036201199322, 73100910499359018906232643625137816913092974010380891690790399896278905104746, 31108869584700062044590534650561511646351960867183307212117054067315447898954, 74183451517413980819391948523174461497702107773913529821867046615628007863716, 73257844315559211171831727895804593692294765027290093730954170515746954956341]