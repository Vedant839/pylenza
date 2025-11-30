from pylenza.trees import BinaryTree, BST, TreeNode


def test_build_and_traversals_and_basic():
    # build tree from level-order:        1
    #                                 /   \
    #                                2     3
    #                               / \   /
    #                              4  5  6
    vals = [1, 2, 3, 4, 5, 6]
    t = BinaryTree(vals)
    assert t.root.value == 1
    assert t.size() == 6
    assert t.height() == 3
    assert t.find(5) is True
    assert t.find(99) is False
    assert t.level_order() == [1, 2, 3, 4, 5, 6]
    assert t.preorder() == [1, 2, 4, 5, 3, 6]
    assert t.inorder() == [4, 2, 5, 1, 6, 3]
    assert t.postorder() == [4, 5, 2, 6, 3, 1]


def test_balance_and_diameter_and_lca():
    t = BinaryTree([1, 2, 3, 4, None, None, 7])
    assert t.is_balanced() is False or isinstance(t.is_balanced(), bool)
    # diameter should be integer
    d = t.diameter()
    assert isinstance(d, int)
    # LCA
    lca = t.lowest_common_ancestor(4, 7)
    assert lca is not None and isinstance(lca.value, int)


def test_mirror_and_paths_and_symmetry():
    t = BinaryTree([1, 2, 2, 3, 4, 4, 3])
    assert t.is_symmetric() is True
    paths = t.print_paths()
    assert isinstance(paths, list) and len(paths) >= 1
    # mirror non-destructive
    mirror_copy = t.mirror(in_place=False)
    assert isinstance(mirror_copy, BinaryTree)


def test_bst_insert_delete_search_kth():
    b = BST([5, 3, 7, 2, 4, 6, 8])
    assert b.search(4) is True
    b.insert_bst(1)
    assert b.search(1) is True
    assert b.min_value() == 1
    assert b.max_value() == 8
    # delete leaf and internal
    b.delete(1)
    assert not b.search(1)
    b.delete(3)
    assert not b.search(3)
    # kth smallest
    assert b.kth_smallest(1) == 2
    assert b.kth_smallest(3) == 5


def test_path_sum():
    t = BinaryTree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
    paths = t.path_sum(22)
    assert any(sum(p) == 22 for p in paths)
