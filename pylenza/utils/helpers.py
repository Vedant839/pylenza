"""Small, generic helpers used across the repository.

These functions are intentionally implementation-light and dependency-free
so every other module can import them safely. They focus on clarity and
teaching-friendly behavior.
"""
from __future__ import annotations

from typing import Any, Generator, Iterable, List, Optional
import time
import random


def is_prime(n: int) -> bool:
    """Return True if n is prime using a simple trial division.

    Complexity: O(sqrt(n)). Not optimized for very large numbers but
    fine for educational use and testing.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def gcd(a: int, b: int) -> int:
    """Greatest common divisor (Euclid's algorithm)."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Least common multiple; returns 0 if one of inputs is 0."""
    if a == 0 or b == 0:
        return 0
    return abs(a // gcd(a, b) * b)


def factorial(n: int) -> int:
    """Basic iterative factorial. Raises ValueError for negative inputs."""
    if n < 0:
        raise ValueError("n must be non-negative")
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res


def ncr(n: int, r: int) -> int:
    """Compute n choose r using an efficient multiplicative approach."""
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)
    num = 1
    den = 1
    for i in range(1, r + 1):
        num *= n - (r - i)
        den *= i
    return num // den


def chunks(iterable: Iterable[Any], size: int) -> Generator[List[Any], None, None]:
    """Yield successive chunks (lists) from iterable of given size.

    Example: list(chunks(range(6), 2)) -> [[0,1],[2,3],[4,5]]
    """
    if size <= 0:
        raise ValueError("size must be positive")
    buf: List[Any] = []
    for item in iterable:
        buf.append(item)
        if len(buf) == size:
            yield list(buf)
            buf.clear()
    if buf:
        yield list(buf)


def _is_iterable_but_not_str(obj: Any) -> bool:
    if isinstance(obj, (str, bytes, bytearray)):
        return False
    try:
        iter(obj)
    except TypeError:
        return False
    return True


def flatten_iterable(iterable: Iterable[Any]) -> List[Any]:
    """Flatten nested lists/tuples/iterables (strings are treated as atoms).

    This is an iterative, non-recursive approach to avoid recursion depth
    issues and remains explicit for educational purposes.
    """
    out: List[Any] = []
    stack: List[Any] = list(iterable)
    while stack:
        item = stack.pop(0)
        if _is_iterable_but_not_str(item):
            stack[0:0] = list(item)
        else:
            out.append(item)
    return out


def unique_elements(seq: Iterable[Any]) -> List[Any]:
    """Return elements preserving first-occurrence order."""
    seen = set()
    out: List[Any] = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def is_palindrome(s: str, ignore_case: bool = True) -> bool:
    if ignore_case:
        s = s.lower()
    return s == s[::-1]


def reverse_string(s: str) -> str:
    return s[::-1]


def count_chars(s: str) -> dict:
    d: dict = {}
    for ch in s:
        d[ch] = d.get(ch, 0) + 1
    return d


def print_matrix(matrix: List[List[Any]]) -> None:
    for row in matrix:
        print(' '.join(str(x) for x in row))


def print_linkedlist(head: Any) -> None:
    vals: List[str] = []
    cur = head
    while cur is not None:
        vals.append(str(getattr(cur, 'value', cur)))
        cur = getattr(cur, 'next', None)
    print(' -> '.join(vals))


def time_function(func: Callable[..., Any]):
    """Decorator that measures a function's execution time and returns result and elapsed seconds.

    Usage:
        @time_function
        def work(...):
            ...

    The wrapper returns a tuple (result, elapsed_seconds) for visibility.
    """
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        res = func(*args, **kwargs)
        t1 = time.perf_counter()
        return res, t1 - t0

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


def random_int_list(size: int, start: int = 0, end: int = 10) -> List[int]:
    if size < 0:
        raise ValueError("size must be non-negative")
    return [random.randint(start, end) for _ in range(size)]


def shuffle_list(lst: List[Any]) -> List[Any]:
    out = list(lst)
    random.shuffle(out)
    return out


__all__ = [
    'is_prime', 'gcd', 'lcm', 'factorial', 'ncr',
    'chunks', 'flatten_iterable', 'unique_elements',
    'is_palindrome', 'reverse_string', 'count_chars',
    'print_matrix', 'print_linkedlist', 'time_function',
    'random_int_list', 'shuffle_list'
]
