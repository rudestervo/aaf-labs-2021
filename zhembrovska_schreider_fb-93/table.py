from tree import *
from prettytable import PrettyTable

class Table:
    def __init__(self):
        self.table_name = None
        self.columns = None
        self.rows = {}
        self.trees = {}
        self.index = 0


    def create(self, data):
        name, columns = data[0], data[1]
        self.table_name = name
        self.columns = list(columns.keys())
        for column_name in columns.keys():
            if columns[column_name]:
                self.trees[column_name] = RedBlackTree()
        print('table was created')

    def insert(self, data):
        tname = data[0]
        row = data[1]
        if self.table_name != tname or self.table_name == None:
            print('there is no table called ', tname)
        elif(len(self.columns) != len(row)):
            print('wrong number of argumments')
        else:
            for i in range(len(row)):
                if self.columns[i] in self.trees.keys():
                    self.trees[self.columns[i]].insert(row[i], self.index)
            self.rows[self.index] = row
            self.index += 1
            print('data was inserted')

    def select(self, data):
        tname, columns, conditions, relations = data[0],data[1],data[2], data[3]
        if self.table_name != tname or self.table_name == None:
            print('there is no table called ', tname)
        else:
            if len(self.rows) != 0:
                if len(conditions) == 0:
                    self.select_zero(columns)
                else:
                    cond_index = []
                    for cond in range(len(conditions)):
                        if conditions[cond][1] == '=':
                            x = (self.trees[conditions[cond][0]].searchTree(conditions[cond][-1])).index
                            cond_index.append(x)


                    if len(conditions) == 1:
                        self.select_one(cond_index,columns)

            else: print('there is no such value in the table')

    def select_zero(self, columns):
        t = PrettyTable()
        if columns[0] == '*':
            t.field_names = self.columns
            for i in self.rows:
                t.add_row(self.rows[i])
        else:
            c, r = [], []
            for col in columns:
                c.append(col)
            t.field_names = c
            for i in self.rows.keys():
                r = []
                for col in columns:
                    ind = self.columns.index(col)
                    r.append(self.rows[i][ind])
                t.add_row(r)
        print(t)

    def select_one(self, cond_index, columns):
        t = PrettyTable()
        index = cond_index[0]
        if columns[0] == '*':
            t.field_names = self.columns
            t.add_row(self.rows[index])
        else:
            c, r = [], []
            for col in columns:
                c.append(col)
                i = self.columns.index(col)
                r.append(self.rows[index][i])
            t.field_names = c
            t.add_row(r)
        print(t)

    def delete(self, data):
        if self.table_name != data[0] or self.table_name == None:
            print('there is no table called ', data[0])
        else:
            if len(data) == 1:
                self.rows = {}
                self.columns = []
                self.trees = {}
                self.index = 0
                print('data was deleted')
            else:
                column, operator, value = data[1],data[2], data[3]
                todelete = self.trees[column].searchTree(value)
                if todelete.data == 0:
                    print('there is no such value in the table')
                else:
                    self.trees[column].delete_node(todelete.data)
                    self.rows.pop(todelete.index)
                    print('data was deleted')

    def print_table(self):
        print(self.table_name)
        t = PrettyTable()
        t.field_names = self.columns
        for i in self.rows:
            t.add_row(self.rows[i])
        print(t)
