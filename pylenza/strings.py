"""Small string utilities focused on readability and teaching.

All functions return new strings (strings are immutable) and avoid
dependencies beyond Python's standard library.
"""
from __future__ import annotations

from collections import Counter
from functools import reduce as _reduce
from typing import Any, Callable, Dict, Generator, List, Optional, Sequence
import itertools


def to_list(s: str) -> List[str]:
	"""Convert string to list of characters.

	Time: O(n)
	"""
	return list(s)


def from_list(lst: Sequence[str]) -> str:
	"""Convert a list of characters back to a string.

	Time: O(n)
	"""
	return ''.join(lst)


def reverse(s: str) -> str:
	"""Return the reversed string."""
	return s[::-1]


def is_palindrome(s: str, ignore_case: bool = True) -> bool:
	"""Check if string is palindrome. Defaults to ignore case."""
	if ignore_case:
		s = s.lower()
	return s == s[::-1]


def count_chars(s: str) -> Dict[str, int]:
	"""Return a mapping from character to frequency."""
	return dict(Counter(s))


def unique_chars(s: str) -> str:
	"""Return string of unique characters preserving first-occurrence order."""
	seen = set()
	out: List[str] = []
	for ch in s:
		if ch not in seen:
			seen.add(ch)
			out.append(ch)
	return ''.join(out)


# --- Transformations -------------------------------------------------


def capitalize_words(s: str) -> str:
	"""Capitalize the first character of each word (space-separated)."""
	return ' '.join(w.capitalize() for w in s.split(' '))


def to_lower(s: str) -> str:
	return s.lower()


def to_upper(s: str) -> str:
	return s.upper()


def swap_case(s: str) -> str:
	return s.swapcase()


def remove_whitespace(s: str) -> str:
	"""Remove spaces, tabs and newlines from the string."""
	return ''.join(ch for ch in s if not ch.isspace())


def normalize_spaces(s: str) -> str:
	"""Collapse consecutive whitespace characters into a single space and strip ends."""
	return ' '.join(s.split())


# -- Substrings & Patterns -------------------------------------------


def substring(s: str, start: int, end: Optional[int] = None) -> str:
	return s[start:end]


def count_substring(s: str, sub: str) -> int:
	"""Return the number of (possibly overlapping) occurrences of sub in s."""
	if not sub:
		return 0
	count = start = 0
	while True:
		idx = s.find(sub, start)
		if idx == -1:
			break
		count += 1
		start = idx + 1  # allow overlapping
	return count


def find_all(s: str, sub: str, verbose: bool = False) -> List[int]:
	"""Return list of start indices where sub occurs (allows overlaps)."""
	out: List[int] = []
	if not sub:
		return out
	start = 0
	while True:
		idx = s.find(sub, start)
		if idx == -1:
			break
		if verbose:
			print(f"found {sub!r} at {idx}")
		out.append(idx)
		start = idx + 1
	return out


def starts_with(s: str, prefix: str) -> bool:
	return s.startswith(prefix)


def ends_with(s: str, suffix: str) -> bool:
	return s.endswith(suffix)


# --- Functional & mapping helpers -----------------------------------


def map_chars(s: str, func: Callable[[str], str]) -> str:
	return ''.join(func(ch) for ch in s)


def filter_chars(s: str, func: Callable[[str], bool]) -> str:
	return ''.join(ch for ch in s if func(ch))


def reduce_chars(s: str, func: Callable[[Any, str], Any], initial: Optional[Any] = None) -> Any:
	it = iter(s)
	if initial is None:
		try:
			acc = next(it)
		except StopIteration:
			raise TypeError("reduce() of empty string with no initial value")
	else:
		acc = initial
	for ch in it:
		acc = func(acc, ch)
	return acc


# --- Numeric & string utilities -------------------------------------


def to_int_list(s: str, sep: str = ',') -> List[int]:
	if not s:
		return []
	parts = [p.strip() for p in s.split(sep) if p.strip()]
	return [int(p) for p in parts]


def to_float_list(s: str, sep: str = ',') -> List[float]:
	if not s:
		return []
	parts = [p.strip() for p in s.split(sep) if p.strip()]
	return [float(p) for p in parts]


def sum_digits(s: str) -> int:
	return sum(int(ch) for ch in s if ch.isdigit())


def numeric_only(s: str) -> str:
	return ''.join(ch for ch in s if ch.isdigit())


def alpha_only(s: str) -> str:
	return ''.join(ch for ch in s if ch.isalpha())


# --- Advanced / Learning-Friendly helpers ----------------------------


def anagrams(s1: str, s2: str, ignore_case: bool = True, ignore_whitespace: bool = True) -> bool:
	"""Return True if s1 and s2 are anagrams (same letters in different order)."""
	def _prep(s: str) -> str:
		if ignore_whitespace:
			s = ''.join(s.split())
		return s.lower() if ignore_case else s

	return Counter(_prep(s1)) == Counter(_prep(s2))


def longest_common_prefix(strings: Sequence[str]) -> str:
	if not strings:
		return ''
	shortest = min(strings, key=len)
	for i, ch in enumerate(shortest):
		for other in strings:
			if other[i] != ch:
				return shortest[:i]
	return shortest


def palindromic_substrings(s: str, verbose: bool = False) -> List[str]:
	"""Return all palindromic substrings (naive O(n^2) approach).

	For teaching purposes this enumerates centers and expands.
	"""
	out: List[str] = []
	n = len(s)
	for center in range(n):
		# odd length
		l = r = center
		while l >= 0 and r < n and s[l] == s[r]:
			substr = s[l:r+1]
			if len(substr) > 1:
				out.append(substr)
				if verbose:
					print('odd center', center, '=>', substr)
			l -= 1; r += 1

		# even length
		l = center; r = center + 1
		while l >= 0 and r < n and s[l] == s[r]:
			substr = s[l:r+1]
			out.append(substr)
			if verbose:
				print('even center', center, '=>', substr)
			l -= 1; r += 1

	# returning unique palindromes preserving first-seen order
	seen = set()
	uniq: List[str] = []
	for p in out:
		if p not in seen:
			seen.add(p)
			uniq.append(p)
	return uniq


def all_permutations(s: str) -> List[str]:
	"""Return all permutations of characters in s (warning: factorial size)."""
	return [''.join(p) for p in itertools.permutations(s)]


__all__ = [
	'to_list', 'from_list', 'reverse', 'is_palindrome', 'count_chars', 'unique_chars',
	'capitalize_words', 'to_lower', 'to_upper', 'swap_case', 'remove_whitespace', 'normalize_spaces',
	'substring', 'count_substring', 'find_all', 'starts_with', 'ends_with',
	'map_chars', 'filter_chars', 'reduce_chars',
	'to_int_list', 'to_float_list', 'sum_digits', 'numeric_only', 'alpha_only',
	'anagrams', 'longest_common_prefix', 'palindromic_substrings', 'all_permutations'
]

