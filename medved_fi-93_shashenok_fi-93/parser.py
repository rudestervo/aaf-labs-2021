import sys
import re
from collection import Collection


def remove_first_spaces(query: str):
    return query.lstrip()


class Parser:
    def __init__(self):
        self.command = ''
        self.commands = ['create', 'insert', 'contains', 'search', 'exit', 'print_tree', 'help']
        self.args = sys.argv[1:]
        self.len_args = len(self.command)
        self.command_func = {
            'create': self.get_create_argument,
            'insert': self.get_insert_argument,
            'contains': self.get_contains_argument,
            'search': self.get_search_argument,
            'exit': self.exit,
            'print_tree': self.print_tree,
            'help': self.help
        }
        self.cl = Collection()
        self.collection_func = {
            'create': self.cl.create_collection,
            'insert': self.cl.insert_data,
            'search': self.cl.search,
            'print_tree': self.cl.print_tree
        }
        print('Enter "help;" to get list of commands')
        self.start_query()

    def start_query(self):
        query = ''
        while not query.endswith(';'):
            query = query + ' ' + input('>')
        for command in query.split(';'):
            if command:
                command = remove_first_spaces(command)
                self.command = re.split(',| ', command)
                self.len_args = len(self.command)
                self.get_arguments()
        self.start_query()

    def exit(self):
        quit()

    def clean_query(self, query):
        for word in query:
            if not word:
                query.remove(word)
        return query

    def get_command(self):
        clean_command = self.clean_query(self.command)
        command = clean_command[0].lower().strip()
        if command not in self.commands:
            print('ERROR! Wrong command')
            return None
        return command

    def print_tree(self):
        if self.command[0] == 'print_tree':
            return self.command
        else:
            print('ERROR! Incorrect command')
            return None

    def help(self):
        help_message = """
        PRINT_TREE;  -- prints tree structure --
        CREATE collection_name; -- create collection with entered name name "collection_name" --
        INSERT collection_name {val1, val2, ..., valn}; -- insert in collection set of values --
        CONTAINS collection_name {val1, val2, ..., valn}; -- check if values are in collection_name --
        SEARCH collection_name; -- get all values in collection --
        SEARCH collection_name WHERE [OPTIONS] {val1, val2, ..., valn}; -- search in collecection with option --
        #   SEARCH OPTIONS:
        #   INTERSECTS -- get sets from collection that intersects with entered set --
        #   CONTAINS -- get sets from collection that contains entered set (contain all of elements) -- 
        #   CONTAINED_BY -- get sets from collection that are subset of entered set --
        """
        print(help_message)
        return None

    def get_create_argument(self):
        if len(self.command) == 1:
            print('ERROR! Missing positional argument "collection_name"')
            return None
        if len(self.command) > 2:
            print(f'ERROR! Unnecessary positional arguments: {self.command[1:]}')
            return None
        return self.command[0].lower(), self.command[1]

    def get_insert_argument(self):
        if len(self.command) == 1:
            print('ERROR! Missing positional arguments "collection_name" and "values to insert"')
            return None
        if len(self.command) == 2:
            print('ERROR! Missing positional arguments "values to insert"')
            return None
        if not (self.command[2].startswith('{') and self.command[len(self.command) - 1].endswith('}')):
            print('ERROR! Syntax error in "values to insert"')
            return None
        values = []
        vals = []
        for arg in self.command[2:]:
            value = re.sub('[a-zA-Z]|,|{', '', arg)
            if value:
                if value.endswith('}'):
                    vals.append(int(value[:-1]))
                    values.append(vals)
                    vals = []
                    continue
                vals.append(int(value))
        return self.command[0].lower(), self.command[1].lower(), values

    def get_contains_argument(self):
        if len(self.command) == 1:
            print('ERROR! Missing positional arguments "collection_name" and "contained values"')
            return None
        if len(self.command) == 2:
            print('ERROR! Missing positional arguments "contained values"')
            return None
        if not (self.command[2].startswith('{') and self.command[len(self.command) - 1].endswith('}')):
            print('ERROR! Syntax error in "values to insert"')
            return None
        values = []
        for arg in self.command[2:]:
            value = re.sub('\D', '', arg)
            if value:
                values.append(int(value))
        return self.command[0].lower(), self.command[1], values

    def get_search_argument(self):
        search_queries = ['intersects', 'contains', 'contained_by']
        if len(self.command) == 1:
            print('ERROR! Missing positional arguments "collection_name"')
            return None
        if len(self.command) == 2:
            return self.command[0].lower(), self.command[1]
        if self.command[2].lower() != 'where':
            print('ERROR! Syntax error. To search by some option use command "WHERE" after collection name')
            return None
        if len(self.command) == 3:
            print('ERROR! Specify search option')
            return None
        if self.command[3].lower() not in search_queries:
            print('ERROR! Wrong option for search')
            return None
        if len(self.command) == 4:
            print('ERROR! Input values to search')
            return None
        if not (self.command[4].startswith('{') and self.command[len(self.command) - 1].endswith('}')):
            print('ERROR! Syntax error in "values to search"')
            return None
        values = []
        for arg in self.command[3:]:
            value = re.sub('[^0-9-]', '', arg)
            if value:
                values.append(int(value))
        return self.command[0].lower(), self.command[1], self.command[3].lower(), values

    def get_arguments(self):
        command = self.get_command()
        if not command:
            return None
        args = self.command_func[command]()
        self.run_collection_command(args)
        return args

    def run_collection_command(self, command):
        if command:
            command[0].lower()
            if command[0] == 'create':
                self.cl.create_collection(collection_name=command[1])
                return None
            if command[0] == 'insert':
                for arg in command[2]:
                    self.cl.insert_data(command[1], arg)
                return None
            if command[0] == 'search':
                if len(command) == 2:
                    self.cl.search(command[1])
                else:
                    self.cl.search(command[1], command[2], command[3])
                print(command)
                return None
            if command[0] == 'print_tree':
                self.cl.print_tree(command[1])
            if command[0] == 'contains':
                self.cl.contains(command[1], command[2])


if __name__ == '__main__':
    client = Parser()
