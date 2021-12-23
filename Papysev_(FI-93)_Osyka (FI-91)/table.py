from container import Tree, Row, pass_tree
from interface import message

import numpy as np

class Table:
    def __init__(self, name, cols, indexed_cols_mask, ordered=False):
        self.size = 1
        self.ordered = ordered
        self.name = name
        self.cols = cols
        self.w = 0
        self.imask = [i for i in range(len(indexed_cols_mask)) if indexed_cols_mask[i]]
        if self.imask == []:
            self.data = Tree(Row(0, np.random.randint(10000) + 1))
        else:
            self.data = Tree(Row(0, self.imask)) # create root non-used node
        message("Table {} 'created' operation finished".format(name))

    def __generate_index(self, values):
        index = [values[k] for k in self.imask]
        if not index:
            index = np.random.randint(10000) + 1
            message("[Warning]: default indexation used")
            if self.ordered:
                return self.size + 1
        return index
    

    def wideness(self):
            array = []
            pass_tree(self.data.root, self.data.root, array)
            widthes = []
            for row in array:
                widthes.append(max([len(str(col)) for col in row[0:-1]]))
            for val in self.cols:
                widthes.append(len(val))
            self.w = max(widthes) + 2
            return self.w


    def display(self, start=0, end=-1):
        array = []
        pass_tree(self.data.root, self.data.root, array)
        
        stxt = "+" + ("-"*self.wideness() + "+")*len(self.cols)
        txt = "|"
        for rn in self.cols:
            txt = txt + " " + str(rn)  + str(" "*max(self.wideness() - len(str(rn)) - 2 , 0)) + " |"

        message(stxt)
        message(txt)
        message(stxt)
        
        for row in array:
            rtxt = "|"
            for col in row[0:-1]:
                rtxt = rtxt + " " + str(col) + " "*max(self.wideness() - len(str(col)) - 2 , 0) + " |"
            message(rtxt)
        message(stxt)

    def insert(self, values):
        self.size += 1
        if  len(values) == len(self.cols):
            for key in self.imask:
                values[key] = int(values[key])
            index = self.__generate_index(values)
            if index:
                row = Row(values, index)
                ####################################
                self.data.add(row)
        else:
            message("[Insert error]: row size incorrect")
            
            
    def delete(self, operand1, sign, operand2):
                
        array, arr = [], []
        pass_tree(self.data.root, self.data.root, arr)
        
        if operand1 and sign and operand2:
            if operand1 in self.cols:
                i1 = self.cols.index(operand1)
                val = operand2
            elif operand2 in self.cols:
                i1 = self.cols.index(operand2)
                val = operand1
            else:
                message("[Delete error]: incorrect operand")
                return
                
            if i1 in self.imask:
                try:
                    val = int(val)
                except:
                    pass
            # get all table in array view
            
            if sign == '=':
                array = [row for row in arr if row[i1] == val]                 
            elif sign == "!=":
                array = [row for row in arr if not row[i1] == val]
            elif sign == ">":
                array = [row for row in arr if row[i1] > val]
            elif sign == "<":
                array = [row for row in arr if row[i1] < val]
            elif sign == ">=":
                array = [row for row in arr if row[i1] >= val]
            elif sign == "<=":
                array = [row for row in arr if row[i1] <= val]        
            else:
                message("[Delete error]: incorrect operation")    
             # delete all
            for row in array:
                self.data.delete(self.data.root, row[len(row)-1])
                
        else:
            for row in arr:
                self.data.delete(self.data.root, row[len(row)-1])

        
        
        
    def select(self, cols, operand1, sign, operand2, f):
        if cols == [] or cols == None:
            cols = self.cols
        # get all table in array view
        array, arrr, arr = [], [], []
        pass_tree(self.data.root, self.data.root, arrr)
        for c in cols:
            if c not in self.cols:
                message("[Select error]: incorrect column names")
                return
             
        for row in arrr:
            a = []
            for col in cols:
                a.append(row[self.cols.index(col)])
            arr.append(a)

        ####################
        # manage conditons
        if operand1 in self.cols and operand2 in self.cols:
            if operand1 not in cols or operand2 not in cols:
                message("[Select error]: incorrect command")
            i1, i2 = self.cols.index(operand1),  self.cols.index(operand2)
            if sign == '=':
                array = [row for row in arr if f(row[i1]) == f(row[i2])]                
            elif sign == "!=":
                array = [row for row in arr if not f(row[i1]) == f(row[i2])]
            elif sign == ">":
                array = [row for row in arr if f(row[i1]) > f(row[i2])]
            elif sign == "<":
                array = [row for row in arr if f(row[i1]) < f(row[i2])]
            elif sign == ">=":
                array = [row for row in arr if f(row[i1]) >= f(row[i2])]
            elif sign == "<=":
                array = [row for row in arr if f(row[i1]) <= f(row[i2])]        
            else:
                message("[Select error]: incorrect operation")
              
        elif operand1 in self.cols and operand2 not in self.cols:
            i1 = self.cols.index(operand1)

            if sign == '=':
                array = [row for row in arr if f(row[i1]) == f(operand2) ]                
            elif sign == "!=":
                array = [row for row in arr if not f(row[i1]) == f(operand2) ]
            elif sign == ">":
                array = [row for row in arr if f(row[i1]) > f(operand2) ]
            elif sign == "<":
                #print("COMP", row[i1], operand2)
                array = [row for row in arr if f(row[i1]) < f(operand2)]
            elif sign == ">=":
                array = [row for row in arr if f(row[i1]) >= f(operand2) ]
            elif sign == "<=":
                array = [row for row in arr if f(row[i1]) <= f(operand2) ]        
            else:
                message("[Select error]: incorrect operation")
        elif operand1 not in self.cols and operand2 in self.cols:

            i2 = self.cols.index(operand2)
            if sign == '=':
                array = [row for row in arr if f(operand1) == f(row[i2]) ]                
            elif sign == "!=":
                array = [row for row in arr if not f(operand1)  == f(row[i2]) ]
            elif sign == ">":
                array = [row for row in arr if f(operand1)  > f(row[i2]) ]
            elif sign == "<":
                array = [row for row in arr if f(operand1)  < f(row[i2]) ]
            elif sign == ">=":
                array = [row for row in arr if f(operand1)  >= f(row[i2]) ]
            elif sign == "<=":
                array = [row for row in arr if f(operand1)  <= f(row[i2]) ]        
            else:
                message("[Select error]: incorrect operation")    
        else:
            if sign == '=':
                array = [row for row in arr if f(operand1)  == f(operand2) ]                
            elif sign == "!=":
                array = [row for row in arr if not f(operand1)  == f(operand2) ]
            elif sign == ">":
                array = [row for row in arr if f(operand1)  > f(operand2) ]
            elif sign == "<":
                array = [row for row in arr if f(operand1)  < f(operand2) ]
            elif sign == ">=":
                array = [row for row in arr if f(operand1)  >= f(operand2) ]
            elif sign == "<=":
                array = [row for row in arr if f(operand1)  <= f(operand2) ]        
            else:
                message("[Select error]: incorrect operation")    
            
        stxt = "+" + ("-"*self.wideness() + "+")*len(cols)
        txt = "|"
        for rn in cols:
            txt = txt + " " + str(rn)  + str(" "*max(self.wideness() - len(rn) - 2 , 0)) + " |"

        message(stxt)
        message(txt)
        message(stxt)
        for row in array:
            rtxt = "|"
            for col in row:
                rtxt = rtxt + " " + str(col) + " "*max(self.wideness() - len(str(col)) - 2 , 0) + " |"
            message(rtxt)
        message(stxt)  
        


