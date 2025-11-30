"""Queue data structure with useful utilities for learning and practice.

Primarily backed by collections.deque for O(1) enqueue/dequeue operations.
The implementation offers both FIFO queue behavior and a simple priority
queue helper for common learning scenarios.
"""
from __future__ import annotations

from collections import deque
from collections import Counter
from functools import reduce as _reduce
from typing import Any, Callable, Deque, Generator, Iterable, List, Optional, Tuple
import math


class EmptyQueueError(IndexError):
    """Raised when attempting to dequeue or peek from an empty queue."""


class Queue:
    """A flexible queue implementation backed by deque.

    It supports common queue operations plus bulk operations, simple
    priority insert, functional helpers (map/filter/reduce), and
    numeric convenience methods when the queue contains numeric data.
    """

    def __init__(self, data: Optional[Iterable[Any]] = None) -> None:
        self._dq: Deque[Any] = deque()
        # queue may optionally store (priority, value) tuples for priority usage
        if data is not None:
            for v in data:
                self.enqueue(v)

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"Queue({self.to_list()!r})"

    def __len__(self) -> int:
        return len(self._dq)

    # --- conversions ------------------------------------------------------
    def to_list(self) -> List[Any]:
        """Return a list copying queue contents from front to back."""
        return list(self._dq)

    # --- core operations -------------------------------------------------
    def enqueue(self, value: Any) -> None:
        """Add value to the back of the queue (FIFO)."""
        self._dq.append(value)

    def dequeue(self) -> Any:
        """Remove and return the front element. Raises EmptyQueueError if empty."""
        if not self._dq:
            raise EmptyQueueError("dequeue from empty queue")
        return self._dq.popleft()

    def peek(self) -> Any:
        """Return the front element without removing it."""
        if not self._dq:
            raise EmptyQueueError("peek from empty queue")
        return self._dq[0]

    def is_empty(self) -> bool:
        return len(self._dq) == 0

    def clear(self) -> None:
        self._dq.clear()

    # --- bulk & utils ----------------------------------------------------
    def enqueue_multiple(self, iterable: Iterable[Any]) -> None:
        """Enqueue all items from an iterable, preserving order."""
        for v in iterable:
            self.enqueue(v)

    def dequeue_n(self, n: int) -> List[Any]:
        """Dequeue and return a list of up to n items. Raises if n < 0."""
        if n < 0:
            raise ValueError("n must be non-negative")
        out: List[Any] = []
        for _ in range(n):
            if not self._dq:
                break
            out.append(self.dequeue())
        return out

    def contains(self, value: Any) -> bool:
        return value in self._dq

    def index(self, value: Any) -> int:
        """Return index of value from front, or -1 if not found."""
        try:
            return self.to_list().index(value)
        except ValueError:
            return -1

    def rotate(self, k: int) -> "Queue":
        """Rotate the queue circularly by k to the right (positive k).

        Returns self for convenience (in-place operation).
        """
        if not self._dq:
            return self
        self._dq.rotate(k)
        return self

    # --- iteration & transformations -------------------------------------
    def __iter__(self) -> Generator[Any, None, None]:
        for v in self._dq:
            yield v

    def reverse(self, in_place: bool = True) -> "Queue":
        """Reverse queue order. In place if requested, otherwise return a new Queue."""
        if in_place:
            self._dq = deque(reversed(self._dq))
            return self
        return Queue(reversed(self._dq))

    def merge(self, other: "Queue") -> "Queue":
        """Return a new Queue containing items from self followed by other."""
        return Queue(list(self._dq) + list(other._dq))

    def chunk(self, size: int) -> List["Queue"]:
        if size <= 0:
            raise ValueError("chunk size must be positive")
        data = self.to_list()
        return [Queue(data[i : i + size]) for i in range(0, len(data), size)]

    # --- functional utilities --------------------------------------------
    def map(self, func: Callable[[Any], Any], in_place: bool = False) -> "Queue":
        mapped = [func(x) for x in self._dq]
        if in_place:
            self._dq = deque(mapped)
            return self
        return Queue(mapped)

    def filter(self, func: Callable[[Any], bool]) -> "Queue":
        return Queue([x for x in self._dq if func(x)])

    def reduce(self, func: Callable[[Any, Any], Any], initial: Optional[Any] = None) -> Any:
        it = iter(self._dq)
        if initial is None:
            try:
                acc = next(it)
            except StopIteration:
                raise TypeError("reduce() of empty Queue with no initial value")
        else:
            acc = initial
        for v in it:
            acc = func(acc, v)
        return acc

    # --- simple priority helpers ----------------------------------------
    def enqueue_priority(self, value: Any, priority: float = 0.0) -> None:
        """Insert an item with a numeric priority; lower values dequeue first.

        This is a simple O(n) insertion-based priority queue for teaching.
        Items are stored as tuples (priority, counter, value) so FIFO is preserved
        among equal-priority items.
        """
        # locate insertion point
        # we will store as (priority, value) for simplicity
        inserted = False
        i = 0
        while i < len(self._dq):
            try:
                pr, _ = self._dq[i]
            except Exception:
                # if existing items are non-priority, treat them as lowest priority
                pr = float('inf')
            if priority < pr:
                self._dq.insert(i, (priority, value))
                inserted = True
                break
            i += 1
        if not inserted:
            self._dq.append((priority, value))

    # --- numeric helpers (operate on flattened numeric values) -----------
    def _numeric_list(self) -> List[float]:
        data = list(self._dq)
        # if priority tuples present, extract values
        cleaned = []
        for x in data:
            if isinstance(x, tuple) and len(x) == 2 and isinstance(x[0], (int, float)):
                val = x[1]
            else:
                val = x
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                cleaned.append(float(val))
            else:
                raise ValueError("All elements must be numeric to use numeric helpers")
        return cleaned

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
        data = [x[1] if isinstance(x, tuple) and len(x) == 2 and isinstance(x[0], (int, float)) else x for x in list(self._dq)]
        if not data:
            raise ValueError("mode of empty sequence")
        cnt = Counter(data)
        return cnt.most_common(1)[0][0]

    def normalize(self, in_place: bool = False) -> "Queue":
        nums = self._numeric_list()
        if not nums:
            return self if in_place else Queue()
        mn = min(nums)
        mx = max(nums)
        if mx == mn:
            normalized = [0.0 for _ in nums]
        else:
            normalized = [(x - mn) / (mx - mn) for x in nums]
        if in_place:
            self._dq = deque(normalized)
            return self
        return Queue(normalized)

    def standardize(self, in_place: bool = False) -> Tuple["Queue", dict]:
        nums = self._numeric_list()
        if not nums:
            return (self if in_place else Queue(), {'mean': 0.0, 'std': 1.0})
        m = sum(nums) / len(nums)
        var = sum((x - m) ** 2 for x in nums) / len(nums)
        s = math.sqrt(var)
        if s == 0.0:
            standardized = [0.0 for _ in nums]
        else:
            standardized = [(x - m) / s for x in nums]
        params = {'mean': m, 'std': s}
        if in_place:
            self._dq = deque(standardized)
            return (self, params)
        return (Queue(standardized), params)


__all__ = ["Queue", "EmptyQueueError"]
