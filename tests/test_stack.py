from pylenza.stack import Stack, EmptyStackError


def test_basic_push_pop_peek_len():
    s = Stack()
    assert len(s) == 0
    s.push(1)
    s.push(2)
    s.push(3)
    assert len(s) == 3
    assert s.peek() == 3
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1
    try:
        s.pop()
        raise AssertionError("expected exception on empty pop")
    except EmptyStackError:
        pass


def test_bulk_operations_contains_index_reverse_merge_chunk():
    s = Stack([1, 2, 3])
    s.push_multiple([4, 5])
    assert s.to_list() == [1, 2, 3, 4, 5]
    assert s.contains(4) is True
    assert s.index(5) == 0  # top-based index
    assert s.index(99) == -1

    popped = s.pop_n(2)
    assert popped == [5, 4]
    assert s.to_list() == [1, 2, 3]

    r = s.reverse(in_place=False)
    assert r.to_list() == [3, 2, 1]

    m = s.merge(Stack([7, 8]))
    assert m.to_list() == [1, 2, 3, 7, 8]

    chunks = Stack(list(range(6))).chunk(2)
    assert [c.to_list() for c in chunks] == [[0, 1], [2, 3], [4, 5]]


def test_numeric_helpers_and_functionals():
    s = Stack([1, 2, 3, 4])
    assert s.sum() == 10.0
    assert s.product() == 24.0
    assert s.mean() == 2.5
    assert s.median() == 2.5
    assert s.mode() in [1, 2, 3, 4]

    mapped = s.map(lambda x: x * 2)
    assert mapped.to_list() == [2, 4, 6, 8]
    filtered = s.filter(lambda x: x % 2 == 0)
    assert filtered.to_list() == [2, 4]
    total = s.reduce(lambda a, b: a + b)
    assert total == 10


def test_edge_cases_empty_stack():
    s = Stack()
    try:
        s.peek()
        raise AssertionError("peek should raise on empty")
    except EmptyStackError:
        pass

    try:
        s.reduce(lambda a, b: a + b)
        raise AssertionError("reduce should raise when no initial and empty")
    except TypeError:
        pass
