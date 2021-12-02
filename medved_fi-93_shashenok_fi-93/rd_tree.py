class Node:
    """
    Class Node
    """

    def __init__(self, value: set):
        self.left = None
        self.data = value
        self.right = None


class RDTree:
    root = None

    def set_compare(self, set1, set2):
        return len(set1.intersection(set2))

    def createNode(self, data):
        return Node(data)

    def is_full_node(self, node):
        if node.left and node.right:
            return 0
        if node.left:
            return -1
        if node.right:
            return 1
        return None

    def initial_insert(self, data):
        self.root = self.createNode(data)
        return self.root

    def insert(self, node, data: set):
        """
        Insert function will insert a node into tree.
        Duplicate keys are not allowed.
        """
        # if not self.root:
        #     return self.initial_insert(data)

        # if tree is empty , return a root node
        if not node:
            return self.createNode(data)
        self.root = node

        if not self.is_leaf(node):
            if self.set_compare(node.left.data, data) > self.set_compare(node.right.data, data):
                node.data = node.data.union(data)
                self.insert(node.left, data)
                    # temp = self.createNode(node.left.data.union(data))
                    # temp.left = node.left
                    # temp.right = self.createNode(data)
                    # new_root.left = temp
                    # new_root.right = node.right
            else:
                node.data = node.data.union(data)
                self.insert(node.right, data)
                    # new_root.left = node.left
        else:
            node.left = self.createNode(node.data)
            node.data = node.data.union(data)
            node.right = self.createNode(data)
        return node

    def is_leaf(self, node: Node) -> bool:
        if node.left or node.right:
            return False
        return True

    def get_leaf_nodes(self, start_node):
        leaves = []

        def _get_leaf_nodes(node):
            if node is not None:
                if not (node.left or node.right):
                    leaves.append(node.data)
                _get_leaf_nodes(node.left)
                _get_leaf_nodes(node.right)

        _get_leaf_nodes(start_node)
        return leaves

    def contains(self, node: Node, data: set) -> bool:
        res = False
        if node.data == data and self.is_leaf(node):
            return True
        if data.issubset(node.data):
            res = self.contains(node.left, data)
            if res:
                return res
            res = self.contains(node.right, data)
            if res:
                return res
        return res

    def search_contains(self, node: Node, data: set):
        res = []
        def _search_contains(node, data):
            if data.issubset(node.data):
                if self.is_leaf(node):
                    return node.data
                tmp = _search_contains(node.left, data)
                if tmp:
                    res.append(tmp)
                tmp = _search_contains(node.right, data)
                if tmp:
                    res.append(tmp)

        _search_contains(node, data)
        return res

    def search_inrersects(self, node: Node, data: set) ->list:
        res = []

        def _search_intersects(node: Node, data: set) -> set:
            if data.intersection(node.data) != set():
                if self.is_leaf(node):
                    return node.data
                tmp = _search_intersects(node.left, data)
                if tmp:
                    res.append(tmp)
                tmp = _search_intersects(node.right, data)
                if tmp:
                    res.append(tmp)
        _search_intersects(node, data)
        return res

    def search_contained_by(self, node: Node, data: set) -> list:
        res = []
        intersects = self.search_inrersects(node, data)
        for st in intersects:
            if st.issubset(data):
                res.append(st)
        return res

    def print_tree(self, node, level=0):
        if node:
            if level != 0:
                print('|   ' * level + 'L_', node.data)
            else:
                print(' ' * 4 * level + 'L_', node.data)
            self.print_tree(node.left, level + 1)
            self.print_tree(node.right, level + 1)

    def convert_tree_to_dict(self, node):
        tree = {}
        def _convert_tree_to_dict(node):
            if self.is_leaf(node):
                return tree
            tree[str(node.data)] = {str(node.left.data), str(node.right.data)}
            _convert_tree_to_dict(node.left)
            _convert_tree_to_dict(node.right)
        _convert_tree_to_dict(node)
        return tree

    def print_dependency_tree(self, tree, root, *, indent=0, ctx=None):
        # """
        # >>> tree = {"a": {"b", "c"},
        # >>>         "b": {"d"},
        # >>>         "c": {"b", "d"}}
        # >>> print_dependency_tree(tree, "a")
        # a
        # ├─b
        # │ └─d
        # └─c
        #   ├─b
        #   │ └─d
        #   └─d
        # """
        depth, branches, seen = ctx or (0, [], set())
        if depth == 0:
            print(" " * indent + root)
        if root not in tree:
            return
        branches += [None]
        seen |= {root}
        children = set(tree[root]) - seen
        more = len(children)
        for child in sorted(children):
            more -= 1
            branches[depth] = ("├" if more else "└") + "─"
            if child in seen:
                continue
            print(" " * indent + "".join(branches) + child)
            if child in tree:
                branches[depth] = ("│" if more else " ") + " "
                ctx = depth + 1, branches.copy(), seen.copy()
                self.print_dependency_tree(tree, child, indent=indent, ctx=ctx)

def main():
    tree = RDTree()
    tree.insert(tree.root, {1, 3, 4})
    tree.insert(tree.root, {1, 3, 2})
    tree.print_tree(tree.root)


if __name__ == "__main__":
    main()
