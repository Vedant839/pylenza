"""Top-level package exports for pylenza.

Expose commonly used modules and primary public symbols so callers can
import either modules (e.g. `from pylenza import sort`) or classes/functions
directly (e.g. `from pylenza import Stack`).
"""
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
from . import logic as logic

# -- common/primary names (convenience imports) -----------------------
from .arrays import PyArray
from .linkedlist import LinkedList, Node
from .queue import Queue, EmptyQueueError
from .stack import Stack, EmptyStackError
from .trees import TreeNode, BinaryTree, BST
from .logic.patterns import *
from .logic.puzzles import *
from .logic.reasoning import *

__all__ = [
	# modules
	"arrays", "linkedlist", "queue", "stack", "search", "sort", "strings", "recursion", "trees", "logic",
	# convenience symbols
	"PyArray", "LinkedList", "Node", "Queue", "EmptyQueueError", "Stack", "EmptyStackError", "TreeNode", "BinaryTree", "BST",
]
