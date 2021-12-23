from sortedcontainers import SortedDict

# Indexing for columns
class indexColumns:
    def __init__(self):
        self.container = SortedDict()

    def insert(self, value, pointer):
        # Return key value if it is available in the dictionary
        self.container.setdefault(value, set()).add(pointer)

# Database 
class db:
    def __init__(self, table_name, columns):
        self.name = table_name
        self.table = {}
        self.columns = {}
        self.row_id = 0
        self.index = {}

        # Indexing
        for i, (column_name, index_flag) in enumerate(columns):
            self.columns[column_name] = i
            if index_flag == True:
                self.index[i] = indexColumns()

    # Insert rows to database table
    def insert(self, table_name, values):
        rows_insert = []
        if len(values) != len(self.columns):
            print(f"Invalid amount of values to insert into {table_name}!")
        else:
            row = self.row_id
            #print(f"self.columns  {self.columns}")
            for indexed_columns in self.index:
                #print(f"index[indexed-col]   {self.index[indexed_columns]}")
                row_i = list(self.columns.keys())[list(self.columns.values()).index(indexed_columns)]
                col_i = int(self.columns[row_i])
                #print(f"row_i   {row_i}")
                #print(f"col_i   {col_i}")
                #print(f"index[row_i]   {self.index[col_i]}")
                self.index[col_i].insert(values[col_i], row)
            self.table[row] = values
            self.row_id += 1
            rows_insert.append(values)
        return rows_insert

# Storager
class storager:
    def __init__(self):
        self.table = {}

    # Create Database
    def create_db(self, table_name, columns):
        if columns:
            self.table[table_name] = db(table_name, columns)
            print(f"Table {table_name} has been successfully created!")
        else:
            print(f"Table {table_name} columns are empty!")

    # Insert data to storage
    def insert_db(self, table_name, values):
        if table_name not in self.table:
            print(f"Table {table_name} does not exist!")
        else:
            if len(values) != len(self.table[table_name].columns):
                print(f"Invalid amount of values to insert into {table_name}!")
            else:
                rows_insert = self.table[table_name].insert(table_name, values)
                print(f"{len(rows_insert)} row(s) has been inserted into {table_name}!")

    def select_db(self, table_name, columns, condition, order):
        #print(f"Select {columns} from {table_name}!")
        # Check table existance in database
        if table_name not in self.table:
            print(f"Table {table_name} does not exist!")
        else:
            for column in columns:
                # Check columns existance in table
                if column not in self.table[table_name].columns:
                    print(f"Invalid values to select from database!")
                else:


if __name__ == "__main__":
    storage = storager()
    index = indexColumns()
