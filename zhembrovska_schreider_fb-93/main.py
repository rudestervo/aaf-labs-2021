from lexpar import *
from table import *

def menu():
    table = Table()
    while True:
        try:
            cmd = input('< ')
            command, data = lexpar(cmd)
            if command == 'exit': break
            if command == 0 or data == 0:
                print('wrong command')
                continue
            if command == 'CREATE':
                table.create(data)
            elif command == 'INSERT':
                table.insert(data)
            elif command == 'SELECT':
                table.select(data)
            elif command == 'DELETE':
                table.delete(data)
            table.print_table()
        except:
            print('ups. error(')



 