from pylenza.linkedlist import LinkedList


def test_init_and_conversion():
    l = LinkedList()
    assert repr(l).startswith("LinkedList(")
    assert len(l) == 0
    assert l.to_list() == []

    l2 = LinkedList([1, 2, 3])
    assert l2.to_list() == [1, 2, 3]
    assert len(l2) == 3


def test_mutators_and_accessors():
    l = LinkedList()
    l.append(1)
    l.append(2)
    l.prepend(0)
    assert l.to_list() == [0, 1, 2]

    l.insert(1, 5)
    assert l.to_list() == [0, 5, 1, 2]

    assert l.pop() == 2
    assert l.to_list() == [0, 5, 1]

    assert l.delete(5) is True
    assert l.to_list() == [0, 1]
    assert l.delete(99) is False

    assert l.contains(1) is True
    assert l.index(1) == 1
    assert l.index(99) == -1
    assert l.get(0) == 0


def test_find_middle_and_nth_from_end_and_iter():
    l = LinkedList([1, 2, 3, 4, 5])
    mid = l.find_middle()
    assert mid.value in (2, 3, 4)  # left-middle or middle acceptable in our implementation

    assert l.nth_from_end(0) == 5
    assert l.nth_from_end(1) == 4

    collected = [x for x in l]
    assert collected == [1, 2, 3, 4, 5]


def test_transformations_and_advanced():
    l = LinkedList([1, 2, 3, 4])
    # reverse non-destructive
    r = l.reverse(in_place=False)
    assert r.to_list() == [4, 3, 2, 1]
    # rotate
    l2 = LinkedList([1, 2, 3, 4, 5])
    l2.rotate(2)
    assert l2.to_list() == [4, 5, 1, 2, 3]

    # merge
    merged = LinkedList([1, 2]).merge(LinkedList([3, 4]))
    assert merged.to_list() == [1, 2, 3, 4]

    # remove duplicates
    dup = LinkedList([1, 2, 2, 3, 1]).remove_duplicates()
    assert dup.to_list() == [1, 2, 3]

    # split_middle and sort
    l3 = LinkedList([5, 2, 3, 1, 4])
    left, right = l3.split_middle()
    assert isinstance(left, LinkedList) and isinstance(right, LinkedList)
    sorted_l3 = l3.sort()
    assert sorted_l3.to_list() == [1, 2, 3, 4, 5]


def test_palindrome_and_cycle_and_common_and_flatten_and_numeric():
    p = LinkedList([1, 2, 3, 2, 1])
    assert p.is_palindrome() is True

    # create cycle: last node -> second node
    c = LinkedList([1, 2, 3])
    # create a cycle by pointing tail.next to head.next
    head = c._head
    if head and head.next and c._tail:
        c._tail.next = head.next
    assert c.detect_cycle() is True

    # common elements
    a = LinkedList([1, 2, 3])
    b = LinkedList([2, 4])
    assert a.common_elements(b).to_list() == [2]

    # flatten nested lists
    nested = LinkedList([1, LinkedList([2, 3]), [4, [5]]])
    assert nested.flatten().to_list() == [1, 2, 3, 4, 5]

    # numeric ops
    nums = LinkedList([1, 2, 3, 4])
    assert nums.sum() == 10.0
    assert nums.product() == 24.0
    assert nums.mean() == 2.5
    assert nums.median() == 2.5
    assert nums.mode() in [1, 2, 3, 4]

    norm = nums.normalize(in_place=False)
    assert min(norm.to_list()) == 0.0 and max(norm.to_list()) == 1.0

    s, params = nums.standardize(in_place=False)
    assert 'mean' in params and 'std' in params

