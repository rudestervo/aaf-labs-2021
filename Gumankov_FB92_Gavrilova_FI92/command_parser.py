import re

CREATE = r"\s*(?i)create\s+(?P<word>\w*[^(),; ])(\s*)+$"
INSERT = r"\s*(?i)insert\s+(?P<word>\w*[^(),; ])\s*\(\s*(?P<x>-?\d+)\s*,\s*(?P<y>-?\d+)\s*\)\s*"
PRINT_TREE = r"\s*(?i)print_tree\s+(?P<word>\w*[^(),; ])(\s*)+$"
CONTAINS = r"\s*(?i)contains\s+(?P<word>\w*[^(),; ])\s*\(\s*(?P<x>-?\d+)\s*,\s*(?P<y>-?\d+)\s*\)\s*"
SEARCH = r"(?i)(\s*search\s+(?P<word>\w*[^(),; ])(\s*)+|( where\s+)((\s*(?P<inside>inside)\s*\(\s*(?P<x1>-?\d+)\s*," \
         r"\s*(?P<y1>-?\d+)\s*\)\s*,\s\(\s*(?P<x2>-?\d+)\s*,\s*(?P<y2>-?\d+)\s*\)\s*)|(\s*(?P<above_to>above_to)\s*(" \
         r"?P<x>-?\d+)\s*)|(\s*(?P<nn>nn)\s*\(\s*(?P<nnx>-?\d+)\s*,\s*(?P<nny>-?\d+)\s*\)\s*)))+$"


def parse(text):
    commands = text.split(";")
    command_tokens = []
    for command in commands:
        if not command:
            break
        tokens = []
        m = re.match(CREATE, command)
        if m:
            tokens.append("CREATE")
            tokens.append(m.group("word"))
            command_tokens.append(tokens)
            continue
        m = re.match(INSERT, command)
        if m:
            tokens.append("INSERT")
            tokens.append(m.group("word"))
            tokens.append(m.group("x"))
            tokens.append(m.group("y"))
            command_tokens.append(tokens)
            continue
        m = re.match(PRINT_TREE, command)
        if m:
            tokens.append("PRINT_TREE")
            tokens.append(m.group("word"))
            command_tokens.append(tokens)
            continue
        m = re.match(CONTAINS, command)
        if m:
            tokens.append("CONTAINS")
            tokens.append(m.group("word"))
            tokens.append(m.group("x"))
            tokens.append(m.group("y"))
            command_tokens.append(tokens)
            continue

        m = re.match(SEARCH, command)
        if m:
            tokens.append("SEARCH")
            tokens.append(m.group("word"))
            groups = m.groupdict()
            if groups.get("inside"):
                tokens.append("INSIDE")
                tokens.append(groups["x1"])
                tokens.append(groups["y1"])
                tokens.append(groups["x2"])
                tokens.append(groups["y2"])
                command_tokens.append(tokens)
                continue
            if groups.get("above_to"):
                tokens.append("ABOVE_TO")
                tokens.append(groups["x"])
                command_tokens.append(tokens)
                continue
            elif groups.get("nn"):
                tokens.append("NN")
                tokens.append(groups["nnx"])
                tokens.append(groups["nny"])
                command_tokens.append(tokens)
                continue
            command_tokens.append(tokens)
            continue

        tokens.append("CMD_NOT_FOUND_ERROR")
        command_tokens.append(tokens)
    return command_tokens
