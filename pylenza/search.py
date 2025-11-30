"""Search algorithms and helpers — clear, small implementations for teaching.

Each algorithm is implemented to be readable and include a short
docstring describing complexities and behavior. The functions favor
predictable return types: integer index (or -1) for single-index searches
and lists of indices when returning multiple occurrences.

No external dependencies are required — just Python standard library.
"""
from __future__ import annotations

from math import sqrt
from typing import Any, Callable, Iterable, List, Optional, Sequence, Tuple


def _get_key(x: Any, key: Optional[Callable[[Any], Any]]) -> Any:
    return key(x) if key is not None else x


def linear_search(arr: Iterable[Any], target: Any, key: Optional[Callable[[Any], Any]] = None, verbose: bool = False) -> int:
    """Linear search (O(n)).

    Returns index of the first matching element or -1 if not found.
    Accepts an optional key function similar to sorting.
    """
    for i, item in enumerate(arr):
        if verbose:
            print(f"linear: checking index={i}, value={item}")
        if _get_key(item, key) == target:
            return i
    return -1


def linear_search_all(arr: Iterable[Any], target: Any, key: Optional[Callable[[Any], Any]] = None, verbose: bool = False) -> List[int]:
    """Return list of all indices where items match target (O(n))."""
    hits: List[int] = []
    for i, item in enumerate(arr):
        if verbose:
            print(f"linear_all: checking index={i}, value={item}")
        if _get_key(item, key) == target:
            hits.append(i)
    return hits


def binary_search(arr: Sequence[Any], target: Any, low: int = 0, high: Optional[int] = None, key: Optional[Callable[[Any], Any]] = None, verbose: bool = False) -> int:
    """Iterative binary search (O(log n)).

    Works on sorted sequences. Returns index or -1 if not found.
    If high is None it defaults to len(arr)-1.
    """
    if high is None:
        high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        midval = _get_key(arr[mid], key)
        if verbose:
            print(f"binary: low={low}, mid={mid}, high={high}, midval={midval}")
        if midval == target:
            return mid
        elif midval < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def binary_search_recursive(arr: Sequence[Any], target: Any, low: int = 0, high: Optional[int] = None, key: Optional[Callable[[Any], Any]] = None, verbose: bool = False) -> int:
    """Recursive binary search wrapper — teaching-focused (O(log n))."""
    if high is None:
        high = len(arr) - 1
    if low > high:
        return -1
    mid = (low + high) // 2
    midval = _get_key(arr[mid], key)
    if verbose:
        print(f"binary_rec: low={low}, mid={mid}, high={high}, midval={midval}")
    if midval == target:
        return mid
    if midval < target:
        return binary_search_recursive(arr, target, mid + 1, high, key, verbose)
    return binary_search_recursive(arr, target, low, mid - 1, key, verbose)


def jump_search(arr: Sequence[Any], target: Any, key: Optional[Callable[[Any], Any]] = None, verbose: bool = False) -> int:
    """Jump search (O(√n)) — good for sorted arrays stored in arrays.

    The algorithm jumps ahead by block size =~ sqrt(n) and then performs
    a linear scan in the found block.
    """
    n = len(arr)
    if n == 0:
        return -1
    step = int(sqrt(n))
    prev = 0
    while prev < n and _get_key(arr[min(prev + step, n) - 1], key) < target:
        if verbose:
            print(f"jump: jump to index {prev+step-1}")
        prev += step
        if prev >= n:
            return -1

    # linear scan within block
    i = prev
    while i < min(prev + step, n):
        if verbose:
            print(f"jump linear: checking {i}")
        if _get_key(arr[i], key) == target:
            return i
        i += 1
    return -1


def interpolation_search(arr: Sequence[float], target: float, verbose: bool = False) -> int:
    """Interpolation search for uniformly distributed sorted numeric arrays.

    Average O(log log n) on good data, worst-case O(n). Only for numeric types.
    """
    lo = 0
    hi = len(arr) - 1
    while lo <= hi and arr[lo] <= target <= arr[hi]:
        if lo == hi:
            return lo if arr[lo] == target else -1
        # probe position
        # handle division by zero when arr[hi] == arr[lo]
        if arr[hi] == arr[lo]:
            pos = lo
        else:
            pos = lo + int((target - arr[lo]) * (hi - lo) / (arr[hi] - arr[lo]))
        if pos < lo or pos > hi:
            return -1
        if verbose:
            print(f"interpolation: lo={lo}, pos={pos}, hi={hi}, arr[pos]={arr[pos]}")
        if arr[pos] == target:
            return pos
        if arr[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1


def exponential_search(arr: Sequence[Any], target: Any, key: Optional[Callable[[Any], Any]] = None, verbose: bool = False) -> int:
    """Exponential search — finds range then uses binary search (O(log n)).

    Useful when searching in an unbounded or very large array where the
    target is likely near the beginning.
    """
    n = len(arr)
    if n == 0:
        return -1
    if _get_key(arr[0], key) == target:
        return 0
    # find range by repeated doubling
    i = 1
    while i < n and _get_key(arr[i], key) <= target:
        if verbose:
            print(f"exponential: probing index {i}")
        i *= 2
    # binary search on found range
    low = i // 2
    high = min(i, n - 1)
    return binary_search(arr, target, low, high, key=key, verbose=verbose)


def find_min(arr: Sequence[Any], key: Optional[Callable[[Any], Any]] = None) -> int:
    """Return index of minimum element in arr; raises ValueError on empty."""
    if not arr:
        raise ValueError("find_min on empty sequence")
    min_i = 0
    min_val = _get_key(arr[0], key)
    for i in range(1, len(arr)):
        val = _get_key(arr[i], key)
        if val < min_val:
            min_val = val
            min_i = i
    return min_i


def find_max(arr: Sequence[Any], key: Optional[Callable[[Any], Any]] = None) -> int:
    """Return index of maximum element in arr; raises ValueError on empty."""
    if not arr:
        raise ValueError("find_max on empty sequence")
    max_i = 0
    max_val = _get_key(arr[0], key)
    for i in range(1, len(arr)):
        val = _get_key(arr[i], key)
        if val > max_val:
            max_val = val
            max_i = i
    return max_i


def find_duplicates(arr: Iterable[Any], key: Optional[Callable[[Any], Any]] = None) -> List[int]:
    """Return list of indices which are duplicate values (except first occurrence)."""
    seen = {}
    res: List[int] = []
    for i, item in enumerate(arr):
        k = _get_key(item, key)
        if k in seen:
            res.append(i)
        else:
            seen[k] = i
    return res


def count_occurrences(arr: Iterable[Any], value: Any, key: Optional[Callable[[Any], Any]] = None) -> int:
    """Count how many times value appears in arr (O(n))."""
    cnt = 0
    for item in arr:
        if _get_key(item, key) == value:
            cnt += 1
    return cnt


__all__ = [
    "linear_search",
    "linear_search_all",
    "binary_search",
    "binary_search_recursive",
    "jump_search",
    "interpolation_search",
    "exponential_search",
    "find_min",
    "find_max",
    "find_duplicates",
    "count_occurrences",
]
