from pylenza import strings


def test_basic_utilities():
    assert strings.to_list('abc') == ['a', 'b', 'c']
    assert strings.from_list(['x', 'y']) == 'xy'
    assert strings.reverse('ab') == 'ba'
    assert strings.is_palindrome('Racecar') is True
    assert strings.count_chars('aab') == {'a': 2, 'b': 1}
    assert strings.unique_chars('abca') == 'abc'


def test_transformations():
    assert strings.capitalize_words('hello world') == 'Hello World'
    assert strings.to_lower('A') == 'a'
    assert strings.to_upper('a') == 'A'
    assert strings.swap_case('aB') == 'Ab'
    assert strings.remove_whitespace(' a \n b\t') == 'ab'
    assert strings.normalize_spaces('  a   b  ') == 'a b'


def test_substrings_and_patterns():
    s = 'ababa'
    assert strings.substring(s, 1, 4) == 'bab'
    assert strings.count_substring(s, 'aba') == 2
    assert strings.find_all(s, 'aba') == [0, 2]
    assert strings.starts_with('hello', 'he')
    assert strings.ends_with('hello', 'lo')


def test_functional_helpers():
    assert strings.map_chars('abc', lambda c: c.upper()) == 'ABC'
    assert strings.filter_chars('a1b2', lambda ch: ch.isalpha()) == 'ab'
    assert strings.reduce_chars('123', lambda a, b: a + b, '') == '123'


def test_numeric_string_helpers():
    assert strings.to_int_list('1,2,3') == [1, 2, 3]
    assert strings.to_float_list('1.5, 2') == [1.5, 2.0]
    assert strings.sum_digits('a1b2') == 3
    assert strings.numeric_only('a1b2') == '12'
    assert strings.alpha_only('a1b2') == 'ab'


def test_advanced_helpers():
    assert strings.anagrams('listen', 'silent') is True
    assert strings.longest_common_prefix(['flower', 'flow', 'flight']) == 'fl'
    pals = strings.palindromic_substrings('aba')
    # 'aba' has palindromic substrings 'aba' and 'aa'(?). at least 'aba' and 'b' excluded since len>1
    assert 'aba' in pals
    perms = strings.all_permutations('ab')
    assert set(perms) == {'ab', 'ba'}


def test_edge_cases():
    assert strings.count_substring('', '') == 0
    assert strings.find_all('', '') == []
    assert strings.to_int_list('') == []
    assert strings.to_float_list('') == []
