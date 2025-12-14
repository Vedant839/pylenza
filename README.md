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
print(arr.mean())  # prints the mean
```

Minimal runnable example

```bash
python examples/canonical_example.py
```

This prints the package version and runs a couple of small operations so you can
verify the package works directly from the repository.

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

	Publishing to PyPI

	There are two common ways to publish releases:

	1) Manual local publish (useful for quick releases):

		1. Create an API token on PyPI (Account → API tokens) and copy it.
		2. Either create a local `~/.pypirc` following `.pypirc.example` (username __token__, password = token),
			or pass credentials directly to twine.
		3. Build and upload:

	```bash
	python -m pip install --upgrade build twine
	python -m build  # produces dist/ wheel and sdist
	python -m twine upload dist/* --username __token__ --password ${PYPI_TOKEN}
	```

	2) Automated CI publishing (recommended):

		- A GitHub Actions workflow is included at `.github/workflows/publish.yml`. It will:
		  - run on pushed git tags that start with `v` (for example `v0.1.0`)
		  - build wheel and sdist, then publish to PyPI via `twine`.

		- To enable it create a repository secret named `PYPI_API_TOKEN` with the token value
		  (generated at https://pypi.org/manage/account/ ). Then push a tag:

	```bash
	git tag v0.1.0
	git push origin v0.1.0
	```

	Security note

	- Do NOT store PyPI tokens or credentials in source control. Use GitHub repository secrets for CI or `~/.pypirc` locally.


License

This project is distributed under the MIT License.

Contributing
- Pull requests and issues are welcome — keep contributions small and well-documented so they are easy to review.

Contact
- Author: Vedant Shukla <vedantshukla1056@gmail.com>

