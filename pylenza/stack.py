"""Simple, learning-friendly LIFO stack implementation.

Backed by a Python list with the top of the stack at the list end. The
class provides useful helpers (bulk operations, functional utilities,
numeric helpers) following the same style as other modules in pylenza.
"""
from __future__ import annotations

from collections import Counter
from functools import reduce as _reduce
from typing import Any, Callable, Iterable, List, Optional, Tuple
import math


class EmptyStackError(IndexError):
    """Raised when popping/peeking from an empty stack."""


def _is_iterable_but_not_str(obj: Any) -> bool:
    if isinstance(obj, (str, bytes, bytearray)):
        return False
    try:
        iter(obj)
    except TypeError:
        return False
    return True


class Stack:
    """A simple last-in-first-out stack with teaching-friendly helpers."""

    def __init__(self, data: Optional[Iterable[Any]] = None) -> None:
        self._data: List[Any] = []
        if data is None:
            return
        if isinstance(data, Stack):
            self._data = list(data._data)
            return
        if isinstance(data, list):
            self._data = list(data)
            return
        if isinstance(data, tuple):
            self._data = list(data)
            return

        if _is_iterable_but_not_str(data):
            self._data = list(data)
            return

        raise TypeError("data must be an iterable or None")

    def __repr__(self) -> str:  # pragma: no cover - readability only
        return f"Stack({self._data!r})"

    def __len__(self) -> int:
        return len(self._data)

    # --- conversions ----------------------------------------------------
    def to_list(self) -> List[Any]:
        """Return a shallow list copy of the stack (bottom .. top)."""
        return list(self._data)

    # --- core operations ------------------------------------------------
    def push(self, value: Any) -> None:
        """Push value onto the stack."""
        self._data.append(value)

    def pop(self) -> Any:
        """Remove and return the top element. Raises EmptyStackError if empty."""
        if not self._data:
            raise EmptyStackError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Any:
        """Return the top element without removing it."""
        if not self._data:
            raise EmptyStackError("peek from empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def clear(self) -> None:
        self._data.clear()

    # --- bulk & utility -------------------------------------------------
    def push_multiple(self, iterable: Iterable[Any]) -> None:
        for v in iterable:
            self.push(v)

    def pop_n(self, n: int) -> List[Any]:
        if n < 0:
            raise ValueError("n must be non-negative")
        out: List[Any] = []
        for _ in range(n):
            if not self._data:
                break
            out.append(self.pop())
        return out

    def contains(self, value: Any) -> bool:
        return value in self._data

    def index(self, value: Any) -> int:
        """Return top-based index: 0 for top, 1 for next-from-top, -1 if missing."""
        try:
            # list.index is bottom-based; convert
            pos = len(self._data) - 1 - self._data[::-1].index(value)
            # convert to top-based index
            return len(self._data) - 1 - pos
        except ValueError:
            return -1

    def reverse(self, in_place: bool = True) -> "Stack":
        if in_place:
            self._data.reverse()
            return self
        return Stack(list(reversed(self._data)))

    def merge(self, other: "Stack") -> "Stack":
        """Return new Stack with items from self bottom..top followed by other's bottom..top."""
        return Stack(self._data + list(other._data))

    def chunk(self, size: int) -> List["Stack"]:
        if size <= 0:
            raise ValueError("chunk size must be positive")
        out: List[Stack] = []
        for i in range(0, len(self._data), size):
            out.append(Stack(self._data[i : i + size]))
        return out

    # --- functional helpers ---------------------------------------------
    def map(self, func: Callable[[Any], Any], in_place: bool = False) -> "Stack":
        mapped = [func(x) for x in self._data]
        if in_place:
            self._data = mapped
            return self
        return Stack(mapped)

    def filter(self, func: Callable[[Any], bool]) -> "Stack":
        return Stack([x for x in self._data if func(x)])

    def reduce(self, func: Callable[[Any, Any], Any], initial: Optional[Any] = None) -> Any:
        it = iter(self._data)
        if initial is None:
            try:
                acc = next(it)
            except StopIteration:
                raise TypeError("reduce() of empty Stack with no initial value")
        else:
            acc = initial
        for v in it:
            acc = func(acc, v)
        return acc

    # --- numeric helpers -----------------------------------------------
    def _numeric_list(self) -> List[float]:
        flat = list(self._data)
        nums: List[float] = []
        for x in flat:
            if isinstance(x, (int, float)) and not isinstance(x, bool):
                nums.append(float(x))
            else:
                raise ValueError("All elements must be numeric to use numeric helpers")
        return nums

    def sum(self) -> float:
        return float(sum(self._numeric_list()))

    def product(self) -> float:
        nums = self._numeric_list()
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

    def mode(self) -> Any:
        flat = list(self._data)
        if not flat:
            raise ValueError("mode of empty sequence")
        counter = Counter(flat)
        return counter.most_common(1)[0][0]

    def normalize(self, in_place: bool = False) -> "Stack":
        nums = self._numeric_list()
        if not nums:
            return self if in_place else Stack()
        mn = min(nums)
        mx = max(nums)
        if mx == mn:
            normalized = [0.0 for _ in nums]
        else:
            normalized = [(x - mn) / (mx - mn) for x in nums]
        if in_place:
            self._data = normalized
            return self
        return Stack(normalized)

    def standardize(self, in_place: bool = False) -> Tuple["Stack", dict]:
        nums = self._numeric_list()
        if not nums:
            return (self if in_place else Stack(), {'mean': 0.0, 'std': 1.0})
        m = sum(nums) / len(nums)
        var = sum((x - m) ** 2 for x in nums) / len(nums)
        s = math.sqrt(var)
        if s == 0.0:
            standardized = [0.0 for _ in nums]
        else:
            standardized = [(x - m) / s for x in nums]
        params = {'mean': m, 'std': s}
        if in_place:
            self._data = standardized
            return (self, params)
        return (Stack(standardized), params)

    # --- advanced helpers ----------------------------------------------
    def flatten(self, in_place: bool = False) -> "Stack":
        out: List[Any] = []

        def _extend(item):
            if isinstance(item, Stack):
                for v in item._data:
                    _extend(v)
            elif _is_iterable_but_not_str(item):
                for v in item:
                    _extend(v)
            else:
                out.append(item)

        for v in self._data:
            _extend(v)

        if in_place:
            self._data = out
            return self
        return Stack(out)

    def unique(self, stable: bool = True) -> "Stack":
        if stable:
            seen = set()
            out: List[Any] = []
            for x in self._data:
                if x not in seen:
                    seen.add(x)
                    out.append(x)
            return Stack(out)
        return Stack(list(dict.fromkeys(self._data)))

    def all_satisfy(self, func: Callable[[Any], bool]) -> bool:
        return all(func(x) for x in self._data)

    def any_satisfy(self, func: Callable[[Any], bool]) -> bool:
        return any(func(x) for x in self._data)


__all__ = ["Stack", "EmptyStackError"]
