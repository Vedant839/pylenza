"""Recursive algorithms and helpers for educational use.

Functions are intentionally simple and include docstrings explaining
base case and recursive step so students can follow the logic.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any, List, Optional, Tuple


def factorial(n: int) -> int:
	"""Return n! for n >= 0 using recursion. Raises ValueError for negative n.

	Complexity: O(n)
	"""
	if n < 0:
		raise ValueError("factorial not defined for negative values")
	if n == 0:
		return 1
	return n * factorial(n - 1)


@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
	"""Return the n-th Fibonacci number (0-indexed) using recursion with memoization.

	Complexity: O(n) with memoization
	"""
	if n < 0:
		raise ValueError("fibonacci not defined for negative values")
	if n in (0, 1):
		return n
	return fibonacci(n - 1) + fibonacci(n - 2)


def gcd(a: int, b: int) -> int:
	"""Compute greatest common divisor using Euclidean algorithm (recursive)."""
	a, b = abs(a), abs(b)
	if b == 0:
		return a
	return gcd(b, a % b)


def lcm(a: int, b: int) -> int:
	"""Compute least common multiple using gcd."""
	if a == 0 or b == 0:
		return 0
	return abs(a // gcd(a, b) * b)


def power(x: float, n: int) -> float:
	"""Compute x**n using recursion and exponentiation by squaring.

	Supports negative n.
	"""
	if n == 0:
		return 1.0
	if n < 0:
		return 1.0 / power(x, -n)
	if n % 2 == 0:
		half = power(x, n // 2)
		return half * half
	return x * power(x, n - 1)


def sum_list(lst: List[int]) -> int:
	"""Recursively compute the sum of a list of integers."""
	if not lst:
		return 0
	return lst[0] + sum_list(lst[1:])


def product_list(lst: List[int]) -> int:
	if not lst:
		return 1
	return lst[0] * product_list(lst[1:])


def max_list(lst: List[int]) -> int:
	if not lst:
		raise ValueError("max_list on empty list")
	if len(lst) == 1:
		return lst[0]
	rest_max = max_list(lst[1:])
	return lst[0] if lst[0] > rest_max else rest_max


def min_list(lst: List[int]) -> int:
	if not lst:
		raise ValueError("min_list on empty list")
	if len(lst) == 1:
		return lst[0]
	rest_min = min_list(lst[1:])
	return lst[0] if lst[0] < rest_min else rest_min


def find_index(lst: List[Any], value: Any, start: int = 0) -> int:
	"""Find first index of value starting at `start` or -1 if not found using recursion."""
	if start >= len(lst):
		return -1
	if lst[start] == value:
		return start
	return find_index(lst, value, start + 1)


def reverse_string(s: str) -> str:
	if s == '':
		return ''
	return s[-1] + reverse_string(s[:-1])


def is_palindrome(s: str) -> bool:
	s = ''.join(s.split())  # ignore whitespace for simplicity
	if len(s) <= 1:
		return True
	if s[0] != s[-1]:
		return False
	return is_palindrome(s[1:-1])


def count_char(s: str, char: str) -> int:
	if not s:
		return 0
	return (1 if s[0] == char else 0) + count_char(s[1:], char)


def all_substrings(s: str) -> List[str]:
	"""Return all substrings using recursion (teaching-friendly)."""
	out: List[str] = []

	def _recur(start: int, end: int) -> None:
		if start >= len(s):
			return
		if end > len(s):
			_recur(start + 1, start + 1)
			return
		out.append(s[start:end])
		_recur(start, end + 1)

	_recur(0, 1)
	return [x for x in out if x]


def permutations(lst: List[Any]) -> List[List[Any]]:
	"""Generate all permutations recursively."""
	if len(lst) <= 1:
		return [list(lst)]
	res: List[List[Any]] = []
	for i, item in enumerate(lst):
		rest = lst[:i] + lst[i + 1:]
		for p in permutations(rest):
			res.append([item] + p)
	return res


def combinations(lst: List[Any], k: int) -> List[List[Any]]:
	if k == 0:
		return [[]]
	if not lst:
		return []
	head, *tail = lst
	with_head = [[head] + c for c in combinations(tail, k - 1)]
	without_head = combinations(tail, k)
	return with_head + without_head


def tower_of_hanoi(n: int, source: str, target: str, auxiliary: str) -> List[Tuple[str, str]]:
	"""Return list of moves to solve Tower of Hanoi for n disks.

	Moves are represented as (from, to) tuples.
	"""
	if n <= 0:
		return []
	if n == 1:
		return [(source, target)]
	moves = []
	moves.extend(tower_of_hanoi(n - 1, source, auxiliary, target))
	moves.append((source, target))
	moves.extend(tower_of_hanoi(n - 1, auxiliary, target, source))
	return moves


def binary_search_recursive(lst: List[int], target: int, left: int = 0, right: Optional[int] = None) -> int:
	if right is None:
		right = len(lst) - 1
	if left > right:
		return -1
	mid = (left + right) // 2
	if lst[mid] == target:
		return mid
	if lst[mid] < target:
		return binary_search_recursive(lst, target, mid + 1, right)
	return binary_search_recursive(lst, target, left, mid - 1)


def subset_sum(lst: List[int], target: int) -> bool:
	"""Return True if some subset sums to target (classic recursive solution)."""
	if target == 0:
		return True
	if not lst:
		return False
	if lst[0] > target:
		return subset_sum(lst[1:], target)
	# choose or skip
	return subset_sum(lst[1:], target - lst[0]) or subset_sum(lst[1:], target)


__all__ = [
	'factorial', 'fibonacci', 'gcd', 'lcm', 'power',
	'sum_list', 'product_list', 'max_list', 'min_list', 'find_index',
	'reverse_string', 'is_palindrome', 'count_char', 'all_substrings',
	'permutations', 'combinations', 'tower_of_hanoi', 'binary_search_recursive', 'subset_sum'
]
