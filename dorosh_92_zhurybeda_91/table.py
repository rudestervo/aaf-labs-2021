from tabulate import tabulate
from tree import *



class Table:
    def __init__(self):
        self.table_name = None
        self.col_name = None
        self.value = {}
        self.tree = {}
        self.index = {}

    def create(self, table_name, col_dict):
        self.table_name = table_name
        self.col_name = list(col_dict.keys())
        for name in col_dict.keys():
            if col_dict[name] == 1:
                self.tree[name] = Node((None, None))
                self.index[name] = list(col_dict.keys()).index(name)
        print(f'Table {self.table_name} has been created')

    def insert(self, value):
        if len(value) == len(self.col_name):
            length = len(self.value)
            self.value[length] = value
            if self.tree:
                for name in self.tree:
                    self.tree[name].insert((length, list(self.value.items())[length][1][self.index[name]]))
            print(f'1 row has been inserted into {self.table_name}.')
        else:
            print("insertion failed")

    def simple_select(self, col_name):
        if col_name == ['*']:
            print(tabulate(self.value.values(), headers=self.col_name, tablefmt='pretty'))
        elif set(self.col_name) >= set(col_name):
            icol = []
            for i in range(len(col_name)):
                for j in range(len(self.col_name)):
                    if self.col_name[j] == col_name[i]:
                        icol.append(j)
            value = []
            for row in self.value.values():
                temp = []
                for i in icol:
                    temp.append(row[i])
                value.append(temp)
            print(tabulate(value, headers=col_name, tablefmt='pretty'))
        else:
            print("column not exist")

    def cond_calc(self, cond):
        stack = []
        for token in cond:
            if token[1] in ["T_EQ", "T_LESS", "T_MORE", "T_MORE_EQ", "T_LESS_EQ"]:
                if stack[-1][1] == "T_VALUE" and stack[-2][1] == "T_STR":
                    value = stack.pop()[0]
                    col_name = stack.pop()[0]
                    if value in self.index.keys():
                        stack.append(index_op(self, token[1], col_name, value))
                    else:
                        stack.append(apply_arith_op_val(self, token[1], col_name, value))
                elif stack[-1][1] == "T_STR" and stack[-2][1] == "T_VALUE":
                    col_name = stack.pop()[0]
                    value = stack.pop()[0]
                    if value in self.index.keys():
                        stack.append(index_op(self, token[1], col_name, value))
                    else:
                        stack.append(apply_arith_op_val(self, token[1], col_name, value))
                elif stack[-1][1] == "T_STR" and stack[-2][1] == "T_STR":
                    col_name1 = stack.pop()[0]
                    col_name2 = stack.pop()[0]
                    stack.append(apply_arith_op_col(self, token[1], col_name1, col_name2))
            elif token[1] in ["T_OR", "T_AND"]:
                tbl1 = stack.pop()
                tbl2 = stack.pop()
                stack.append(apply_set_op(token[1], tbl1, tbl2))
            else:
                stack.append(token)
        res_table = stack.pop()
        return res_table

    def cond_select(self, col_name, cond):
        if col_name == ["*"]:
            res_table = self.cond_calc(cond)
            print(tabulate(res_table.values(), headers=self.col_name, tablefmt='pretty'))
        elif set(self.col_name) >= set(col_name):
            res_table = self.cond_calc(cond)
            icol = []
            for i in range(len(col_name)):
                for j in range(len(self.col_name)):
                    if self.col_name[j] == col_name[i]:
                        icol.append(j)
            value = []
            for row in res_table.values():
                temp = []
                for i in icol:
                    temp.append(row[i])
                value.append(temp)
            print(tabulate(value, headers=col_name, tablefmt='pretty'))
        else:
            print("column not exist")

    def delete_rows(self, cond):
        rows_ind = list(self.cond_calc(cond).keys())
        for ind in rows_ind:
            self.value.pop(ind)
        self.value = {i: v for i, v in enumerate(self.value.values())}
        if self.index:
            for name in self.tree:
                self.tree[name] = Node((None, None))
            for name in self.index:
                for ind, row in self.value.items():
                    self.tree[name].insert((ind, row[self.index[name]]))
        print(f"{len(rows_ind)} rows have been deleted from the {self.table_name} table")


def index_op(table, op, col_name, value):
    if op == 'T_OR':
        ind = table.tree[col_name].search(value)
        temp = {}
        for i in ind:
            temp[i] = table.value[i]
        return temp
    elif op == 'T_MORE':
        temp = {}
        _, _, ind = table.tree[col_name].greater(value)
        for i in ind:
            temp[i] = table.value[i]
        return temp
    elif op == 'T_MORE_EQ':
        temp = {}
        _, _, ind = table.tree[col_name].greater(value, eq=True)
        for i in ind:
            temp[i] = table.value[i]

        return temp
    elif op == 'T_LESS':
        temp = {}
        _, _, ind = table.tree[col_name].smaller(value)
        for i in ind:
            temp[i] = table.value[i]
        return temp
    elif op == 'T_LESS_EQ':
        temp = {}
        _, _, ind = table.tree[col_name].smaller(value, eq=True)
        for i in ind:
            temp[i] = table.value[i]
        return temp


def apply_arith_op_val(table, op, col_name, value):
    if op == 'T_EQ':
        temp = {}
        ind = table.col_name.index(col_name)
        for key, row in table.value.items():
            if row[ind] == value:
                temp[key] = row
        return temp
    elif op == 'T_MORE':
        temp = {}
        ind = table.col_name.index(col_name)
        for key, row in table.value.items():
            if row[ind] > value:
                temp[key] = row
        return temp
    elif op == 'T_MORE_EQ':
        temp = {}
        ind = table.col_name.index(col_name)
        for key, row in table.value.items():
            if row[ind] >= value:
                temp[key] = row
        return temp
    elif op == 'T_LESS':
        temp = {}
        ind = table.col_name.index(col_name)
        for key, row in table.value.items():
            if row[ind] < value:
                temp[key] = row
        return temp
    elif op == 'T_LESS_EQ':
        temp = {}
        ind = table.col_name.index(col_name)
        for key, row in table.value.items():
            if row[ind] <= value:
                temp[key] = row
        return temp


def apply_arith_op_col(table, op, col_name1, col_name2):
    if op == 'T_EQ':
        temp = {}
        print(col_name1, col_name2)
        ind1 = table.col_name.index(col_name1)
        ind2 = table.col_name.index(col_name2)
        for key, row in table.value.items():
            if row[ind1] == row[ind2]:
                temp[key] = row
        return temp
    elif op == 'T_MORE':
        temp = {}
        ind1 = table.col_name.index(col_name1)
        ind2 = table.col_name.index(col_name2)
        for key, row in table.value.items():
            if row[ind2] > row[ind1]:
                temp[key] = row
        return temp
    elif op == 'T_MORE_EQ':
        temp = {}
        ind1 = table.col_name.index(col_name1)
        ind2 = table.col_name.index(col_name2)
        for key, row in table.value.items():
            if row[ind2] >= row[ind1]:
                temp[key] = row
        return temp
    elif op == 'T_LESS':
        temp = {}
        ind1 = table.col_name.index(col_name1)
        ind2 = table.col_name.index(col_name2)
        for key, row in table.value.items():
            if row[ind2] < row[ind1]:
                temp[key] = row
        return temp
    elif op == 'T_LESS_EQ':
        temp = {}
        ind1 = table.col_name.index(col_name1)
        ind2 = table.col_name.index(col_name2)
        for key, row in table.value.items():
            if row[ind2] >= row[ind1]:
                temp[key] = row
        return temp


def apply_set_op(op, table1, table2):
    if op == "T_OR":
        table1.update(table2)
        res = dict(sorted(table1.items()))
        return res
    elif op == "T_AND":
        res = {}
        unique_key = list(set(table1.keys()) & set(table2.keys()))
        table1.update(table2)
        for key in unique_key:
            res[key] = table1[key]
        res = dict(sorted(res.items()))
        return res

# table = Table()
# table.create("dogs", {'s': 0, 'ff': 0, 'aaa': 0})
# table.insert(["saaaaa1", 'ff2', 'aaa1'])
# table.insert(["s2", 'ff2', 'ff2'])
# table.insert(["a", 'aaa', 'aaa1'])
# table.insert(["s3", 'f', 'aaa3'])
# table.insert(["nnn1", 'aaa1', 'aaa1'])
# table.insert(["s3", 'ff2', 'aaa3'])
# table.simple_select(["*"])
#
# table.cond_select(["*"], [('ff', "T_STR"), ('s', "T_STR"), ("<", "T_LESS")])
# table.cond_select(["*"],[('ff', "T_STR"), ('aaa', "T_STR"), (">", "T_MORE")])
# table.delete_rows([('ff', "T_STR"), ('aaa', "T_STR"), (">", "T_MORE")])
# table.cond_select(["*"],[('ff', "T_STR"), ('ff2', "T_VALUE"), ("=", "T_EQ")])
# table.simple_select(["*"])



