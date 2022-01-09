import command_parser
import kdtree

import sys

from database import Database
from node import Node

if __name__ == '__main__':
    database = Database()
    List = []
    carry = ""
    while True:
        print("Enter command >:")
        text = carry + " " + sys.stdin.readline()
        if "exit" in text:
            break
        if ";" in text:
            tokens = command_parser.parse(text)
            for token in tokens:
                if token[0] == "CREATE":
                    database.create_table(token[1], List)
                elif token[0] == "INSERT":
                    database.insert(token[1], token[2], token[3], List)
                elif token[0] == "PRINT_TREE":
                    database.print_tree(token[1], List)
                elif token[0] == "CONTAINS":
                    database.contains(token[1], token[2], token[3], List)
                elif token[0] == "SEARCH":
                    database.search(token[1], List, token[2:])
                else:
                    print("Error: ", token)

            carry = " "
        else:
            carry = " " + text
