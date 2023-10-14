from exercise_1 import decrypt, encrypt, prepare_key, prepare_message


def test_check_key():
    k1 = [['l', 'y', 'n', 'b', 'e'],
          ['z', 'm', 'V', 'r', 'h'],
          ['j', 'g', 'u', 'q', 'a'],
          ['c', 't', 'o', 's', 'w'],
          ['d', 'k', 'x', 'p', 'f']]
    k2 = [['l', 'y', 'n', 'b', 'e'],
          ['z', 'l', 'v', 'r', 'h'],
          ['i', 'g', 'u', 'q', 'a'],
          ['c', 't', 'o', 's', 'w'],
          ['d', 'k', 'x', 'p', 'f']]
    k3 = [['l', 'y', 'n', 'b', 'e'],
          ['z', 'm', 'v', 'r'],
          ['i', 'g', 'u', 'q', 'a'],
          ['c', 't', 'o', 's', 'w'],
          ['d', 'k', 'x', 'p', 'f']]
    k4 = [['l', 'y', 'n', 'bp', 'e'],
          ['z', 'm', 'v', 'r', 'h'],
          ['i', 'g', 'u', 'q', 'a'],
          ['c', 't', 'o', 's', 'w'],
          ['d', 'k', 'x', 'p', 'f']]
    k5 = [['l', 'y', 'n', 'b', 'e'],
          ['i', 'g', 'u', 'q', 'a'],
          ['c', 't', 'o', 's', 'w'],
          ['d', 'k', 'x', 'p', 'f']]

    assert prepare_key(k1) == [['l', 'y', 'n', 'b', 'e'],
                               ['z', 'm', 'v', 'r', 'h'],
                               ['i', 'g', 'u', 'q', 'a'],
                               ['c', 't', 'o', 's', 'w'],
                               ['d', 'k', 'x', 'p', 'f']]

    try:
        prepare_key(k2)
        assert False
    except RuntimeError:
        pass
    try:
        prepare_key(k3)
        assert False
    except RuntimeError:
        pass
    try:
        prepare_key(k4)
        assert False
    except RuntimeError:
        pass
    try:
        prepare_key(k5)
        assert False
    except RuntimeError:
        pass


def test_prepare_message():
    assert prepare_message('abc') == [('a', 'b'), ('c', 'x')]
    assert prepare_message('caesar') == [('c', 'a'), ('e', 's'), ('a', 'r')]
    assert prepare_message('abba') == [('a', 'b'), ('x', 'b'), ('a', 'x')]

    try:
        prepare_message('xamax')
        assert False
    except RuntimeError:
        pass

    try:
        prepare_message('zaxxaz')
        assert False
    except RuntimeError:
        pass


def test_encrypt():
    assert encrypt([['f', 'o', 'l', 'i', 's'], ['h', 'c', 'm', 'p', 'a'], ['n', 'y', 'b', 'd', 'e'], [
        'g', 'k', 'q', 'r', 't'], ['u', 'v', 'w', 'x', 'z']], 'caesar') == 'mhtapt'


def test_decrypt():
    assert decrypt([['f', 'o', 'l', 'i', 's'], ['h', 'c', 'm', 'p', 'a'], ['n', 'y', 'b', 'd', 'e'], [
        'g', 'k', 'q', 'r', 't'], ['u', 'v', 'w', 'x', 'z']], 'mhtapt') == 'caesar'


if __name__ == "__main__":
    test_check_key()
    test_prepare_message()
    test_encrypt()
    test_decrypt()
