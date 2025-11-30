from pylenza.queue import Queue, EmptyQueueError


def test_basic_fifo_and_peek_and_len():
    q = Queue()
    assert len(q) == 0
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert len(q) == 3
    assert q.peek() == 1
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.dequeue() == 3
    try:
        q.dequeue()
        raise AssertionError("expected exception on empty dequeue")
    except EmptyQueueError:
        pass


def test_bulk_operations_and_contains_index_rotate():
    q = Queue([1, 2, 3])
    q.enqueue_multiple([4, 5])
    assert q.to_list() == [1, 2, 3, 4, 5]
    assert q.contains(3) is True
    assert q.index(4) == 3
    assert q.dequeue_n(2) == [1, 2]
    assert q.to_list() == [3, 4, 5]
    q.rotate(1)
    assert q.to_list() == [5, 3, 4]


def test_map_filter_reduce_and_reverse_merge_chunk():
    q = Queue([1, 2, 3, 4])
    q2 = q.map(lambda x: x * 10)
    assert q2.to_list() == [10, 20, 30, 40]
    q3 = q.filter(lambda x: x % 2 == 0)
    assert q3.to_list() == [2, 4]
    total = q.reduce(lambda a, b: a + b)
    assert total == 10

    r = q.reverse(in_place=False)
    assert r.to_list() == [4, 3, 2, 1]

    merged = q.merge(Queue([5, 6]))
    assert merged.to_list() == [1, 2, 3, 4, 5, 6]

    chunks = q.chunk(2)
    assert [c.to_list() for c in chunks] == [[1, 2], [3, 4]]


def test_priority_and_numeric_helpers():
    pq = Queue()
    pq.enqueue_priority('low', 10)
    pq.enqueue_priority('high', 1)
    pq.enqueue_priority('mid', 5)
    # after priority enqueue, internal items are tuples; mode should extract values
    assert pq.mode() in ('low', 'mid', 'high')

    qn = Queue([1, 2, 3, 4])
    assert qn.sum() == 10.0
    assert qn.product() == 24.0
    assert qn.mean() == 2.5
    assert qn.median() == 2.5
    assert qn.mode() in [1, 2, 3, 4]


def test_edge_cases():
    q = Queue()
    try:
        q.peek()
        raise AssertionError("peek should raise on empty")
    except EmptyQueueError:
        pass

    try:
        q.reduce(lambda a, b: a + b)
        raise AssertionError("reduce should raise when no initial and empty")
    except TypeError:
        pass
