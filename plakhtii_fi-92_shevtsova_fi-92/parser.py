# command:
#     CREATE set_name;
#     INSERT set_name (x, y);
#     PRINT_TREE set_name;
#     CONTAINS set_name (x, y);
#     SEARCH set_name [WHERE query];
#             query := INSIDE (x_left, y_bottom), (x_right, y_top)
#             | LEFT_OF x
#             | NN (x, y)
import re
from R_Tree_To_compile.build.R_Tree import R_Tree, Rect

from database import Database


class Parser:
    def __init__(self):
        self.database = Database()

    def main(self):
        while True:
            inpt = ''
            inpt = input("=> ")
            if inpt:
                command, properties = self.get_command(inpt)
                if command.upper() == 'CREATE':
                    self.create(properties)
                elif command.upper() == 'INSERT':
                    self.insert(properties)
                elif command.upper() == 'PRINT_TREE':
                    self.print_tree(properties)
                elif command.upper() == 'CONTAINS':
                    self.contains(properties)
                elif command.upper() == 'SEARCH':
                    self.search(properties)
                else:
                    print("Wrong command!")

    def get_command(self, inpt: str):
        command = inpt.split()[0]
        properties = " ".join(inpt.split()[1:])
        return command, properties

    def create(self, properties):
        regex = r'^(\w+)\s*;\s*$'
        res = re.match(regex, properties)
        if res:
            name = res.group(1)
            if not self.database.contain(name):
                self.database.create_table(name)
                print("Set {} has been created".format(name))
            else:
                print('Table with same name already exist! name: {}'.format(name))
                return
        else:
            print("Wrong command!")
            return

    def insert(self, properties):
        regex = r'^(\w+)\s+\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*;\s*$'
        res = re.match(regex, properties)
        if res:
            name = res.group(1)
            x = int(res.group(2))
            y = int(res.group(3))
            if self.database.contain(name):
                self.database[name].insert(x, y)
                print("Point ({}, {}) has been added to {}".format(x, y, name))
            else:
                print("Table: {} not exist!".format(name))
                return


        else:
            print("Wrong command!")
            return

    def print_tree(self, properties):
        regex = r'^(\w+)\s*;\s*$'
        res = re.match(regex, properties)
        if res:
            name = res.group(1)
            if self.database.contain(name):
                self.database[name].print_tree()
            else:
                print("Table: {} not exist!".format(name))
                return
        else:
            print("Wrong command!")
            return

    def contains(self, properties):
        regex = r'^(\w+)\s+\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*;\s*$'
        res = re.match(regex, properties)
        if res:
            name = res.group(1)
            x = int(res.group(2))
            y = int(res.group(3))
            if self.database.contain(name):
                print(self.database[name].is_contain(x, y))
            else:
                print("Table: {} not exist!".format(name))
                return


        else:
            print("Wrong command!")
            return

    def search(self, properties):
        regex = r'^(\w+)\s+(\w+)(.*);\s*$'
        empty_search_regex = r'^(\w+)\s*;\s*$'
        res = re.match(regex, properties)
        if res:
            name = res.group(1)
            where = res.group(2)
            query = res.group(3)
            if self.database.contain(name):
                if where.upper() == "WHERE":
                    command = query.split()[0]
                    parameters = " ".join(query.split()[1:])
                    if command.upper() == "INSIDE":
                        self.inside(parameters, name)
                    elif command.upper() == "LEFT_OF":
                        self.left_of(parameters, name)
                    elif command.upper() == "NN":
                        self.nn(parameters, name)
                else:
                    print("Wrong command!")
                    return
            else:
                print("Table: {} not exist!".format(name))
                return
        else:
            res = re.match(empty_search_regex, properties)
            if res:
                name = res.group(1)
                if self.database.contain(name):
                    self.database[name].get_all()
                else:
                    print(f"Table: {name} not exist!")
                    return
            else:
                print("Wrong command!")
                return

    def inside(self, parameters, name):
        regex = r'^\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*,\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*'
        res = re.match(regex, parameters)
        if res:
            ltx = float(res.group(1))
            lty = float(res.group(2))
            rbx = float(res.group(3))
            rby = float(res.group(4))
            self.database[name].search(ltx, lty, rbx, rby)
        else:
            print("Wrong parameters!")

    def left_of(self, parameters, name):
        res = re.match(r'^\s*(-?\d+)\s*$', parameters)
        if res:
            x = int(res.group(1))
            self.database[name].left_of(x)
        else:
            print("Wrong parameters!")
            return

    def nn(self, parameters, name):
        regex = r'^\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*'
        res = re.match(regex, parameters)
        if res:
            x = int(res.group(1))
            y = int(res.group(2))
            self.database[name].nn(x, y)

        else:
            print("Wrong parameters!")
            return


try:
    parser = Parser()
    parser.main()

except Exception as ex:
    print(ex)
