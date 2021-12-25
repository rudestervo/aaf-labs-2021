from table_func import *
import sys
### Parser :



class Parser(object):
    def __init__(self):
        self.tokens_arr = []
        tables_arr = []

    # def __init__(self, comand):
    #     self.tokens_arr = comand
    #     tables_arr = []

    def parse(self, comm_array):
        self.tokens_arr = comm_array

    def start(self):
        if len(self.tokens_arr)==0:
            print("Empty!")
        while(len(self.tokens_arr)!=0):
            if self.tokens_arr[0].type == 'CREATE TABLE':
                self.create_table(len(self.tokens_arr))
            elif self.tokens_arr[0].type == 'INSERT':
                self.insert(len(self.tokens_arr))
            elif self.tokens_arr[0].type == 'SELECT':
                self.select(len(self.tokens_arr))
            elif self.tokens_arr[0].type == 'DELETE':
                self.delete(len(self.tokens_arr))
            elif self.tokens_arr[0].type == "EXIT":
                print("exit")
                sys.exit()
            elif self.tokens_arr[0].type=="SEMICOLON":
                print("Semicolon")
                self.tables_arr = []
                return
            elif len(self.tokens_arr) == 0:
                print("empty")
            else:
                if len(self.tokens_arr)>=2:
                    print("Unknown command "+str(self.tokens_arr[0].text)+ " "+ str(self.tokens_arr[1].text) +" use commands (only uppercase for commands)\'CREATE TABLE\' , \'INSERT\', \'SELECT\', \'EXIT\' ")
                    for i in range(0, len(self.tokens_arr)):
                        self.tokens_arr.pop(0)
                elif len(self.tokens_arr)==1:
                    print("Unknown command "+str(self.tokens_arr[0].text)+ " use commands (only uppercase for commands)\'CREATE TABLE\' , \'INSERT\', \'SELECT\', \'EXIT\' ")
                    for i in range(0, len(self.tokens_arr)):
                        self.tokens_arr.pop(0)

    def create_table(self, command_length):
        if command_length<4:
            print("Pattern: CREATE TABLE tablename (field [INDEXED],...)")
            for i in range(0, command_length):
                self.tokens_arr.pop(0)
            return
        elif self.tokens_arr[1].type == 'VAR' and self.tokens_arr[2].type == '(':
            endindex = False
            for token in self.tokens_arr:
                if token.type == ')':
                    endindex=self.tokens_arr.index(token)
                    break
            if endindex:
                tablename=self.tokens_arr[1].text
                # CREATE cats (id INDEXED, name INDEXED, favourite_food); - patern metodichka
                columnsname=[]
                indexedcol=[]
                step=2 # as a default
                index=0
                i=3
                while(i<endindex):
                    if self.tokens_arr[i].type == "COMA":
                        i += 1
                    if self.tokens_arr[i].type == "VAR" and self.tokens_arr[i + 1].type == "INDEXED" and (
                            self.tokens_arr[i + 2].type == "COMA" or self.tokens_arr[i + 2].type == ")"):
                        columnsname.append(self.tokens_arr[i].text)
                        indexedcol.append(index)

                    elif self.tokens_arr[i].type == "VAR" and (self.tokens_arr[i + 1].type == "COMA" or self.tokens_arr[i + 1].type == ")"):
                        columnsname.append(self.tokens_arr[i].text)
                    else:
                        for i in range(0, endindex + 1):
                            self.tokens_arr.pop(0)
                        print("Pattern: CREATE TABLE tablename (field [INDEXED],...)")
                        return
                    i+=2
                    index += 1
                print("Fields: "+str(columnsname))
                print("Indexed"+str(indexedcol))
                # удалим создание (засунем в массив и выполним)
                for table in tables_arr:
                    if table.get_name()==tablename:
                        print('Table with this name already exists:')
                        for i in range(0, endindex + 1):
                            self.tokens_arr.pop(0)
                        return
                table = Table(tablename, columnsname, indexedcol)
                table.show_table()
                tables_arr.append(table)
            else:
                print('Invalid syntax in CREATE\n u didnt close parentheses')
                for i in range(0, command_length):
                    self.tokens_arr.pop(0)
                return
        else:
            print('Invalid syntax in CREATE\n syntax: CREATE TABLE tablename (field [INDEXED],...)')
            for i in range(0, command_length):
                self.tokens_arr.pop(0)
            return
        for i in range(0, endindex + 1):
            self.tokens_arr.pop(0)


            
            
    def insert(self, comand_length):
        tablename = ''
        #   INSERT tablename (“2”, “Pushok”, “Fish”)
        if comand_length<5:
            print("Pattern: INSERT tablename (\"fields\")")
            for i in range(0, comand_length):
                self.tokens_arr.pop(0)
            return
        elif self.tokens_arr[1].type == 'VAR'and self.tokens_arr[2].type == '(' and self.tokens_arr[3].type == 'STR':
            for token in self.tokens_arr:
                if token.type == ')':
                    endindex=self.tokens_arr.index(token)
                    break
            tablename = self.tokens_arr[1].text
            curr_table=False
            for j in range(0, len(tables_arr)):
                if tables_arr[j].tablename == tablename :
                    curr_table = tables_arr[j]
    #               print(curr_table.tablename + ' was found')
                    break
                else:
                    print('No table with name ' + tablename)
                    for i in range(0, comand_length):
                        self.tokens_arr.pop(0)
                    return
            if endindex:
                values=[]
                for i in range(3, endindex):
                    if i%2==1:
                        if self.tokens_arr[i].type=="STR":
                            values.append(self.tokens_arr[i].text)
                        else:
                            print('Invalid syntax in INSERT\n syntax: INSERT tablename (“str”...)')
                            for i in range(0, endindex+1):
                                self.tokens_arr.pop(0)
                            return
                    else:
                        if self.tokens_arr[i].type == "COMA":
                            continue
                        else:
                            print('Invalid syntax in INSERT\n syntax: INSERT tablename (“str”...)')
                            for i in range(0, endindex+1):
                                self.tokens_arr.pop(0)

                for i in range(len(values)):
                    values[i]=values[i].replace("\"", "")
                curr_table.insertion(values)
                curr_table.show_table()
                for i in range(0, endindex + 1):
                    self.tokens_arr.pop(0)
            else:
                print('Invalid syntax in INSERT\n u didnt close parentheses')
                for i in range(0, endindex + 1):
                    self.tokens_arr.pop(0)
        else:
            print('Invalid syntax in INSERT\n')
            for i in range(0, comand_length):
                self.tokens_arr.pop(0)

    def select(self, comand_length):
#   SELECT ( * | column_name [, ...])  FROM table_name # [WHERE condition]   [ORDER_BY column_name [(ASC|DESC)] [, ...] ];
        endindex=0
        where=False
        order=False
        if comand_length<4:
            print("Error in select \n SELECT ( * | column_name [, ...])  FROM table_name # [WHERE condition]   [ORDER_BY column_name ASC|DESC")
            for i in range(0,comand_length):
                self.tokens_arr.pop(0)
            return
        endindex = len(self.tokens_arr) - 1
        for token in self.tokens_arr:
            if token.type == 'CREATE TABLE':
                endindex=self.tokens_arr.index(token)-1
                break
            elif token.type == 'INSERT':
                endindex=self.tokens_arr.index(token)-1
                break
            elif token.type == 'SELECT' and self.tokens_arr.index(token)!=0:
                endindex=self.tokens_arr.index(token)-1
                break
            elif token.type == 'EXIT':
                endindex = self.tokens_arr.index(token)-1
                break
            elif token.type == 'SEMICOLON':
                endindex=self.tokens_arr.index(token)-1
                break
            elif token.type == 'DELETE':
                endindex=self.tokens_arr.index(token)-1
                break

        if self.tokens_arr[1].type == 'ALL':
            if self.tokens_arr[2].type == 'FROM':
                table=False
                if self.tokens_arr[3].type == 'VAR':
                    table_name = self.tokens_arr[3].text
                    for t in tables_arr:
                        if t.tablename == table_name:
                            table = self.tokens_arr[3]
                            break
                    if table:# Если таблица есть в массиве с таблицами
                        if endindex >= 7:
                            if self.tokens_arr[4].type == 'WHERE' and self.tokens_arr[5].type == 'VAR' and self.tokens_arr[7].type == 'STR' and \
                                    (self.tokens_arr[6].type == 'EQUAL' or self.tokens_arr[6].type == 'NOT_EQUAL'):
                                where=[self.tokens_arr[5], self.tokens_arr[6], self.tokens_arr[7]]
                                if endindex > 7:
                                    if self.tokens_arr[8].type == 'ORDER_BY':
                                        if self.tokens_arr[9].type == 'VAR' and (self.tokens_arr[10].type == 'ASC' or self.tokens_arr[10].type == 'DESC'):
                                            order=[self.tokens_arr[9], self.tokens_arr[10]]
                                            select_in_table(self.tokens_arr[1].type, table, where, order)
                                        else:
                                            print("ORDER_BY column_name ASC|DESC")
                                    else:
                                        print("After where ORDER_BY column_name ASC|DESC")
                                else: select_in_table(self.tokens_arr[1].type, table, where, order)
                            else:
                                print("Error in where:   Where field ==/!= \"value\"")
                        elif endindex == 6:
                            if self.tokens_arr[4].type == 'ORDER_BY':
                                if self.tokens_arr[5].type == 'VAR' and (self.tokens_arr[6].type == 'ASC' or self.tokens_arr[6].type == 'DESC'):
                                    order=[self.tokens_arr[5], self.tokens_arr[6]]
                                    select_in_table(self.tokens_arr[1].type, table, where, order)
                                else:
                                    print("ORDER_BY column_name ASC|DESC")
                            else:
                                print("ORDER_BY column_name ASC|DESC")
                        else:
                            select_in_table(self.tokens_arr[1].type, table, where, order)
                    else:
                        print(f"No table with name {table_name}")
                else:
                    print("Use VAR for tablename")
            else:
                print("U didnt selected table\n SELECT ( * | column_name [, ...])  FROM table_name # [WHERE condition]   [ORDER_BY column_name [(ASC|DESC)] [, ...] ];")
        elif self.tokens_arr[1].type == "VAR":
            fromindex=False
            for token in self.tokens_arr:
                if token.type == 'FROM':
                    fromindex=self.tokens_arr.index(token)
                    break
            if fromindex==False:
                for i in range(0, endindex + 1):
                    self.tokens_arr.pop(0)
                return False

            fields_arr=[]
            for i in range(1, fromindex, 2): #val, val from
                if self.tokens_arr[i].type == 'VAR' and self.tokens_arr[i+1].type == 'COMA':
                    fields_arr.append(self.tokens_arr[i].text)
                elif self.tokens_arr[i].type == 'VAR' and self.tokens_arr[i+1].type == 'FROM':
                    fields_arr.append(self.tokens_arr[i].text)
                else:
                    print("error in enumeration of fields \n SELECT ( * | column_name [, ...])  FROM table_name # [WHERE condition]   [ORDER_BY column_name [(ASC|DESC)] [, ...] ];")
            table_name=self.tokens_arr[fromindex+1].text
            table = False
            for t in tables_arr:
                if t.tablename==table_name:
                    table=self.tokens_arr[fromindex+1]
                    break
            if table:
                if endindex==fromindex+1:
                    select_in_table(fields_arr, table, where, order)
                index=fromindex+2  #index фактически индекс where or order by если они есть
                # if endindex<index+2:
                #     select_in_table(fields_arr,table_name,where,order)
                #     for i in range(0, endindex + 1):
                #         self.tokens_arr.pop(0)
                #         return
                if index+3<=endindex:
                    if self.tokens_arr[index].type == 'WHERE':
                        if self.tokens_arr[index+1].type == 'VAR' and self.tokens_arr[index+3].type == 'STR' and \
                                (self.tokens_arr[index+2].type == 'EQUAL' or self.tokens_arr[index+2].type == 'NOT_EQUAL'):
                            where = [self.tokens_arr[index+1], self.tokens_arr[index+2], self.tokens_arr[index+3]]
                        if index+6<=endindex:
                            if self.tokens_arr[index+4].type == 'ORDER_BY':
                                if self.tokens_arr[index+5].type == 'VAR' and (
                                        self.tokens_arr[index+6].type == 'ASC' or self.tokens_arr[index+6].type == 'DESC'):
                                    order = [self.tokens_arr[index+5], self.tokens_arr[index+6]]
                                    select_in_table(fields_arr, table, where, order)
                                    for i in range(0, endindex + 1):
                                        self.tokens_arr.pop(0)
                                    return
                                else:
                                    print("Error in order by \nORDER_BY column_name (ASC|DESC)")
                            else:
                                print("Error After where statement")
                        else:
                            select_in_table(fields_arr, table, where, order)
                if index+2==endindex:
                    if self.tokens_arr[index].type == 'ORDER_BY':
                        if self.tokens_arr[index+1].type == 'VAR' and (
                                self.tokens_arr[index+2].type == 'ASC' or self.tokens_arr[index+2].type == 'DESC'):
                            order = [self.tokens_arr[index+1], self.tokens_arr[index+2]]
                            select_in_table(fields_arr, table, where, order)

                        else:
                            print("ORDER_BY column_name (ASC|DESC)")
                    else:
                        print("ORDER_BY column_name [(ASC|DESC)]")
            else:
                print(f"table named {table_name} not found ")
                for i in range(0, comand_length):
                    self.tokens_arr.pop(0)
                return
        else:
            print("* or fieldname")
        for i in range(0, endindex + 1):
            self.tokens_arr.pop(0)

    def delete(self,comand_length):
        table_name=False
        condition="ALL"
        endindex = 0
        table=False
        if comand_length < 2:
            print("Pattern: DELETE table_name [WHERE condition] condition:field ==/!= \"str\"")
            for i in range(0, comand_length):
                self.tokens_arr.pop(0)
            return
        elif self.tokens_arr[1].type == 'VAR':
            endindex = len(self.tokens_arr) - 1
            for token in self.tokens_arr:
                if token.type == 'CREATE TABLE':
                    endindex = self.tokens_arr.index(token) - 1
                    break
                elif token.type == 'INSERT':
                    endindex = self.tokens_arr.index(token) - 1
                    break
                elif token.type == 'SELECT':
                    endindex = self.tokens_arr.index(token) - 1
                    break
                elif token.type == "EXIT":
                    endindex = self.tokens_arr.index(token) - 1
                    break
                elif token.type == "SEMICOLON":
                    endindex = self.tokens_arr.index(token) - 1
                    break
                elif token.type == "DELETE" and self.tokens_arr.index(token) != 0:
                    endindex = self.tokens_arr.index(token) - 1
                    break

            table_name=self.tokens_arr[1].text
            for t in tables_arr:
                if t.tablename == table_name:
                    table = self.tokens_arr[1]
                    break
            if table:
                if endindex==1:
                    del_func(self.tokens_arr[1], condition)
                elif endindex==5:
                    if self.tokens_arr[2].type == 'WHERE':
                        if self.tokens_arr[3].type == 'VAR' and self.tokens_arr[5].type == 'STR' and \
                        (self.tokens_arr[4].type == 'EQUAL' or self.tokens_arr[4].type == 'NOT_EQUAL'):
                            condition=[self.tokens_arr[3], self.tokens_arr[4], self.tokens_arr[5]]
                            del_func(self.tokens_arr[1],condition)
                        else:
                            print("Error in WHERE condition, WHERE field==/!=\"value\"")
                    else:
                        print("After table_name have to be [WHERE condition]")
                else:
                    print("You can add only WHERE field==/!=\"value\"")
            else:
                print(f"No table with name {table_name}")
        else:
            print("use var to set tablename")
            for i in range(0, comand_length):
                self.tokens_arr.pop(0)
            return
        for i in range(0, endindex + 1):
            self.tokens_arr.pop(0)