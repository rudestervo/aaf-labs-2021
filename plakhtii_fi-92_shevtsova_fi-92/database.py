from table import Table


class Database:
    def __init__(self):
        self.tables = []

    def create_table(self, name):
        self.tables.append(Table(name))

    def contain(self, name):
        return any(map(lambda t: t.name == name, self.tables))

    def __getitem__(self, item):
        return [t for t in self.tables if t.name == item][0]