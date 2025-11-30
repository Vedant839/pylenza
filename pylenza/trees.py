"""Definitions and utilities for binary trees and BSTs.

This module provides teaching-friendly implementations of tree nodes,
binary trees and a BST subclass with recursive traversals and common
algorithms like height, diameter, LCA and path_sum.
"""
from __future__ import annotations

from collections import deque
from typing import Any, Generator, List, Optional, Tuple


class TreeNode:
    __slots__ = ("value", "left", "right")

    def __init__(self, value: Any, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None) -> None:
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"TreeNode({self.value!r})"


class BinaryTree:
    """Simple binary tree with value-bearing nodes.

    The tree supports level-order insertion (to fill by level), common
    traversals, and utilities suitable for learning code examples.
    """

    def __init__(self, values: Optional[List[Any]] = None):
        self.root: Optional[TreeNode] = None
        if values:
            self.build_from_level_order(values)

    def build_from_level_order(self, values: List[Any]) -> None:
        """Build a binary tree from a level-order list of values (None = empty node)."""
        if not values:
            self.root = None
            return
        it = iter(values)
        root_val = next(it)
        self.root = TreeNode(root_val)
        q = deque([self.root])
        for val in it:
            node = q[0]
            if node.left is None:
                if val is not None:
                    node.left = TreeNode(val)
                    q.append(node.left)
            elif node.right is None:
                if val is not None:
                    node.right = TreeNode(val)
                    q.append(node.right)
                q.popleft()

    def insert(self, value: Any) -> None:
        """Insert value in level-order (fills left-to-right by level)."""
        node = TreeNode(value)
        if self.root is None:
            self.root = node
            return
        q = deque([self.root])
        while q:
            cur = q.popleft()
            if cur.left is None:
                cur.left = node
                return
            q.append(cur.left)
            if cur.right is None:
                cur.right = node
                return
            q.append(cur.right)

    def size(self, node: Optional[TreeNode] = None) -> int:
        def _size(n: Optional[TreeNode]) -> int:
            if n is None:
                return 0
            return 1 + _size(n.left) + _size(n.right)

        if node is None:
            node = self.root
        return _size(node)

    def height(self, node: Optional[TreeNode] = None) -> int:
        def _height(n: Optional[TreeNode]) -> int:
            if n is None:
                return 0
            return 1 + max(_height(n.left), _height(n.right))

        if node is None:
            node = self.root
        return _height(node)

    def find(self, value: Any, node: Optional[TreeNode] = None) -> bool:
        def _find(n: Optional[TreeNode]) -> bool:
            if n is None:
                return False
            if n.value == value:
                return True
            return _find(n.left) or _find(n.right)

        if node is None:
            node = self.root
        return _find(node)

    # --- traversals -------------------------------------------------
    def inorder(self, node: Optional[TreeNode] = None, recursive: bool = True) -> List[Any]:
        # Public wrapper: if no node passed, start at root
        if node is None:
            node = self.root
        if node is None:
            return []

        def _rec(n: Optional[TreeNode]) -> List[Any]:
            if n is None:
                return []
            return _rec(n.left) + [n.value] + _rec(n.right)

        if recursive:
            return _rec(node)

        # iterative implementation
        res = []
        stack = []
        cur = node
        while stack or cur is not None:
            while cur is not None:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            res.append(cur.value)
            cur = cur.right
        return res

    def preorder(self, node: Optional[TreeNode] = None, recursive: bool = True) -> List[Any]:
        if node is None:
            node = self.root
        if node is None:
            return []

        def _rec(n: Optional[TreeNode]) -> List[Any]:
            if n is None:
                return []
            return [n.value] + _rec(n.left) + _rec(n.right)

        if recursive:
            return _rec(node)
        stack = [node]
        res = []
        while stack:
            cur = stack.pop()
            res.append(cur.value)
            if cur.right:
                stack.append(cur.right)
            if cur.left:
                stack.append(cur.left)
        return res

    def postorder(self, node: Optional[TreeNode] = None, recursive: bool = True) -> List[Any]:
        if node is None:
            node = self.root
        if node is None:
            return []

        def _rec(n: Optional[TreeNode]) -> List[Any]:
            if n is None:
                return []
            return _rec(n.left) + _rec(n.right) + [n.value]

        if recursive:
            return _rec(node)
        # iterative using two stacks
        stack1 = [node]
        stack2: List[TreeNode] = []
        while stack1:
            cur = stack1.pop()
            stack2.append(cur)
            if cur.left:
                stack1.append(cur.left)
            if cur.right:
                stack1.append(cur.right)
        return [n.value for n in reversed(stack2)]

    def level_order(self) -> List[Any]:
        if self.root is None:
            return []
        res = []
        q = deque([self.root])
        while q:
            cur = q.popleft()
            res.append(cur.value)
            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)
        return res

    # --- utilities --------------------------------------------------
    def is_balanced(self, node: Optional[TreeNode] = None) -> bool:
        if node is None:
            node = self.root

        def _height(n: Optional[TreeNode]) -> int:
            if n is None:
                return 0
            return 1 + max(_height(n.left), _height(n.right))

        def _check(n: Optional[TreeNode]) -> bool:
            if n is None:
                return True
            lh = _height(n.left)
            rh = _height(n.right)
            if abs(lh - rh) > 1:
                return False
            return _check(n.left) and _check(n.right)

        return _check(node)

    def diameter(self) -> int:
        """Return diameter (#nodes on longest path) using recursive post-order approach."""
        best = 0

        def _dfs(node: Optional[TreeNode]) -> int:
            nonlocal best
            if node is None:
                return 0
            lh = _dfs(node.left)
            rh = _dfs(node.right)
            best = max(best, lh + rh + 1)
            return 1 + max(lh, rh)

        _dfs(self.root)
        return best

    def lowest_common_ancestor(self, n1: Any, n2: Any) -> Optional[TreeNode]:
        """Return LCA node for values n1 and n2 in this binary tree (not necessarily BST)."""
        def _lca(node: Optional[TreeNode]) -> Optional[TreeNode]:
            if node is None:
                return None
            if node.value == n1 or node.value == n2:
                return node
            left = _lca(node.left)
            right = _lca(node.right)
            if left and right:
                return node
            return left if left else right

        return _lca(self.root)

    def max_value(self) -> Any:
        vals = self.level_order()
        if not vals:
            raise ValueError("empty tree")
        return max(vals)

    def min_value(self) -> Any:
        vals = self.level_order()
        if not vals:
            raise ValueError("empty tree")
        return min(vals)

    def sum_values(self) -> Any:
        return sum(self.level_order())

    def mirror(self, in_place: bool = False) -> "BinaryTree":
        def _mirror(node: Optional[TreeNode]) -> Optional[TreeNode]:
            if node is None:
                return None
            left = _mirror(node.left)
            right = _mirror(node.right)
            node.left, node.right = right, left
            return node

        if in_place:
            _mirror(self.root)
            return self
        # produce a copy
        import copy

        copy_tree = copy.deepcopy(self)
        copy_tree.mirror(in_place=True)
        return copy_tree

    # --- advanced helpers --------------------------------------------
    def path_sum(self, target: int) -> List[List[Any]]:
        out: List[List[Any]] = []

        def _dfs(node: Optional[TreeNode], cur_sum: int, path: List[Any]):
            if node is None:
                return
            cur_sum += node.value
            path.append(node.value)
            if node.left is None and node.right is None:
                if cur_sum == target:
                    out.append(list(path))
            else:
                _dfs(node.left, cur_sum, path)
                _dfs(node.right, cur_sum, path)
            path.pop()

        _dfs(self.root, 0, [])
        return out

    def print_paths(self) -> List[List[Any]]:
        """Return all root-to-leaf paths as lists (also useful for testing)."""
        paths: List[List[Any]] = []

        def _dfs(node: Optional[TreeNode], path: List[Any]):
            if node is None:
                return
            path.append(node.value)
            if node.left is None and node.right is None:
                paths.append(list(path))
            else:
                _dfs(node.left, path)
                _dfs(node.right, path)
            path.pop()

        _dfs(self.root, [])
        return paths

    def is_symmetric(self) -> bool:
        def _is_mirror(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
            if a is None and b is None:
                return True
            if a is None or b is None:
                return False
            return a.value == b.value and _is_mirror(a.left, b.right) and _is_mirror(a.right, b.left)

        if self.root is None:
            return True
        return _is_mirror(self.root.left, self.root.right)


class BST(BinaryTree):
    def __init__(self, values: Optional[List[Any]] = None):
        super().__init__()
        if values:
            for v in values:
                self.insert_bst(v)

    def insert_bst(self, value: Any) -> None:
        if self.root is None:
            self.root = TreeNode(value)
            return
        cur = self.root
        while True:
            if value < cur.value:
                if cur.left is None:
                    cur.left = TreeNode(value)
                    return
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = TreeNode(value)
                    return
                cur = cur.right

    def search(self, value: Any) -> bool:
        cur = self.root
        while cur is not None:
            if cur.value == value:
                return True
            if value < cur.value:
                cur = cur.left
            else:
                cur = cur.right
        return False

    def min_value(self) -> Any:
        if self.root is None:
            raise ValueError("empty tree")
        cur = self.root
        while cur.left:
            cur = cur.left
        return cur.value

    def max_value(self) -> Any:
        if self.root is None:
            raise ValueError("empty tree")
        cur = self.root
        while cur.right:
            cur = cur.right
        return cur.value

    def delete(self, value: Any) -> None:
        def _delete(node: Optional[TreeNode], val: Any) -> Optional[TreeNode]:
            if node is None:
                return None
            if val < node.value:
                node.left = _delete(node.left, val)
            elif val > node.value:
                node.right = _delete(node.right, val)
            else:
                # node to delete
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                # two children: replace with inorder successor
                succ = node.right
                while succ.left:
                    succ = succ.left
                node.value = succ.value
                node.right = _delete(node.right, succ.value)
            return node

        self.root = _delete(self.root, value)

    def kth_smallest(self, k: int) -> Any:
        """Return k-th smallest value (1-indexed)."""
        stack: List[TreeNode] = []
        cur = self.root
        count = 0
        while stack or cur is not None:
            while cur is not None:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            count += 1
            if count == k:
                return cur.value
            cur = cur.right
        raise IndexError("k out of range")


__all__ = ["TreeNode", "BinaryTree", "BST"]
