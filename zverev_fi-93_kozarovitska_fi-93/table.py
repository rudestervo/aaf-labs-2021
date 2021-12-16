import tree
import parsing


def delete(column_names, columns, right_rows):
    indexes_of_right_col = []
    for i in range(len(column_names)):
        indexes_of_right_col.append(i)
    for j in reversed(right_rows):
        for i in reversed(indexes_of_right_col):
            if columns[i]:
                columns[i].pop(j)

def check_condition(columns1,columns2,numb_col1,numb_col2,symbol, number_of_row):
    if numb_col1==None or numb_col2==None:
        return 'yes'
    else:
        if len(columns1)>number_of_row and len(columns2)>number_of_row:
            if symbol== '=':
                if columns1[numb_col1][number_of_row]==columns2[numb_col2][number_of_row]:
                    return ('yes')
            if symbol== '>':
                if columns1[numb_col1][number_of_row]>columns2[numb_col2][number_of_row]:
                    return ('yes')
            if symbol== '<':
                if columns1[numb_col1][number_of_row]<columns2[numb_col2][number_of_row]:
                    return ('yes')
            if symbol== '>=':
                if columns1[numb_col1][number_of_row]>=columns2[numb_col2][number_of_row]:
                    return ('yes')
            if symbol== '<=':
                if columns1[numb_col1][number_of_row]<=columns2[numb_col2][number_of_row]:
                    return ('yes')


def check_condition_value(value_in_table, value,symbol):
    if symbol == '=':
        if value_in_table == value:
            return ('yes')
    if symbol == '>':
        if value_in_table > value:
            return ('yes')
    if symbol == '<':
        if value_in_table < value:
            return ('yes')
    if symbol == '>=':
        if value_in_table >= value:
            return ('yes')
    if symbol == '<=':
        if value_in_table <= value:
            return ('yes')
    if symbol == '!=':
        if value_in_table != value:
            return ('yes')
def get_real_right_rows(right_rows, elem):
    right_arr_rows = []
    for j in right_rows:
        for k in range(len(elem.number)):
            if j == elem.number[k]:
                right_arr_rows.append(k)
    return right_arr_rows
def full_join_with_indexed(t1,  col_from_table1,col_from_table2,  columns1, columns2,number1,number2, elem1, elem2, rows_from_t2_without_pair):
    rows_from_t2_without_pair = []
    new_table = []
    for j in range(len(columns2[0])):
        rows_from_t2_without_pair.append(0)
    for j in range(len(columns1[0])):
        row_from_t1_found = 0
        right_rows1 = elem2.find_in_tree(t1, '=', columns1[number1][j])
        right_rows=get_real_right_rows(right_rows1,elem2)
        if right_rows:
            for numb in right_rows:
                rows_from_t2_without_pair[numb] = 1
                table_row = []

                for k in col_from_table1:
                    table_row.append(columns1[k][j])
                for k in col_from_table2:
                    if number2 in col_from_table2:
                        table_row.append(columns2[k][numb])
                    else:
                        if k != number2:
                            table_row.append(columns2[k][numb])

                new_table.append(table_row)
                row_from_t1_found = 1
        if row_from_t1_found == 0:
            table_row = []
            for k in col_from_table1:
                table_row.append(columns1[k][j])
            for k in col_from_table2:
                # if number2 in col_from_table2:
                table_row.append(' ')
            new_table.append(table_row)
    for a in range(len(rows_from_t2_without_pair)):

        if rows_from_t2_without_pair[a] == 0:
            table_row = []
            for k in col_from_table1:
                # if number2 in col_from_table2:
                table_row.append(' ')
            for k in col_from_table2:
                table_row.append(columns2[k][a])
            new_table.append(table_row)
    return  new_table

def  full_join_without_indexed(col_from_table1,col_from_table2,  columns1, columns2,number1,number2, rows_from_t2_without_pair):
    new_table=[]
    for j in range(len(columns1[0])):
        row_from_t1_found = 0
        for t in range(len(columns2[0])):
            if columns1[number1][j] == columns2[number2][t]:
                rows_from_t2_without_pair[t] = 1
                table_row = []
                if col_from_table1:
                    for k in col_from_table1:
                        table_row.append(columns1[k][j])
                if col_from_table2:
                    for k in col_from_table2:
                        if number2 in col_from_table2:
                            table_row.append(columns2[k][t])
                        else:
                            if k != number2:
                                table_row.append(columns2[k][t])

                new_table.append(table_row)
                row_from_t1_found = 1
        if row_from_t1_found == 0:
            table_row = []
            for k in col_from_table1:
                table_row.append(columns1[k][j])
            for k in col_from_table2:
                # if number2 in col_from_table2:
                table_row.append(' ')
            new_table.append(table_row)

    for a in range(len(rows_from_t2_without_pair)):

        if rows_from_t2_without_pair[a] == 0:
            table_row = []
            for k in col_from_table1:
                # if number2 in col_from_table2:
                table_row.append(' ')
            for k in col_from_table2:
                table_row.append(columns2[k][a])
            new_table.append(table_row)
    return new_table
def rebuild_table(new_table):
    table = []
    if new_table:
        for t in range(len(new_table[0])):
            table_temp = []
            for a in range(len(new_table)):
                table_temp.append(new_table[a][t])
            table.append(table_temp)
    return table

def full_join(col_from_table1,col_from_table2, columns1,columns2, column1 , column2, numb_of_first_col, numb_of_second_col, symbol, elem1, elem2):
    new_table=[]
    rows_from_t2_without_pair = []
    rows_from_t1_without_pair = []
    number1=elem1.find_col_in_dict_col_names(column1)
    number2 = elem2.find_col_in_dict_col_names(column2)
    case=0
    for q in range (len(columns2[0])):
        rows_from_t2_without_pair.append(0)
    for q in range(len(columns1[0])):
        rows_from_t1_without_pair.append(0)
    if col_from_table1 is None and col_from_table2 is None:
        raise Exception
    t2= elem2.find_col_in_dict_node(column2)
    t1 = elem1.find_col_in_dict_node(column1)
    if t2 is not None:
        new_table=full_join_with_indexed(t2, col_from_table1, col_from_table2, columns1, columns2, number1, number2, elem1, elem2, rows_from_t2_without_pair)
        case=1
    elif t1 is not None:
        case=2
        new_table = full_join_with_indexed(t1, col_from_table2, col_from_table1, columns2, columns1, number2, number1, elem2, elem1, rows_from_t1_without_pair)
    else:
        """
        for j in range (len(columns1[0])):
            row_from_t1_found=0
            for t in range (len(columns2[0])):
                if columns1[number1][j]==columns2[number2][t] and check_condition(columns1, columns2, numb_of_first_col, numb_of_second_col, symbol, j)=='yes':
                    rows_from_t2_without_pair[t]=1
                    table_row=[]
                    if col_from_table1:
                        for k in col_from_table1:
                            table_row.append(columns1[k][j])
                    if col_from_table2:
                        for k in col_from_table2:
                            if number2 in col_from_table2:
                                table_row.append(columns2[k][t])
                            else:
                                if k!= number2:
                                    table_row.append(columns2[k][t])

                    new_table.append(table_row)
                    row_from_t1_found=1
            if row_from_t1_found==0:
                table_row = []
                for k in col_from_table1:
                    table_row.append(columns1[k][j])
                for k in col_from_table2:
                    #if number2 in col_from_table2:
                        table_row.append(' ')
                new_table.append(table_row)

        for a in range (len(rows_from_t2_without_pair)):

            if rows_from_t2_without_pair[a]==0:
                table_row = []
                for k in col_from_table1:
                    #if number2 in col_from_table2:
                        table_row.append(' ')
                for k in col_from_table2:
                    table_row.append(columns2[k][a])
                new_table.append(table_row)
   """
        new_table=full_join_without_indexed(col_from_table1,col_from_table2,  columns1, columns2,number1,number2, rows_from_t2_without_pair)
    table=rebuild_table(new_table)
    if case==2:
        table1=[]
        size2= len(col_from_table2)
        for k in range (len(col_from_table1)):
            table1.append(table[size2+k])
        for i in range (len(col_from_table2)):
            table1.append(table[i])
        return table1
    return table

def full_join_where_condition(table, numb__col1,numb__col2, value, symbol, value2):
    new_table=[]
    if value2 is not None:
        if check_condition_value(value, value2, symbol)=='yes':
            return table
        else:
            return new_table
    if value==None:
        case=2
    elif numb__col2==None:
        case=1
    for i in range(len(table[0])):
        if (case==1 and check_condition_value(table[numb__col1][i],value,symbol)) or (case==2 and check_condition_value(table[numb__col1][i],table[numb__col2][i],symbol) ) :
            table_row=[]
            for k in range (len(table)):
                table_row.append(table[k][i])
            #if table_row:
            new_table.append(table_row)
    new_table1=rebuild_table(new_table)
    return new_table1

class Table:
    size_table = 0
    size_indexed = 0

    def __init__(self, name, result, indexed, number_of_index):
        self.name = name
        self.numb_of_rows = 0
        self.number = []
        self.column_names = []
        self.columns = []
        self.name_of_indexed = []
        self.number_of_index = []
        self.del_all = 1
        self.dict_rows={}

        self.size_indexed = len(indexed)
        for k in range(self.size_indexed):
            self.name_of_indexed.append(indexed[k])
            self.number_of_index.append(number_of_index[k])
        size = len(result)
        self.dict_col_names={}
        self.size_table = len(result)
        for i in range(size):
            self.columns.append(result[i])
            self.column_names.append(result[i])
            self.columns[i] = []
        i=0
        for a in self.column_names:
            self.dict_rows[a]=None
            i=i+1
        i = 0
        for a in self.column_names:
            self.dict_col_names[a] = i
            i = i + 1
        self.dict_node={}
        for t in self.name_of_indexed:
            self.dict_node[t]=None
    def add_row(self, result):
        if (len(self.number) == 0):
            n = 0
        else:
            n = max(self.number) + 1
        self.number.append(n)
        size = len(self.column_names)
        size_col = len(self.columns[0])
        for i in range(size):
            self.columns[i].append(result[i])
        if self.numb_of_rows == 0:
            k=0
            for i in self.dict_node:
                temp1 = self.number_of_index[k]
                self.dict_node[i]=tree.newNode(result[temp1], 0)
                k=k+1

        elif self.numb_of_rows != 0:
            k = 0
            for i in self.dict_node:
                temp1 = self.number_of_index[k]
                self.dict_node[i] = tree.insert(self.dict_node[i], result[temp1], n)

                k = k + 1
        self.numb_of_rows = self.numb_of_rows + 1

    def get_name(self):
        return self.name

    def get_numb_of_rows(self):
        return self.numb_of_rows

    def get_table(self):
        return self.columns

    def get_col_name(self, arr):
        for i in range(self.size_table):
            arr.append(self.column_names[i])

    def get_size(self):
        return self.size_table

    def show(self, indexes_of_right_col1, right_rows1):
        indexes_of_right_col = []
        right_rows = []
        size_col = len(self.columns[0])
        for t in range(size_col):
            right_rows.append(t)
        for i in range(len(self.column_names)):
            indexes_of_right_col.append(i)
        parsing.assign(indexes_of_right_col, indexes_of_right_col1)
        parsing.assign(right_rows, right_rows1)

    def delete_all(self):
        indexes_of_right_col = []
        self.number = []
        self.numb_of_rows = 0
        right_rows = []
        self.del_all = 0
        for i in self.dict_node:
            self.dict_node[i]=None
        size_col = len(self.columns[0])
        for t in range(size_col):
            right_rows.append(t)
        for i in range(len(self.column_names)):
            indexes_of_right_col.append(i)
        delete(self.column_names, self.columns, right_rows)

    def check_if_order_of_col_correct(self,numbers_of_col ):
        for i in range(len(numbers_of_col) - 1):
            if numbers_of_col[i + 1] < numbers_of_col[i]:
                raise Exception("wrong order")

    def show_col(self,names_of_col, right_rows1):
        right_rows = []
        size_col = len(self.columns[0])
        for t in range(size_col):
            right_rows.append(t)
        parsing.assign(right_rows, right_rows1)
        numbers_of_col = []
        for a in names_of_col:
            t=self.dict_col_names.get(a)
            if t is not None:
                numbers_of_col.append(t)
        self.check_if_order_of_col_correct(numbers_of_col)
        return numbers_of_col

    def find_in_tree(self,t, symbol, value):
        right_rows = []
        if (symbol == "="):
            tree.find(t, value, right_rows)
        elif (symbol == "<"):
            tree.find_l(t, value, right_rows)
        elif (symbol == "<="):
            tree.find_l_eq(t, value, right_rows)
        elif (symbol == ">"):
            tree.find_g(t, value, right_rows)
        elif (symbol == ">="):
            tree.find_g_eq(t, value, right_rows)
        return right_rows
    def find_in_table(self,number, symbol, value):
        right_rows=[]
        if (symbol == "="):
            for k in range(len(self.columns[number])):
                if self.columns[number][k] == value:
                    right_rows.append(k)
        elif (symbol == "<"):
            for k in range(len(self.columns[number])):
                if self.columns[number][k] < value:
                    right_rows.append(k)
        elif (symbol == "<="):
            for k in range(len(self.columns[number])):
                if self.columns[number][k] <= value:
                    right_rows.append(k)
        elif (symbol == ">"):
            for k in range(len(self.columns[number])):
                if self.columns[number][k] > value:
                    right_rows.append(k)
        elif (symbol == ">="):
            for k in range(len(self.columns[number])):
                if self.columns[number][k] >= value:
                    right_rows.append(k)
        elif (symbol == "!="):
            for k in range(len(self.columns[number])):
                if self.columns[number][k]!= value:
                    right_rows.append(k)
        return right_rows

    def find_col_in_dict_col_names(self, column):
        t = self.dict_col_names.get(column)
        if t is not None:
            number1 = t
            return number1
        #else:
            #raise Exception

    def find_col_in_dict_node(self, column):
        t = self.dict_node.get(column)
        if t is not None:
            number1 = t
            return number1
        else:
            #raise Exception
            return None
    def show_col_where(self, right_columns,name_of_col, symbol, value, right_arr_rows1, case):

        numbers_of_right_columns = []
        if right_columns:
            for a in right_columns:
                t=self.find_col_in_dict_col_names(a)
                if t is not None:
                    numbers_of_right_columns.append(t)
                else:
                    raise Exception
            self.check_if_order_of_col_correct(numbers_of_right_columns)
        else:
            for i in range(len(self.column_names)):
                right_columns.append(i)
        if case==0:
            if check_condition_value(name_of_col, value, symbol)=='yes':
               return self.show_col(right_columns,right_arr_rows1)
        else:
            x=self.dict_node.get(name_of_col)
            if x is not None and symbol != '!=':
                right_rows = self.find_in_tree(x, symbol, value)
                right_arr_rows=[]
                for j in right_rows:
                    for k in range(len(self.number)):
                        if j  == self.number[k]:
                            right_arr_rows.append(k)
            else:
                right_arr_rows = []

                t = self.dict_col_names.get(name_of_col)
                if t is not None:
                    right_rows=self.find_in_table(t, symbol, value)
                    parsing.assign(right_rows, right_arr_rows)
                else:
                    raise Exception("wrong column")
            parsing.assign(right_arr_rows, right_arr_rows1)
            if numbers_of_right_columns:
                return numbers_of_right_columns

    def return_specific_col_from_table(self, right_rows):
        edited_table=[]
        for i in range (len(self.columns)):
            temp_table = []
            for t in right_rows:
                temp_table.append(self.columns[i][t])
            edited_table.append(temp_table)
        return edited_table

    def delete_rows_from_tree(self, right_rows, a):
        right_arr_rows = []
        for j in right_rows:
            for k in range(len(self.number)):
                if j  == self.number[k]:
                    right_arr_rows.append(k)
        numb_of_rows_to_del = []
        if a==0:
            parsing.assign(right_rows, numb_of_rows_to_del )
        else:
            #for j in range(len(right_rows)):
            for j in right_rows:
                numb_of_rows_to_del.append(self.number[j])
        values_from_other_ind_col = []
        for i in self.number_of_index:
            qwq=0
            # if i!=number:
            #print(self.columns[i])
        if a==0:
            for i in right_arr_rows:
                # if j != number:
                for j in self.number_of_index:
                    # print(self.columns[j][i])
                    values_from_other_ind_col.append(self.columns[j][i])
        else:
            for i in right_rows:
                # if j != number:
                for j in self.number_of_index:
                    # print(self.columns[j][i])
                    values_from_other_ind_col.append(self.columns[j][i])
        i = 0
        j = 0
        for e in range(len(numb_of_rows_to_del)):
            # i=0
            for q in self.dict_node:
                #tree.inorder(self.dict_node[q])
                self.dict_node[q] = tree.deleteNode_number(self.dict_node[q], values_from_other_ind_col[i],
                                                           numb_of_rows_to_del[e])
                #print('\n')
                #tree.inorder(self.dict_node[q])
                #print('\n')
                #print(values_from_other_ind_col[i], numb_of_rows_to_del[e])
                i = i + 1
        number_of_del_col = 0
        if a==1:
            for m in numb_of_rows_to_del:
                self.number.remove(m)
            for m in right_rows:
                self.numb_of_rows = self.numb_of_rows - 1
                number_of_del_col = number_of_del_col + 1
        else:

            for m in right_rows:
                self.number.remove(m)
            for m in right_arr_rows:
                self.numb_of_rows = self.numb_of_rows - 1
                number_of_del_col=number_of_del_col+1
        return (number_of_del_col, right_arr_rows)

    def delete_col_where(self, name_of_col, symbol, value, case):
        if case==0:
            if check_condition_value(name_of_col, value, symbol) == 'yes':
                number_of_del_col= self.numb_of_rows
                self.delete_all()
                return  number_of_del_col

            else:
                return 0
        number=self.dict_node.get(name_of_col)
        if number and symbol !='!=':

            right_rows = self.find_in_tree(number, symbol, value)
            result_of_delete_from_tree=self.delete_rows_from_tree(right_rows,0)
            right_arr_rows=result_of_delete_from_tree[1]
            number_of_del_col=result_of_delete_from_tree[0]
            delete(self.column_names, self.columns, right_arr_rows)
        else:
            number1=self.find_col_in_dict_col_names(name_of_col)
            if number1 is not None:
                right_rows = self.find_in_table(number1, symbol, value)
                number_of_del_col=self.delete_rows_from_tree(right_rows,1)[0]
                delete(self.column_names, self.columns, right_rows)
            else:
                raise  Exception
        return number_of_del_col


    def two_col(self, number1, number2, symbol):
        right_rows = []
        if (symbol == "="):
            for k in range(len(self.columns[0])):
                if self.columns[number1][k] == self.columns[number2][k]:
                    right_rows.append(k)
        elif (symbol == "<"):
            for k in range(len(self.columns[number1])):
                if self.columns[number1][k] < self.columns[number2][k]:
                    right_rows.append(k)
        elif (symbol == "<="):
            for k in range(len(self.columns[number1])):
                if self.columns[number1][k] <= self.columns[number2][k]:
                    right_rows.append(k)
        elif (symbol == ">"):
            for k in range(len(self.columns[number1])):
                if self.columns[number1][k] > self.columns[number2][k]:
                    right_rows.append(k)
        elif (symbol == ">="):
            for k in range(len(self.columns[number1])):
                if self.columns[number1][k] >= self.columns[number2][k]:
                    right_rows.append(k)
        elif (symbol == "!="):
            for k in range(len(self.columns[number1])):
                if self.columns[number1][k] != self.columns[number2][k]:
                    right_rows.append(k)
        return right_rows

    def show_col_where_two_col(self, columns_to_display, column1, column2, symbol, right_rows1):

        number1=self.find_col_in_dict_col_names(column1)
        number2 = self.find_col_in_dict_col_names(column2)
        if number1 is not None and number2 is not None:
            if number1>number2:
                raise  Exception
            else:
                right_rows =self.two_col(number1, number2, symbol)
                numbers_of_right_columns = []
                if columns_to_display:
                    for a in columns_to_display:
                        t = self.find_col_in_dict_col_names(a)
                        if t is not None:
                            numbers_of_right_columns.append(t)
                        else:
                            raise Exception
                else:
                    for i in range(len(self.column_names)):
                        columns_to_display.append(i)
                parsing.assign(right_rows, right_rows1)
                return numbers_of_right_columns
        else:
            raise Exception

    def delete_col_where_two_col(self, column1, column2, symbol):

        number1 = self.find_col_in_dict_col_names(column1)
        number2 = self.find_col_in_dict_col_names(column2)
        if number1 is not None and number2 is not None:
            if number1 > number2:
                raise Exception
            right_rows = self.two_col(number1, number2, symbol)
            number_of_del_col =self.delete_rows_from_tree(right_rows,1)[0]
            delete(self.column_names, self.columns, right_rows)
            return number_of_del_col
        else:
            raise Exception







