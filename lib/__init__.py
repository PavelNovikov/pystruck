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
        result = self.root.find(item)
        if result is None:
            raise ValueError
        else:
            if result.parent.left == result:
                result.parent.left = result.delete_head()
            else:
                result.parent.right = result.delete_head()

    def output(self):
        data = []
        if self.root is None:
            print("The tree is empty")
        else:
            def propagate(param):
                return param + 1

            def fun(key, value, param):
                data.append((param, key))

            self.root.preorder_traversal(fun, 0, propagate)
        for tabs, key in data:
            print(tabs * " " + str(key))







class Node:

    def __init__(self, key, value, parent=None):
        self.value = value
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent

    def insert(self, key, value):
        if key < self.key:
            if self.left is None:
                self.left = Node(key, value, self)
            else:
                self.left.insert(key, value)
        else:
            if self.right is None:
                self.right = Node(key, value, self)
            else:
                self.right.insert(key, value)

    def preorder_traversal(self, fun, param=None, propagate=lambda x: x):
        fun(self.key, self.value, param)
        if self.left is not None:
            self.left.preorder_traversal(fun, propagate(param), propagate)
        if self.right is not None:
            self.right.preorder_traversal(fun, propagate(param), propagate)

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
        if self.left is None:
            replacement = self.right
        elif self.right is None:
            replacement = self.left
        else:
            successor = self.successor()
            successor.parent.left = successor.delete_head()
            replacement = successor
        if replacement is not None:
            replacement.parent = self.parent
            replacement.left = self.left
            replacement.right = self.right
        return replacement

    def rotate_left(self):
        right = self.right
        self.right = right.left
        right.left.parent = self
        right.parent = self.parent
        self.parent = right
        right.left = self
        return right

    def rotate_right(self):
        left = self.left
        self.left = left.right
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


