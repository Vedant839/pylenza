from pylenza import search


def test_linear_search_and_all_and_count():
    arr = [1, 2, 3, 2, 4]
    assert search.linear_search(arr, 2) == 1
    assert search.linear_search(arr, 99) == -1
    assert search.linear_search_all(arr, 2) == [1, 3]
    assert search.count_occurrences(arr, 2) == 2


def test_binary_iterative_and_recursive_and_key():
    arr = [1, 2, 3, 4, 5]
    assert search.binary_search(arr, 3) == 2
    assert search.binary_search(arr, 9) == -1
    assert search.binary_search_recursive(arr, 4) == 3

    # key function: search for object with property
    objs = [{'x': 1}, {'x': 3}, {'x': 5}]
    idx = search.binary_search(objs, 3, key=lambda o: o['x'])
    assert idx == 1


def test_jump_and_interpolation_and_exponential():
    arr = list(range(1, 101))
    assert search.jump_search(arr, 50) == 49
    assert search.jump_search(arr, 101) == -1

    # interpolation search requires numeric sorted array
    flt = [0.0, 2.0, 4.0, 6.0, 8.0]
    assert search.interpolation_search(flt, 6.0) == 3
    assert search.interpolation_search(flt, 7.0) == -1

    # exponential search works on sorted arrays
    assert search.exponential_search(arr, 1) == 0
    assert search.exponential_search(arr, 90) == 89
    assert search.exponential_search(arr, -10) == -1


def test_find_min_max_and_duplicates():
    arr = [5, 2, 9, 2, 10, 1]
    assert search.find_min(arr) == 5  # index of 1
    assert search.find_max(arr) == 4  # index of 10
    assert search.find_duplicates(arr) == [3]


def test_edge_and_verbose():
    assert search.linear_search([], 1) == -1
    assert search.binary_search([], 1) == -1
    # verbose runs without error (we don't inspect prints)
    _ = search.binary_search([1,2,3], 2, verbose=True)
