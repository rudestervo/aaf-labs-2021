from table import Table
from container import pass_tree_dfs, pass_tree
from interface import message



class Database:
    def __init__(self):
        self.T = [] # tables    
    
    def cmd(self,cmd):
        if cmd == None:
            return
        if cmd['cmd'] == "CREATE":
            self.create(cmd)
        elif cmd['cmd'] == "INSERT":
            self.insert(cmd)
        elif cmd['cmd'] == "DELETE":
            self.delete(cmd)
        elif cmd['cmd'] == "SELECT":
            self.select(cmd)
        else:
            message("[Incorrect command]")
            
    
    def create(self,cmd):
        if cmd['args'] == [] or cmd['args'] == None:
            message("[Create error]: incorrect columns list")
            return
        self.T.append(Table(cmd['table_name'], cmd['args'], cmd['condition']))
        message("[Created \"{}\" successfully]".format(cmd['table_name']))

        
    def delete(self,cmd):
        for table in self.T:
            if table.name == cmd['table_name']:
                table.delete(cmd['condition']['value1'], cmd['condition']['operator'], cmd['condition']['value2'])
                message("[Deleted successfully]")
        
        
    def display(self, cmd):
        for table in self.T:
            if table.name == cmd['table_name']:
                table.display()
        
    def insert(self, cmd):
        for table in self.T:
            if table.name == cmd['table_name']:
                table.insert(cmd['args'])
                message("[Inserted in  \"{}\" successfully]".format(cmd['table_name']))
            
        
        
    def select(self, cmd):
        
        for table in self.T:
            if table.name == cmd['table_name'] and not cmd["JOIN"]:
                if not cmd['args']:
                    cmd['args'] = table.cols
                if not cmd['condition']:
                    table.select(cmd['args'], 1, '=', 1, lambda x: x)
                else:
                    table.select(cmd['args'], cmd['condition']['value1'], cmd['condition']['operator'], cmd['condition']['value2'], lambda x: x)
                    
        if cmd["JOIN"]:
            for table in self.T:
                if table.name ==cmd['table_name']:
                    t1 = table
                if table.name ==cmd['join_table']:
                    t2 = table
            
            # read all tables into array
            arr1, arr2 = [],[]
            pass_tree_dfs(t1.data.root, t1.data.root, arr1)
            pass_tree_dfs(t2.data.root, t2.data.root , arr2)
            wide_table_to_disp = Table("wide", t1.cols + t2.cols, [False for i in range(len(t1.cols + t2.cols))], ordered=True)
           
            while len(arr1) < len(arr2):
                arr1.append(['' for i in range(len(arr1[0]))])

            while len(arr2) < len(arr1):
                arr2.append(['' for i in range(len(arr2[0]))])
        
             # joined to common table
                
                
              #  
                #
               # 
                #
               # 
                #
               ## 
        ####################
        # manage conditons
            try:
                a, b = cmd['join_args'] 
                if a in t1.cols:
                    i1 = t1.cols.index(a)
                    i2 = t2.cols.index(b)
                if a in t2.cols:
                    i1 = t1.cols.index(b) 
                    i2 = t2.cols.index(a)     
            except:
                message("enter valid command")  
                return
            a1, a2 = [], []
            
            for node1 in arr1:
                flag = False
                for node2 in arr2:
                    if str(node1[i1]) == str(node2[i2]):
                        wide_table_to_disp.insert(node1 + node2)  
                        flag = True
                if flag:
                    flag = False
                else:
                    a1.append(node1)
                #  a2.append(node2)                
            for node2 in arr2:
                flag = False
                for node1 in arr1:
                        if str(node1[i1]) == str(node2[i2]):
                            flag = True
                if flag:
                    flag = False
                else:
                    a2.append(node2)
                #  a2.append(node2)  
            
            for node1 in a1:
                wide_table_to_disp.insert(node1 + ['' for i in range(len(arr2[0]))])
            for node2 in a2:
                wide_table_to_disp.insert(['' for i in range(len(arr1[0]))] + node2)                
            if cmd['condition']:
                wide_table_to_disp.select(cmd['args'], cmd['condition']['value1'], cmd['condition']['operator'], cmd['condition']['value2'], lambda x: str(x))
            else:
                wide_table_to_disp.display()

        # wide_table.display()