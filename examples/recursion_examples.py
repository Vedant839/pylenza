"""Recursion examples demonstrating algorithms from pylenza.recursion and pylenza.trees.

Run standalone with:
    python examples/recursion_examples.py

The examples show small recursion problems and a tree example learners can follow.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pylenza import recursion
from pylenza import trees


def simple_recursion_examples():
    print('\n--- Simple recursion examples ---')
    print('factorial(5) ->', recursion.factorial(5))
    print('fibonacci(10) ->', recursion.fibonacci(10))
    print('gcd(24, 18) ->', recursion.gcd(24, 18))
    print('power(2, 10) ->', recursion.power(2, 10))

    arr = [1, 2, 3, 4]
    print('sum_list([1,2,3,4]) ->', recursion.sum_list(arr))
    print('product_list([1,2,3,4]) ->', recursion.product_list(arr))
    print('max_list([5,2,9,1]) ->', recursion.max_list([5, 2, 9, 1]))


def nested_and_string_recursion():
    print('\n--- Nested & string recursion ---')
    nested = [[1, [2]], 3, [4, [5, [6]]]]
    print('flatten (using permutations/combinators is not needed here) - show recursion helper: permutations of [1,2,3] ->', recursion.permutations([1,2,3]))

    s = 'level'
    print('reverse_string("level") ->', recursion.reverse_string(s))
    print('is_palindrome("level") ->', recursion.is_palindrome(s))
    print('all_substrings("abc") ->', recursion.all_substrings('abc'))


def tower_and_subset_examples():
    print('\n--- Tower of Hanoi & subset sum ---')
    moves = recursion.tower_of_hanoi(3, 'A', 'C', 'B')
    print('Tower of Hanoi moves for 3 disks:')
    for i, m in enumerate(moves, 1):
        print(f" {i}: {m[0]} -> {m[1]}")

    print('subset_sum([3, 34, 4, 12, 5, 2], target=9) ->', recursion.subset_sum([3, 34, 4, 12, 5, 2], 9))


def tree_recursion_examples():
    print('\n--- Tree recursion (BinaryTree) ---')
    # level-order list (None means empty spot)
    vals = [1, 2, 3, 4, 5, None, 7]
    bt = trees.BinaryTree(vals)
    print('level-order input:', vals)
    print('level_order() ->', bt.level_order())
    print('preorder (recursive) ->', bt.preorder())
    print('inorder (recursive) ->', bt.inorder())
    print('postorder (recursive) ->', bt.postorder())
    print('size ->', bt.size())
    print('height ->', bt.height())
    print('find 7? ->', bt.find(7))
    print('paths ->', bt.print_paths())
    print('is_balanced? ->', bt.is_balanced())


if __name__ == '__main__':
    simple_recursion_examples()
    nested_and_string_recursion()
    tower_and_subset_examples()
    tree_recursion_examples()
