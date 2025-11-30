"""Examples for pylenza.logic.* showing puzzles, patterns and reasoning utilities.

Run with:

    python examples/logic_examples.py

These examples print short, self-contained outputs suitable for learners.
"""

import os
import sys

# ensure repository root is on sys.path when running examples directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pylenza.logic import puzzles, patterns, reasoning


def puzzles_examples():
    print('\n--- Puzzles examples ---')

    print('\nN-Queens (n=4) solutions:')
    sols = puzzles.n_queens(4)
    for s in sols:
        print('\n'.join(s))
        print('-' * 12)

    print('\nA simple Sudoku checker (valid) ->', puzzles.sudoku_checker([
        [5,3,4,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,9],
    ]))

    print('Is this 3x3 magic square? ->', puzzles.is_magic_square([[8,1,6],[3,5,7],[4,9,2]]))

    print('coin_change_min_coins coins=[1,3,4] amount=6 ->', puzzles.coin_change_min_coins([1,3,4], 6))
    print('coin_change_count_ways coins=[1,2,5] amount=5 ->', puzzles.coin_change_count_ways([1,2,5], 5))


def patterns_examples():
    print('\n--- Patterns examples ---')

    arr = [1, 2, 3, 4, 5]
    print('prefix_sums of', arr, '->', patterns.prefix_sums(arr))
    print('apply_sliding_window sum k=3 ->', patterns.apply_sliding_window(arr, 3, sum))

    ar2 = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print('max_subarray_kadane on', ar2, '->', patterns.max_subarray_kadane(ar2))

    sorted_arr = [1,2,3,4,5,6]
    print('two_pointer_sum_sorted target 7 ->', patterns.two_pointer_sum_sorted(sorted_arr, 7))

    print('merge_intervals ->', patterns.merge_intervals([(1,3),(2,6),(8,10),(15,18)]))


def reasoning_examples():
    print('\n--- Reasoning examples ---')

    print('factorial(6) ->', reasoning.factorial(6))
    print('nCr(6, 2) ->', reasoning.nCr(6, 2))

    seq = [2,4,6,8]
    print('is_arithmetic_seq', seq, '->', reasoning.is_arithmetic_seq(seq))
    print('is_geometric_seq [2,4,8,16] ->', reasoning.is_geometric_seq([2,4,8,16]))

    s = 'radar'
    print('is_palindrome_recursive("radar") ->', reasoning.is_palindrome_recursive(s))

    # permutations_generator yields tuples lazily; show first 3 permutations for brevity
    gen = reasoning.permutations_generator([1,2,3])
    print('first three permutations of [1,2,3]:')
    for i, p in enumerate(gen):
        if i>=3:
            break
        print(' ', p)


if __name__ == '__main__':
    puzzles_examples()
    patterns_examples()
    reasoning_examples()
