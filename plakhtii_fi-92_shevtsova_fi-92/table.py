from R_Tree_To_compile.build.R_Tree import R_Tree, Rect


class Table:
    def __init__(self, name):
        self.name = name
        self.tree = R_Tree()

    def insert(self, x, y):
        self.tree.insert(Rect(x, y, x, y))
        root = str(self.tree.get_root())

    def search(self, ltx, lty, rbx, rby):
        for n in self.tree.search(Rect(ltx, lty, rbx, rby)):
            print(n)

    def is_contain(self, x, y):
        return self.tree.is_contain(Rect(x, y, x, y))

    def print_tree(self):
        self.tree.print_tree()

    def left_of(self, x):
        root = self.tree.get_root()
        ltx = root.get_ltx()
        lty = root.get_lty()
        rby = root.get_rby()
        if ltx >= x:
            print("Wrong input: ltx of root >= x!")
            return

        for n in self.tree.search(Rect(ltx, lty, x, rby)):
            print(n)

    def nn(self, x, y):
        for n in self.tree.nn(Rect(x, y, x, y)):
            print(n)

    def get_all(self):
        for n in self.tree.search(self.tree.get_root()):
            print(n)
