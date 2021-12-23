import command_parser
import sys

from database import Database

if __name__ == '__main__':
    database = Database()

    while True:
        text = input(">: ")

        if input == "exit":
            break
        while True:
            text += " " + sys.stdin.readline()

            if ";" in text:
                tokens = command_parser.parse(text)
                print(tokens[0])
                for token in tokens:
                    if token[0] == "CREATE":
                        database.create_table(token[1])
                    elif token[0] == "INSERT":
                        database.insert(token[1], token[2], token[3])
                    elif token[0] == "PRINT_TREE":
                        database.print_tree(token[1])
                    elif token[0] == "CONTAINS":
                        database.contains(token[1], token[2], token[3])
                    elif token[0] == "SEARCH":
                        database.search(token[1], token[2:])
                    else:
                        print("Error: ", token)
                break
