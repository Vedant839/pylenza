from pylenza.utils import helpers


def test_math_helpers():
    assert helpers.is_prime(2) is True
    assert helpers.is_prime(15) is False
    assert helpers.gcd(12, 8) == 4
    assert helpers.lcm(6, 8) == 24
    assert helpers.factorial(5) == 120
    assert helpers.ncr(5, 2) == 10


def test_iterable_helpers():
    assert list(helpers.chunks([1,2,3,4,5], 2)) == [[1,2], [3,4], [5]]
    assert helpers.flatten_iterable([1, [2, 3], (4, [5])]) == [1,2,3,4,5]
    assert helpers.unique_elements([1,2,1,3]) == [1,2,3]


def test_string_helpers_and_prints_and_random():
    assert helpers.is_palindrome('racecar')
    assert helpers.reverse_string('ab') == 'ba'
    assert helpers.count_chars('aab') == {'a':2, 'b':1}
    # I/O helpers: ensure they run without error
    helpers.print_matrix([[1,2],[3,4]])
    class N:
        def __init__(self, v, nxt=None):
            self.value = v; self.next = nxt
    head = N(1, N(2))
    helpers.print_linkedlist(head)
    lst = helpers.random_int_list(3, 0, 5)
    assert len(lst) == 3
    shuffled = helpers.shuffle_list([1,2,3])
    assert set(shuffled) == {1,2,3}


def test_time_decorator_returns_elapsed():
    @helpers.time_function
    def slow(x):
        s = 0
        for i in range(x):
            s += i
        return s

    res, elapsed = slow(1000)
    assert isinstance(elapsed, float) and res == sum(range(1000))
