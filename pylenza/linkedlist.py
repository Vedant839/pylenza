"""Linked list data structures and utilities for educational use.

This module provides a simple singly-linked list implementation with
useful methods that are easy to read and extend.
"""
from __future__ import annotations

from typing import Any, Callable, Generator, Iterable, Optional, Tuple

try:
    # OPTIONAL: import PyArray from the package if present
    from .arrays import PyArray  # type: ignore
except Exception:  # pragma: no cover - optional
    PyArray = None  # type: ignore


class Node:
    """A node in a singly linked list.

    Attributes:
        value: payload stored in the node
        next: reference to the next Node or None
    """

    __slots__ = ("value", "next")

    def __init__(self, value: Any, nxt: Optional["Node"] = None) -> None:
        self.value = value
        self.next = nxt

    def __repr__(self) -> str:  # pragma: no cover - trivial repr
        return f"Node({self.value!r})"


class LinkedList:
    """A simple singly-linked list.

    The class aims to be easy to read and educational. Methods that
    would normally be destructive are implemented both in destructive
    (in-place) and non-destructive (return new list) forms where it
    makes sense.
    """

    def __init__(self, data: Optional[Iterable[Any]] = None) -> None:
        """Create a LinkedList from an optional iterable (list/tuple/PyArray).

        If data is None, an empty list is created. The constructor will
        accept PyArray or regular Python iterables.
        """
        self._head: Optional[Node] = None
        self._tail: Optional[Node] = None
        self._length: int = 0

        if data is None:
            return

        # Accept a PyArray-like object if available
        if PyArray is not None and isinstance(data, PyArray):
            seq = data.to_list()
        else:
            seq = list(data)

        for item in seq:
            self.append(item)

    def __repr__(self) -> str:  # pragma: no cover - representation
        return f"LinkedList({self.to_list()!r})"

    def __len__(self) -> int:
        return self._length

    # --- Conversions -------------------------------------------------
    def to_list(self) -> list:
        """Return a Python list with the linked list values (shallow copy)."""
        out = []
        cur = self._head
        while cur is not None:
            out.append(cur.value)
            cur = cur.next
        return out

    def to_array(self):
        """Convert to a PyArray if available, otherwise return a list."""
        if PyArray is None:
            return self.to_list()
        return PyArray(self.to_list())

    # --- Basic mutators ----------------------------------------------
    def append(self, value: Any) -> None:
        """Append value to the end of the list (O(1) with tail)."""
        node = Node(value)
        if self._head is None:
            self._head = self._tail = node
        else:
            assert self._tail is not None
            self._tail.next = node
            self._tail = node
        self._length += 1

    def prepend(self, value: Any) -> None:
        """Insert value at the start of the list (O(1))."""
        node = Node(value, self._head)
        self._head = node
        if self._tail is None:
            self._tail = node
        self._length += 1

    def insert(self, index: int, value: Any) -> None:
        """Insert value before index (0-based). If index >= len, appends."""
        if index <= 0 or self._head is None:
            return self.prepend(value)
        if index >= self._length:
            return self.append(value)

        prev = None
        cur = self._head
        i = 0
        while i < index and cur is not None:
            prev = cur
            cur = cur.next
            i += 1
        node = Node(value, cur)
        assert prev is not None
        prev.next = node
        self._length += 1

    def pop(self, index: int = -1) -> Any:
        """Remove and return element at index. Default last element."""
        if self._head is None:
            raise IndexError("pop from empty list")

        # normalize index
        if index < 0:
            index = self._length + index
        if index < 0 or index >= self._length:
            raise IndexError("index out of range")

        prev = None
        cur = self._head
        i = 0
        while i < index:
            prev = cur
            assert cur is not None
            cur = cur.next
            i += 1

        assert cur is not None
        value = cur.value
        # remove cur
        if prev is None:
            # popping head
            self._head = cur.next
            if self._head is None:
                self._tail = None
        else:
            prev.next = cur.next
            if prev.next is None:
                self._tail = prev

        self._length -= 1
        return value

    def delete(self, value: Any) -> bool:
        """Remove first occurrence of value; return True if removed, else False."""
        prev = None
        cur = self._head
        while cur is not None:
            if cur.value == value:
                if prev is None:
                    self._head = cur.next
                    if self._head is None:
                        self._tail = None
                else:
                    prev.next = cur.next
                    if prev.next is None:
                        self._tail = prev
                self._length -= 1
                return True
            prev = cur
            cur = cur.next
        return False

    def clear(self) -> None:
        """Remove all nodes from the list."""
        self._head = None
        self._tail = None
        self._length = 0

    # --- Accessors & queries ----------------------------------------
    def contains(self, value: Any) -> bool:
        return self.index(value) != -1

    def index(self, value: Any) -> int:
        i = 0
        cur = self._head
        while cur is not None:
            if cur.value == value:
                return i
            cur = cur.next
            i += 1
        return -1

    def get(self, index: int) -> Any:
        if index < 0:
            index = self._length + index
        if index < 0 or index >= self._length:
            raise IndexError("index out of range")
        cur = self._head
        i = 0
        while i < index:
            assert cur is not None
            cur = cur.next
            i += 1
        assert cur is not None
        return cur.value

    def find_middle(self) -> Optional[Node]:
        """Return middle node using slow/fast pointers. If even, returns left-middle."""
        slow = self._head
        fast = self._head
        while fast is not None and fast.next is not None and fast.next.next is not None:
            slow = slow.next  # type: ignore
            fast = fast.next.next
        return slow

    def nth_from_end(self, n: int) -> Any:
        """Return value of nth node from end (n=0 returns last)."""
        if n < 0:
            raise IndexError("n must be non-negative")

        if self._head is None:
            raise IndexError("list is empty")

        a = self._head
        b = self._head

        # advance `b` n steps; if we walk off the end, n is too large
        for _ in range(n):
            if b is None:
                raise IndexError("n is larger than list length")
            b = b.next

        if b is None:
            # exact length == n -> nth from end does not exist
            raise IndexError("n is larger than list length")

        # Move both pointers until `b` is at the last node; then `a` is nth from end
        while b.next is not None:
            a = a.next  # type: ignore
            b = b.next

        return a.value

    # --- Iteration & functional utilities ---------------------------
    def __iter__(self) -> Generator[Any, None, None]:
        cur = self._head
        while cur is not None:
            yield cur.value
            cur = cur.next

    def map(self, func: Callable[[Any], Any]) -> "LinkedList":
        out = LinkedList()
        for v in self:
            out.append(func(v))
        return out

    def filter(self, func: Callable[[Any], bool]) -> "LinkedList":
        out = LinkedList()
        for v in self:
            if func(v):
                out.append(v)
        return out

    def reduce(self, func: Callable[[Any, Any], Any], initial: Any = None) -> Any:
        it = iter(self)
        if initial is None:
            try:
                acc = next(it)
            except StopIteration:
                raise TypeError("reduce() of empty LinkedList with no initial value")
        else:
            acc = initial
        for v in it:
            acc = func(acc, v)
        return acc

    # --- Transformations --------------------------------------------
    def reverse(self, in_place: bool = True) -> "LinkedList":
        """Reverse the list.

        If in_place True the list is modified and returned, otherwise a new
        LinkedList is returned leaving the original list intact.
        """
        if self._length <= 1:
            return self if in_place else LinkedList(self.to_list())

        if not in_place:
            # copy then reverse in place
            copy = LinkedList(self.to_list())
            copy.reverse(in_place=True)
            return copy

        prev = None
        cur = self._head
        self._tail = self._head
        while cur is not None:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self._head = prev
        return self

    def merge(self, other: "LinkedList") -> "LinkedList":
        """Return a new LinkedList containing elements from self followed by other."""
        return LinkedList(self.to_list() + other.to_list())

    def rotate(self, k: int) -> "LinkedList":
        """Rotate the list circularly to the right by k nodes (in-place)."""
        n = self._length
        if n <= 1:
            return self
        k = k % n
        if k == 0:
            return self
        # new tail is at n - k - 1
        split = n - k
        prev = None
        cur = self._head
        i = 0
        while i < split:
            prev = cur
            cur = cur.next  # type: ignore
            i += 1
        # cur is new head
        assert prev is not None
        assert cur is not None
        prev.next = None
        old_tail = self._tail
        assert old_tail is not None
        old_tail.next = self._head
        self._head = cur
        self._tail = prev
        return self

    def remove_duplicates(self) -> "LinkedList":
        """Remove duplicate values, keeping the first occurrence (in-place)."""
        seen = set()
        prev = None
        cur = self._head
        while cur is not None:
            if cur.value in seen:
                assert prev is not None
                prev.next = cur.next
                if prev.next is None:
                    self._tail = prev
                self._length -= 1
                cur = prev.next
            else:
                seen.add(cur.value)
                prev = cur
                cur = cur.next
        return self

    # --- Advanced / algorithmic utilities --------------------------
    def is_palindrome(self) -> bool:
        """Detect whether the linked list values form a palindrome."""
        vals = self.to_list()
        return vals == list(reversed(vals))

    def detect_cycle(self) -> bool:
        """Detect cycle using Floyd's Tortoise and Hare algorithm."""
        slow = self._head
        fast = self._head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    def split_middle(self) -> Tuple["LinkedList", "LinkedList"]:
        """Split the list into two halves and return (left, right).

        If length is odd, left will contain the extra element.
        """
        if self._head is None:
            return (LinkedList(), LinkedList())
        mid = self.find_middle()
        if mid is None:
            return (LinkedList(), LinkedList())

        # left from head to mid inclusive
        left = LinkedList()
        cur = self._head
        while True:
            left.append(cur.value)  # type: ignore
            if cur is mid:
                break
            cur = cur.next  # type: ignore

        # right is remainder
        right = LinkedList()
        cur = mid.next
        while cur is not None:
            right.append(cur.value)
            cur = cur.next

        return left, right

    def sort(self) -> "LinkedList":
        """Sort the linked list using merge sort and return new sorted LinkedList."""
        # Non-destructive: operate on a list-of-values approach for clarity
        vals = self.to_list()
        if not vals:
            return LinkedList()

        def _merge_sort(arr: list) -> list:
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = _merge_sort(arr[:mid])
            right = _merge_sort(arr[mid:])
            i = j = 0
            out = []
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    out.append(left[i]); i += 1
                else:
                    out.append(right[j]); j += 1
            out.extend(left[i:]); out.extend(right[j:])
            return out

        return LinkedList(_merge_sort(vals))

    def common_elements(self, other: "LinkedList") -> "LinkedList":
        """Return a LinkedList with elements found in both lists (order from self)."""
        other_set = set(other.to_list())
        return LinkedList([x for x in self.to_list() if x in other_set])

    # --- Nested and numeric utilities -------------------------------
    def flatten(self, in_place: bool = False) -> "LinkedList":
        """Flatten nested LinkedLists and iterables (strings treated as scalars).

        The result contains all leaf values in a single-level LinkedList.
        """
        out = LinkedList()

        def _extend(item):
            if isinstance(item, LinkedList):
                for v in item:
                    _extend(v)
            elif _is_iterable_but_not_str(item):
                for v in item:
                    _extend(v)
            else:
                out.append(item)

        # local helper to detect iterables without importing top-level helper
        from collections.abc import Iterable

        def _is_iterable_but_not_str(obj: Any) -> bool:  # local copy
            if isinstance(obj, (str, bytes, bytearray)):
                return False
            return isinstance(obj, Iterable)

        for v in self:
            _extend(v)

        if in_place:
            self.clear()
            for v in out:
                self.append(v)
            return self
        return out

    def _numeric_list(self) -> list:
        """Return flattened list of numeric (float) values. Raises ValueError on non-numeric."""
        fl = self.flatten().to_list()
        nums = []
        for x in fl:
            if isinstance(x, (int, float)) and not isinstance(x, bool):
                nums.append(float(x))
            else:
                raise ValueError("All elements must be numeric to perform numeric operations")
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

    def mode(self):
        from collections import Counter

        flat = self.flatten().to_list()
        if not flat:
            raise ValueError("mode of empty sequence")
        counter = Counter(flat)
        return counter.most_common(1)[0][0]

    def normalize(self, in_place: bool = False) -> "LinkedList":
        nums = self._numeric_list()
        if not nums:
            return self if in_place else LinkedList()
        mn = min(nums)
        mx = max(nums)
        if mx == mn:
            normalized = [0.0 for _ in nums]
        else:
            normalized = [(x - mn) / (mx - mn) for x in nums]
        if in_place:
            self.clear()
            for v in normalized:
                self.append(v)
            return self
        return LinkedList(normalized)

    def standardize(self, in_place: bool = False) -> Tuple["LinkedList", dict]:
        nums = self._numeric_list()
        if not nums:
            return (self if in_place else LinkedList(), {'mean': 0.0, 'std': 1.0})
        m = sum(nums) / len(nums)
        var = sum((x - m) ** 2 for x in nums) / len(nums)
        s = var ** 0.5
        if s == 0.0:
            standardized = [0.0 for _ in nums]
        else:
            standardized = [(x - m) / s for x in nums]
        params = {'mean': m, 'std': s}
        if in_place:
            self.clear()
            for v in standardized:
                self.append(v)
            return (self, params)
        return (LinkedList(standardized), params)


__all__ = ["Node", "LinkedList"]
