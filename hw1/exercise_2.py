import hashlib
import string

from rubik.cube import Cube


class CubeCipher:
    def __init__(self, seed):
        self.seed = seed
        # Create a Rubik's Cube with the specified seed
        self.cube = Cube(self.seed) 

    """
    Displays the current state of the cube. Example:
        MEM # M is the upper right corner of the top face. Accessed via cube.get_piece(1, 1, -1).colors[1]
        JJF 
        MTZ # Z is the bottom right corner of the top face.Accessed via cube.get_piece(1, 1, 1).colors[1]
    UJU XVE VKJ NYJ
    QTA FDX UHK DIG
    GGX PEX KRH TNO
        UIN
        OVG
        PTS

    """
    def display_state(self):
        print(self.cube())

    # Reset the state back to the initialized one.
    def reset(self):
        self.cube = Cube(self.seed)
    
    # Encrypts a plaintext pt with the cube cipher
    def encrypt(self, pt):
        ct = ""
        pos = 0 # used for keeping track of the current position of the plaintext
        
        # - Normally, you can execute the move 'R' with self.cube.R()
        # Since we will repedeatly execute R U R' and U', we prepare the
        # following list of functions
        # - Ri and Ui corresponds to R' and U'.
        moves = [self.cube.R, self.cube.U, self.cube.Ri, self.cube.Ui]
        while len(pt) - len(ct) >= 2:
            # We encrypt two characters with the the two characters we read from the cube
            # Hence, we keep track of this using char_count
            char_count = 0 
            while char_count != 2 and len(ct) != len(pt):
                # We skip the characters that are not in string.ascii_uppercase
                if pt[pos] not in string.ascii_uppercase:
                    ct += pt[pos] # write the skipped characters to ct to preserve strcuture.
                    pos += 1
                    continue
                # Execute R U R' U'
                for move in moves:
                    move()
                # Use upper right for the first character
                if char_count == 0:
                    ct += chr((ord(pt[pos]) + ord(self.cube.get_piece(1, 1, -1).colors[1]))% 26 + ord('A'))
                else: # Use bottom right for the second character.
                    ct += chr((ord(pt[pos]) + ord(self.cube.get_piece(1, 1, 1).colors[1]))% 26 + ord('A'))
                
                # Advance the positions
                pos += 1
                char_count += 1

        # Encrypt the left over character if any.
        if len(pt) != len(ct) and pt[pos] in string.ascii_uppercase:
            # Execute R U R' U'
            for move in moves:
                move()
            ct += chr((ord(pt[pos]) + ord(self.cube.get_piece(1, 1, -1).colors[1]))% 26 + ord('A')) 
            pos += 1

        # Add remaining skipped characters if any
        while len(ct) != len(pt):
            ct += pt[pos]
            pos += 1
        
        return ct

    def decrypt(self, ct):
        print("TODO!")
        
if __name__ == "__main__":
    seed1 = 'KKCVNCQDEPZJCPRHQUFRDQJWKMWHFIJHLACXZNBKDNZZEQHSXOFGUR'
    encrypted1 = 'WVDYN E AZWAVI PELTKP (HYH JYYAUQA QYTJV VP AWRW ZYVI ZW DKW) HTUHDGWZQN KRS JFYKQQCLUQ EQFXA SR IYH JRMBEHF MPDJH HLSKV KLB: XWVQ, ZKCXEJ AY LTIVLVJ IYLZ SW QZOS, CLT XDCO SCV VOKVE BLJU, ECU ZHSXTU WV CIT NKHD ADLOK REEGHU XIMK.  WOO JXIVA DLXEJ ZRI WVDYN APJ D NORTIDS MLDIXZ YJ IYHYO KDVV ISPA! KKLX XWV UHLFXKV CYMRV DSYRV--TDAML WZP, FYY QP WOO LTUJL! DLTE VPVICTH, HXH IYHU KRDKKLB GDEIBCMDE RM FSXTHZ--RSAU XW RMH YHHN--FGRQKI RDN--GVXX RYRRO LXD--KVG APJ LA, YPS WHSVSL? NKHD LPGSLXIS KR FYY? IVOS EW PCO HLSJK LA!  VEHK FHWI P CLADPT WHLLPT, JTBOEZZQN FSXTH, (AREIJ EPVP, IYRBQLI ROPMI,) LVOS, S LPIGSI OCFZ--UY QDIH, ARECB BL; SQ QVWAOV CFZ--IEX XD D KOEA KRV PPJJWLBIS KR AOPA PRB--KPA Z NUYA XJ, VVWIIYLUQ GDDHZ KX BV OPUI P ADJU-MC-KKL-LSM, RQK ET X XRLC PXBH H CON-IRJUII!  JR FYY SZG, VVH UVOSYA! HRLK DLT FWOOVH.  NH TEWI SXYX XWV KVEWT URDX! WPZG ARI GREISXH MRPMI; PEG HVMRV FHVPTU RBD EH CRBN EH JKL MSJCG, PP CDL GV. SPA JHA NMCRK HD CDL!  WOOVT NDZ K HTRG ZSPTEFL SRHKDUDPN, RQK KPXTH ARSJXKA DS WVUZOPU, Z ZVXHTI ZOKX IYHF GMAC GV XIMK! LM DLTP KHN ECP VLXWT, KKLIH IRNL DLT IRVP SUW. DMDIG R PPXYIV RY DAD, KKLI FTXDU WSKZQN KFDLW HQEXE, DUN EAZFL RIPIG ARI GREISX HRB, H LEGI'
    checksum1 = 'f187ebde770eae681488e27fe9511434ad81585a0334348be21625fa03772f58'

    cube1 = CubeCipher(seed1)
    m1 = cube1.decrypt(encrypted1)
    assert hashlib.sha256(m1.encode()).hexdigest() == checksum1
    print(f'Question 2.1: {m1}')
