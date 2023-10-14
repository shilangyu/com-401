import hashlib
import string
from collections import Counter
from collections.abc import Callable

from rubik.cube import Cube


class CubeCipher:
    def __init__(self, seed):
        self.seed = seed

    @staticmethod
    def from_key(key: str) -> 'CubeCipher':
        """
        Given a key of length 12 constructs a CubeCipher with a proper seed.
        """
        assert len(key) == 12

        # manually went through cube moves to see where each key lands
        seed = f'{key[8]}!{key[10]}!!!!!{key[11]}{key[0]}!!!!{key[3]}{key[7]}!{key[6]}{key[2]}!{key[4]}!!!!!!!!!!!!!!!!!{key[1]}{key[9]}!!!!!!!{key[5]}!!!!!!'
        return CubeCipher(seed)


    @staticmethod
    def is_encryptable(s: str) -> bool:
        """
        Indicates if a character is encryptable or skipped by the cipher.
        """
        assert len(s) == 1
        return s in string.ascii_uppercase
    
    def get_key(self) -> str:
        """
        Simulates moves of the cube to retrieve the key.
        """
        cube = Cube(self.seed)
        res = ''

        for _ in range(6):
            self.sexy_move(cube)
            res += cube.get_piece(1, 1, -1).colors[1]
            res += cube.get_piece(1, 1, 1).colors[1]
        return res
    
    def sexy_move(self, cube: Cube):
        cube.R()
        cube.U()
        cube.Ri()
        cube.Ui()


    # Maps a string with f using the cube cipher
    def _map_through_sexy_move(self, input: str, f: Callable[[str, str], str]):
        # Create a Rubik's Cube with the specified seed
        cube = Cube(self.seed)

        output = ""
        pos = 0 # used for keeping track of the current position of the plaintext
        
        while len(input) > len(output) + 1:
            # We encrypt two characters with the two characters we read from the cube
            # Hence, we keep track of this using char_count
            char_count = 0 
            while char_count != 2 and len(output) != len(input):
                # We skip the characters that are not in string.ascii_uppercase
                if not CubeCipher.is_encryptable(input[pos]):
                    output += input[pos] # write the skipped characters to ct to preserve structure.
                    pos += 1
                    continue
                # Execute R U R' U'
                self.sexy_move(cube)
                # Use upper right for the first character
                if char_count == 0:
                    output += f(input[pos], cube.get_piece(1, 1, -1).colors[1])
                else: # Use bottom right for the second character.
                    output += f(input[pos], cube.get_piece(1, 1, 1).colors[1])
                
                # Advance the positions
                pos += 1
                char_count += 1

        # Encrypt the left over character if any.
        if len(input) != len(output) and input[pos] in string.ascii_uppercase:
            # Execute R U R' U'
            self.sexy_move(cube)
            output += f(input[pos], cube.get_piece(1, 1, -1).colors[1])
            pos += 1

        # Add remaining skipped characters if any
        while len(output) != len(input):
            output += input[pos]
            pos += 1
        
        return output

    def encrypt(self, m: str) -> str:
        return self._map_through_sexy_move(m, lambda s, k: chr((ord(s) + ord(k)) % 26 + ord('A')))
    
    def decrypt(self, encrypted: str) -> str:
        return self._map_through_sexy_move(encrypted, lambda s, k: chr((ord(s) - ord(k)) % 26 + ord('A')))
    
def mse(xs: dict[str, float], ys: dict[str, float]) -> float:
    return 1/len(xs) * sum((xs[c] - ys[c]) ** 2 for c in string.ascii_uppercase)

def break_cipher(encrypted: str) -> CubeCipher:
    """
    Given an encrypted text we find the seed for the CubeCipher to decrypt it.

    The (R U R' U') sequence is called the sexy move. A Rubik's cube can be seen as a group. Executing the
    sexy move on a cube is an action cube's symmetry. Assuming an initial fixed seed of a cube and then
    performing the sexy move we generate new elements of the symmetry group. In fact, this group has order
    of 6. Indeed, performing the sexy move 6 times brings the cube back to its initial state. This means
    we already know the length of a key: regardless of the seed the key is of length 6 * 2 = 12.

    Knowing the key length allows us to skip the Kasiski test and just start breaking each key character one
    by one. Every 12th character (with the consideration of skipped characters) is encrypted using the same
    key character. We can consider each key character independently trying to find something that resembles
    the distribution of letter from English texts. We consider this key for each of the "quotient groups"
    (every 12th character, every 12th+1 character, every 12th+2 character, etc). The key character that is
    closest to the letter frequencies is assumed to be the character used in the key. The metric for closest
    is the mean squared error.
    """
    
    # source: https://en.wikipedia.org/wiki/Letter_frequency
    eng_freq = {
        'A': 0.082,
        'B': 0.015,
        'C': 0.028,
        'D': 0.043,
        'E': 0.127,
        'F': 0.022,
        'G': 0.020,
        'H': 0.061,
        'I': 0.070,
        'J': 0.0015,
        'K': 0.0077,
        'L': 0.040,
        'M': 0.024,
        'N': 0.067,
        'O': 0.075,
        'P': 0.019,
        'Q': 0.00095,
        'R': 0.060,
        'S': 0.063,
        'T': 0.091,
        'U': 0.028,
        'V': 0.0098,
        'W': 0.024,
        'X': 0.0015,
        'Y': 0.020,
        'Z': 0.0007,
    }
    key_length = 12

    key = ''

    for n in range(key_length):
        # collect pos = n (mod 12) characters
        letters = ''
        i = n
        while i < len(encrypted):
            # skip non encryptable
            while i < len(encrypted) and not CubeCipher.is_encryptable(encrypted[i]):
                i += 1
            if i < len(encrypted):
                letters += encrypted[i]
                i += key_length
        
        # max value of mse is 1, so we pick 2 to always be overriden in the first loop
        best = (None, 2)
        for c in string.ascii_uppercase:
            # try a seed of all c characters
            cube = CubeCipher.from_key(c * 12)
            chars = cube.decrypt(letters)
            freqs = Counter(chars)
            
            error = mse(eng_freq, dict((c, freqs.get(c, 0) / len(chars)) for c in string.ascii_uppercase))
            if best[1] > error:
                best = (c, error)
        key += best[0]

    return CubeCipher.from_key(key)


        
if __name__ == "__main__":
    seed1 = 'KKCVNCQDEPZJCPRHQUFRDQJWKMWHFIJHLACXZNBKDNZZEQHSXOFGUR'
    encrypted1 = 'WVDYN E AZWAVI PELTKP (HYH JYYAUQA QYTJV VP AWRW ZYVI ZW DKW) HTUHDGWZQN KRS JFYKQQCLUQ EQFXA SR IYH JRMBEHF MPDJH HLSKV KLB: XWVQ, ZKCXEJ AY LTIVLVJ IYLZ SW QZOS, CLT XDCO SCV VOKVE BLJU, ECU ZHSXTU WV CIT NKHD ADLOK REEGHU XIMK.  WOO JXIVA DLXEJ ZRI WVDYN APJ D NORTIDS MLDIXZ YJ IYHYO KDVV ISPA! KKLX XWV UHLFXKV CYMRV DSYRV--TDAML WZP, FYY QP WOO LTUJL! DLTE VPVICTH, HXH IYHU KRDKKLB GDEIBCMDE RM FSXTHZ--RSAU XW RMH YHHN--FGRQKI RDN--GVXX RYRRO LXD--KVG APJ LA, YPS WHSVSL? NKHD LPGSLXIS KR FYY? IVOS EW PCO HLSJK LA!  VEHK FHWI P CLADPT WHLLPT, JTBOEZZQN FSXTH, (AREIJ EPVP, IYRBQLI ROPMI,) LVOS, S LPIGSI OCFZ--UY QDIH, ARECB BL; SQ QVWAOV CFZ--IEX XD D KOEA KRV PPJJWLBIS KR AOPA PRB--KPA Z NUYA XJ, VVWIIYLUQ GDDHZ KX BV OPUI P ADJU-MC-KKL-LSM, RQK ET X XRLC PXBH H CON-IRJUII!  JR FYY SZG, VVH UVOSYA! HRLK DLT FWOOVH.  NH TEWI SXYX XWV KVEWT URDX! WPZG ARI GREISXH MRPMI; PEG HVMRV FHVPTU RBD EH CRBN EH JKL MSJCG, PP CDL GV. SPA JHA NMCRK HD CDL!  WOOVT NDZ K HTRG ZSPTEFL SRHKDUDPN, RQK KPXTH ARSJXKA DS WVUZOPU, Z ZVXHTI ZOKX IYHF GMAC GV XIMK! LM DLTP KHN ECP VLXWT, KKLIH IRNL DLT IRVP SUW. DMDIG R PPXYIV RY DAD, KKLI FTXDU WSKZQN KFDLW HQEXE, DUN EAZFL RIPIG ARI GREISX HRB, H LEGI'
    checksum1 = 'f187ebde770eae681488e27fe9511434ad81585a0334348be21625fa03772f58'

    cube1 = CubeCipher(seed1)
    m1 = cube1.decrypt(encrypted1)
    assert hashlib.sha256(m1.encode()).hexdigest() == checksum1
    print(f'Question 2.1: {m1}')

    encrypted2 = 'UHQLF MC WW RGTH BV Y GNFKG. LN, BZE TMND TBZQS, LVX AYHW, OGL QDX KAMRGXF BBQ LTFDMB "OHWLWL" NK BHB; DNK GAM FZW FXIB RXJXZYK GWVM JHMHEM FHLHHZGDL OUWSS VVBTBQXB PPM GTR ZWR ANFGB, YMW STBCM ND UG UHER UMYRMG TVB NMVXZ SMIZXIQZGH MPGMZG, TTJ AXQTCQD MVXG UNNZW VMS KSFMKAXF MPC RBAITC QNZXA RGXWK NPHXBWA FZW HTCEGM HAMK: RNQA IQ, SAOM I PDW-VHB NNDSK EGKE PNZL XHI BN WNN VHTB HM HHW JNGU; TVB SAOM QD XHI VCR XHIK NGMZSK DCQR RXMNKR KBBF Z DBBNC, HM ILCYKEM UTCDWG; TVB RAS AIB MXJXZ DNKUHBRDG HAIR, HY MHC BQBBD USBA TKWK Z UCMBJD FOKSCC ICBAMM, BH BA YKFCLB ADKHTQL SH RBAYFKSX EGSA MHC, QNHBXZ MQ EOMMP.  GHKXDCQ, MVBA ZNMHEM UZL BHB KZKYXL NNBGHV, QN TZBKC UXBMCPDW HH BYRMS BB, YMW TBVBHGU BB TDKM GQAD, (BH AIB, HG TTKR, Z LCKB ME FWQMB EEOOWSQ HT VPCQKM-MIPS, VILBYQW, DBVC-ZIDEM, PNTGM BSQDSR, BMEYSX, ILC ACM JSSMSKMB SHOLB,) QGX JXZW RHCG NGMBGAMB HM CYN.  UGTH T KSQBCNA DDXZBVE! RTWW IJHVS; B USRM PX AFTMHBVE TI ZBSC Z MSEMQBHDX.  ILC LC BB UZL WGLCDW: GAM UZL BHE MMEM MML HGQAMQ GBUA, ILC ASK NYBX PKQEGMSGMB TI OM BFD MVHCEGM HAIR RAS PIQ MHK MPC QBUAB QHSS YWP FHWGO RGKCNOF SAS EQRSES WWMQ BBMW RGTH EWTDEM ZIPCXB. YQPRM, VHECUXF, LPC VTWMMB EHF T NCV FWGCRDL HH ACD BT LPC VTG'
    checksum2 = '406c70ca3c75bb6b12063ae0fb15d635b34a522504192796909b5f44a7c0366b'

    cube2 = break_cipher(encrypted2)
    m2 = cube2.decrypt(encrypted2)
    assert hashlib.sha256(m2.encode()).hexdigest() == checksum2
    print(f'Question 2.2: {m2}')
