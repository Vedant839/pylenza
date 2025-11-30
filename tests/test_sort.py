from pylenza import sort


def _bases():
    return [5, 3, 2, 8, 1, 4, 7, 6]


def test_basic_sorts_and_is_sorted():
    a = _bases()
    for fn in (sort.bubble_sort, sort.selection_sort, sort.insertion_sort, sort.merge_sort, sort.quick_sort, sort.tim_sort):
        s = fn(a)
        assert sort.is_sorted(s)
        assert s == sorted(a)

    # quick sort pivot strategies
    assert sort.quick_sort(a, pivot_strategy='first') == sorted(a)
    assert sort.quick_sort(a, pivot_strategy='middle') == sorted(a)


def test_heap_counting_radix():
    a = [3, 1, 2, 4, 2, 0, -1]
    assert sort.heap_sort(a) == sorted(a)
    assert sort.counting_sort(a) == sorted(a)
    assert sort.radix_sort(a) == sorted(a)


def test_reverse_and_key_and_almost_sorted():
    a = _bases()
    assert sort.bubble_sort(a, reverse=True) == sorted(a, reverse=True)

    people = [{'age': 30}, {'age': 20}, {'age': 40}]
    s = sort.merge_sort(people, key=lambda p: p['age'])
    assert [p['age'] for p in s] == [20, 30, 40]

    assert sort.almost_sorted([1, 2, 4, 3], max_swaps=1) is True
    assert sort.almost_sorted([4, 3, 2, 1], max_swaps=1) is False


def test_edge_cases():
    assert sort.bubble_sort([]) == []
    assert sort.merge_sort([1]) == [1]
    assert sort.counting_sort([]) == []
