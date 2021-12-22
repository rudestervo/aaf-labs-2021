import re
from cond_parser_tuple import *
from imp_lexer import *

def parse_create(tokens):
    if tokens[0][1] == "T_CREATE":
        com_name = tokens.pop(0)
        table_name = tokens.pop(0)
        match(tokens, "T_LPAR")
        col_name = {}
        for i in range(len(tokens)):
            if tokens[i][1] == "T_STR":
                if tokens[i + 1][1] == "T_INDEXED":
                    col_name[tokens[i][0]] = 1
                else:
                    col_name[tokens[i][0]] = 0
        if tokens[-2][1] != "T_RPAR" or tokens[-1][1] != "T_END":
            print("syntx error")
            return None
        return com_name, table_name[0], col_name


# com = imp_lex("CREATE cats (id INDEXED, name INDEXED, favourite_food)")
# print(com)
# print(parse_create(com))

def parse_insert(tokens):
    if tokens[0][1] == "T_INSERT":
        com_name = tokens.pop(0)
        table_name = tokens.pop(0)[0]
        match(tokens, "T_LPAR")
        col_name = []
        for i in range(len(tokens)):
            if tokens[i][1] == "T_VALUE":
                val = tokens[i][0]
                col_name.append(find_between(val,'"', '"'))
            if tokens[-2][1] != "T_RPAR" or tokens[-1][1] != "T_END":
                print("syntx error")
        return com_name, table_name, col_name


# com = imp_lex('INSERT INTO cats ("1", "Murzik", "Sausages")')
# print(parse_insert(com))

def parse_select(tokens):
    col_name = []
    icond = None
    if tokens[0][1] == "T_SELECT":
        com_name = tokens[0]
        for i in range(len(tokens)):
            if tokens[i][1] == "T_WHERE":
                icond = i
        if icond:
            for i in range(icond):
                if tokens[i][1] == "T_ALL" or tokens[i][1] == "T_STR":
                    col_name.append(tokens[i][0])
            cond = parse(tokens[icond + 1:])
            tab_name = col_name.pop(-1)
            return com_name,tab_name, col_name,  cond
        else:
            for i in range(len(tokens)):
                if tokens[i][1] == "T_ALL" or tokens[i][1] == "T_STR":
                    col_name.append(tokens[i][0])
            tab_name = col_name.pop(-1)
            return com_name, tab_name, col_name

# com1 = imp_lex('SELECT * FROM cats')
# string = imp_lex('SELECT id, favourite_food FROM cats WHERE (name <= "Murzik") OR (name = "Pushok")')
# print(parse_select(string))
# print(parse_select(com1))


def parse_delete(tokens):
    icond = None
    if tokens[0][1] == "T_DELETE":
        com_name = tokens[0]
        for i in range(len(tokens)):
            if tokens[i][1] == "T_WHERE":
                icond = i
        if icond:
            tab_name = tokens[icond-1][0]
            cond = parse(tokens[icond+1:])
            return com_name, tab_name, cond
        else:
            for i in range(len(tokens)):
                if tokens[i][1] == "T_STR":
                    tab_name = tokens[i][0]
            return com_name, tab_name

# com1 = imp_lex('DELETE FROM cats')
# com2 = imp_lex('DELETE cats WHERE name = "Murzik"')
# com3 = imp_lex('DELETE cats WHERE id != "2"')
# print(parse_delete(com1))
# print(parse_delete(com2))
# print(parse_delete(com3))

def all_parse(input):
    tokens = imp_lex(input)
    if tokens[0][1] == "T_CREATE":
        return parse_create(tokens)
    elif tokens[0][1] == "T_INSERT":
        return parse_insert(tokens)
    elif tokens[0][1] == "T_SELECT":
        return parse_select(tokens)
    elif tokens[0][1] == "T_DELETE":
        return parse_delete(tokens)
    else:
        print("wrong command name")

#TODO debug CLI
def many_lines_input():
    contents = []
    while True:
        line = input()
        if line.find(";") != -1:
            line = line[:line.find(";")]
            contents.append(line)
            break
        elif re.match(r"\.(?i)exit", line):
            return line
        else:
            contents.append(line)
# spaces del
    str1 = " ".join(contents)
    return " ".join(str1.split())



def parse666():
    string = many_lines_input()
    if re.match(r"(?i)\.exit", string):
        return ".EXIT"
    else:
        return all_parse(string)


# com = all_parse('SELECT id, favourite_food FROM cats WHERE (name = "Murzik") AND (dog = "shiba")')
# com1 = all_parse('SELECT id, favourite_food FROM cats')
# com3 = all_parse('CREATE cats (id INDEXED, name INDEXED, favourite_food)')
# com = parse666()
# printPostorder(com[3])
# print(com1)
# print(com3)
# com4 = all_parse('select a from dogs where (a>"4") or ("4"<=bb)')
# print(com4)


# if re.match(r"(?i)\.exit", ".ExIT"):
#     print(".EXIT")