# PyLenza

PyLenza is a small, beginner-friendly Python library of readable implementations
for common data structures and algorithms. Use it when you want clear, well-
documented examples for teaching, learning, or quick prototyping — not when you
need optimized production-grade data structures.

Quick highlights
- Lightweight, readable implementations for common data structures (arrays, linked lists, stacks, queues, trees).
- Algorithm templates for search & sort plus algorithmic patterns and puzzles (Tower of Hanoi, Kadane, etc.).
- Helpers for recursion, string manipulation, numeric operations and small utilities for learning.

Installation

The package is ready to publish; for local development you can install in editable mode:

```bash
python -m pip install -e .
```

install with:

```bash
pip install pylenza
```

Usage (copy-paste friendly)

```python
from pylenza import PyArray

arr = PyArray([1, 2, 3, 4])
arr.append(5)

# PyLenza

PyLenza is a small, beginner-friendly library of readable implementations
for common data structures and algorithms. It is intended for learning, teaching, and quick
prototyping — not for production-grade performance.

Version: 0.1.2

## Overview

PyLenza provides clear, well-documented, and self-contained examples of:
- Arrays and helpers (`PyArray`)
- Singly linked lists (`LinkedList`, `Node`)
- Stacks and Queues with small utilities
- Binary trees and a simple BST implementation
- Classic search and sorting algorithms
- String and recursion helpers and small logic puzzles

Use PyLenza when you want code that is:
- Easy to read and understand
- Good for learning algorithmic patterns
- Useful as teaching examples or interview practice

## Features (high level)

- **Readable implementations**: code prioritizes clarity over micro-optimizations.
- **Educational helpers**: small utilities for common algorithmic tasks.
- **Minimal dependencies**: NumPy is optional for array-to-numpy conversion.
- **Examples**: runnable example scripts in the `examples/` folder.

## Installation

Install from PyPI:
```bash
pip install pylenza
```

For local development (editable install):
```bash
python -m pip install -e .
```

## Quickstart (copy-paste friendly)

```python
from pylenza import PyArray, LinkedList, __version__

print("PyLenza version:", __version__)

# PyArray usage
arr = PyArray([1, 2, 3, 4])
arr.append(5)
print("Array:", arr)           # PyArray([1, 2, 3, 4, 5])
print("Mean:", arr.mean())     # 3.0

# LinkedList usage
ll = LinkedList(["a", "b", "c", "d"])
print("List:", ll.to_list())   # ['a', 'b', 'c', 'd']
print("Last element (n=0):", ll.nth_from_end(0))
```

A minimal runnable example is included at `examples/canonical_example.py`. Run it directly:
```bash
python examples/canonical_example.py
```

This prints the package version and runs a couple of small operations so you can
verify the package works directly from the repository.

## Modules (quick reference)

- `pylenza.arrays` — `PyArray` and numeric helpers
- `pylenza.linkedlist` — `LinkedList`, `Node`
- `pylenza.stack` — `Stack`, `EmptyStackError`
- `pylenza.queue` — `Queue`, `EmptyQueueError`
- `pylenza.trees` — `TreeNode`, `BinaryTree`, `BST`
- `pylenza.search` — search algorithms (linear, binary, jump, etc.)
- `pylenza.sort` — sorting algorithms (bubble, merge, quick, timsort, etc.)
- `pylenza.strings` — string utilities and helpers
- `pylenza.recursion` — recursive algorithms and helpers
- `pylenza.logic` — (lazy-loaded) puzzles, patterns and reasoning helpers

## Tests

Run tests locally (install test dependencies first if needed):
```bash
python -m pip install pytest
pytest -q
```

## Building & Publishing

Build source + wheel distributions:
```bash
python -m pip install --upgrade build
python -m build
```

Upload to PyPI (use an API token or `~/.pypirc`):
```bash
python -m pip install --upgrade twine
python -m twine upload dist/*
```

Note: Do not store PyPI API tokens in source control — use CI secrets or `~/.pypirc`.

## Contributing

- Keep changes small and focused.
- Aim for readability and correctness.
- Add tests for bug fixes and new features.
- Please open an issue or PR with a clear description and small diff.

## License

This project is distributed under the MIT License — see the `LICENCE` file.

## Changelog

See `CHANGELOG.md` for release notes. v0.1.2 contains bug fixes and stability improvements.

