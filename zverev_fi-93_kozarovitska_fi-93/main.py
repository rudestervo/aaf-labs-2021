import re
import tree
import parsing
import table

exc_name= 'wrong name of table, please try again'
exc_name_col= 'wrong name of column, please try again'
exc_wrong='something went wrong, please try again'
exc_size='wrong size, please try again'
exc_name_taken='this name is already taken, please try again'
exc_parsing='something went wrong in parsing, please try again'
exc_order='wrong order of columns, please try again'
def beatiful_print(column_names, columns, indexes_of_right_col, right_rows):
    if not right_rows:
        print("selection is empty")
    else:
        size = len(column_names)
        size_col = len(columns[0])
        max = []
        for i in range(size):
            max.append(len(column_names[i]))

        # print('\n')
        for j in right_rows:
            for i in indexes_of_right_col:
                #print(f'{i} {j} ')
                #print(columns[i][j])
                if len(columns[i][j]) > max[i]:
                    max[i] = len(columns[i][j])

        for i in indexes_of_right_col:
            t = max[i] - len(column_names[i])
            if (t % 2 == 0):
                print("|", end='')
                k = 0
                while k < t / 2:
                    print(" ", end='')
                    k = k + 1
                print(column_names[i], end='')
                k = 0
                while k < t / 2:
                    print(" ", end='')
                    k = k + 1

            else:
                print("|", end='')
                k = 0
                while k < t / 2 - 1:
                    print(" ", end='')
                    k = k + 1
                print(column_names[i], end='')
                k = 0
                while k < t / 2:
                    print(" ", end='')
                    k = k + 1
        print("|", end='') #!!!
        print('\n', end='')
        print("+", end='')
        for i in indexes_of_right_col:
            k = 0
            while k < max[i]:
                print("-", end='')
                k = k + 1
            print("+", end='')
        print('\n', end='') #!!!
        for j in right_rows:
            for i in indexes_of_right_col:
                t = max[i] - len(columns[i][j])
                if (t % 2 == 0):
                    print("|", end='')
                    k = 0
                    while k < t / 2:
                        print(" ", end='')
                        k = k + 1
                    print(columns[i][j], end='')
                    k = 0
                    while k < t / 2:
                        print(" ", end='')
                        k = k + 1

                else:
                    print("|", end='')
                    k = 0
                    while k < t / 2 - 1:
                        print(" ", end='')
                        k = k + 1
                    print(columns[i][j], end='')
                    k = 0
                    while k < t / 2:
                        print(" ", end='')
                        k = k + 1
            print("|", end='')
            print('\n', end='')
        print("+", end='')
        for i in indexes_of_right_col:
            k = 0
            while k < max[i]:
                print("-", end='')
                k = k + 1
            print("+", end='')
        print('\n', end='')


def delete(column_names, columns, right_rows):
    indexes_of_right_col = []
    for i in range(len(column_names)):
        indexes_of_right_col.append(i)
    for j in reversed(right_rows):
        for i in reversed(indexes_of_right_col):
            if columns[i]:
                columns[i].pop(j)

def get_input():
    EmpInput = ""
    while ";" not in EmpInput:
        EmpInput += input()
        EmpInput += '  '
    return EmpInput


def add_col_to_selection(col_in_first_table,col_from_table1,col_names, col_to_compare, indexes_of_right_col, case ):
    col_names_new = []

    #if col_in_first_table in col_from_table1:
    if col_to_compare in col_names:
        return 'already in selection'
    else:
        #case += '0'
        col_from_table1.append(col_in_first_table)
        if case==1:
            for r in range(len(col_from_table1) - 1):
                col_names_new.append(col_names[r])
            for k in range(len(indexes_of_right_col)):
                if k >= len(col_from_table1) - 1:
                    indexes_of_right_col[k] += 1
            col_names_new.append(col_to_compare)
            r = r + 1
            while (r < len(col_names)):
                col_names_new.append(col_names[r])
                r = r + 1
        else:
            parsing.assign(col_names, col_names_new)
            col_names_new.append(col_to_compare)
        dict_col_names = {}
        r = 0
        for i in col_names_new:
            dict_col_names[i] = r
            r = r + 1
        return (col_names_new,dict_col_names)
def get_table_by_name(name_of_insert, tables, command):
   #check_if_name_is_right = -1

   if command!="create":
        elem = tables.get(name_of_insert)
        if elem is not None:
            return elem
        else:
            print(exc_name)
   else:

       if tables:
           elem = tables.get(name_of_insert)
           if elem is not None:
               print(exc_name)
           else:
               return 1
       else:
           return 1

tables={}
print("Please create table to start ")
EmpInput1=''
EmpInput=""
while parsing.exit(EmpInput) is None:
    EmpInput = get_input()
    EmpInput1 = EmpInput
    EmpInput1 = EmpInput1.casefold()
    first_command = EmpInput1.split()[0]
    second_command = EmpInput1.split()[1]
    result = []
    index = []
    number_of_index = []
    result_full_join=parsing.full_join(EmpInput)
    if result_full_join is not None:
        col_names=result_full_join[0]
        table1=result_full_join[1]
        table2 = result_full_join[2]
        col1=result_full_join[3]
        col2=result_full_join[4]
        command= result_full_join[5]
        elem1=get_table_by_name(table1, tables, 'select full join')
        elem2 = get_table_by_name(table2, tables, 'select full join')
        if elem1 and elem2 is not None:
            col_from_table1=[]
            col_from_table2 = []
            went_wrong=0
            if col_names:
                for a in range (len(col_names)):
                    x = elem1.find_col_in_dict_col_names(col_names[a])
                    if x is not None:
                        col_from_table1.append(x)
                    else:
                        break
                while a<len(col_names):
                    y = elem2.find_col_in_dict_col_names(col_names[a])
                    if y is not None:
                        col_from_table2.append(y)
                        a+=1
                    else:
                        went_wrong = 1
                        break
                if went_wrong == 1:
                    print(exc_order)
                    continue
            try:
                elem1.check_if_order_of_col_correct(col_from_table1)
                elem1.check_if_order_of_col_correct(col_from_table2)
                columns1 = elem1.get_table()
                columns2 = elem2.get_table()
                number1 = elem1.find_col_in_dict_col_names(col1)
                number2 = elem2.find_col_in_dict_col_names(col2)
                indexes_of_right_col = []
                right_rows = []

                if command == "* full join" or command == "* full join where two col" or command == '* full join where "" ' or command =='* full join where two val ':
                    col_from_table1 = []
                    for i in range(elem1.get_size()):
                        col_from_table1.append(i)
                    col_from_table2 = []
                    for i in range(elem2.get_size()):
                        col_from_table2.append(i)
                    col_names=[]
                    elem1.get_col_name(col_names)
                    col_names_table_2=[]
                    elem2.get_col_name(col_names_table_2)
                    for name in col_names_table_2:
                        col_names.append(name)

                for l in range(len(col_names)):
                    indexes_of_right_col.append(l)
                if command=="full join" or  command=="* full join":
                    try:
                        new_table=table.full_join(col_from_table1,col_from_table2, columns1, columns2,col1,col2, None, None, None, elem1, elem2)
                        if new_table:
                            for r in range(len(new_table[0])):
                                right_rows.append(r)
                        beatiful_print(col_names, new_table, indexes_of_right_col, right_rows)
                    except:
                        print(exc_wrong)
                        continue
                elif command=='full join where "" ' or command=='* full join where "" ' or command=='full join where two val ' or command =='* full join where two val ':
                    col_to_compare=result_full_join[6]
                    value=result_full_join[7]
                    symbol=result_full_join[8]
                    col_in_first_table = elem1.find_col_in_dict_col_names(col_to_compare)
                    col_in_second_table = elem2.find_col_in_dict_col_names(col_to_compare)
                    right_rows=[]
                    column_names = []
                    try:
                        if col_in_first_table is not None:
                            elem1.get_col_name(column_names)
                            elem1.show_col_where(column_names,col_to_compare, symbol, value,right_rows,1)
    
                        elif col_in_second_table is not None:
                            elem2.get_col_name(column_names)
                            elem2.show_col_where(column_names,col_to_compare, symbol, value,right_rows,1)
                        else:
                            if command!='full join where two val ' and command!='* full join where two val ':
                                print(exc_name_col)
                                continue
                        right_rows=[]
                        case=''
                        col_names_new = []
                        parsing.assign(col_names, col_names_new)
    
                        number_of_col_to_del=None
                        if col_in_first_table is not None:
                            result=add_col_to_selection(col_in_first_table, col_from_table1, col_names,col_to_compare, indexes_of_right_col, 1)
                        if col_in_second_table is not None:
                            case+='1'
                            result = add_col_to_selection(col_in_second_table, col_from_table2, col_names, col_to_compare, indexes_of_right_col, 2)
                        if result != 'already in selection' and command!='full join where two val ' and command !='* full join where two val ':
                            col_names_new = []
                            parsing.assign(result[0], col_names_new)
                        new_table = table.full_join(col_from_table1, col_from_table2, columns1, columns2, col1, col2, None, None, None, elem1, elem2)
                        for r in range(len(new_table[0])):
                            right_rows.append(r)
                        if col_in_first_table is not None:
                            new_table=table.full_join_where_condition(new_table, col_in_first_table,None, value, symbol, None)
                        if col_in_second_table is not None:
                            col_in_second_table+=len(col_from_table1)
                            new_table = table.full_join_where_condition(new_table, col_in_second_table,None,value, symbol, None)
                        if command == 'full join where two val ' or command=='* full join where two val ':
                            new_table = table.full_join_where_condition(new_table,None, None, value,
                                                                        symbol, col_to_compare)
                        right_rows=[]
                        if new_table:
                            for r in range(len(new_table[0])):
                                right_rows.append(r)
                        beatiful_print( col_names_new, new_table, indexes_of_right_col, right_rows)
                    except:
                        print(exc_wrong)
                        continue
                else:
                    col_to_compare1 = result_full_join[6]
                    col_to_compare2 = result_full_join[7]
                    symbol = result_full_join[8]
                    numb_of_first_col = None
                    numb_of_second_col = None
                    col2_in_first_table = None
                    col1_in_second_table = None
                    right_rows = []
                    col_names_new = []
                    parsing.assign(col_names, col_names_new)
                    case=''
                    dict_col_names={}
                    r=0
                    for i in col_names:
                        dict_col_names[i]=r
                        r=r+1
                    try:
                        numb_of_first_col = elem1.find_col_in_dict_col_names(col_to_compare1)
                        if numb_of_first_col is not None:
                            case='1'
                            result1 = add_col_to_selection(numb_of_first_col, col_from_table1, col_names, col_to_compare1,
                                                         indexes_of_right_col, 1)
                        else:
                            numb_of_first_col = elem2.find_col_in_dict_col_names(col_to_compare1)
                            if numb_of_first_col is not None:
                                result1 = add_col_to_selection(numb_of_first_col, col_from_table2, col_names_new,
                                                              col_to_compare1, indexes_of_right_col, 2)
                                case = '2'
                            else:
                                print(exc_name_col)
                                continue
                        if result1 != 'already in selection':
                            col_names_new = []
                            parsing.assign(result1[0], col_names_new)
                            dict_col_names = result1[1]
                        numb_of_second_col = elem1.find_col_in_dict_col_names(col_to_compare2)
                        if numb_of_second_col is not None:
                            case+='1'
                            result2 = add_col_to_selection(numb_of_second_col, col_from_table1, col_names_new, col_to_compare2,
                                                           indexes_of_right_col, 1)
                        else:
                            numb_of_second_col = elem2.find_col_in_dict_col_names(col_to_compare2)
                            if numb_of_second_col is not None:
                                case+='2'
                                result2 = add_col_to_selection(numb_of_second_col, col_from_table2, col_names_new,
                                                               col_to_compare2, indexes_of_right_col, 2)
                            else:
                                print(exc_name_col)
                                continue
                        right_rows = []
                        if case=='21':
                            print(exc_order)
                            continue
                        if result2 != 'already in selection':
                            col_names_new = []
                            parsing.assign(result2[0], col_names_new)
                            dict_col_names = result2[1]
                        new_table = table.full_join(col_from_table1, col_from_table2, columns1, columns2, col1, col2, None,
                                                    None, None, elem1, elem2)
                        numb_of_first_col_in_table=dict_col_names[col_to_compare1]
                        numb_of_second_col_in_table = dict_col_names[col_to_compare2]
                        new_table = table.full_join_where_condition(new_table, numb_of_first_col_in_table,numb_of_second_col_in_table, None, symbol, None)
                        if new_table:
                            for r in range(len(new_table[0])):
                                right_rows.append(r)
                        beatiful_print(col_names_new, new_table, indexes_of_right_col, right_rows)
                    except:
                        print(exc_wrong)
                        continue

                continue
            except:
                print(exc_order)
                continue
        continue
    if first_command=='create':
        name_table_create = parsing.create_table(EmpInput, result, index, number_of_index)
        if name_table_create:
            name_table1 = name_table_create
            result_correct_name=get_table_by_name(name_table_create, tables, "create")
            if result_correct_name:
                    try:
                        name_table_create = table.Table(name_table_create, result, index, number_of_index)
                        print(f"Table {name_table1} has been created")
                        tables[name_table1]=name_table_create
                        #tables.append(name_table_create)
                    except:
                        print(exc_wrong)
                        continue
            continue
        else:
            print(exc_wrong)
            continue

    column_values = []

    if first_command=='insert':
        name_table_insert = parsing.insert_table(EmpInput, column_values)
        if name_table_insert:
            elem = get_table_by_name(name_table_insert, tables, "insert")
            if elem:

                if (elem.get_size() != len(column_values)):
                    print(exc_size)
                    continue
                else:
                    try:
                        r1 = elem.add_row(column_values)
                        print(f"Row has been added to table {elem.get_name()}")
                        continue
                    except:
                        print(exc_wrong)
                        continue
            else:
                #print(exc_name)
                continue
        else:
            print(exc_wrong)
            continue



    result1=[]
    result_of_parsing_all_where=parsing.command_all_where(EmpInput, result1)
    if result_of_parsing_all_where:
        name_all_where =result_of_parsing_all_where[0]
        command = result_of_parsing_all_where[1]
        elem = get_table_by_name(name_all_where, tables, "select/delete")
        if elem:
            col_names = []
            elem.get_col_name(col_names)
            size_col_names = len(col_names)
            right_rows = []
            number = 0
            size_res = len(result1)
            columns = elem.get_table()
            case=1
            if command=="select where two val" or command=="delete where two val":
                case=0
            if command == "select where ''" or command=="select where two val":
                try:
                    indexes_of_right_col = []
                    all_columns = []
                    elem.show_col_where(all_columns, result1[size_res - 3], result1[size_res - 2],
                                        result1[size_res - 1], right_rows,case)
                    print(f"this is selection from '{elem.get_name()}' table")
                    beatiful_print(col_names, columns, all_columns, right_rows)
                except:
                    print(exc_wrong)
                    continue
            elif command == "select where two col":
                try:
                    all_columns = []
                    elem.show_col_where_two_col(all_columns, result1[size_res - 3], result1[size_res - 1],
                                                result1[size_res - 2], right_rows)
                    print(f"this is selection from '{elem.get_name()}' table")
                    beatiful_print(col_names, columns, all_columns, right_rows)
                except:
                    print(exc_wrong)
                    continue
            elif command=="delete where ''" or command=="delete where two val":
                try:
                    number_of_del_col = elem.delete_col_where(result1[size_res - 3], result1[size_res - 2],
                                                              result1[size_res - 1],case)
                    print(f"we deleted {number_of_del_col} rows from '{elem.get_name()}' table")
                except:
                    print(exc_wrong)
                    continue
            elif command=="delete where two col":
                try:
                    size_res = len(result1)
                    number_of_del_col = elem.delete_col_where_two_col(result1[size_res - 3], result1[size_res - 1],
                                                                      result1[size_res - 2])
                    print(f"we deleted {number_of_del_col} rows from '{elem.get_name()}' table")
                    continue
                except:
                    print(exc_wrong)
                    continue
            else:
                print(exc_parsing)
        #else:
            #print(exc_name)
        continue

    result1 = []
    name_select_col = parsing.select_columns(EmpInput, result1)

    if name_select_col:
            elem=get_table_by_name(name_select_col, tables, "select")
            if elem:
                arr = []
                elem.get_col_name(arr)
                size_arr = len(arr)
                size_res = len(result1)
                result1.pop(size_res - 1)
                size_res = len(result1)
                try:
                    column_names = []
                    right_rows = []
                    columns = elem.get_table()
                    elem.get_col_name(column_names)
                    indexes = elem.show_col(result1, right_rows)
                    print(f"this is {elem.get_name()} table")
                    beatiful_print(column_names, columns, indexes, right_rows)
                except:
                    print(exc_name)
                    continue
            else:
                print(exc_name)
            continue
        #continue

    result1 = []
    result_select_columns_where=parsing.select_columns_where(EmpInput,result1)
    if result_select_columns_where:
        name_select_columns_where=result_select_columns_where[0]
        command=result_select_columns_where[1]
        elem = get_table_by_name(name_select_columns_where, tables, "select")
        if elem:
            col_names = []
            elem.get_col_name(col_names)
            size_col_names = len(col_names)
            size_res = len(result1)
            columns = elem.get_table()
            right_arr_rows = []
            right_rows = []
            if command=="select col where ''":
                try:
                    names_of_right_col = []
                    parsing.assign(result1, names_of_right_col)
                    for i in range(3):
                        size_col = len(names_of_right_col)
                        names_of_right_col.pop(size_col - 1)
                    indexes = elem.show_col_where(names_of_right_col, result1[size_res - 3], result1[size_res - 2],
                                                  result1[size_res - 1], right_arr_rows,1)
                    print(f"this is selection from '{elem.get_name()}' table")
                    beatiful_print(col_names, columns, indexes, right_arr_rows)
                except:
                    print(exc_wrong)
                    continue
            elif command=="select col where two col":
                try:
                    columns_to_display = []
                    parsing.assign(result1, columns_to_display)
                    for i in range(3):
                        size_col = len(columns_to_display)
                        columns_to_display.pop(size_col - 1)
                    indexes = elem.show_col_where_two_col(columns_to_display, result1[size_res - 3], result1[size_res - 1],
                                                          result1[size_res - 2], right_rows)
                    print(f"this is selection from '{elem.get_name()}' table")
                    beatiful_print(col_names, columns, indexes, right_rows)
                except:
                    print(exc_wrong)
                    continue
            elif command == "select col where two val":
                try:
                    names_of_right_col = []
                    parsing.assign(result1, names_of_right_col)
                    for i in range(3):
                        size_col = len(names_of_right_col)
                        names_of_right_col.pop(size_col - 1)
                    indexes = elem.show_col_where(names_of_right_col, result1[size_res - 2], result1[size_res - 3],
                                                  result1[size_res - 1], right_arr_rows,0)
                    print(f"this is selection from '{elem.get_name()}' table")
                    beatiful_print(col_names, columns, indexes, right_arr_rows)
                except:
                    print(exc_wrong)
                    continue
            else:
                print(exc_parsing)
        continue

    result_of_parsing_all = parsing.command_all(EmpInput)
    if result_of_parsing_all:
        name_all = result_of_parsing_all[0]
        command = result_of_parsing_all[1]
        elem = get_table_by_name(name_all, tables, "select/delete")
        if elem:
            if command == "select":
                try:
                    column_names = []
                    indexes_of_right_col = []
                    right_rows = []
                    columns = elem.get_table()
                    elem.get_col_name(column_names)
                    elem.show(indexes_of_right_col, right_rows)
                    print(f"this is {elem.get_name()} table")
                    beatiful_print(column_names, columns, indexes_of_right_col, right_rows)
                    continue
                except:
                    print(exc_wrong)
            elif command == "delete":
                try:
                    elem.delete_all()
                    print(f"we deleted everything from {elem.get_name()} table")
                    continue
                except:
                    print(exc_wrong)
            else:
                print(exc_parsing)
        #else:
            #print(exc_name)
        continue
    print('please insert supported function')
    continue


