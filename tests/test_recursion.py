from pylenza import recursion


def test_basic_recursion_math():
	assert recursion.factorial(0) == 1
	assert recursion.factorial(5) == 120
	assert recursion.fibonacci(0) == 0
	assert recursion.fibonacci(10) == 55
	assert recursion.gcd(12, 8) == 4
	assert recursion.lcm(6, 8) == 24
	assert recursion.power(2, 10) == 1024
	assert recursion.power(2, -2) == 0.25


def test_list_recursions():
	arr = [1, 2, 3, 4]
	assert recursion.sum_list(arr) == 10
	assert recursion.product_list(arr) == 24
	assert recursion.max_list(arr) == 4
	assert recursion.min_list(arr) == 1
	assert recursion.find_index(arr, 3) == 2
	assert recursion.find_index(arr, 99) == -1


def test_strings_and_perms():
	assert recursion.reverse_string('abc') == 'cba'
	assert recursion.is_palindrome('aba') is True
	assert recursion.count_char('banana', 'a') == 3
	subs = recursion.all_substrings('ab')
	assert set(subs) >= {'a', 'b', 'ab'}
	perms = recursion.permutations([1, 2])
	assert sorted(perms) == [[1, 2], [2, 1]]
	combs = recursion.combinations([1, 2, 3], 2)
	assert sorted(combs) == [[1, 2], [1, 3], [2, 3]]


def test_hanoi_and_search_and_subset():
	moves = recursion.tower_of_hanoi(2, 'A', 'C', 'B')
	assert moves == [('A', 'B'), ('A', 'C'), ('B', 'C')]
	assert recursion.binary_search_recursive([1, 2, 3, 4], 3) == 2
	assert recursion.binary_search_recursive([], 1) == -1
	assert recursion.subset_sum([3, 34, 4, 12, 5, 2], 9) is True
	assert recursion.subset_sum([3, 34, 4], 100) is False
