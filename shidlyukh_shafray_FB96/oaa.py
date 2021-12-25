import operator

class Table():
    column={}
    indx={}
    database=[]
    k=0
    op = ['=', '!=', '>', '<', '>=', '<=']
    ops={
        '=':operator.eq,
        '!=':operator.ne,
        '>':operator.gt,
        '<':operator.lt,
        '>=':operator.ge,
        '<=':operator.le
    }
    def create(self, table_name, columns):
        col=[]
        c=[]
        if table_name in self.column.keys():
            print("Taka tablica isnue")
            return 0
        for i in columns:
            i=i.replace(' ', '')
            if i[-7:].lower() == "indexed":
                c.append(i[:-7])
                col.append(i[:-7])
            else:col.append(i)
        self.indx[table_name] = c
        self.column[table_name]=col
        print('created',table_name,'with columns', self.column[table_name])

    def insert(self, table_name, data):
        if table_name not in self.column.keys():
            print ("table name error")
            return 0
        if len(data) != len(self.column[table_name]):
            print('error')
            return 0
        for i in range(len(self.column[table_name])):
            if self.column[table_name][i] in self.indx[table_name]:
                for j in self.database:
                    if j[0]==table_name and j[1]==self.column[table_name][i] and j[2]==data[i]:
                        print('we have this value ('+j[2]+') on indexed',j[0],j[1])
                        return 0
        for i in range(len(data)):
            self.database.append([table_name, self.column[table_name][i], data[i],self.k])
        print(data,'added to',table_name)
        self.k+=1

    def select(self, table_name, column):
        print(self.database)
        print(self.column)
        print(self.indx)
        if table_name not in self.column.keys():
            print("table name error")
            return 0
        temp=[]
        if column=="*":
            for i in range(len(self.database)):
                if self.database[i][0]==table_name: temp.append(self.database[i])
        else:
            temp_col=column.replace(" ","").split(",")
            for i in temp_col:
                if i not in self.column[table_name]:
                    print("Table", table_name,"have not",i)
                    return 0
                for j in range(len(self.database)):
                    if self.database[j][0] == table_name and self.database[j][1]==i: temp.append(self.database[j])
        self.goodprint(temp)
        pass

    def delete(self, table_name):
        temp = []
        print("+" + table_name + "+", self.column.keys())
        if table_name not in self.column.keys():
            print("table name error")
            return 0
        else:
            print(self.database)
            del self.column[table_name]
            del self.indx[table_name]
            for i in range(len(self.database)):
                if table_name == self.database[i][0]:
                    temp.append(self.database[i])
            print(temp)
            for i in temp:
                print(i)
                self.database.remove(i)

    def delete_were(self,table_name, condition):
        out = []
        oper = 0
        print("k"+table_name+"k",self.column.keys())
        if table_name not in self.column.keys():
            print("table name error")
            return 0
        for i in self.op:
            if i in condition:
                oper = i
        if oper == 0:
            print('invalid condition operator')
            return 0
        cond1, cond2 = condition.split(oper, 1)
        cond1, cond2 = cond1[:-1], cond2[1:]
        if (cond1[0] == '"' == cond1[-1]) and (cond2[0] == '"' == cond2[-1]):
            case = 1
            cond1, cond2 = cond1[1:-1], cond2[1:-1]
            print(case)
            print(self.ops[oper](cond1, cond2))
            if self.ops[oper](cond1, cond2):
                for i in range(len(self.database)):
                    if table_name == self.database[i][0]:
                        out.append(self.database[i])
                for i in out:
                    print(i)
                    self.database.remove(i)
            else:
                print("condition False nothing to delete")
                self.select(table_name, '*')
                return 0
        elif (cond1[0] != '"' != cond1[-1]) and (cond2[0] != '"' != cond2[-1]):
            case = 2
            print(case)
            for i in self.database:
                for j in self.database:
                    if i[1] == cond1 and j[1] == cond2 and i[-1] == j[-1] and self.ops[oper](i[2], j[2]):
                        for m in self.database:
                            if m[-1] == i[-1]:
                                out.append(m)
            for i in out:
                self.database.remove(i)
            if out == []:
                print('conditional false')
                self.select(table_name, '*')
                return 0
            self.goodprint(out)
        elif (cond1[0] == '"' == cond1[-1]) and (cond2[0] != '"' != cond2[-1]):
            case = 3
            print(case)
            cond1 = cond1[1:-1]
            for i in self.database:
                if i[1] == cond2 and self.ops[oper](i[2], cond1) and i[0] == table_name:
                    for m in self.database:
                        if m[-1] == i[-1] :
                            out.append(m)
            for i in out:
                self.database.remove(i)
            if out == []:
                print('conditional false')
                self.select(table_name, '*')
                return 0
            self.goodprint(out)
        elif (cond1[0] != '"' != cond1[-1]) and (cond2[0] == '"' == cond2[-1]):
            case = 4
            print(case)
            cond2 = cond2[1:-1]
            for i in self.database:
                if i[1] == cond1 and self.ops[oper](i[2], cond2):
                    for m in self.database:
                        if m[-1] == i[-1]:
                            out.append(m)
            for i in out:
                self.database.remove(i)
            if out == []:
                print('conditional false')
                self.select(table_name, '*')
                return 0
            self.goodprint(out)
        else:
            print("condition error")
            return 0

    def select_were (self, table_name, column, condition):
        out=[]
        oper = 0
        if column=="*":
            column=self.column[table_name]

        if table_name not in self.column.keys():
            print("table name error")
            return 0
        for i in self.op:
            if i in condition:
                oper=i
        if oper == 0:
            print('invalid condition operator')
            return 0
        cond1, cond2 = condition.split(oper, 1)
        cond1, cond2 = cond1[:-1], cond2[1:]
        if (cond1[0] == '"' == cond1[-1]) and (cond2[0] == '"' == cond2[-1]):
            case=1
            cond1, cond2=cond1[1:-1], cond2[1:-1]
            print(case)
            print(self.ops[oper](cond1, cond2))
            if self.ops[oper](cond1, cond2):
                self.select(table_name, column)
            else:
                print("condition False")
                self.select(table_name, column)
                return 0
        elif (cond1[0] != '"' != cond1[-1]) and (cond2[0] != '"' != cond2[-1]):
            case=2
            print(case)
            for i in self.database:
                for j in self.database:
                    if i[1]==cond1 and j[1]==cond2 and i[-1]==j[-1] and self.ops[oper](i[2], j[2]):
                        for m in self.database:
                            if m[-1]==i[-1] and (m[1] in column):
                                out.append(m)
            if out==[]:
                print('conditional false')
                self.select(table_name, column)
                return 0
            self.goodprint(out)
        elif (cond1[0] == '"' == cond1[-1]) and (cond2[0] != '"' != cond2[-1]):
            case=3
            print(case)
            cond1=cond1[1:-1]
            for i in self.database:
                if i[1]==cond2 and self.ops[oper](i[2],cond1) and i[0]==table_name:
                    for m in self.database:
                        if m[-1] == i[-1] and (m[1] in column):
                            out.append(m)
            if out==[]:
                print('conditional false')
                self.select(table_name, column)
                return 0
            self.goodprint(out)
        elif (cond1[0] != '"' != cond1[-1]) and (cond2[0] == '"' == cond2[-1]):
            case=4
            print(case)
            cond2 = cond2[1:-1]
            for i in self.database:
                if i[1] == cond1 and self.ops[oper](i[2], cond2):
                    for m in self.database:
                        if m[-1] == i[-1] and (m[1] in column):
                            out.append(m)
            if out == []:
                print('conditional false')
                self.select(table_name, column)
                return 0
            self.goodprint(out)
        else:
            print("condition error")
            return 0

    def goodprint(self, arr):
        temp1 = []
        if arr == []:
            print('database is empty')
            return 0
        for i in range(len(arr), 0, -1):
            for j in range(0, len(arr) - 1):
                if arr[j][-1] > arr[j + 1][-1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        temp = arr
        for i in range(len(temp)):
            if temp[i][1] not in temp1:
                temp1.append(temp[i][1])
        for i in temp1: print(i, end=' ')
        print("")
        for i in range(0, len(temp), len(temp1)):
            for j in range(len(temp1)):
                print(temp[i + j][2], end=" ")
            print("")

    def sortirovka(self, sort, ord):
        for i in range(len(sort), 0, -1):
            for j in range(0, len(sort)-1):
                if sort[j][0].lower()>sort[j+1][0].lower():
                    sort[j], sort [j+1] = sort [j+1], sort[j]
        print("+"+ord+'+')
        if ord.lower()=="desc":
            sort.reverse()
        return sort

    def select_order(self, table_name, column, ordered):
        sort=[]
        if table_name not in self.column.keys():
            print("table name error")
            return 0
        if column == "*":
            column = self.column[table_name]
        else:
            column=column.replace(", ",",").replace(" ,",",").split(",")
        ordered=ordered.replace(', ', ',').replace(' ,',',').split(',')

        print(ordered, '=ordered')
        for i in range(len(ordered)):
            if ordered[i].find(" ")==-1:
                ordered[i]=[ordered[i], 'ASC']
            else:
                ordered[i]=ordered[i].split(' ', 1)
                if ordered[i][0] not in self.column[table_name]:
                    print('order column error')
                    return 0
                if ordered[i][1].lower()!='asc' and ordered[i][1].lower()!='desc':
                    print("order error")
                    return 0


            # ordered[i] = ordered[i].split()
            # if ordered[i].lower() in ('asc','desc'):
            #     print('dont use saved words in order')
            #     return 0
            # if (ordered[i][-3:].lower() !='asc' or len(ordered[i])<3) and (ordered[i][-4:].lower() !='desc' or len(ordered[i])<4):
            #     ordered[i]=ordered[i]+' ASC'

        if table_name not in self.column.keys():
            print('table not exist')
            return 0

        for i in column:
            if i not in self.column[table_name]:
                print('column not exist', i)
                return 0
        print(ordered)
        for i in self.database:
            if i[1]==ordered[0][0] and table_name==i[0]:
                sort.append([i[2], i[3]])
        sort=self.sortirovka(sort, ordered[0][1])
        print(sort)
        for i in range(1, len(ordered)):
            #ordered[i]=[column, ord]
            #sorted[i]=[[value,id]]
            t=1
            while t!=0:
                t=0
                for n in range(len(sort)-1):
                    if sort[n][0]==sort[n+1][0]:
                        t+=1
                        check1=check2=0
                        if ordered[i][1].lower()=='asc':
                            for j in self.database:
                                if j[1]==ordered[i][0] and j[-1]==sort[n][1]:
                                    check1=j[2]
                                if j[1]==ordered[i][0] and j[-1]==sort[n+1][1]:
                                    check2=j[2]
                            if check1>check2:
                                sort[n], sort[n+1]=sort[n+1], sort[n]
                        elif ordered[i][1].lower()=='desc':
                            for j in self.database:
                                if j[1]==ordered[i][0] and j[-1]==sort[n][1]:
                                    check1=j[2]
                                if j[1]==ordered[i][0] and j[-1]==sort[n+1][1]:
                                    check2=j[2]
                            if check1<check2:
                                sort[n], sort[n+1]=sort[n+1], sort[n]
        print(sort)

def Command():
    command = str(" ")
    while ';' not in command:
        command_ = str(input('\n'))
        if command_ == ';':
            command = command + command_
        elif command_ == '\n': pass
        else: command = command +" "+ command_
    if command[-1] == " ":
        command = command[0:-1]
    command = ' '.join(command.split()).split(';', 1)[0]
    return command.replace('“','"').replace('”','"')

def Check(command):
    check = command.split(" ")
    if check[0].lower() == "create":
        create, table_name, columns = command.split(" ",2)
        if columns[0] !='(':
            print('incorect (')
        elif columns[-1] != ')':
            print('incorect )')
        elif not columns[1:-2]:
            print('enter value')
        else:
            column = columns[1:-1].split(",")
            t.create(table_name, column)

    elif check[0].lower() == "insert":
        if command[7:11].lower() == "into":
            command = command[:6]+ " " +command[12:]
        insert, table_name, values = command.split(" ", 2)
        values.split(",")
        if values[0] != '(':
            print('incorect insert (')
        elif values[-1] != ')':
            print('incorect insert )')
        elif not values[1:-2]:
            print('enter values')
        else:
            value = []
            k=0
            i = 0
            while i <= len(values)-1:
                if values[i] == '"':
                    value.append(values[i+1:values.find('"',i+1)])
                    i = values.find('"', i+1)+1
                else: i = i + 1
            t.insert(table_name,value)
    elif check[0].lower() == "select":
        command+=' nothing'
        colunm_name = command[7:command.lower().find(" from ")]
        table_name, other = command[command.lower().find(" from ") + 6:].split(" ", 1)
        if ("where" in other.lower()) and ("order_by" in other.lower()):

            condition = other[other.lower().find("where")+6 :other.lower().find(" order_by")]
            ordered = other[other.lower().find("order_by")+9:other.find(" nothing")]
            print(colunm_name, table_name, condition, ordered)

        elif "where" in other.lower():
            condition = other[other.lower().find("where")+6:other.find(" nothing")]
            t.select_were(table_name, colunm_name, condition)
        elif "order_by" in other.lower():
            ordered = other[other.lower().find("order_by")+9:other.find(" nothing")]
            if ordered[-1]==" ":
                ordered=ordered[:-1]
            t.select_order(table_name, colunm_name, ordered)
        else:
            t.select(table_name, colunm_name)
    elif check[0].lower() == "delete":
        if command[7:11].lower() == "from":
            command = command[12:]
        else:
            command = command[7:]
        if "where" in command:
            table_name = command[:command.lower().find(' where')]
            condition = command[command.lower().find(" where ")+7:]
            t.delete_were(table_name, condition)
        else:
            table_name = command
            t.delete(table_name)
            print(table_name)
    elif check[0].lower() == "exit":
        raise SystemExit
    else: print('incorect')
    del check

t=Table()
while True:
    Check(Command())
