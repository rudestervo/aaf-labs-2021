from table import *
from cond_parser_tuple import postorder, parse
from imp_lexer import imp_lex

class DB:

    def __init__(self):
        self.tables = []

    def create(self, table_name, col_dict):
        if col_dict:
            for i in self.tables:
                if i.table_name == table_name:
                    print("table already exist")
                    break
            else:
                table = Table()
                table.create(table_name, col_dict)
                self.tables.append(table)
        else:
            print("give a column name")

    def insert(self, table_name, value):
        for table in self.tables:
            if table.table_name == table_name:
                table.insert(value)
                break
            else:
                print("table not exist")

    def select(self, table_name, col_name, cond=None):
        for table in self.tables:
            if table.table_name == table_name:
                if cond:
                    _, stacked_cond = postorder(cond)
                    table.cond_select(col_name, stacked_cond)
                else:
                    table.simple_select(col_name)
                break
            else:
                print("table not exist")

    def delete(self, table_name, cond=None):
        for table in self.tables:
            if table.table_name == table_name:
                if cond:
                    _, stacked_cond = postorder(cond)
                    table.delete_rows(stacked_cond)
                else:
                    print(f"table {table.table_name} was dropped")
                    table.value.clear()
                    break
            else:
                print("table not exist")
# db = DB()
# db.create("dogs", ['s', 'ff', 'aaa'])
# db.insert("dogs", ["s1", 'ff2', 'aaa1'])
# db.insert("dogs", ["s2", 'ff2', 'aaa2'])
# db.insert("dogs", ["nnn1", 'ff2', 'aaa1'])
# db.insert("dogs", ["s3", 'f', 'aaa3'])
# db.insert("dogs", ["nnn1", 'fr1', 'aaa1'])
# db.insert("dogs", ["s3", 'ff2', 'aaa1'])
# db.select("dogs", ["*"])
# cond = imp_lex('(a>"4")')
# ast = parse(cond)
# print(postorder(ast))
# db.select("dogs", ["*"], ast)
# db.delete("dogs", ast)
# db.select("dogs", ["*"])
# db.select("dogs", ["aaa", "ff"])
# db.select("dogs", ["aaa", "ff", "ff333"])
# db.delete("dog")
# db.delete("dogs")
# create dog(ff,aaa);
# Table dog has been created
# insert into dog("sss","shiba);
# insertion failed
# insert into dog("sss","shiba';
# invalid command
# insert into dog("sss","shiba");
# invalid command
