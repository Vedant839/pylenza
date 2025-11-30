# PyLenza

PyLenza is a beginner-friendly Python package for learning data structures, algorithms, recursion, and logical reasoning.
It provides clean, well-documented teaching helpers and small, self-contained algorithms suitable for learners and interview prep.

Quick highlights
- Lightweight, readable implementations for common data structures (arrays, linked lists, stacks, queues, trees).
- Algorithm templates for search & sort plus algorithmic patterns and puzzles (N-Queens, Tower of Hanoi, Kadane, etc.).
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
print(arr.mean())  # prints the mean
```

Modules (overview)

- arrays — PyArray: list-like API + numeric, transform, search & sort helpers
- linkedlist — Singly LinkedList with traversal, mutators and utilities
- queue / stack — Teaching-friendly FIFO / LIFO containers with helpers
- search / sort — Classic search and sorting implementations for learning
- strings — String helpers (palindromes, parsing, substring utilities)
- recursion / trees — Recursion exercises and BinaryTree / BST utilities
- logic — `patterns`, `puzzles`, `reasoning` for algorithmic thinking

Examples & how to run
- Examples are available in the `examples/` folder. Each script is standalone and runnable:
	- python examples/array_examples.py
	- python examples/logic_examples.py
	- python examples/recursion_examples.py

License

This project is distributed under the MIT License.

Contributing
- Pull requests and issues are welcome — keep contributions small and well-documented so they are easy to review.

Contact
- Author: Vedant Shukla <vedantshukla1056@gmail.com>

