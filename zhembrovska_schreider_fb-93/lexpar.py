import re
from table import *

class Token:
    def __init__(self, type, text):
        self.type = type
        self.text = text

    def print_token(self):
        print(self.type, self.text)

token_types = {
    'SPACE': '[\n\t\s]+',
    'CREATE': '[Cc][Rr][Ee][Aa][Tt][Ee]',
    'INDEXED': '[Ii][Nn][Dd][Ee][Xx][Ee][Dd]',
    'INSERT': '[Ii][Nn][Ss][Ee][Rr][Tt]',
    'INTO': '[Ii][Nn][Tt][Oo]',
    'SELECT': '[Ss][Ee][Ll][Ee][Cc][Tt]',
    'ALL': '\*',
    'FROM': '[Ff][Rr][Oo][Mm]',
    'WHERE': '[Ww][Hh][Ee][Rr][Ee]',
    'DELETE': '[Dd][Ee][Ll][Ee][Tt][Ee]',
    'OR': '[Oo][Rr]',
    'AND': '[Aa][Nn][Dd]',
    'LPAR': '\(',
    'RPAR': '\)',
    'EQUAL': '=',
    'NOT_EQUAL': '!=',
    'MORE': '>',
    'LESS': '<',
    'MORE_EQUAL': '>=',
    'LESS_EQUAL': '<=',
    'COMMA': ',',
    'END': ';',
    'NAME': '[_a-zA-Z0-9]+'
}

def getTokens(str):
    tokens = []
    tstart = 0
    while tstart != len(str):
        str = str[tstart:]
        for i in range(len(token_types)):
            value = list(token_types.values())[i]
            res = re.match(value, str)
            if res:
                key = list(token_types.keys())[i]
                if key != 'SPACE':
                    tokens.append(Token(key,str[:res.end()]))
                tstart = res.end()
                break
        if res == None:
            return 0
    return tokens

def parser_create(tokens):
    if tokens[0].type != 'NAME':
        return 0
    table_name = tokens.pop(0).text
    columns = {}
    if tokens.pop(0).type == 'LPAR':
        while tokens:
            if tokens[0].type == 'COMMA':
                tokens.pop(0)
                continue
            if tokens[0].type == 'RPAR':
                tokens.pop(0)
                break
            if len(tokens) > 1 and tokens[1].type == 'INDEXED':
                columns[tokens.pop(0).text] = 1
                tokens.pop(0)
            else: columns[tokens.pop(0).text] = 0
    else:
        return 0
    return (table_name, columns)


def parser_insert(tokens):
    row = []
    if tokens[0].type == 'INTO': tokens.pop(0)
    table_name = tokens.pop(0).text
    if tokens.pop(0).type == 'LPAR':
        while tokens:
            if tokens[0].type == 'COMMA':
                tokens.pop(0)
                continue
            if tokens[0].type == 'RPAR':
                tokens.pop(0)
                break
            row.append(tokens.pop(0).text)
    else: return 0
    return (table_name, row)

def parser_delete(tokens):
    if tokens[0].type == 'FROM': tokens.pop(0)
    table_name = tokens.pop(0).text
    if tokens[0].type == 'WHERE':
        tokens.pop(0)
        column = tokens.pop(0).text
        operator = tokens.pop(0).text
        value = tokens.pop(0).text
    else: return [table_name]
    return (table_name, column,operator,value)

def parser_select(tokens):
    columns = []
    conditions = []
    relations = []
    while tokens[0].type != 'FROM':
        if tokens[0].type == 'COMMA':
            tokens.pop(0)
            continue
        col = tokens.pop(0).text
        columns.append(col)
        if col == '*':
            break
    tokens.pop(0)
    table_name = tokens.pop(0).text
    cond = 0
    if tokens[0].type == 'WHERE':
        tokens.pop(0)
        for i in range(len(tokens)):
            if (tokens[i].type == 'LPAR'):
                cond += 1
        for i in range(cond):
                if tokens[0].type == 'LPAR':
                    tokens.pop(0)
                    column = tokens.pop(0).text
                    operator = tokens.pop(0).text
                    value = tokens.pop(0).text
                    conditions.append([column,operator,value])
                    tokens.pop(0).text
                    if cond > 1 and i != cond-1:
                        relations.append(tokens.pop(0).type)
    return (table_name, columns, conditions, relations)

def lexpar(cmd):
    cmd = cmd.replace("'", "")
    cmd = cmd.replace('"', '')
    tokens = getTokens(cmd)
    if tokens == 0:
        return 0, 0
    if re.match(r'^[Ee][Xx][Ii][Tt]', tokens[0].text):
        return 'exit', 0
    if tokens[-1].type != 'END':
        print('you missed ;')
        return 0,0
    command = tokens.pop(0).type
    if command == 'CREATE':
        return command, parser_create(tokens)
    elif command == 'INSERT':
        return command, parser_insert(tokens)
    elif command == 'SELECT':
        return command, parser_select(tokens)
    elif command == 'DELETE':
        return command, parser_delete(tokens)
