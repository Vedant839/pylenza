"""Algorithmic problem patterns (sliding window, two pointers, prefix sums, etc.).

These small, reusable helpers illustrate common patterns used in
interviews and competitive programming. Functions are intentionally
small and readable so students can map real problems to these templates.
"""
from __future__ import annotations

from collections import deque
from typing import Any, Callable, Generator, Iterable, List, Optional, Sequence, Tuple


def prefix_sums(arr: Sequence[float]) -> List[float]:
    """Return prefix sums array where ps[i] = sum(arr[:i]). O(n)."""
    out: List[float] = [0.0]
    s = 0.0
    for x in arr:
        s += x
        out.append(s)
    return out


def apply_sliding_window(arr: Sequence[Any], k: int, func: Callable[[Sequence[Any]], Any]) -> List[Any]:
    """Apply func to every sliding window of size k and return results.

    Example: apply_sliding_window([1,2,3,4], 3, sum) -> [6,9]
    """
    if k <= 0:
        raise ValueError("k must be positive")
    res: List[Any] = []
    if k > len(arr):
        return res
    for i in range(len(arr) - k + 1):
        res.append(func(arr[i : i + k]))
    return res


def max_subarray_kadane(arr: Sequence[float]) -> float:
    """Kadane's algorithm: return maximum subarray sum. O(n)."""
    if not arr:
        return 0.0
    max_ending = max_so_far = arr[0]
    for x in arr[1:]:
        max_ending = max(x, max_ending + x)
        max_so_far = max(max_so_far, max_ending)
    return max_so_far


def two_pointer_sum_sorted(arr: Sequence[int], target: int) -> Optional[Tuple[int, int]]:
    """Given a sorted array, return pair of values summing to target (or None).

    Classic two-pointer pattern: O(n).
    """
    i, j = 0, len(arr) - 1
    while i < j:
        s = arr[i] + arr[j]
        if s == target:
            return (arr[i], arr[j])
        if s < target:
            i += 1
        else:
            j -= 1
    return None


def two_pointer_two_sum(arr: Sequence[int], target: int) -> Optional[Tuple[int, int]]:
    """Two-sum using hash-table — returns first matching pair of indices.

    Not exactly two-pointer but commonly used with this family of approaches.
    """
    seen = {}
    for i, v in enumerate(arr):
        need = target - v
        if need in seen:
            return (seen[need], i)
        seen[v] = i
    return None


def merge_intervals(intervals: Iterable[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Merge overlapping intervals. Returns list sorted and merged.

    intervals are (start, end) inclusive/exclusive depending on usage — we
    treat end as inclusive in this simple implementation.
    """
    arr = sorted(intervals, key=lambda x: x[0])
    if not arr:
        return []
    merged: List[Tuple[int, int]] = [arr[0]]
    for s, e in arr[1:]:
        last_s, last_e = merged[-1]
        if s <= last_e:
            merged[-1] = (last_s, max(last_e, e))
        else:
            merged.append((s, e))
    return merged


# --- Linked list patterns (works with LinkedList Node-like objects) ----


def fast_slow_cycle_detection(head: Any) -> bool:
    """Detect cycle using Floyd's algorithm. `head` must support .next"""
    slow = fast = head
    while fast is not None and getattr(fast, 'next', None) is not None:
        slow = getattr(slow, 'next', None)
        fast = getattr(getattr(fast, 'next', None), 'next', None)
        if slow is fast and slow is not None:
            return True
    return False


def reverse_linked_list(head: Any) -> Any:
    """Reverse singly-linked list in-place and return new head. Expects .next attribute."""
    prev = None
    cur = head
    while cur is not None:
        nxt = getattr(cur, 'next', None)
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


# --- Tree & graph patterns (small wrappers) -------------------------


def dfs_preorder(root: Any) -> List[Any]:
    """Pre-order traversal of a tree (expects node.value, node.left, node.right)."""
    out: List[Any] = []

    def _rec(n: Any) -> None:
        if n is None:
            return
        out.append(n.value)
        _rec(getattr(n, 'left', None))
        _rec(getattr(n, 'right', None))

    _rec(root)
    return out


def dfs_inorder(root: Any) -> List[Any]:
    out: List[Any] = []

    def _rec(n: Any) -> None:
        if n is None:
            return
        _rec(getattr(n, 'left', None))
        out.append(n.value)
        _rec(getattr(n, 'right', None))

    _rec(root)
    return out


def dfs_postorder(root: Any) -> List[Any]:
    out: List[Any] = []

    def _rec(n: Any) -> None:
        if n is None:
            return
        _rec(getattr(n, 'left', None))
        _rec(getattr(n, 'right', None))
        out.append(n.value)

    _rec(root)
    return out


def bfs(root: Any) -> List[Any]:
    out: List[Any] = []
    q = deque([root]) if root is not None else deque()
    while q:
        n = q.popleft()
        out.append(n.value)
        if getattr(n, 'left', None) is not None:
            q.append(n.left)
        if getattr(n, 'right', None) is not None:
            q.append(n.right)
    return out


def recursive_helper_template():
    """A tiny reusable template showing the recursive structure.

    Use this as a pedagogical tool to copy/paste for new recursive functions.
    """
    def helper(node):
        # base case
        if node is None:
            return
        # pre-processing
        # recurse
        helper(node.left)
        helper(node.right)
        # post-processing

    return helper


__all__ = [
    'prefix_sums', 'apply_sliding_window', 'max_subarray_kadane',
    'two_pointer_sum_sorted', 'two_pointer_two_sum', 'merge_intervals',
    'fast_slow_cycle_detection', 'reverse_linked_list',
    'dfs_preorder', 'dfs_inorder', 'dfs_postorder', 'bfs', 'recursive_helper_template',
]
