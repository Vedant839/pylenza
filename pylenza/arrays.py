"""A learning-friendly array wrapper with utility methods.

The PyArray class implements a variety of operations that mimic and
extend Python's list behavior in a small, well-documented package useful
for teaching algorithms and providing convenient helpers.

The implementation favors readability and correctness over micro-optimizations.
"""
from __future__ import annotations

from collections import Counter, deque
from functools import reduce as _reduce
from typing import Any, Callable, Generator, Iterable, List, Optional, Sequence, Tuple
import math

try:
    import numpy as _np  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    _np = None


def _is_iterable_but_not_str(obj: Any) -> bool:
    """Return True for iterable containers except str/bytes/bytearray."""
    if isinstance(obj, (str, bytes, bytearray)):
        return False
    try:
        iter(obj)
    except TypeError:
        return False
    return True


class PyArray:
    """A compact, learning-friendly array wrapper around a Python list.

    Methods intentionally return new PyArray objects (or values) except
    when an in-place behaviour is requested. The class keeps a plain
    Python list internally (self._data).
    """

    def __init__(self, data: Optional[Iterable[Any]] = None, validate: bool = True) -> None:
        """Create a PyArray.

        - data: optional iterable (list, tuple, PyArray) or None.
        - validate: if True, raise TypeError for non-iterable inputs.
        Tuples are converted to lists automatically.
        """
        if data is None:
            self._data: List[Any] = []
            return

        if isinstance(data, PyArray):
            self._data = list(data._data)
            return

        # Convert tuples to list and accept lists as-is
        if isinstance(data, tuple):
            self._data = list(data)
            return

        # Accept any sequence / iterable
        if isinstance(data, list):
            self._data = list(data)
            return

        if validate and not _is_iterable_but_not_str(data):
            raise TypeError("data must be an iterable (list/tuple/PyArray) or None")

        # Final fallback: try to build a list from the iterable
        self._data = list(data)

    def __repr__(self) -> str:  # pragma: no cover - representation only
        return f"PyArray({self._data!r})"

    # --- Conversions -------------------------------------------------
    def to_list(self) -> List[Any]:
        """Return a shallow Python list copy of the array."""
        return list(self._data)

    def to_numpy(self):
        """Return a NumPy array if NumPy is installed, otherwise raise ImportError."""
        if _np is None:
            raise ImportError("NumPy is not installed; cannot convert to numpy array")
        return _np.array(self._data)

    # --- Basic mutators ----------------------------------------------
    def append(self, value: Any) -> None:
        """Append `value` to the end of the array (in-place)."""
        self._data.append(value)

    def insert(self, index: int, value: Any) -> None:
        """Insert value at `index` (in-place). Works like list.insert."""
        self._data.insert(index, value)

    def pop(self, index: int = -1) -> Any:
        """Remove and return item at index (default last)."""
        return self._data.pop(index)

    def delete(self, value: Any) -> None:
        """Remove the first occurrence of `value`. Raises ValueError if not present."""
        self._data.remove(value)

    # --- Accessors & queries ----------------------------------------
    def index(self, value: Any, start: int = 0) -> int:
        """Return first index of value at or after start, or -1 if not found."""
        try:
            return self._data.index(value, start)
        except ValueError:
            return -1

    def count(self, value: Any) -> int:
        """Return number of occurrences of value."""
        return self._data.count(value)

    def slice(self, start: Optional[int] = None, end: Optional[int] = None, step: Optional[int] = None) -> "PyArray":
        """Return a PyArray slice (like list[start:end:step])."""
        return PyArray(self._data[start:end:step])

    def contains(self, value: Any) -> bool:
        """Return True if value is present in the array."""
        return value in self._data

    # --- Transformations & nested handling ---------------------------
    def reverse(self, in_place: bool = True) -> "PyArray":
        """Reverse the array; in-place when requested, otherwise return a new PyArray."""
        if in_place:
            self._data.reverse()
            return self
        return PyArray(list(reversed(self._data)))

    def rotate(self, k: int, in_place: bool = True) -> "PyArray":
        """Circular rotation by k positions to the right (positive k).

        Example: [1,2,3,4] rotate(1) -> [4,1,2,3]
        """
        n = len(self._data)
        if n == 0:
            return self if in_place else PyArray([])
        k = k % n
        if k == 0:
            return self if in_place else PyArray(list(self._data))
        rotated = self._data[-k:] + self._data[:-k]
        if in_place:
            self._data[:] = rotated
            return self
        return PyArray(rotated)

    def merge(self, other: Iterable[Any]) -> "PyArray":
        """Merge with another iterable and return a new PyArray (non-destructive)."""
        if isinstance(other, PyArray):
            other_seq = other._data
        else:
            other_seq = list(other)
        return PyArray(self._data + list(other_seq))

    def flatten(self, in_place: bool = False) -> "PyArray":
        """Flatten nested arrays and sequences iteratively.

        The method treats strings/bytes as scalars and does not expand them.
        """
        out: List[Any] = []
        stack = list(self._data)
        while stack:
            item = stack.pop(0)
            if isinstance(item, PyArray):
                stack[0:0] = list(item._data)
            elif _is_iterable_but_not_str(item):
                # expand iterable while preserving order
                stack[0:0] = list(item)
            else:
                out.append(item)

        if in_place:
            self._data = out
            return self
        return PyArray(out)

    def flatten_copy(self) -> List[Any]:
        """Return a flattened shallow copy as a list (non-destructive)."""
        return PyArray(self._data).flatten(in_place=False).to_list()

    def chunk(self, size: int) -> List["PyArray"]:
        """Split into chunks of given size and return a list of PyArray objects."""
        if size <= 0:
            raise ValueError("chunk size must be positive")
        return [PyArray(self._data[i : i + size]) for i in range(0, len(self._data), size)]

    def chunk_iter(self, size: int) -> Generator["PyArray", None, None]:
        """Generator yielding PyArray chunks of the provided size."""
        if size <= 0:
            raise ValueError("chunk size must be positive")
        for i in range(0, len(self._data), size):
            yield PyArray(self._data[i : i + size])

    # --- Utilities --------------------------------------------------
    def unique(self, stable: bool = True) -> "PyArray":
        """Return a new PyArray with duplicates removed.

        If stable=True the original order is preserved.
        """
        if stable:
            seen = set()
            out = []
            for x in self._data:
                if x not in seen:
                    seen.add(x)
                    out.append(x)
            return PyArray(out)

        # Unstable - use set to remove duplicates (order not guaranteed)
        return PyArray(list(set(self._data)))

    def map(self, func: Callable[[Any], Any], in_place: bool = False) -> "PyArray":
        """Apply func to every element and return a PyArray (or mutate in-place)."""
        mapped = [func(x) for x in self._data]
        if in_place:
            self._data[:] = mapped
            return self
        return PyArray(mapped)

    def filter(self, func: Callable[[Any], bool]) -> "PyArray":
        """Filter elements by predicate and return a new PyArray."""
        return PyArray([x for x in self._data if func(x)])

    def reduce(self, func: Callable[[Any, Any], Any], initial: Any = None) -> Any:
        """Aggregate elements using func. Works like functools.reduce but supports an initial value."""
        if initial is None:
            return _reduce(func, self._data)
        return _reduce(func, self._data, initial)

    # --- Numeric helpers (operating on flattened numeric arrays) -----
    def _numeric_list(self) -> List[float]:
        """Return a flattened numeric list (raises ValueError for non-numeric members)."""
        flat = self.flatten_copy()
        nums: List[float] = []
        for x in flat:
            if isinstance(x, (int, float)) and not isinstance(x, bool):
                nums.append(float(x))
            else:
                raise ValueError("All elements must be numeric to perform numeric operations")
        return nums

    def sum(self) -> float:
        return float(sum(self._numeric_list()))

    def product(self) -> float:
        nums = self._numeric_list()
        try:
            return math.prod(nums)
        except AttributeError:
            prod = 1.0
            for n in nums:
                prod *= n
            return prod

    def mean(self) -> float:
        nums = self._numeric_list()
        if not nums:
            raise ValueError("mean of empty sequence")
        return float(sum(nums) / len(nums))

    def median(self) -> float:
        nums = sorted(self._numeric_list())
        n = len(nums)
        if n == 0:
            raise ValueError("median of empty sequence")
        mid = n // 2
        if n % 2 == 1:
            return nums[mid]
        return (nums[mid - 1] + nums[mid]) / 2.0

    def mode(self):
        nums = self.flatten_copy()
        if not nums:
            raise ValueError("mode of empty sequence")
        counter = Counter(nums)
        most_common = counter.most_common(1)
        return most_common[0][0]

    def normalize(self, in_place: bool = False) -> "PyArray":
        """Scale numeric values to the range 0..1 based on min/max of flattened array."""
        nums = self._numeric_list()
        if not nums:
            return self if in_place else PyArray([])
        mn = min(nums)
        mx = max(nums)
        if math.isclose(mx, mn):
            normalized = [0.0 for _ in nums]
        else:
            normalized = [(x - mn) / (mx - mn) for x in nums]
        if in_place:
            self._data = normalized
            return self
        return PyArray(normalized)

    def standardize(self, in_place: bool = False) -> Tuple["PyArray", dict]:
        """Return a zero-mean unit-variance version with parameters (mean/std).

        Return value is (PyArray_of_standardized_values, {'mean': m, 'std': s})
        """
        nums = self._numeric_list()
        if not nums:
            return (self if in_place else PyArray([]), {'mean': 0.0, 'std': 1.0})
        m = sum(nums) / len(nums)
        # population std (ddof=0)
        var = sum((x - m) ** 2 for x in nums) / len(nums)
        s = math.sqrt(var)
        if math.isclose(s, 0.0):
            standardized = [0.0 for _ in nums]
        else:
            standardized = [(x - m) / s for x in nums]

        params = {'mean': m, 'std': s}
        if in_place:
            self._data = standardized
            return (self, params)
        return (PyArray(standardized), params)

    # --- Search & sorting -------------------------------------------
    def search(self, value: Any, algorithm: str = "linear", verbose: bool = False) -> int:
        """Search for value using linear or binary algorithm. Returns index or -1.

        For binary search the array must be sorted in non-decreasing order.
        """
        if algorithm not in ("linear", "binary"):
            raise ValueError("algorithm must be 'linear' or 'binary'")
        if algorithm == "linear":
            if verbose:
                print("Linear search: scanning elements")
            return self.index(value)

        # binary search
        lo = 0
        hi = len(self._data) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if self._data[mid] == value:
                return mid
            if self._data[mid] < value:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1

    def sort(self, key: Optional[Callable[[Any], Any]] = None, reverse: bool = False, algorithm: str = "tim", verbose: bool = False) -> "PyArray":
        """Sort the array and return a PyArray. Methods supported: 'tim' (Python's Timsort), 'quicksort', 'mergesort'."""
        if algorithm == "tim":
            if verbose:
                print("Using built-in Timsort")
            out = list(self._data)
            out.sort(key=key, reverse=reverse)
            return PyArray(out)

        if algorithm == "quicksort":
            if verbose:
                print("Using quicksort (recursive)")

            key_func = (lambda x: key(x)) if key is not None else (lambda x: x)

            def _quicksort(lst: List[Any]) -> List[Any]:
                if len(lst) <= 1:
                    return lst
                pivot = lst[len(lst) // 2]
                left = [x for x in lst if key_func(x) < key_func(pivot)]
                middle = [x for x in lst if key_func(x) == key_func(pivot)]
                right = [x for x in lst if key_func(x) > key_func(pivot)]
                return _quicksort(left) + middle + _quicksort(right)

            result = _quicksort(list(self._data))
            if reverse:
                result.reverse()
            return PyArray(result)

        if algorithm == "mergesort":
            if verbose:
                print("Using mergesort")

            key_func = (lambda x: key(x)) if key is not None else (lambda x: x)

            def _mergesort(lst: List[Any]) -> List[Any]:
                if len(lst) <= 1:
                    return lst
                mid = len(lst) // 2
                left = _mergesort(lst[:mid])
                right = _mergesort(lst[mid:])
                res: List[Any] = []
                i = j = 0
                while i < len(left) and j < len(right):
                    a = key_func(left[i])
                    b = key_func(right[j])
                    if a <= b:
                        res.append(left[i]); i += 1
                    else:
                        res.append(right[j]); j += 1
                res.extend(left[i:]); res.extend(right[j:])
                return res

            result = _mergesort(list(self._data))
            if reverse:
                result.reverse()
            return PyArray(result)

        raise ValueError("Unsupported sorting algorithm")

    # --- Optional / Advanced ---------------------------------------
    def find_missing(self) -> List[int]:
        """For a flattened numeric integer array, return missing integers between min and max (exclusive)."""
        flat = self.flatten_copy()
        integers = [int(x) for x in flat if isinstance(x, (int,)) and not isinstance(x, bool)]
        if not integers:
            return []
        lo, hi = min(integers), max(integers)
        present = set(integers)
        return [i for i in range(lo, hi + 1) if i not in present]

    def common_elements(self, other: Iterable[Any]) -> "PyArray":
        """Return a PyArray containing elements present in both arrays (order preserved from self)."""
        if isinstance(other, PyArray):
            other_set = set(other._data)
        else:
            other_set = set(other)
        return PyArray([x for x in self._data if x in other_set])

    def all_satisfy(self, func: Callable[[Any], bool]) -> bool:
        """Return True if predicate holds for every element."""
        return all(func(x) for x in self._data)

    def any_satisfy(self, func: Callable[[Any], bool]) -> bool:
        """Return True if predicate holds for any element."""
        return any(func(x) for x in self._data)


__all__ = ["PyArray"]
