class Tree:

    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
        else:
            self.root.insert(key, value)

    def __getattr__(self, item):
        result = self.root.find(item) is not None
        if result is None:
            raise ValueError
        else:
            return result

    def __contains__(self, item):
        return self.root.find(item) is not None

    def __delitem__(self, item):
        if self.root is None:
            raise ValueError
        else:
            result = self.root.find(item)
            if result is None:
                raise ValueError
            else:
                if result.parent is None:
                    self.root = result.delete_head()
                elif result.parent.left == result:
                    result.parent.left = result.delete_head()
                else:
                    result.parent.right = result.delete_head()

    def check_consistency(self):
        if self.root is not None:
            self.root.check_consistency()

    def output(self):
        data = []
        if self.root is None:
            print("The tree is empty")
        else:
            def propagate(param):
                return param + 1

            def fun(node, param):
                data.append((param, node.key))
                print(param * " " + str(node.key))

            self.root.preorder_traversal(fun, 0, propagate)

    def get_ordering(self, return_values=False):
        data = []
        if self.root is None:
            return []
        else:

            def fun_with_values(node, param):
                data.append((node.key, node.value))

            def fun_without_values(node, param):
                data.append(node.key)

            if return_values:
                self.root.inorder_traversal(fun_with_values)
            else:
                self.root.inorder_traversal(fun_without_values)
            return data


def replace_node(old_node, new_node):
    assert old_node is not None
    assert new_node is not None
    new_node.parent = old_node.parent if old_node.parent != new_node else None
    if old_node.left != new_node:
        new_node.left = old_node.left
        if old_node.left is not None:
            old_node.left.parent = new_node
    else:
        new_node.left = None
    if old_node.right != new_node:
        new_node.right = old_node.right
        if old_node.right is not None:
            old_node.right.parent = new_node
    else:
        new_node.right = None
    if old_node.parent is not None:
        if old_node.parent.left == old_node:
            old_node.parent.left = new_node
        else:
            old_node.parent.right = new_node


def replace_node_with_subtree(old_node, subtree_root):
    assert old_node is not None
    assert subtree_root is not None
    subtree_root.parent = old_node.parent if old_node.parent != subtree_root else None
    if old_node.parent is not None:
        if old_node.parent.left == old_node:
            old_node.parent.left = subtree_root
        else:
            old_node.parent.right = subtree_root
    if old_node.left is not None and old_node.left != subtree_root:
        if subtree_root.left is None:
            subtree_root.left = old_node.left
            old_node.left.parent = subtree_root
        else:
            raise ValueError
    if old_node.right is not None and old_node.right != subtree_root:
        if subtree_root.right is None:
            subtree_root.right = old_node.right
            old_node.right.parent = subtree_root
        else:
            raise ValueError


class Node:

    def __init__(self, key, value, parent=None):
        self.value = value
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent

    def check_consistency(self):
        if self.left is not None:
            assert self.left.parent == self

            self.left.check_consistency()
        if self.right is not None:
            assert self.right.parent == self
            self.right.check_consistency()

    def insert(self, key, value):
        if key < self.key:
            if self.left is None:
                self.left = Node(key, value, self)
            else:
                self.left.insert(key, value)
        elif key > self.key:
            if self.right is None:
                self.right = Node(key, value, self)
            else:
                self.right.insert(key, value)
        else:
            raise ValueError

    def is_leaf(self):
        return self.left is None and self.right is None

    def preorder_traversal(self, fun, param=None, propagate=lambda x: x):
        fun(self, param)
        if self.left is not None:
            self.left.preorder_traversal(fun, propagate(param), propagate)
        if self.right is not None:
            self.right.preorder_traversal(fun, propagate(param), propagate)

    def inorder_traversal(self, fun, param=None, propagate=lambda x: x):
        if self.left is not None:
            self.left.inorder_traversal(fun, propagate(param), propagate)
        fun(self, param)
        if self.right is not None:
            self.right.inorder_traversal(fun, propagate(param), propagate)

    def remove(self):
        if self.parent is not None:
            if self.parent.left == self:
                self.parent.left = None
            else:
                self.parent.right = None

    def find(self, key):
        if self.key == key:
            return self
        elif key < self.key:
            if self.left is None:
                return None
            else:
                return self.left.find(key)
        else:
            if self.right is None:
                return None
            else:
                return self.right.find(key)

    def delete_head(self):
        if self.left is None or self.right is None:
            if self.left is None:
                replacement = self.right
            else:
                replacement = self.left
            if replacement is None:
                self.remove()
            else:
                replace_node_with_subtree(self, replacement)
        else:
            successor = self.successor()
            if successor.parent != self:
                new_child = successor.delete_head()
                if new_child is not None:
                    new_child.parent = successor.parent

                replace_node(self, successor)
            else:
                replace_node_with_subtree(self, successor)
            replacement = successor
        return replacement

    def rotate_left(self):
        right = self.right
        self.right = right.left
        if right.left is not None:
            right.left.parent = self
        right.parent = self.parent
        self.parent = right
        right.left = self
        return right

    def rotate_right(self):
        left = self.left
        self.left = left.right
        if left.right is not None:
            left.right.parent = self
        left.parent = self.parent
        self.parent = left
        left.right = self
        return left

    def smallest(self):
        if self.left is None:
            return self
        else:
            return self.left.smallest()

    def greatest(self):
        if self.right is None:
            return self
        else:
            return self.right.greatest()

    def successor(self):
        if self.right is not None:
            return self.right.smallest()
        else:
            previous = self
            candidate = self.parent
            while candidate is not None and candidate.left != previous:
                previous = candidate
                candidate = candidate.parent
            return candidate


class AVLTree(Tree):

    def check_balance_invariant(self):
        if self.root is not None:
            self.root.check_balance_invariant()

    def insert(self, key, value):
        if self.root is None:
            self.root = AVLNode(key, value)
        else:
            self.root = self.root.insert(key, value)

    def output(self):
        data = []
        if self.root is None:
            print("The tree is empty")
        else:
            def propagate(param):
                return param + 1

            def fun(node, param):
                print(param * " " + "%d[%d]" % (node.key, node.height))

            self.root.preorder_traversal(fun, 0, propagate)

    def __delitem__(self, item):
        if self.root is None:
            raise ValueError
        else:
            self.root = self.root.delete(item)


class AVLNode(Node):

    def check_balance_invariant(self):
        left_height = 0
        right_height = 0
        if self.left is not None:
            left_height = self.left.check_balance_invariant()
        if self.right is not None:
            right_height = self.right.check_balance_invariant()
        assert abs(left_height - right_height) <= 1
        return max(left_height, right_height) + 1

    def __init__(self, key, value, parent=None):
        Node.__init__(self, key, value, parent)
        self.balance_factor = 0
        self.height = 1

    def left_height(self):
        if self.left is None:
            return 0
        else:
            return self.left.height

    def right_height(self):
        if self.right is None:
            return 0
        else:
            return self.right.height

    def recompute_height_and_balance(self):
        self.height = 1 + max(self.left_height(), self.right_height())
        self.balance_factor = self.right_height() - self.left_height()

    def rotate_left(self):
        result = super(AVLNode, self).rotate_left()
        result.left.recompute_height_and_balance()
        result.recompute_height_and_balance()
        return result

    def rotate_right(self):
        result = super(AVLNode, self).rotate_right()
        result.right.recompute_height_and_balance()
        result.recompute_height_and_balance()
        return result

    def correct_left_overbalance(self):
        if self.left.balance_factor == 1:
            self.left = self.left.rotate_left()
        return self.rotate_right()

    def correct_right_overbalance(self):
        if self.right.balance_factor == -1:
            self.right = self.right.rotate_right()
        result = self.rotate_left()
        return result

    def insert(self, key, value):
        if key < self.key:
            if self.left is None:
                self.left = AVLNode(key, value, self)
                if self.balance_factor == 0:
                    self.balance_factor = -1
                else:
                    self.balance_factor = 0
                self.height = 2
                return self
            else:
                self.left = self.left.insert(key, value)
                self.balance_factor = self.right_height() - self.left_height()
                if self.balance_factor < -1:
                    return self.correct_left_overbalance()
                else:
                    self.height = 1 + max(self.left_height(), self.right_height())
                    return self
        elif key > self.key:
            if self.right is None:
                self.right = AVLNode(key, value, self)
                if self.balance_factor == 0:
                    self.balance_factor = 1
                else:
                    self.balance_factor = 0
                self.height = 2
                return self
            else:
                self.right = self.right.insert(key, value)
                self.balance_factor = self.right_height() - self.left_height()
                if self.balance_factor > 1:
                    return self.correct_right_overbalance()
                else:
                    self.height = 1 + max(self.left_height(), self.right_height())
                    return self
        else:
            raise ValueError

    def find(self, key):
        if self.key == key:
            return self
        elif key < self.key:
            if self.left is None:
                return None
            else:
                return self.left.find(key)
        else:
            if self.right is None:
                return None
            else:
                return self.right.find(key)

    def delete(self, key):
        if self.key == key:
            return self.delete_head()
        elif key < self.key:
            if self.left is None:
                raise ValueError
            else:
                self.left = self.left.delete(key)
                if self.left is not None:
                    self.left.parent = self
                self.recompute_height_and_balance()
        else:
            if self.right is None:
                raise ValueError
            else:
                self.right = self.right.delete(key)
                if self.right is not None:
                    self.right.parent = self
                self.recompute_height_and_balance()
        if self.balance_factor > 1:
            return self.correct_right_overbalance()
        elif self.balance_factor < -1:
            return self.correct_left_overbalance()
        else:
            return self

    def delete_head(self):

        if self.right is None:
            result = self.left
            if result is not None:
                result.parent = self.parent
            return result
        else:
            result = self.right.smallest()
            result.parent = self.parent
            result.right = self.right.delete(result.key)
            result.left = self.left
            if result.left is not None:
                result.left.parent = result
            if result.right is not None:
                result.right.parent = result

            result.recompute_height_and_balance()
            if result.balance_factor > 1:
                result = result.correct_right_overbalance()
            elif result.balance_factor < -1:
                result = result.correct_left_overbalance()

            return result


