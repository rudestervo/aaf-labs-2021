from DataBase.Table import Table
from prettytable import PrettyTable

class DataBase:
    def __init__(self):
        self.dataBase = {}
        self.allTablesName = []
    def PrintDB(self):
        for Table in  self.allTablesName:
            Tab = self.dataBase[Table]
            print(Tab.columns)
            print(Tab.indexedColumns)
            print(Tab.table)
            for key in Tab.indexes.keys():
                print(key, end=": ")
                Tab.indexes[key].PrintTree()
                print()

    def DoseTableExist(self, name):
        if name not in self.allTablesName:
            raise Exception ('There is no table with name', name)

    def CreateTable(self, name, columns, indexes):
        if name not in self.allTablesName:
            self.allTablesName.append(name) 
            self.dataBase[name] = Table(columns, indexes)
            print('table with name', name, 'created')
        else :
            raise Exception ('Table with this name already exists')

    def Insert(self, name, varsToInsert):
        self.DoseTableExist(name)
        self.dataBase[name].CheckNumberOfColumns(len(varsToInsert))
        self.dataBase[name].Insert(varsToInsert)
        print('row inserted in table', name)

    def Delete(self, name, param1, condition, param2):
        self.DoseTableExist(name)
        toCheck = []
        if param1.type == 'VAR':
            toCheck.append(param1)
        if param2.type == 'VAR':
            toCheck.append(param2)  
        self.dataBase[name].CheckIfInColumns(toCheck)
        self.dataBase[name].Delete(param1, condition, param2)
        print('deleted row from table', name)

    def Select(self, name ,columns, var1, condition ,var2, groupByFields, aggFunctions, fieldsToAggregate):
        self.DoseTableExist(name)
        data = self.dataBase[name].Select(columns, var1, condition ,var2, groupByFields, aggFunctions, fieldsToAggregate)
        print('====',name.upper(),'====')
        self.PrintTable(data)
        

    def PrintTable(self, data):
        names = data[1]
        rows = data[0]
        table =  PrettyTable()
        table.field_names = names
        table.add_rows(rows)
        print(table)

    





