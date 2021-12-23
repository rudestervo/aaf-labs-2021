class Database:
    def create_table(self, table):
        print(f"Set {table} has been created")

    def insert(self, table, x, y):
        print(f"Point ({x}, {y}) has been added to {table}")

    def print_tree(self, table):
        print(f"Point tree of set {table}: None")

    def contains(self, table, x, y):
        print(f"Contains in {table} with point ({x}, {y})")
        return False

    def search(self, table, args):
        print(f"Search in {table} with args {args}")
