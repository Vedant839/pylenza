"""Examples showing how to use PyArray from the pylenza package.

Run this file stand-alone with:

	python examples/array_examples.py

The examples intentionally print short explanatory lines so learners
can read inputs and outputs in sequence.
"""

from __future__ import annotations

import os
import sys

# When running this file directly the interpreter's import path will
# have the script directory at position 0. Ensure the project root is on
# sys.path so 'pylenza' (a sibling package) can be imported.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pylenza import PyArray


def show_basic_creation_and_mutation():
	print('\n--- Basic creation and mutation ---')
	arr = PyArray([1, 2, 3, 4])
	print('initial:', arr)

	arr.append(5)
	print('append(5):', arr)

	arr.insert(2, 99)
	print('insert(2, 99):', arr)

	popped = arr.pop()
	print('pop() ->', popped, 'result:', arr)

	arr.delete(99)
	print('delete(99) ->', arr)

	print('index of 3:', arr.index(3))
	print('count of 2:', arr.count(2))
	print('contains 42?:', arr.contains(42))


def show_transforms_and_nesting():
	print('\n--- Transformations & nested handling ---')
	nested = PyArray([1, [2, 3], PyArray([4, [5, 6]]), 'a'])
	print('nested:', nested)
	print('flatten() ->', nested.flatten())
	print('flatten_copy() ->', nested.flatten_copy())
	print('chunk(2) ->', [c.to_list() for c in nested.chunk(2)])

	sample = PyArray([1, 2, 3, 4])
	print('rotate(1):', sample.rotate(1, in_place=False))
	print('reverse (non-destructive):', sample.reverse(in_place=False))
	print('merge with [9,9]:', sample.merge([9, 9]))


def show_numeric_helpers():
	print('\n--- Numeric helpers ---')
	nums = PyArray([10, 0, 5, 5, 20])
	print('nums:', nums)
	print('sum:', nums.sum())
	print('product:', nums.product())
	print('mean:', nums.mean())
	print('median:', nums.median())
	print('mode:', nums.mode())
	print('normalize:', nums.normalize())
	std_arr, params = nums.standardize()
	print('standardize ->', std_arr, 'params:', params)


def show_search_and_sort():
	print('\n--- Searching & sorting ---')
	arr = PyArray([7, 1, 5, 3, 9])
	print('array:', arr)
	print('linear search for 3 -> index:', arr.search(3, algorithm='linear'))

	sorted_arr = arr.sort(algorithm='tim')
	print('timsort ->', sorted_arr)
	print('binary search (3) -> index:', sorted_arr.search(3, algorithm='binary'))

	print('quicksort ->', arr.sort(algorithm='quicksort'))
	print('mergesort ->', arr.sort(algorithm='mergesort'))


def show_functional_style_and_advanced():
	print('\n--- Functional and advanced helpers ---')
	arr = PyArray([1, 2, 3, 4, 5, 6])
	print('map *2 ->', arr.map(lambda x: x * 2))
	print('filter odd ->', arr.filter(lambda x: x % 2 == 1))
	print('reduce (sum) ->', arr.reduce(lambda a, b: a + b))

	missing = PyArray([1, 2, 4, 6]).find_missing()
	print('find_missing in [1,2,4,6] ->', missing)

	print('common_elements with [2,6,99] ->', arr.common_elements([2, 6, 99]))
	print('all_satisfy >0 ->', arr.all_satisfy(lambda x: x > 0))
	print('any_satisfy >4 ->', arr.any_satisfy(lambda x: x > 4))


if __name__ == '__main__':
	show_basic_creation_and_mutation()
	show_transforms_and_nesting()
	show_numeric_helpers()
	show_search_and_sort()
	show_functional_style_and_advanced()

