import lexer


token_exprs = [
    (r'[\s\n\t]+', None),
    # (r'#[^\n]*', None),
    (r'(?i)create', "T_CREATE"),
    (r'(?i)delete', "T_DELETE"),
    (r'(?i)insert', "T_INSERT"),
    (r'(?i)select', "T_SELECT"),
    (r'(?i)INDEXED', "T_INDEXED"),
    (r'(?i)into', None),
    (r'(?i)from', "T_FROM"),
    (r'((?i)where)', "T_WHERE"),
    (r',', "T_SEP"),
    (r'\(', 'T_LPAR'),
    (r'\)', "T_RPAR"),
    (r'<=', "T_LESS_EQ"),
    (r'<', "T_LESS"),
    (r'>=', "T_MORE_EQ"),
    (r'>', "T_MORE"),
    (r'=', "T_EQ"),
    (r'!=', "T_UNEQ"),
    (r'(?i)and', "T_AND"),
    (r'(?i)or', "T_OR"),
    (r'\|', "T_OR"),
    # (r'[A-z\d]+', "NAME"),
    # (r'\"[A-z\d\s.,_]+\"', "T_VALUE"),
    (r'\"(.*?)\"', "T_VALUE"),
    (r'[A-z\d"]+', "T_STR"),
    (r'\*', "T_ALL"),
    (None, "T_END")
    ]

def imp_lex(characters):
    tokens = lexer.lex(characters, token_exprs)
    tokens.append((None, "T_END"))
    return tokens

# tokens = imp_lex('(name <= "Murzik") Or (name = "Pushok")')

# string = 'SELECT id, favourite_food FROM cats WHERE (name <= "Murzik, @#$@%$#%$^*( d") OR (name = "Pushok")'
# print(imp_lex(string))
# print(tokens)
