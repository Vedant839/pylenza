"""Sorting algorithms for teaching and small tasks.

Each function returns a new list and accepts an optional key function and
reverse flag to behave similarly to Python's builtin sorting.
"""
from __future__ import annotations

from typing import Any, Callable, Iterable, List, Optional
import heapq
import math
import random


def _keyed(x: Any, key: Optional[Callable[[Any], Any]]):
	return key(x) if key is not None else x


def bubble_sort(arr: Iterable[Any], key: Optional[Callable[[Any], Any]] = None, reverse: bool = False, verbose: bool = False) -> List[Any]:
	"""Simple bubble sort — O(n^2). Good for teaching, not for production.

	Returns a new sorted list.
	"""
	a = list(arr)
	n = len(a)
	for i in range(n):
		swapped = False
		for j in range(0, n - i - 1):
			if verbose:
				print(f"bubble: comparing {a[j]} and {a[j+1]}")
			if (not reverse and _keyed(a[j], key) > _keyed(a[j + 1], key)) or (reverse and _keyed(a[j], key) < _keyed(a[j + 1], key)):
				a[j], a[j + 1] = a[j + 1], a[j]
				swapped = True
		if not swapped:
			break
	return a


def selection_sort(arr: Iterable[Any], key: Optional[Callable[[Any], Any]] = None, reverse: bool = False) -> List[Any]:
	"""Selection sort — O(n^2). Finds min (or max) each pass.

	Returns a new list.
	"""
	a = list(arr)
	n = len(a)
	for i in range(n):
		idx = i
		for j in range(i + 1, n):
			if (not reverse and _keyed(a[j], key) < _keyed(a[idx], key)) or (reverse and _keyed(a[j], key) > _keyed(a[idx], key)):
				idx = j
		a[i], a[idx] = a[idx], a[i]
	return a


def insertion_sort(arr: Iterable[Any], key: Optional[Callable[[Any], Any]] = None, reverse: bool = False) -> List[Any]:
	"""Insertion sort — good for small or nearly-sorted arrays (O(n^2) worst-case, O(n) best-case)."""
	a = list(arr)
	for i in range(1, len(a)):
		cur = a[i]
		j = i - 1
		while j >= 0 and ((not reverse and _keyed(a[j], key) > _keyed(cur, key)) or (reverse and _keyed(a[j], key) < _keyed(cur, key))):
			a[j + 1] = a[j]
			j -= 1
		a[j + 1] = cur
	return a


def merge_sort(arr: Iterable[Any], key: Optional[Callable[[Any], Any]] = None, reverse: bool = False) -> List[Any]:
	"""Merge sort (O(n log n)) — stable divide-and-conquer algorithm."""
	a = list(arr)

	def _merge(left: List[Any], right: List[Any]) -> List[Any]:
		out: List[Any] = []
		i = j = 0
		while i < len(left) and j < len(right):
			if (not reverse and _keyed(left[i], key) <= _keyed(right[j], key)) or (reverse and _keyed(left[i], key) >= _keyed(right[j], key)):
				out.append(left[i]); i += 1
			else:
				out.append(right[j]); j += 1
		out.extend(left[i:]); out.extend(right[j:])
		return out

	if len(a) <= 1:
		return a
	mid = len(a) // 2
	left = merge_sort(a[:mid], key=key, reverse=reverse)
	right = merge_sort(a[mid:], key=key, reverse=reverse)
	return _merge(left, right)


def quick_sort(arr: Iterable[Any], key: Optional[Callable[[Any], Any]] = None, reverse: bool = False, pivot_strategy: str = "middle") -> List[Any]:
	"""Quick sort (average O(n log n), worst O(n^2)) — recursive teaching version.

	pivot_strategy: 'first', 'middle', 'random', or 'median' (median of three)
	"""
	a = list(arr)
	if len(a) <= 1:
		return a

	def _choose_pivot(lst: List[Any]) -> Any:
		if pivot_strategy == 'first':
			return lst[0]
		if pivot_strategy == 'middle':
			return lst[len(lst) // 2]
		if pivot_strategy == 'random':
			return random.choice(lst)
		if pivot_strategy == 'median':
			candidates = [lst[0], lst[len(lst) // 2], lst[-1]]
			candidates.sort(key=lambda x: _keyed(x, key))
			return candidates[1]
		raise ValueError("Unknown pivot_strategy")

	pivot = _choose_pivot(a)
	left = [x for x in a if (not reverse and _keyed(x, key) < _keyed(pivot, key)) or (reverse and _keyed(x, key) > _keyed(pivot, key))]
	middle = [x for x in a if _keyed(x, key) == _keyed(pivot, key)]
	right = [x for x in a if (not reverse and _keyed(x, key) > _keyed(pivot, key)) or (reverse and _keyed(x, key) < _keyed(pivot, key))]
	return quick_sort(left, key=key, reverse=reverse, pivot_strategy=pivot_strategy) + middle + quick_sort(right, key=key, reverse=reverse, pivot_strategy=pivot_strategy)


def heap_sort(arr: Iterable[int], reverse: bool = False) -> List[int]:
	"""Heap sort using heapq — O(n log n). Returns new list."""
	a = list(arr)
	if reverse:
		a = [-x for x in a]
		heapq.heapify(a)
		out = [-(heapq.heappop(a)) for _ in range(len(a))]
	else:
		heapq.heapify(a)
		out = [heapq.heappop(a) for _ in range(len(a))]
	return out


def counting_sort(arr: Iterable[int], reverse: bool = False) -> List[int]:
	"""Counting sort for integers (works with negatives) — linear time with range O(k).

	Returns a new sorted list.
	"""
	a = list(arr)
	if not a:
		return []
	# support negatives: shift
	mn = min(a)
	mx = max(a)
	shift = -mn if mn < 0 else 0
	size = mx + shift + 1
	counts = [0] * size
	for v in a:
		counts[v + shift] += 1
	out: List[int] = []
	if not reverse:
		for i, c in enumerate(counts):
			out.extend([i - shift] * c)
	else:
		for i in range(len(counts) - 1, -1, -1):
			out.extend([i - shift] * counts[i])
	return out


def radix_sort(arr: Iterable[int], reverse: bool = False) -> List[int]:
	"""LSD radix sort for non-negative integers. If negatives present, we separate and reassemble.

	Returns a new sorted list. Works best for integers.
	"""
	a = list(arr)
	if not a:
		return []
	# separate negatives
	negatives = [x for x in a if x < 0]
	nonneg = [x for x in a if x >= 0]

	def _radix_positive(lst: List[int]) -> List[int]:
		if not lst:
			return []
		max_val = max(lst)
		exp = 1
		out = list(lst)
		while max_val // exp > 0:
			buckets = [[] for _ in range(10)]
			for num in out:
				buckets[(num // exp) % 10].append(num)
			out = [num for bucket in buckets for num in bucket]
			exp *= 10
		return out

	sorted_nonneg = _radix_positive(nonneg)
	# negatives: sort absolute values and reverse
	neg_abs_sorted = _radix_positive([abs(x) for x in negatives])
	sorted_negatives = [-x for x in reversed(neg_abs_sorted)]

	combined = sorted_negatives + sorted_nonneg
	if reverse:
		combined.reverse()
	return combined


def tim_sort(arr: Iterable[Any], key: Optional[Callable[[Any], Any]] = None, reverse: bool = False) -> List[Any]:
	"""Wrapper for Python's highly-optimized timsort (stable)."""
	return sorted(list(arr), key=key, reverse=reverse)


def is_sorted(arr: Iterable[Any], key: Optional[Callable[[Any], Any]] = None, reverse: bool = False) -> bool:
	a = list(arr)
	for i in range(len(a) - 1):
		if (not reverse and _keyed(a[i], key) > _keyed(a[i + 1], key)) or (reverse and _keyed(a[i], key) < _keyed(a[i + 1], key)):
			return False
	return True


def almost_sorted(arr: Iterable[Any], max_swaps: int = 1) -> bool:
	"""Check whether an array can be made sorted by at most `max_swaps` swaps.

	Useful as a teaching helper for adaptive algorithms.
	"""
	a = list(arr)
	target = sorted(a)
	mismatches = 0
	for x, y in zip(a, target):
		if x != y:
			mismatches += 1
	# each swap can fix up to two misplaced elements
	return mismatches <= 2 * max_swaps


__all__ = [
	'bubble_sort', 'selection_sort', 'insertion_sort', 'merge_sort', 'quick_sort', 'heap_sort', 'counting_sort', 'radix_sort', 'tim_sort', 'is_sorted', 'almost_sorted'
]

