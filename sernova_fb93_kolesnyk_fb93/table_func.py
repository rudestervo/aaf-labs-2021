### all for tables like objects
from copy import deepcopy
from prettytable import PrettyTable
from BSTree import *

tables_arr = []

class Column:
    def __init__(self, name, indexed):
        self.name = name
        self.indexed = indexed
        if self.indexed == 1:
            self.index_tree = RedBlackTree()
        elif self.indexed == 0:
            self.value_arr = []
        

class Row:
    def __init__(self, val_arr, is_null = 0):
        self.values = []
        self.values.clear()
        self.is_null = is_null
        for i in range (0, len(val_arr)):
            self.values.append(val_arr[i])
    

class Table:
    columns = []
    rows = []
    tablename = ''
    
    def __init__(self, name, columns_arr, index_arr):
        self.columns.clear()
        self.rows.clear()
        self.tablename = name
        self.column_arr = columns_arr
        self.rows.clear()
        self.columns.clear()
        for i in range (0, len(columns_arr)):
            index_check = 0
            if i in index_arr:
                index_check = 1
            self.columns.append(Column(columns_arr[i], index_check))
     #   tables_arr.append(self)
    def get_name(self):
        return self.tablename
    def check_repeat(self, value, i):
        for j in range (0, len(self.rows)):
            row = self.rows[j]
            if row.values[i] == value:
                return 1
        return 0

    def show_rows(self):
        for i in range(0, len(self.rows)):
            print(str(i+1)+ '. ' + str(self.rows[i].values))

    def show_table(self):
        mytable = PrettyTable()
        col_names = []
        for i in range (0, len(self.columns)):
            col_names.append(self.columns[i].name)
        mytable.field_names = col_names
        for i in range(0, len(self.rows)):
            if self.rows[i].is_null == 0:
                mytable.add_row(self.rows[i].values)
        print(mytable)
    #    print('Table '+ self.tablename + ' with columns ' + str(col_names))
      #  self.show_rows()
    
    def insertion(self, row_arr):
        index = len(self.rows)

        if len(row_arr)!=len(self.columns):
            raise Exception('invalid length!')
        else: 
           
            row_values = []
           
            for i in range (0, len(self.columns)):
                if self.columns[i].indexed == 0:
                    self.columns[i].value_arr.append(row_arr[i])
                elif self.columns[i].indexed == 1:
                    self.columns[i].index_tree.insert(row_arr[i], index)
                row_values.append(row_arr[i])
            self.rows.append(Row(row_values))


def select_in_table(fields, tables, where_statement, order_statement):

    selected_columns = []
    selected_rows = []
    sel_ind = []
    type_of_selection =''
    select_indexes = []
    for i in tables_arr:
        if i.tablename == tables.text:
            curr_tab = deepcopy(i)
            continue
    if type(fields)==str:
        type_of_selection = 'all'                                                   # SELECT * FROM

        for i in range(0, len(curr_tab.columns)):
            selected_columns.append(curr_tab.columns[i].name)
            sel_ind.append(curr_tab.columns[i].indexed)

        if where_statement == 0 and order_statement == 0:                           # реально просто SELECT * FROM
            selected_rows = curr_tab.rows.copy()


        if where_statement == 0 and type(order_statement) != bool:              # SELECT * FROM ORDER_BY
            col_for_cond = order_statement[0].text
            if order_statement[1].text == 'ASC':
                asc = 1
            else: asc = 0
            for col in curr_tab.columns:
                if col.name == col_for_cond:
                    column = col
                    col_id = curr_tab.columns.index(col)

            if column.indexed == 1:                                                        # индексированый ORDER_BY
                indexes = column.index_tree.inorder()
                if asc == 1:
                    for index in indexes:
                        selected_rows.append(curr_tab.rows[index])
                else:
                    for index in indexes[::-1]:
                        selected_rows.append(curr_tab.rows[index])
            else:                                                                               #  неиндексированый ORDER_BY
                selected_rows = sorted(curr_tab.rows, key=lambda Row: Row.values[col_id])
                if asc == 0:
                    selected_rows.reverse()


    else:                                                                                     ##### SELECT что-то FROM
        type_of_selection = 'with_selection'
        col_ind = []

        for i in range(0, len(curr_tab.columns)):
            if curr_tab.columns[i].name in fields:
                selected_columns.append(curr_tab.columns[i].name)
                sel_ind.append(curr_tab.columns[i].indexed)

                col_ind.append(i)
        for i in range(0, len(curr_tab.rows)):

            if curr_tab.rows[i].is_null != 1:
                row_val = []
                for j in col_ind:
                    row_val.append(curr_tab.rows[i].values[j])
                selected_rows.append(row_val)
                select_indexes.append(i)


    if type(where_statement) != bool:                                       # SELECT smth FROM smwh WHERE a == b

        col_for_cond = where_statement[0].text
        equel_cond = where_statement[1].text
        key = where_statement[2].text.replace('"', '')


        # where_column = Column(0, 0)
        # col_id = 0
        #только для бесконечного цикла

        for i in range(0, len(curr_tab.columns)):
            if curr_tab.columns[i].name == col_for_cond:
                where_column = deepcopy(curr_tab.columns[i])
                col_id = i

        # index = 0
        where_indexes = []
        ind_check = 0
        if where_column.indexed == 1:                                               # работа с индексами

            while ind_check == 0:
                index = where_column.index_tree.searchTree(key).index

                if index != -1:
                    where_indexes.append(index)
                    where_column.index_tree.delete_node(key)
                else:
                    ind_check = 1


        else:                                                                   #без индексов

            for i in range(0, len(curr_tab.rows)):
                if curr_tab.rows[i].values[col_id] == key:
                    where_indexes.append(i)
                    if type_of_selection == 'all':
                        selected_rows.append(curr_tab.rows[i])


        if type_of_selection == 'all':              #SELECT * FROM smwh WHERE ....
            selected_rows.clear()
            if equel_cond == "==":
                for index in where_indexes:
                    selected_rows.append(curr_tab.rows[index])
            else:                                           #SELECT SMTH FROM smwh WHERE ....
                for i in range(0, len(curr_tab.rows)):
                    if i not in where_indexes:
                        selected_rows.append(curr_tab.rows[i])



    sel_tab = Table('selection', selected_columns, sel_ind)                       ### новая табличка для вывода и махинаций


    if type_of_selection == 'all':
        for sel_row in selected_rows:
            sel_tab.insertion(sel_row.values)               #зполняем

        if type(order_statement) != bool:                   # корректирукм с ORDER_BY
            order_col_name = order_statement[0].text
            if order_statement[1].text == 'ASC':
                asc = 1
            else:
                asc = 0

            for col in sel_tab.columns:
                if col.name == order_col_name:
                    order_col = col



            if order_col.indexed == 1:
                selected_rows = []
                indexes = order_col.index_tree.inorder()

                if asc == 1:
                    for index in indexes:
                        selected_rows.append(deepcopy(sel_tab.rows[index]))
                else:
                    for index in indexes[::-1]:
                        selected_rows.append(deepcopy(sel_tab.rows[index]))
                sel_tab.rows.clear()
                for sel_row in selected_rows:
                    sel_tab.insertion(sel_row.values)

    if type_of_selection == 'with_selection':
        if type(where_statement) == bool:
            for sel_row in selected_rows:
                sel_tab.insertion(sel_row)

        elif type(where_statement) != bool:             # SELECT * WHERE
            for i in range (0, len(select_indexes)):

                if where_statement[1].text == '==':
                    if select_indexes[i] in where_indexes:
                        sel_tab.insertion(selected_rows[i])
                elif where_statement[1].text == '!=':
                    if (select_indexes[i] in where_indexes) == False:
                        sel_tab.insertion(selected_rows[i])

        if type(order_statement) != bool:                               #SELECT * (WHERE) ORDER_BY
            col_for_cond = order_statement[0].text
            if order_statement[1].text == 'ASC':
                asc = 1
            else:
                asc = 0
            for col in sel_tab.columns:
                if col.name == col_for_cond:
                    column = deepcopy(col)
                    col_id = sel_tab.columns.index(col)

            if column.indexed == 1:

                indexes = column.index_tree.inorder()
                if asc == 1:
                    for index in indexes:
                        selected_rows.append(sel_tab.rows[index])
                else:
                    for index in indexes[::-1]:
                        selected_rows.append(sel_tab.rows[index])
            else:

                selected_rows = sorted(sel_tab.rows, key=lambda Row: Row.values[col_id])

                if asc == 0:
                    selected_rows.reverse()

                sel_tab.rows.clear()
                sel_tab.rows = selected_rows

    col_names = []

    for i in range(0, len(sel_tab.columns)):
        col_names.append(sel_tab.columns[i].name)
    print('SELECTION RESULT:')
    sel_tab.show_table()
 #   tables_arr.pop(len(tables_arr)-1)





def del_func(table,cond):
    for i in tables_arr:
        if i.tablename == table.text:
            curr_tab = i
    if cond == "ALL":
        print(str(len(curr_tab.rows))  + ' rows have been deleted from the ' + curr_tab.tablename)
        i = tables_arr.index(curr_tab)
        tables_arr.pop(i)

      #  print(len(tables_arr))
        return
    cond_arr = []
    for i in range(0, len(cond)):
        cond_arr.append(cond[i].text)
     #   print(cond[i].text)
    if len(cond_arr) >1:
        col_name = cond_arr[0]
        condition = cond_arr[1]
        key = cond_arr[2].replace('"', '')
        for col in curr_tab.columns:
            if col.name == col_name:
                column = col

        # index = 0
        indexes = []
        ind_check = 0
        if column.indexed == 1:

            while ind_check == 0:
                index = column.index_tree.searchTree(key).index

                if index != -1:
                    indexes.append(index)
                    column.index_tree.delete_node(key)
                else:
                    ind_check = 1


        else:
            while ind_check == 0:
                if key in column.value_arr:

                    index = column.value_arr.index(key)
                    column.value_arr.pop(index)
                    column.value_arr.insert(index, '0')
                    indexes.append(index)

                else:
                    ind_check = 1

        if condition == '==':
            for index in indexes:
                curr_tab.rows.pop(index)
                curr_tab.rows.insert(index, Row([0] * len(curr_tab.columns), 1))


        if condition == '!=':
            for i in range(0, len(curr_tab.rows)):
                if (i in indexes) == 0:
                    curr_tab.rows.pop(i)
                    curr_tab.rows.insert(index, Row([0] * len(curr_tab.columns), 1))
        print(str(len(indexes))  + ' rows have been deleted from the ' + curr_tab.tablename)




