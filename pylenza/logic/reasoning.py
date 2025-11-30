"""Helpers and small exercises to build algorithmic reasoning.

This module contains reusable logical helpers, combinatorics utilities,
and small checks that improve problem solving skills.
"""
from __future__ import annotations

from typing import Any, Callable, Generator, Iterable, List, Tuple
import itertools


def all_true(seq: Iterable[Any], func: Callable[[Any], bool]) -> bool:
	"""Return True if func(x) is True for all elements in seq."""
	return all(func(x) for x in seq)


def any_true(seq: Iterable[Any], func: Callable[[Any], bool]) -> bool:
	"""Return True if func(x) is True for any element in seq."""
	return any(func(x) for x in seq)


def permutations_generator(seq: Iterable[Any]) -> Generator[Tuple[Any, ...], None, None]:
	"""Yield permutations lazily using itertools."""
	for p in itertools.permutations(seq):
		yield p


def combinations_generator(seq: Iterable[Any], k: int) -> Generator[Tuple[Any, ...], None, None]:
	for c in itertools.combinations(seq, k):
		yield c


def factorial(n: int) -> int:
	if n < 0:
		raise ValueError("n must be non-negative")
	res = 1
	for i in range(2, n + 1):
		res *= i
	return res


def nCr(n: int, r: int) -> int:
	if r < 0 or r > n:
		return 0
	# symmetry
	r = min(r, n - r)
	num = 1
	den = 1
	for i in range(1, r + 1):
		num *= n - (r - i)
		den *= i
	return num // den


def is_arithmetic_seq(seq: Iterable[float]) -> bool:
	s = list(seq)
	if len(s) < 2:
		return True
	diff = s[1] - s[0]
	return all((s[i] - s[i - 1]) == diff for i in range(1, len(s)))


def is_geometric_seq(seq: Iterable[float]) -> bool:
	s = list(seq)
	if len(s) < 2:
		return True
	if s[0] == 0:
		return all(x == 0 for x in s)
	ratio = s[1] / s[0]
	return all((s[i] / s[i - 1]) == ratio for i in range(1, len(s)))


def is_palindrome_recursive(seq: Iterable[Any]) -> bool:
	s = list(seq)
	if len(s) <= 1:
		return True
	if s[0] != s[-1]:
		return False
	return is_palindrome_recursive(s[1:-1])


def recursive_template_array():
	"""Demonstration template for recursive array functions.

	Shows the structure: base case, reduce problem, combine results.
	"""
	def helper(arr):
		if not arr:
			return None
		# base case
		# recuse on arr[1:]
		return helper(arr[1:])

	return helper


def probability_nCr_success(n: int, r: int, favorable: int, total: int) -> float:
	"""Return simple hypergeometric-style probability estimate (combinatorial).

	This is P(choose r elements containing exactly 'favorable' successes)
	as a ratio using combinations.
	"""
	if r > n or favorable > total:
		return 0.0
	# probability to choose r elements containing k successes given counts
	numer = nCr(favorable, r)
	denom = nCr(total, r)
	if denom == 0:
		return 0.0
	return numer / denom


__all__ = [
	'all_true', 'any_true', 'permutations_generator', 'combinations_generator', 'factorial', 'nCr',
	'is_arithmetic_seq', 'is_geometric_seq', 'is_palindrome_recursive', 'recursive_template_array', 'probability_nCr_success'
]

