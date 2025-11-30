from pylenza.logic import patterns, puzzles, reasoning

def test_patterns_sliding_prefix_kadane():
	arr = [1, 2, -1, 4, -2, 3]
	assert patterns.prefix_sums(arr)[-1] == sum(arr)
	assert patterns.apply_sliding_window(arr, 3, sum) == [2, 5, 1, 5]
	assert patterns.max_subarray_kadane(arr) == 7

def test_two_pointer_and_merge_intervals():
	assert patterns.two_pointer_sum_sorted([1, 2, 3, 4, 6], 6) == (2, 4)
	assert patterns.two_pointer_two_sum([3, 2, 4], 6) == (1, 2)
	intervals = [(1, 3), (2, 6), (8, 10), (15, 18)]
	assert patterns.merge_intervals(intervals) == [(1, 6), (8, 10), (15, 18)]

def test_linkedlist_and_tree_patterns():
	# linked list: create a tiny Node-like object
	class N:
		def __init__(self, v, nxt=None):
			self.value = v
			self.next = nxt

	a = N(1, N(2, N(3)))
	rev = patterns.reverse_linked_list(a)
	vals = []
	cur = rev
	while cur:
		vals.append(cur.value)
		cur = cur.next
	assert vals == [3, 2, 1]

def test_puzzles_nqueens_and_sudoku_and_coins_and_magic():
	sols = puzzles.n_queens(4)
	assert len(sols) == 2

	# sudoku: valid solved 9x9 grid
	solved = [[5,3,4,6,7,8,9,1,2],[6,7,2,1,9,5,3,4,8],[1,9,8,3,4,2,5,6,7],[8,5,9,7,6,1,4,2,3],[4,2,6,8,5,3,7,9,1],[7,1,3,9,2,4,8,5,6],[9,6,1,5,3,7,2,8,4],[2,8,7,4,1,9,6,3,5],[3,4,5,2,8,6,1,7,9]]
	assert puzzles.sudoku_checker(solved) is True

	assert puzzles.is_magic_square([[2,7,6],[9,5,1],[4,3,8]]) is True
	assert puzzles.coin_change_min_coins([1,2,5], 11) == 3
	assert puzzles.coin_change_count_ways([1,2,5], 5) >= 4

def test_reasoning_helpers():
	assert reasoning.all_true([1,2,3], lambda x: x>0)
	assert reasoning.any_true([0,1,2], lambda x: x>0)
	perms = list(reasoning.permutations_generator([1,2]))
	assert (1,2) in perms and (2,1) in perms
	assert reasoning.factorial(5) == 120
	assert reasoning.nCr(5,2) == 10
	assert reasoning.is_arithmetic_seq([2,4,6])
	assert reasoning.is_geometric_seq([3,9,27])
	assert reasoning.is_palindrome_recursive([1,2,1])
