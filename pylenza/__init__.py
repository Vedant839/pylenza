"""Top-level package exports for pylenza.

Expose commonly used modules and primary public symbols so callers can
import either modules (e.g. `from pylenza import sort`) or classes/functions
directly (e.g. `from pylenza import Stack`).
"""
# Package version
__version__ = "0.1.2"
# re-export submodules for convenience
from . import arrays as arrays
from . import linkedlist as linkedlist
from . import queue as queue
from . import stack as stack
from . import search as search
from . import sort as sort
from . import strings as strings
from . import recursion as recursion
from . import trees as trees

# -- common/primary names (convenience imports) -----------------------
from .arrays import PyArray
from .linkedlist import LinkedList, Node
from .queue import Queue, EmptyQueueError
from .stack import Stack, EmptyStackError
from .trees import TreeNode, BinaryTree, BST
# NOTE: avoid importing `logic.*` at package import time because those submodules
# can import other pylenza modules and create circular import problems. We
# expose `logic` and the submodules lazily via __getattr__ below so callers can
# still do `from pylenza import patterns` (it will import the submodule only
# when accessed).


def __getattr__(name: str):
	"""Lazy-load logic submodules when requested as attributes of the package.

	Supported names:
	  - 'logic' -> import pylenza.logic package
	  - 'patterns', 'puzzles', 'reasoning' -> import pylenza.logic.<name>

	This prevents circular import issues that happen when logic submodules are
	imported at package import time.
	"""
	if name == "logic":
		import importlib

		mod = importlib.import_module(".logic", __name__)
		globals()["logic"] = mod
		return mod

	if name in ("patterns", "puzzles", "reasoning"):
		import importlib

		sub = importlib.import_module(f".logic.{name}", __name__)
		globals()[name] = sub
		return sub

	raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
	# modules
	"arrays", "linkedlist", "queue", "stack", "search", "sort", "strings", "recursion", "trees", "logic",
	# convenience symbols
	"PyArray", "LinkedList", "Node", "Queue", "EmptyQueueError", "Stack", "EmptyStackError", "TreeNode", "BinaryTree", "BST",
]
