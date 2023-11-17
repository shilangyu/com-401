from itertools import product

M = 9151063482979447295197497525159219420159216843808721717858389068195800654942747788107766720996511469789912776999335553540508006644649629228612348410664578156123415272693849701869436525466190748424759940506916663366808463981848264948248442610289001520852941230569149210699065424036406918552037426943293813391

N = 55329523439490792940776556326840034438933797346917829980124667610423818209649647401012921065101508927582981225376194203858481433052266694510798153343866931437962373908913600821954589019333744566016667518558150006696465408044396587824815834823670418516083534442971221387885435778322869619653591417633743376959
# Since the list is of length 2 L[0]**4 mod N == 1
# L[0] is the seed in gen_list(N, seed)
L = [9151063482979447295197497525159219420159216843808721717858389068195800654942747788107766720996511469789912776999335553540508006644649629228612348410664578156123415272693849701869436525466190748424759940506916663366808463981848264948248442610289001520852941230569149210699065424036406918552037426943293784064, 42112042721601009145703761012820681968809008500140429878596325346201759003663622211266927877294828560034644829839400987304155841354208826676307782095229052161872609350987597249107218139058571084419254499654034033795236231624670685833845495408888720442182391422051622812303953847403816748436874681001740468224]   
Y = 16665235139620759082085186776193291633779377325598573700557362024337566288839425793987012850272603177660643335199442734151799958662776827949791363611830471795562612687430139582811821935672715894201730432975404898016108229599837202473374770226371435068804710923569270965997224866156298018940569855851867055423 

def q3a():
    """
    Returns the roots of Y.
    """
    Z_N = Integers(N)
    recoverd_list = []
    # Generate all bits permutations of length 15
    last_bits = ""
    for bits in product(['0','1'], repeat=15):
        guess = Z_N(int(bin(L[0])[2:-15] + "".join(bits), 2))
        if guess**4 == 1:
            recoverd_list.append(guess)
            last_bits = "".join(bits)
            break

    recoverd_list.append(recoverd_list[0]**2)   # recover the second element

    y = Z_N(Y)
    print(y**((N-1)/2))

    """
    y = Z_N(Y)
    print(y**int(last_bits, 2))
    b = Z_N(int(last_bits, 2))
    
    i = 1;
    while b != y:
        b = b**i

    print(i)
    """

    return recoverd_list



if __name__ == "__main__":
    print(q3a())
