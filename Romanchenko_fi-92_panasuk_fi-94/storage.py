# DB structure
import operator
class db:
    OPERATORS = {
        "<": operator.lt,
        "<=": operator.le,
        "=": operator.eq,
        "!=": operator.ne,
        ">": operator.gt,
        ">=": operator.ge
    }
    def __init__(self):
        self._tables = {}
    def __getitem__(self, name):
        return self._tables[name]
    def __setitem__(self, key, value):
        self._tables[key] = value
    @staticmethod
    def check_columns(self, columns: list, table_name) -> bool: # Check if columns are in table
        if len(columns) != len(self[table_name]._scheme.keys()):
            return False
        return True

    def create(self, table_name: str, columns: list) -> str: # Create table
        if columns:
            scheme = {}
            for i in columns:
                scheme[i] = columns[i]
            self[table_name] = table(table_name, scheme)
            return f"Table '{table_name}' has been created!"
        return "invalid columns!"

    def insert(self, table_name: str, values: list) -> str: # Insert into table
        indexator_value = values[self[table_name]._indexator]
        self[table_name][indexator_value] = {}
        if self.check_columns(self, values, table_name):
            for i in range(self[table_name].__len__()):
                self[table_name][indexator_value][list(self[table_name]._scheme.keys())[i]] = values[i]

            return f"{values} has been inserted!"
        else:
            return f"Incorrect input! Try again!"

    def select_valuer(self, value: str, index, keys: list, table_name: str, condition): # runs for printing different values
        global rows
        print('|', end='')
        if value == 'keys':                         # if runs with 'keys' argument =>
            if len(keys) == 1 and keys[0] == '*':   # check if we need to print all the keys in table
                for key in self[table_name]._scheme:
                    print(' ' + key + ' |', end='')
            else:                                   # if not all keys -> print only needed keys
                for key in keys:
                    print(' ' + key + ' |', end='')
        elif value =='data':                        # if runs with 'data' argument -> print data from list
            if len(keys) == 1 and keys[0] == '*':
                if not condition:
                    for i in self[table_name][index]:
                        print(' ', str(self[table_name][index][i]) + ' |', end='')
                    rows+=1
                else:
                    for j in condition:
                        try:
                            bool_op = condition[condition.index(j)+1]
                        except IndexError:
                            bool_op = False
                            pass
                        if j == 'and' or j == 'or':
                            pass
                        else:
                            column, oper, col_val = j    
                            oper = self.OPERATORS[oper]
                            
                            if bool_op == 'and':
                                column2,oper2,col_val2 = condition[condition.index(j)+2]
                                oper2 = self.OPERATORS[oper2]
                                if oper(str(self[table_name][index][column]), col_val) and oper2(str(self[table_name][index][column2], col_val2)):
                                    for j in self[table_name][index]:
                                        print(' ', str(self[table_name][index][j]) + ' |', end='')
                                    rows+=1
                                    break
                            elif bool_op == 'or':
                                column2,oper2,col_val2 = condition[condition.index(j)+2]
                                oper2 = self.OPERATORS[oper2]
                                if oper(str(self[table_name][index][column]), col_val) or oper2(str(self[table_name][index][column2]), col_val2):
                                    for j in self[table_name][index]:
                                        print(' ', str(self[table_name][index][j]) + ' |', end='')
                                    rows+=1
                                    break
                            elif not bool_op:
                                if oper(str(self[table_name][index][column]), col_val):
                                    for j in self[table_name][index]:
                                        print(' ', str(self[table_name][index][j]) + ' |', end='')
                                    rows+=1
                                    break
            else:
                if not condition:
                    print(' '+ str(index) +' |', end='')
                    for j in keys:
                        print(' ', str(self[table_name][index][j]) + ' |', end='')
                    rows+=1
                else:
                    for j in condition:
                        try:
                            bool_op = condition[condition.index(j)+1]
                        except IndexError:
                            bool_op = False
                            pass
                        if j == 'and' or j == 'or':
                            pass
                        else:
                            column, oper, col_val = j    
                            oper = self.OPERATORS[oper]
                            
                            if bool_op == 'and':
                                column2,oper2,col_val2 = condition[condition.index(j)+2]
                                oper2 = self.OPERATORS[oper2]
                                if oper(str(self[table_name][index][column]), col_val) and oper2(str(self[table_name][index][column2], col_val2)):
                                    print(' '+ str(index) +' |', end='')
                                    for j in keys:
                                        print(' ', str(self[table_name][index][j]) + ' |', end='')
                                    rows+=1
                                    break
                            elif bool_op == 'or':
                                column2,oper2,col_val2 = condition[condition.index(j)+2]
                                oper2 = self.OPERATORS[oper2]
                                if oper(str(self[table_name][index][column]), col_val) or oper2(str(self[table_name][index][column2]), col_val2):
                                    print(' '+ str(index) +' |', end='')
                                    for j in keys:
                                        print(' ', str(self[table_name][index][j]) + ' |', end='')
                                    rows+=1
                                    break
                            elif not bool_op:
                                if oper(str(self[table_name][index][column]), col_val):
                                    print(' '+ str(index) +' |', end='')
                                    for j in keys:
                                        print(' ', str(self[table_name][index][j]) + ' |', end='')
                                    rows+=1
                                    break
                        
            print()

    def select_liner(self, keys, table_name: str):
        if len(keys) == 1 and keys[0] == '*':
            for key in self[table_name]._scheme:
                string = '+'+'-'*(2+len(key))
                print(string, end='')
        else:
            string = '+'+'-'*(2+len(str(list(self[table_name]._scheme.keys())[0])))
            print(string, end='')
            for key in keys:
                string = '+'+'-'*(2+len(key))
                print(string, end='')

    def select(self, table_name: str, columns: list, condition: list,) -> str: # Return columns selected
        global rows
        rows = 0
        if len(columns) == 1 and columns[0] == "*":
            self.select_liner('*', table_name)
            print('+')
            self.select_valuer('keys', 0,'*' ,table_name, condition)
            print()
            self.select_liner('*', table_name)
            print()
            for i in self[table_name]._data:
                self.select_valuer('data', i, '*', table_name, condition)
                self.select_liner('*', table_name)
                print('+')

            print()
        else:
            self.select_liner(columns, table_name)
            print('+')
            print('| '+ str(list(self[table_name]._scheme.keys())[0])+ ' ', end='')
            self.select_valuer('keys', 0, columns, table_name, condition)
            print()
            self.select_liner(columns, table_name)
            print('+')

            for i in self[table_name]._data:
                self.select_valuer('data', i, columns, table_name, condition)
                self.select_liner(columns, table_name)
                print('+')

            print()
        return f"{rows} row(s) has been selected from {table_name} with {condition}!"

    def delete(self, table_name: str, condition: list) -> str: # Delete data from table
        rows_to_delete = []
        if not condition:
            for i in self[table_name]._data:
                rows_to_delete.append(i)
        else:
            for j in condition:
                try:
                    bool_op = condition[condition.index(j)+1]
                except IndexError:
                    bool_op = False
                    pass
                if j == 'and' or j == 'or':
                    pass
                else:
                    column, oper, col_val = j    
                    oper = self.OPERATORS[oper]
                    for index in self[table_name]._data:
                        if bool_op == 'and':
                            column2,oper2,col_val2 = condition[condition.index(j)+2]
                            oper2 = self.OPERATORS[oper2]
                            if oper(str(self[table_name][index][column]), col_val) and oper2(str(self[table_name][index][column2], col_val2)):
                                rows_to_delete.append(index)
                        elif bool_op == 'or':
                            column2,oper2,col_val2 = condition[condition.index(j)+2]
                            oper2 = self.OPERATORS[oper2]
                            if oper(str(self[table_name][index][column]), col_val) or oper2(str(self[table_name][index][column2]), col_val2):
                                rows_to_delete.append(index)
                        elif not bool_op:
                            if oper(str(self[table_name][index][column]), col_val):
                                rows_to_delete.append(index)
        for i in list(set(rows_to_delete)):
            self[table_name]._data.pop(i)
        return f"From {table_name} {len(list(set(rows_to_delete)))} row(s) has been deleted from {table_name}!"

if __name__ == "__main__":
    db = db()

class table:
    def __init__(self, table_name, scheme):
        self._table_name = table_name
        self._indexator = list(scheme.values()).index(True)
        self._scheme = scheme
        self._data = {}


    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value
    def __len__(self):
        return len(self._scheme.keys())
    def dict_len(self):
        return len(self._data)