from typing import Text
import re, sys, os
from RDtree import *


keywords=['CREATE','INSERT','PRINT_TREE','CONTAINS','SEARCH','SEARCH_TREE','EXIT']
keywords_search =['INTERSECTS','CONTAINED_BY','CONTAINS','WHERE','EXIT']
tree = RDtree()
class Interpreter(object):
    interpreter_buff = {}
    def __init__(self,text):
        self.text=Text
    def interpreter(self,text):
        k=text.split(';')
        for i in range(len(text.split(';'))-1):
            text=k[i]
            text=text.replace(';', "")
            text =  text.replace('\n', ' ')
            text =  text.replace('  ', ' ')
            text =  text.replace('  ', ' ')
            text =  text.replace('   ', ' ')
            text=text.replace(',', "")
            text=text.split()
            command = text[0]
            if command.upper()==keywords[0]:#create               
                try:
                        self.Create(text)
                except:
                        print("Error. Can`t create collection")
            elif command.upper() == keywords[1]:#insert
                try:
                     self.Insert(text)
                     print("Set has been added " )
                except:
                    print("Error.Can`t insert")
            elif command.upper() == keywords[2]:#print_tree
                try:
                    self.Print(text)  
                except:
                    print("Error. Can`t print tree")              
            elif command.upper() == keywords[3]:#contains
                try:
                    print("Contains")
                    self.Contains(text)
                except:
                    print("Error. Can`t execute contains command")             
            elif command.upper() == keywords[4]:#search
                # self.Search(text)
                search_command = text[3]
                if search_command.upper()==keywords_search[0]:
                    try:
                        self.Intersects(text)
                    except: print("Can`t intersect collection")
                if search_command.upper()==keywords_search[1]:
                    try:
                        self.Contained_By(text)
                    except: print("Can`t execute contained_by command")
                if search_command.upper()==keywords_search[2]:
                    try:
                        self.Contains_Where(text)
                    except: print("Can`t execute where contains command")
            elif command.upper() == keywords[5]:#_search
                try:
                    self.Search(text)
                except: print("Error in search")
            elif command.upper() == keywords[6]:#exit
                try:
                    print("Work finished")
                    os.system("taskkill /F /PID "  + str(os.getpid()))                   
                except:
                    pass
            else:
                print("Error, command not exist")
#     def analyzer(command):
#         if(re.match(r'CREATE \w+',command)):
#                 return True
#         elif(re.match(r'INSERT \w+',command)):
#                 return True
#         elif(re.match(r'PRINT_TREE \w+',command)):
#                 return True
#         elif(re.match(r'SEARCH \w+ WHERE (INTERSECTS|CONTAINS|CONTAINED_BY)',command)):
#                 return True
        
    def Create(self,text):
        try:
                # buffer =[]
                # buffer.append({text[1]:[]})
                collection_name=text[1]
                collection_name=collection_name.replace(';',"")
                print(print("Collection "+ collection_name +" has been created"))
                self.interpreter_buff[collection_name]=None
        except:
                print("Error in creating ")  

    def Insert(self, text):
        if text[1] in self.interpreter_buff.keys():
            try:
                k=text[3:-1]
            # print(k)
                ch=[]
                for ik in range(len(k)):
                    ch.append(int(k[ik]))
                self.insert_data(text[1], ch)
                # global l
                # global m
                tree.l= tree.l + ch
                print(tree.l)
                tree.m.append(ch)
            except:
                pass
        else: print("This collection ", text[1]," isn`t exists")

    def insert_data(self,collection_name: RDtree, data):
            root = self.interpreter_buff[collection_name]
            self.interpreter_buff[collection_name]=tree.insert(root,set(data))

    def Print(self,text):
        if text[1] in self.interpreter_buff.keys():
            try:
                self.print_tree(text[1])
            except:
                print('Error')
        else: print("This collection ", text[1]," isn`t exists")

    def print_tree(self, collection_name):
        print("Printing ",collection_name," tree:")
        root = self.interpreter_buff[collection_name]
        tree.tree_to_dict(root)
        print(" ")

    def Contains(self,text):
        if text[1] in self.interpreter_buff.keys():
            try:
                k = text[3:-1]
                print(k)
                for i in range(len(k)):
                    k[i]=int(k[i])
                print(set(k).issubset(tree.l))
                print(k)
            except:
                print("Error")
        else: print("This collection ", text[1]," isn`t exists")

    def Search(self, text):
        if text[1] in self.interpreter_buff.keys():
            try:
                k=text[3:-1]
                for i in range(len(k)):
                        k[i]=int(k[i])
                self.search_tree(text[1],k)
            except: print("Error")
        else: print("This collection ", text[1]," isn`t exists")
    
    def search_tree(self, collection_name, value:set):
        root=self.interpreter_buff[collection_name]
        a = tree.tree_search(root,set(value))
        if (a): print("Yes")
        else: print("No")
        
    def Intersects(self, text):
        if text[1] in self.interpreter_buff.keys():
            try:
                k = text[5:-1]
                for i in range(len(k)):
                    k[i]=int(k[i])
                if(self.intersect_tree(text[1],k)):
                    for list in tree.m:
                        if(set(k).intersection(list)): print(list)
                else: print ("No intersection")
            except: print("Error")
        else: print("This collection ", text[1]," isn`t exists")

    def intersect_tree(self,collection_name, value):
        root=self.interpreter_buff[collection_name]
        result= tree.search_where_intersects(root, set(value))
        return result

    def Contained_By(self,text):
        if text[1] in self.interpreter_buff.keys():
            try:
                k = text[5:-1]
                for i in range(len(k)):
                    k[i]=int(k[i])
                    for list in tree.m:
                        if(set(k).issuperset(list)): print(list) 
            except:
                print("Error")
        else: print("This collection ", text[1]," isn`t exists") 

    def contained_by_tree(self, collection_name, value):
        root=self.interpreter_buff[collection_name]
        res = tree.search_where_contained_by(root, set(value))
        return res

    def Contains_Where(self,text):
        if text[1] in self.interpreter_buff.keys(): 
            try:
                k = text[5:-1]
                for i in range(len(k)):
                    k[i]=int(k[i])
                if(self.contains_tree(text[1],k)):
                    for list in tree.m:
                        if(set(k).issubset(list)): print(list)
                else: print ("No match")
            except:
                print("Error")
        else: print("This collection ", text[1]," isn`t exists")

    def contains_tree (self, collection_name, value):
          root=self.interpreter_buff[collection_name]
          res = tree.search_where_contains(root,set(value))
          return res
