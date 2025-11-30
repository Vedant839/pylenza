from pylenza.arrays import PyArray


def test_init_and_repr_and_to_list():
	a = PyArray()
	assert repr(a).startswith("PyArray(" )
	assert a.to_list() == []

	b = PyArray((1, 2, 3))
	assert b.to_list() == [1, 2, 3]

	c = PyArray(b)
	assert c.to_list() == [1, 2, 3]


def test_mutators_and_accessors():
	a = PyArray([1, 2, 3])
	a.append(4)
	assert a.to_list() == [1, 2, 3, 4]
	a.insert(1, 10)
	assert a.to_list() == [1, 10, 2, 3, 4]
	val = a.pop()
	assert val == 4
	a.delete(10)
	assert a.to_list() == [1, 2, 3]
	assert a.index(2) == 1
	assert a.index(100) == -1
	assert a.count(2) == 1
	assert a.slice(0, 2).to_list() == [1, 2]
	assert a.contains(3) is True


def test_transformations_nested_and_chunk():
	a = PyArray([1, [2, 3], (4, [5, 6]), "abc"])
	# flatten should not expand strings
	f = a.flatten(in_place=False)
	assert f.to_list() == [1, 2, 3, 4, 5, 6, "abc"]
	# flatten copy
	assert a.flatten_copy() == [1, 2, 3, 4, 5, 6, "abc"]

	# reverse & rotate
	x = PyArray([1, 2, 3, 4])
	r = x.reverse(in_place=False)
	assert r.to_list() == [4, 3, 2, 1]
	assert x.rotate(1, in_place=False).to_list() == [4, 1, 2, 3]

	# merge
	m = PyArray([1, 2]).merge([3, 4])
	assert m.to_list() == [1, 2, 3, 4]

	# chunk and chunk_iter
	ch = PyArray(list(range(7))).chunk(3)
	assert [c.to_list() for c in ch] == [[0, 1, 2], [3, 4, 5], [6]]
	it = PyArray([0, 1, 2, 3]).chunk_iter(2)
	assert [p.to_list() for p in it] == [[0, 1], [2, 3]]


def test_utilities_and_functionals():
	a = PyArray([1, 1, 2, 3, 3])
	assert a.unique().to_list() == [1, 2, 3]
	assert a.unique(stable=False).to_list() and isinstance(a.unique(stable=False).to_list(), list)

	mapped = a.map(lambda x: x * 2)
	assert mapped.to_list() == [2, 2, 4, 6, 6]
	filt = a.filter(lambda x: x % 2 == 1)
	assert filt.to_list() == [1, 1, 3, 3]
	total = PyArray([1, 2, 3]).reduce(lambda a, b: a + b)
	assert total == 6


def test_numeric_ops_and_normalize():
	nums = PyArray([1, 2, 3, 4])
	assert nums.sum() == 10
	assert nums.product() == 24
	assert nums.mean() == 2.5
	assert nums.median() == 2.5
	assert nums.mode() in [1, 2, 3, 4]

	norm = nums.normalize(in_place=False)
	assert min(norm.to_list()) == 0.0 and max(norm.to_list()) == 1.0

	s_arr, params = nums.standardize(in_place=False)
	assert isinstance(params, dict) and 'mean' in params and 'std' in params


def test_search_sort_and_advanced():
	a = PyArray([1, 2, 3, 4, 5])
	assert a.search(3) == 2
	assert a.search(9) == -1

	arr = PyArray([3, 1, 4, 2])
	assert arr.sort().to_list() == [1, 2, 3, 4]
	assert arr.sort(algorithm='mergesort').to_list() == [1, 2, 3, 4]

	# find_missing only works for ints
	holes = PyArray([1, 2, 4, 6]).find_missing()
	assert holes == [3, 5]

	common = PyArray([1, 2, 3]).common_elements([2, 3, 4])
	assert common.to_list() == [2, 3]

	assert PyArray([2, 4, 6]).all_satisfy(lambda x: x % 2 == 0)
	assert PyArray([1, 2, 3]).any_satisfy(lambda x: x == 2)

