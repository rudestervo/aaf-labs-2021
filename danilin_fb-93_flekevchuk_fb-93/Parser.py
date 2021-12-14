from MyTokens.Token import Token
from MyTokens.TokenPaterns import TokenPaterns
from collections import deque

class Parser:
    __pos = 0
    def __init__(self,DB):
        self.__tokens = []
        self.DB = DB

    def setTokens(self, tokens):
        self.__tokens = tokens
    def Insert(self, tokenLen):
        varsToInsert = list()
        if(self.__tokens[1].type != "VAR"):
            raise Exception ("Unknown table name")
        if(self.__tokens[2].type != "("):
            raise Exception ("( Expected")
        if(self.__tokens[tokenLen-1].type != ")"):
            raise Exception (") Expected")

        for i in range (3,tokenLen):# INSERT INTO name (var1,var2,...)
            if(self.__tokens[i].type == ")"):
                break
            if(i % 2 == 1):
                if (self.__tokens[i].type != "NUMBER"):
                    raise Exception ("Unknown token on position ", i)
                varsToInsert.append(int(self.__tokens[i].text))
            if(i % 2 == 0):
                if (self.__tokens[i].type != "COMMA"):
                    raise Exception ("Unknown token on position ", i)
            
        self.DB.Insert(self.__tokens[1].text, varsToInsert)
    
    def CreateTable(self, tokenLen):
        
            if(self.__tokens[1].type != "VAR"):
                raise Exception ('Incorrect table name')
            
            if(self.__tokens[2].type != "("):
                raise Exception (' ( expected ')
            
            if(self.__tokens[3].type != "VAR"):
                raise Exception (' Incorrect field name ')
            
            if(self.__tokens[tokenLen-1].type != ")"):
                raise Exception (' ) expected ')
            
            colums = list()
            
            indexedFields = list()

            colums.append(self.__tokens[3].text)

            oldTokenType = "VAR"
            if(tokenLen > 5):
                for i in range(4 ,tokenLen):
                    newTokenType = self.__tokens[i].type
                    if(newTokenType != "INDEXED" and newTokenType != "COMMA" and newTokenType != ")" and oldTokenType == "VAR"):
                        raise Exception ('Unexpected token on position ', i)
                    if(newTokenType != "VAR" and oldTokenType == "COMMA"):
                        raise Exception ('Unexpected token on position ', i)
                    if(newTokenType != "COMMA" and oldTokenType == "INDEXED"):
                        raise Exception ('Unexpected token on position ', i)
                    if(newTokenType == ")" and (oldTokenType != "VAR" and oldTokenType != "INDEXED")):
                        raise Exception ('Unexpected ) on position ', i)
                    if (newTokenType == "INDEXED"):
                        indexedFields.append(self.__tokens[i-1].text)
                        oldTokenType = "INDEXED"
                    if(newTokenType == "VAR"):
                        colums.append(self.__tokens[i].text)
                        oldTokenType = "VAR"
                    if(newTokenType == "COMMA"):
                        oldTokenType = "COMMA"    
            self.DB.CreateTable(self.__tokens[1].text,colums,indexedFields)


    def Delete(self, tokenLen):
        if(self.__tokens[1].type != "FROM"):
            raise Exception ("FROM expected")
        if(self.__tokens[2].type != "VAR"):
            raise Exception ("Unknown table name")

        if(self.__tokens[3].type != "WHERE"):
            raise Exception ("WHERE expected")
        if(self.__tokens[4].type != "VAR"):
            raise Exception ("Unknown token on position 4")
        if(self.__tokens[5].type != "EQUAL" and 
        self.__tokens[5].type != "NOT_EQUAL" and 
        self.__tokens[5].type != "MORE_EQUAL" and 
        self.__tokens[5].type != "LESS_EQUAL" and
        self.__tokens[5].type != "LESS" and
        self.__tokens[5].type != "MORE"):
            raise Exception ("Unknown token on position 5")
        if(self.__tokens[6].type != "VAR" and self.__tokens[6].type != "NUMBER"):
            raise Exception ("Unknown token on position 6")
            
        print("Deleting from " + self.__tokens[2].text)
        self.DB.Delete(self.__tokens[2].text, self.__tokens[4], self.__tokens[5], self.__tokens[6])

    def Select(self, tokenLen):

        aggregationTypes = ['COUNT_DISTINCT', 'COUNT', 'MAX', 'AVG']
        allTokenTypes = []
        fromPosition = 0
        wherePosition =0
        groupByPosition = 0
        colums = list()
        tableName = ''
        fieldsToAggregate = list()
        aggFunctions =list()
        groupByFields = list()

        for i in range(0, tokenLen):
            allTokenTypes.append(self.__tokens[i].type)
            if self.__tokens[i].type in aggregationTypes:
                aggFunctions.append(self.__tokens[i].text)

        if (self.__tokens[1].type != "VAR" and self.__tokens[1].type != "ALL" and  self.__tokens[1].type not in aggregationTypes ):
                 raise Exception ("Unknown token on position 1")
            
        isAllInSelect = False
        if(self.__tokens[1].type == "ALL"):
            isAllInSelect= True
            if(self.__tokens[2].type != "FROM"):
                raise Exception ("Unknown token on position 2")

        i=1
        while i <= tokenLen: 
            if(isAllInSelect):
                break
            if(self.__tokens[i].type == "FROM"):
                break
            if(self.__tokens[i].type == "VAR"):
                colums.append(self.__tokens[i].text)  
                if (self.__tokens[i+1].type != "COMMA"):
                    if(self.__tokens[i+1].type != "FROM"):
                        raise Exception ("Unknown token on position ", i+1)
                i +=1
            if(self.__tokens[i].type == "COMMA"):
                if(self.__tokens[i+1].type != "VAR" ):
                    if(self.__tokens[i+1].type not in aggregationTypes):
                        raise Exception ("Unknown token on position ", i+1)
                i+=1
            if(self.__tokens[i].type in aggregationTypes):
                if(self.__tokens[i+1].type != "(" and self.__tokens[i+2].type != "VAR" and self.__tokens[i+3].type != ")"):
                    raise Exception ("Aggregation Error!")
                fieldsToAggregate.append(self.__tokens[i+2].text)
                colums.append(self.__tokens[i+2].text)
                i +=4
                    
             
        if 'FROM' not in allTokenTypes:
            raise Exception ("FROM Expected")
        else:
            fromPosition = allTokenTypes.index('FROM') 

        if(self.__tokens[fromPosition + 1].type != "VAR"):
            raise Exception ("Expected Table Name")
        else:
            tableName = self.__tokens[fromPosition + 1].text
            
        if 'WHERE' not in allTokenTypes:
            wherePosition = -1
        else:
            wherePosition = allTokenTypes.index('WHERE') 
        
        if(wherePosition != -1):
            if(self.__tokens[wherePosition].type != "WHERE"):
                raise Exception ("WHERE Expected")
            if(self.__tokens[wherePosition+1].type != "VAR"):
                raise Exception ("Unknown token on position ", wherePosition+1)
            if(
            self.__tokens[wherePosition +2].type != "EQUAL" and 
            self.__tokens[wherePosition +2].type != "NOT_EQUAL" and 
            self.__tokens[wherePosition +2].type != "MORE_EQUAL" and 
            self.__tokens[wherePosition +2].type != "LESS_EQUAL" and
            self.__tokens[wherePosition +2].type != "LESS" and
            self.__tokens[wherePosition +2].type != "MORE"):
                raise Exception ("Unknown token on position ", wherePosition+2)
            if( self.__tokens[wherePosition +3].type != "VAR" and self.__tokens[wherePosition +3].type != "NUMBER"):
                raise Exception ("Unknown token on position ", wherePosition+3)

        #variables to send condition
        var1 = self.__tokens[wherePosition+1] 
        cond = self.__tokens[wherePosition+2]
        var2 = self.__tokens[wherePosition+3]
        
        if 'GROUPBY' not in allTokenTypes:
            groupByPosition = -1
        else:
            groupByPosition = allTokenTypes.index('GROUPBY')

        if(groupByPosition != -1):
            for i in range(groupByPosition+1, tokenLen):
                if (self.__tokens[i].type == "VAR"):
                    groupByFields.append(self.__tokens[i].text)
                if (self.__tokens[i].type == "COMMA" and self.__tokens[i+1].type != "VAR"):
                    raise Exception ("Variable expected on position ", i+1)

        self.DB.Select(tableName ,colums, var1, cond ,var2, groupByFields, aggFunctions, fieldsToAggregate)
            
            
    def parse(self):
        tokenLen = len(self.__tokens)
        if(tokenLen == 0):
            raise Exception ('Empty token array!')
        
        if(self.__tokens[0].type != "CREATETABLE" and self.__tokens[0].type != "SELECT" and self.__tokens[0].type != "DELETE" and self.__tokens[0].type != "INSERTINTO"):
            raise Exception ('Unknown comand!')

        if(self.__tokens[0].type == "CREATETABLE"):
            self.CreateTable(tokenLen)

        if(self.__tokens[0].type == "DELETE"):
            self.Delete(tokenLen)

        if(self.__tokens[0].type == "INSERTINTO"):
            self.Insert(tokenLen)
        
        if(self.__tokens[0].type == "SELECT"):
            self.Select(tokenLen)
