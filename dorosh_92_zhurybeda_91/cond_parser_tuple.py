from imp_lexer import *


def find_between(s, first, last):
    start = s.index(first) + len(first)
    end = s.index(last, start)
    return s[start:end]


class Node:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value
        self.right = None
        self.left = None


def match(tokens, token):
    if tokens[0][1] == token:
        return tokens.pop(0)[0]
    else:
        raise Exception('Invalid syntax on token {}'.format(tokens[0][1]))


def parse_e3(tokens):
    if tokens[0][1] == "T_STR":
        node = Node(tokens[0][1], value=tokens[0][0])
        tokens.pop(0)[0]
        return node
    elif tokens[0][1] == "T_VALUE":
        node = Node(tokens[0][1], value=find_between(tokens[0][0], '"', '"'))
        tokens.pop(0)[0]
        return node

    match(tokens, "T_LPAR")
    expression = parse_e(tokens)
    match(tokens, "T_RPAR")

    return expression


def parse_e2(tokens):
    left_node = parse_e3(tokens)

    while tokens[0][1] in ["T_OR", "T_AND"]:
        node = Node(tokens[0][1], value=tokens[0][0])
        tokens.pop(0)[1]
        node.left = left_node
        node.right = parse_e3(tokens)
        left_node = node

    return left_node


def parse_e(tokens):
    left_node = parse_e2(tokens)

    while tokens[0][1] in ["T_EQ",
                           "T_UNEQ",
                           "T_MORE",
                           "T_LESS",
                           "T_MORE_EQ",
                           "T_LESS_EQ"
                           ]:
        node = Node(tokens[0][1], value=tokens[0][0])
        tokens.pop(0)[0]
        node.left = left_node
        node.right = parse_e2(tokens)
        left_node = node

    return left_node


def parse(tokens):
    ast = parse_e(tokens)
    match(tokens, 'T_END')
    return ast


def printPreorder(root):
    if root:
        print(root.value),

        printPreorder(root.left)

        printPreorder(root.right)


def printPostorder(root):
    if root:
        printPostorder(root.left)

        printPostorder(root.right)

        print(root.value, root.token_type)


def printInorder(root):
    if root:
        printInorder(root.left)

        print(root.value),

        printInorder(root.right)


COUNT = [5]


def print2DUtil(root, space):
    if (root == None):
        return

    space += COUNT[0]

    print2DUtil(root.right, space)

    print()
    for i in range(COUNT[0], space):
        print(end=" ")
    print(root.value)

    print2DUtil(root.left, space)


def print2D(root):
    print2DUtil(root, 0)


def postorder(root, lst=None):
    if lst is None:
        lst = []
    if root:
        postorder(root.left, lst)

        postorder(root.right, lst)
        lst.append((root.value, root.token_type))

        return root.value, lst


# com = imp_lex('(name <= "Murzik") OR (name = "Pushok") AND ((dog = "Shiba") OR (cat = "stas") AND (vidra = "jeka"))')
# ast = parse(com)
# print(postorder(ast))
# print2D(ast)
# printInorder(ast)
# print("================")
# printPostorder(ast)
# print("===========")
# printPreorder(ast)
# print(ast.children[0].value)
# print(ast.children[0].children[0])
# print(ast.children[0].children[1])
# com = imp_lex('(a>"4") or ("4"<=bb)')
# ast = parse(com)
# print(postorder(ast))