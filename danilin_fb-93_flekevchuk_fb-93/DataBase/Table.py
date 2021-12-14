from functools import *

from DataBase.Tree import Node
from DataBase.BinaryOperators import allBinares
from DataBase.AgreggateFunc import AgreggateFunc

ID = 'ID'
INDEX = 'INDEX'

class Table:
    def __init__(self, columns, indexesColumn):
        self.table = list()
        self.columns = dict()
        i = 0
        for column in columns:
            self.columns[column] = {}
            self.columns[column][ID] = i
            i+=1
            if column in indexesColumn:
                self.columns[column][INDEX] = Node(None, None)
                continue
            self.columns[column][INDEX] = None

    def findInColumns(self, columns, groupByFields = [],  fieldsToAggregate = []):
        
        for column in columns:
            if column not in self.columns:
                raise Exception ('There is no such column as',column)
                

    def Insert(self, varsToInsert):
        id = len(self.table)
        self.table.append(varsToInsert)
        for column in self.columns:
            if self.columns[column][INDEX]:
                self.columns[column][INDEX].insert(varsToInsert[self.columns[column][ID]], id)

    def CheckNumberOfColumns(self, length):
        if length != len(self.columns.keys()):
            raise Exception ('Table has this number of columns ', len(self.columns))

    def CheckIfInColumns(self,columns):
        allCorrectColumns = len([column for column in columns if column.text in self.columns])
        if len(columns) != allCorrectColumns:
            raise Exception ('There is no such columns as',
            [column for column in columns if column not in self.columns] )

    def Delete(self, param1, condition, param2):
        allIDs = self.select(param1, condition, param2)
        for id in allIDs:
            for column in self.columns:
                if self.columns[column][INDEX]:
                    self.columns[column][INDEX].DeleteWithID(self.table[id][ self.columns[column][ID]], id)
            self.table[id] = None

    def select(self, param1, condition, param2):
        if param1.type == param2.type:
            allRows = []
            i=0
            for row in self.table:
                if not row:
                    continue
                if allBinares[condition.type](row[self.columns[param1.text][ID]],row[self.columns[param2.text][ID]]):
                    allRows.append(i)
                i+=1
            return allRows
        elif param1.type == 'VAR':
            if  self.columns[param1.text][INDEX] :
                return self.ParsIndexCondition(param1.text, condition, int(param2.text))
            return self.ParsCondition(param1.text, condition, int(param2.text))
        elif  self.columns[param2.text][INDEX]:
            if self.columns[param2.text][INDEX]:
                return self.ParsIndexCondition(param2.text, condition, int(param1.text))
            return self.ParsCondition(int(param1.text), condition, param2.text)

    def ParsIndexCondition(self, index, condition, number):
        if condition.type == 'EQUAL':
            return self.columns[index][INDEX].find(number)
        if condition.type == 'NOT_EQUAL':
            return self.columns[index][INDEX].find(number)
        if condition.type == 'MORE_EQUAL':
            return self.columns[index][INDEX].getAllIDsMore(number, True)
        if condition.type == 'MORE':
            return self.columns[index][INDEX].getAllIDsMore(number, False)
        if condition.type == 'MORE_LESS':
            return self.columns[index][INDEX].getAllIDsLess(number, True)
        if condition.type == 'LESS':
            return self.columns[index][INDEX].getAllIDsLess(number, False)

    def ParsCondition(self, param1, condition, param2):
        i = 0
        allIDs = []
        for row in self.table:
            if not row:
                continue
            value1 = row[self.columns[param1][ID]]
            if allBinares[condition.type](value1,param2):
                allIDs.append(i)
            i+=1
        return allIDs
    
    def Select(self, columns, var1, condition ,var2 , groupByFields, aggFunctions, fieldsToAggregate):
        self.findInColumns(columns)
        if condition.text in columns:
            columnsID = [self.columns[column][ID] for column in columns ]
            return[map(self.parsColumns(columnsID),self.table), columns]
        allIDS = self.select(var1, condition, var2)
        allRows = []
        for id in allIDS:
            allRows.append(self.table[id])
        if len(groupByFields):
            allRows = self.GroupBY(groupByFields, allRows,  aggFunctions, fieldsToAggregate)
            allColumns = groupByFields + fieldsToAggregate
            columnsID = [self.columns[column][ID] for column in allColumns]
            return [map(self.parsColumns(columnsID),allRows), allColumns]
        columnsID = [self.columns[column][ID] for column in columns ]
        return [map(self.parsColumns(columnsID),allRows), columns]
        
    def parsColumns(self, columnsID):
        return lambda row: [row[id] for id in columnsID]

    def GroupBY(self, groupByFields, allRows, aggFunctions, fieldsToAggregate):
        groupedByRows = dict()
        otherFields = list(filter(lambda column: column not in groupByFields, self.columns.keys()))
        groupByFieldsID = [self.columns[column][ID] for column in groupByFields] 
        for row in allRows:
            keyElements = self.parsColumns(groupByFieldsID)(row)
            key = self.CreateKey(keyElements)
            if key in groupedByRows:
                for field in otherFields:
                    groupedByRows[key][field].append(row[self.columns[field][ID]])
                continue
            groupedByRows[key] = dict()
            for field in otherFields:
                groupedByRows[key][field] = list()
                groupedByRows[key][field].append(row[self.columns[field][ID]]) 
        return self.Agreggate(groupedByRows, groupByFields, aggFunctions, fieldsToAggregate)
        

    def CreateKey(self, valuse):
        string_ints = [str(int) for int in valuse]
        return  ":".join(string_ints)
    
    def parsValues(self, key):
        strings = key.split(':')
        return [float(str) for str in strings]

    def Agreggate(self, groupedByRows, groupByFields, aggFunctions, fieldsToAggregate):
        rowID = 0
        sizeOfRow = len(self.columns.keys())
        allRows = [None]*len(groupedByRows.keys())
        for key in groupedByRows:
            allRows[rowID] = [0]*sizeOfRow 
            parsedValues = self.parsValues(key)
            id = 0
            for field in groupByFields:
                allRows[rowID][self.columns[field][ID]] = parsedValues[id]
                id+=1
            for field in groupedByRows[key]:
                allRows[rowID][self.columns[field][ID]] = groupedByRows[key][field]
            rowID+=1
        for row in allRows:
            id = 0
            for field in fieldsToAggregate: 
                row[self.columns[field][ID]] = AgreggateFunc[aggFunctions[id]](row[self.columns[field][ID]])
                id+=1
        return allRows
            
        
        

#25:45 var1 [3, 5, 6] var2 [] var3 [] .....



        