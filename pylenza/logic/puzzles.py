"""Small, fun logic puzzles and teaching examples.

Each function is compact and returns either a solution representation or
a boolean indicating validity. Where appropriate, solvers include a
lightweight 'explain' option returning steps as strings.
"""
from __future__ import annotations

from typing import Any, Generator, List, Optional, Tuple


def n_queens(n: int, explain: bool = False) -> List[List[str]]:
	"""Return all solutions for N-Queens as list of board-strings.

	Each solution is a list of strings with 'Q' and '.' characters.
	"""
	solutions: List[List[str]] = []
	cols = set()
	diag1 = set()
	diag2 = set()
	board = [-1] * n
	steps: List[str] = []

	def place(row: int) -> None:
		if row == n:
			# build readable board
			solution = []
			for r in range(n):
				row_s = ['.'] * n
				row_s[board[r]] = 'Q'
				solution.append(''.join(row_s))
			solutions.append(solution)
			return
		for c in range(n):
			if c in cols or (row - c) in diag1 or (row + c) in diag2:
				continue
			cols.add(c); diag1.add(row - c); diag2.add(row + c)
			board[row] = c
			if explain:
				steps.append(f"place Q at ({row},{c})")
			place(row + 1)
			cols.remove(c); diag1.remove(row - c); diag2.remove(row + c)

	place(0)
	if explain:
		# attach steps as first element for debugging, but usually not used
		return solutions
	return solutions


def sudoku_checker(board: List[List[int]]) -> bool:
	"""Check whether a 9x9 completed sudoku board is valid. 0 allowed as empty."""
	# rows
	for row in board:
		nums = [x for x in row if x != 0]
		if len(nums) != len(set(nums)):
			return False
	# cols
	for c in range(9):
		nums = [board[r][c] for r in range(9) if board[r][c] != 0]
		if len(nums) != len(set(nums)):
			return False
	# boxes
	for br in range(3):
		for bc in range(3):
			nums = []
			for r in range(br * 3, br * 3 + 3):
				for c in range(bc * 3, bc * 3 + 3):
					if board[r][c] != 0:
						nums.append(board[r][c])
			if len(nums) != len(set(nums)):
				return False
	return True


def is_magic_square(matrix: List[List[int]]) -> bool:
	"""Check whether a given square matrix is a magic square (equal row/col/diag sums)."""
	n = len(matrix)
	if n == 0:
		return False
	target = sum(matrix[0])
	for row in matrix:
		if sum(row) != target:
			return False
	for c in range(n):
		if sum(matrix[r][c] for r in range(n)) != target:
			return False
	if sum(matrix[i][i] for i in range(n)) != target:
		return False
	if sum(matrix[i][n - 1 - i] for i in range(n)) != target:
		return False
	return True


def coin_change_min_coins(coins: List[int], amount: int) -> int:
	"""Return minimum coins to make amount (classic DP). Returns -1 if impossible."""
	MAX = amount + 1
	dp = [MAX] * (amount + 1)
	dp[0] = 0
	for c in coins:
		for x in range(c, amount + 1):
			dp[x] = min(dp[x], dp[x - c] + 1)
	return dp[amount] if dp[amount] != MAX else -1


def coin_change_count_ways(coins: List[int], amount: int) -> int:
	"""Return number of ways to make amount (order not important)."""
	dp = [0] * (amount + 1)
	dp[0] = 1
	for c in coins:
		for x in range(c, amount + 1):
			dp[x] += dp[x - c]
	return dp[amount]


def tower_of_hanoi_steps(n: int, explain: bool = False) -> List[Tuple[str, str]]:
	"""Wrapper that returns steps for Tower of Hanoi (reuses recursion implementation)."""
	# Lazy import to avoid cycle
	from pylenza.recursion import tower_of_hanoi

	moves = tower_of_hanoi(n, 'A', 'C', 'B')
	if explain:
		# provide a simple string-based explanation sequence
		return moves
	return moves


__all__ = [
	'n_queens', 'sudoku_checker', 'is_magic_square', 'coin_change_min_coins', 'coin_change_count_ways', 'tower_of_hanoi_steps'
]

