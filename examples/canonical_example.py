"""Minimal canonical example for PyLenza v0.1.2

This script is intentionally minimal and copy-paste friendly. It demonstrates
importing the package, checking version, and using one example from arrays
and linkedlist. Run with:

    python examples/canonical_example.py

It will work directly from the repository root without installation.
"""
from __future__ import annotations

import os
import sys

# Ensure project root is on sys.path when running examples directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pylenza import PyArray, LinkedList, __version__


def main():
    print(f"PyLenza version: {__version__}")

    arr = PyArray([10, 20, 30, 40])
    print("PyArray:", arr)
    arr.append(50)
    print("After append:", arr)
    print("Mean:", arr.mean())

    ll = LinkedList(["a", "b", "c", "d"])
    print("LinkedList as list:", ll.to_list())
    print("2nd from end (n=1):", ll.nth_from_end(1))


if __name__ == '__main__':
    main()
