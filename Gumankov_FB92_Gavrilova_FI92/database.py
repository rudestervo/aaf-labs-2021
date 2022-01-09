from kdtree import KDTree


class Database:
    def create_table(self, table, list):
        for el in list:
            if el.name == table:
                print(f"Name {table} has been already used!")
                return
        tree = KDTree(table, None, None, 0, None)
        list.append(tree)
        print(f"Set {table} has been created")

    def insert(self, table, x, y, list):
        check = 0
        el0 = KDTree()
        for el in list:
            if el.name == table:
               check = 1
               el0 = el
        if check == 0:
            print(f"Set {table} does not exist!")
            return
        el0.addNode(x, y)
        print(f"Point ({x}, {y}) has been added to {table}")

    def print_tree(self, table, list):
        check = 0
        el0 = KDTree()
        for el in list:
            if el.name == table:
                check = 1
                el0 = el
        if check == 0:
            print(f"Set {table} does not exist!")
            return
        print(f"Set {table}:")
        el0.printTree(0, 0, [])


    def contains(self, table, x, y, list):
        check = 0
        el0 = KDTree()
        for el in list:
            if el.name == table:
                check = 1
                el0 = el
        if check == 0:
            print(f"Set {table} does not exist!")
            return
        if el0.contains(x,y):
            print(f"Contains in set {table} point ({x}, {y})")
        else:
            print(f"Does not contains in {table} point ({x}, {y})")
        return False

    def search(self, table, list, args):
        check = 0
        el0 = KDTree()
        for el in list:
            if el.name == table:
                check = 1
                el0 = el
        if check == 0:
            print(f"Set {table} does not exist!")
            return
        if len(args) == 0:
            self.print_tree(table, list)
            return
        if args[0] == "INSIDE":
            print(f"From set {table} inside of ({args[1]}, {args[2]}), ({args[3]},{args[4]}) :")
            el0.inside(args[1], args[2], args[3], args[4])
        if args[0] == "ABOVE_TO":
            print(f"From set {table} above y = {args[1]} :")
            el0.above(args[1])
        if args[0] == "NN":
            print(f"From set {table} NN of ({args[1]},{args[2]}) :")
            lst = [[]]
            el0.nn(args[1], args[2], lst)

            for el in lst:
                if len(el) > 1:
                    print(f"({el[0]}, {el[1]})")
