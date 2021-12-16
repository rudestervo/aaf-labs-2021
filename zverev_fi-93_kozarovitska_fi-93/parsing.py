import re


def assign(arr1, arr2):
    for i in range(len(arr1)):
        arr2.append(arr1[i])


def create_table(EmpInput, result1, index1, number_of_index1):
    s1 = '\s*(C|c)(r|R)(e|E)(A|a)(t|T)(e|E)\s+[a-zA-Z][a-zA-Z0-9]*\s*\(\s*([a-zA-Z0-9]+\s*((I|i)(N|n)(D|d)(E|e)(X|x)(e|E)(D|d)\s*)*\s*)\s*(\s*,\s*[a-zA-Z0-9]+\s*(\s+(I|i)(N|n)(D|d)(E|e)(X|x)(e|E)(D|d))*)*\s*\)\s*;'
    if re.match(s1, EmpInput) is not None:
        EmpInput1 = EmpInput.casefold()
        first_command = EmpInput1.split()[0]
        temp = re.sub(r'(C|c)(r|R)(e|E)(A|a)(t|T)(e|E)', ' create ', EmpInput)
        temp = re.sub(r'(I|i)(N|n)(D|d)(E|e)(X|x)(e|E)(D|d)', 'indexed', temp)
        temp = temp.replace(first_command, "", 1)
        temp = temp.replace("(", " ")
        temp = temp.replace(")", " ")
        temp = temp.replace(" ", "", 1)
        temp = temp.replace(",", " ")
        temp = temp.replace(";", " ")
        #while temp[-1]!=';':
            #temp = temp[:-1]
        #temp = temp[:-1]
        result = str.split(temp)  # название таблицы re.split(r" ", temp)

        name_table = result[0]
        index = []
        number_of_index = []
        size = len(result)
        i = 0
        while i < size:
            if result[i] == "indexed":
                index.append(result[i - 1])
                number_of_index.append(i - 2)
                result.pop(i)
                size = len(result)
            i = i + 1
        result.pop(0)
        assign(result, result1)
        assign(index, index1)
        assign(number_of_index, number_of_index1)
        return name_table


def insert_table(EmpInput, column_values1):
    s1 = '\s*(I|i)(N|n)(S|s)(E|e)(R|r)(T|t)\s+[a-zA-Z0-9]+\s*\(\s*("[^"]+"\s*,\s*)*("[^"]+"\s*)\)\s*;\s*'
    if re.match(s1, EmpInput) is not None:
        EmpInput1 = EmpInput.casefold()
        first_command = EmpInput1.split()[0]
        temp1 = re.findall(r'\"[^\"]+\"', EmpInput)
        column_values = []
        temp = re.sub(r'(I|i)(N|n)(S|s)(E|e)(R|r)(T|t)', '  insert  ', EmpInput)
        for elem in temp1:
            elem = elem.replace('"', '')
            column_values.append(elem)
        temp = temp.replace('"', '')
        temp = temp.replace(first_command, "", 1)  # ''
        temp = temp.replace("(", " ")
        temp = temp.replace(")", "")
        temp = temp.replace(";", "")
        temp = temp.replace(" ", "", 1)
        temp = temp.replace(",", " ")
        result1 = str.split(temp)  # название таблицы
        name_of_table = result1[0]
        assign(column_values, column_values1)
        return name_of_table


def replace_value(EmpInput, case):
    temp = EmpInput
    if case==0:
        if ("=" in EmpInput):
            temp = temp.replace("=", " ",1)
    else:
        if ("<=" in EmpInput):
            temp = temp.replace("<=", " <= ")
        elif ("=<" in EmpInput):
            temp = temp.replace("=<", " <= ")
        elif (">=" in EmpInput):
            temp = temp.replace(">=", " >=  ")
        elif ("=>" in EmpInput):
            temp = temp.replace("=>", " >=  ")
        elif ("!=" in EmpInput):
            temp = temp.replace("!=", " !=  ")
        elif (">" in EmpInput):
            temp = temp.replace(">", " > ")
        elif ("<" in EmpInput):
            temp = temp.replace("<", " <  ")
        elif ("=" in EmpInput):
            temp = temp.replace("=", " =  ")

    return temp
def replace_value_reversed(EmpInput):
    temp = EmpInput
    if ("<=" in EmpInput):
        temp = temp.replace("<=", " >= ")
    elif ("=<" in EmpInput):
        temp = temp.replace("=<", " >= ")
    elif (">=" in EmpInput):
        temp = temp.replace(">=", " <=  ")
    elif ("=>" in EmpInput):
        temp = temp.replace("=>", " <=  ")
    elif ("!=" in EmpInput):
        temp = temp.replace("!=", " !=  ")
    elif (">" in EmpInput):
        temp = temp.replace(">", " < ")
    elif ("<" in EmpInput):
        temp = temp.replace("<", " >  ")
    elif ("=" in EmpInput):
        temp = temp.replace("=", " =  ")

    return temp
def select_columns_where(EmpInput, result):

    s1='\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s+([a-zA-Z0-9]+\s*)+\s*(\s*,\s*[a-zA-Z0-9]+\s*)*\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (w|W)(h|H)(e|E)(r|R)(e|E)\s+[a-zA-Z0-9]+\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*(\"[^\"]+\"\s*)\s*;'
    s2='\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t) ([a-zA-Z0-9]+\s*)+\s*(\s*,\s*[a-zA-Z0-9]+)*\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (w|W)(h|H)(e|E)(r|R)(e|E)\s+("[^"]+"\s*)((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*[a-zA-Z0-9]+\s*;'
    s3='\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s*([a-zA-Z0-9]+\s*)+\s*(\s*,\s*[a-zA-Z0-9]+)*\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s*(w|W)(h|H)(e|E)(r|R)(e|E)\s+[a-zA-Z0-9]+\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*[a-zA-Z0-9]+\s*;'
    s4='\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s+([a-zA-Z0-9]+\s*)+\s*(\s*,\s*[a-zA-Z0-9]+\s*)*\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (w|W)(h|H)(e|E)(r|R)(e|E)\s+(\"[^\"]+\"\s*)\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*(\"[^\"]+\"\s*)\s*;'
    case=0
    if '"' in EmpInput:
        if re.match(s1, EmpInput) is not None:
            case=1
        if re.match(s2, EmpInput) is not None:
            case=2
        elif re.match(s4, EmpInput) is not None:
            case = 4
    elif re.match(s3, EmpInput) is not None:
        case = 3

    if case!=0:
        EmpInput1 = EmpInput.casefold()
        first_command = EmpInput1.split()[0]
        if case==1 or case==2:
            value = re.findall(r'\"[^\"]+\"', EmpInput)
            value = value[0].replace('"', "")
        if case==4:
            values = re.findall(r'\"[^\"]+\"', EmpInput)
            value1 = values[0].replace('"', "")
            value2 = values[1].replace('"', "")
        if case==1 or case==3 or case==4:
            temp = replace_value(EmpInput,1)
        elif case==2:
            temp=replace_value_reversed(EmpInput)
        temp = re.sub(r'(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)', '  select  ', temp)
        temp = re.sub(r'(f|F)(r|R)(o|O)(M|m)', '  from  ', temp)
        temp = re.sub(r'(w|W)(h|H)(e|E)(r|R)(e|E)', '  where  ', temp)
        temp = temp.replace(first_command, "", 1)
        temp = temp.replace(";", "", 1)
        temp = temp.replace("from", "", 1)
        temp = temp.replace(",", " ")
        result1 = str.split(temp)
        for i in range(len(result1)):
            if result1[i] == "where":
                name_of_insert = result1[i - 1]
                result1.pop(i - 1)
                break
        name_of_col=[]
        for i in range(len(result1)):
            if result1[i]!='select':
                name_of_col.append(result1[i])
            if result1[i] == "from":
                break
        temp = temp.replace("where", "", 1)
        temp = temp.replace('"', " ")
        result1 = str.split(temp)
        result1.pop(len(result1) - 4)
        size_res = len(result1)
        if case==1:
            result1.pop(len(result1) - 1)
            result1.append(value)
            assign(result1, result)
            return (name_of_insert, "select col where ''")
        elif case==2:
            result1[size_res - 3], result1[size_res - 1] = result1[size_res - 1], result1[size_res - 3]
            result1.pop(len(result1) - 1)
            result1.append(value)
            assign(result1, result)
            return (name_of_insert, "select col where ''")
        elif case==3:
            assign(result1, result)
            return (name_of_insert, "select col where two col")
        elif case==4:
            result1.pop(len(result1) - 1)
            result1.pop(len(result1) - 2)

            result1.append(value1)
            result1.append(value2)
            assign(result1, result)
            return (name_of_insert, "select col where two val")

def select_columns(EmpInput, result):

    s1 = '\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s+([a-zA-Z0-9]+\s*)*(\s*,\s*[a-zA-Z0-9]+\s*)*\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s*;'
    if re.match(s1, EmpInput) is not None:
        temp = EmpInput
        EmpInput = EmpInput.replace(";", "", 1)
        EmpInput1 = EmpInput.casefold()
        first_command = EmpInput1.split()[0]
        temp = re.sub(r'(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)', '  select  ', temp)
        temp = re.sub(r'(f|F)(r|R)(o|O)(M|m)', '  from  ', temp)
        temp = temp.replace( first_command, "", 1)
        temp = temp.replace("from", "", 1)
        temp = temp.replace(" ", "", 1)
        temp = temp.replace(",", " ")
        result1 = str.split(temp)  # название таблицы
        size = len(result1)
        assign(result1, result)
        name_of_insert = result1[size - 1]
        name_of_insert = name_of_insert.replace(";", "", 1)
        return name_of_insert

def command_all_where(EmpInput, result):
    s1 = '\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s*\*\s*(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s*(w|W)(h|H)(e|E)(r|R)(e|E)\s+([a-zA-Z0-9]+\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*(\"[^\"]+\"\s*))\s*;'
    s2 = '\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t) \s*\*\s*(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (w|W)(h|H)(e|E)(r|R)(e|E)\s+(\"[^\"]+\"\s*)((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*[a-zA-Z0-9]+\s*\s*;'
    s3 = '\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t) \s*\*\s*(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (w|W)(h|H)(e|E)(r|R)(e|E)\s+[a-zA-Z0-9]+\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*[a-zA-Z0-9]+\s*;'
    s4 = '\s*(D|d)(e|E)(l|L)(e|E)(T|t)(E|e)\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (w|W)(h|H)(e|E)(r|R)(e|E)\s+[a-zA-Z0-9]+\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*(\"[^\"]+\"\s*)\s*;'
    s5 = '\s*(D|d)(e|E)(l|L)(e|E)(T|t)(E|e)\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (w|W)(h|H)(e|E)(r|R)(e|E)\s+(\"[^\"]+\"\s*)\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*[a-zA-Z0-9]+\s*;'
    s6 = '\s*(D|d)(e|E)(l|L)(e|E)(T|t)(E|e)\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (w|W)(h|H)(e|E)(r|R)(e|E)\s+[a-zA-Z0-9]+\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*[a-zA-Z0-9]+\s*;'
    s7='\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s*\*\s*(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s*(w|W)(h|H)(e|E)(r|R)(e|E)\s+((\"[^\"]+\"\s*)\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*(\"[^\"]+\"\s*))\s*;'
    s8='\s*(D|d)(e|E)(l|L)(e|E)(T|t)(E|e)\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (w|W)(h|H)(e|E)(r|R)(e|E)\s+(\"[^\"]+\"\s*)\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*(\"[^\"]+\"\s*)\s*;'

    case=0
    if re.match(s1, EmpInput) is not None:
        case=1
    if re.match(s2, EmpInput) is not None:
        case=2
    if re.match(s3, EmpInput) is not None:
        case=3
    if re.match(s4, EmpInput) is not None:
        case=4
    if re.match(s5, EmpInput) is not None:
        case=5
    if re.match(s6, EmpInput) is not None:
        case = 6
    if re.match(s7, EmpInput) is not None:
        case = 7
    if re.match(s8, EmpInput) is not None:
        case = 8
    if case!=0:
        temp = EmpInput
        if case==1 or case==4 or case==2 or case==5:
            value = re.findall(r'\"[^\"]+\"', EmpInput)
            value = value[0].replace('"', "")
        if case == 7 or case == 8:
            values = re.findall(r'\"[^\"]+\"', EmpInput)
            value1 = values[0].replace('"', "")
            value2 = values[1].replace('"', "")
        if case==1 or case==4 or case==7 or case==8:
            temp = replace_value(EmpInput,1)
        elif case==2 or case==5:
            temp = replace_value_reversed(EmpInput)
        elif case==3 or case==6:
            temp = replace_value(EmpInput,1)
        #EmpInput = EmpInput.replace(";", "", 1)
        EmpInput1 = EmpInput.casefold()
        first_command = EmpInput1.split()[0]
        temp = re.sub(r'(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)', '  select  ', temp)
        temp = re.sub(r'(D|d)(e|E)(l|L)(e|E)(T|t)(E|e)', '  delete  ', temp)
        temp = re.sub(r'(f|F)(r|R)(o|O)(M|m)', '  from  ', temp)
        temp = re.sub(r'(w|W)(h|H)(e|E)(r|R)(e|E)', '  where  ', temp)
        temp = temp.replace(first_command, "", 1)
        #temp = temp.replace("delete", "", 1)
        temp = temp.replace(";", "", 1)
        temp = temp.replace("from", "", 1)
        temp = temp.replace(" ", "", 1)
        temp = temp.replace(",", " ")
        result1 = str.split(temp)  # название таблицы
        for i in range(len(result1)):
            if result1[i] == "where":
                name_of_table = result1[i - 1]
                result1.pop(i - 1)
                break
        temp = temp.replace("where", "", 1)
        temp = temp.replace('"', " ")
        result1 = str.split(temp)
        result1.pop(len(result1) - 4)
        size_res = len(result1)
        if case==1 or case==4:

            result.append(result1[size_res - 3])
            result.append(result1[size_res - 2])
            result.append(value)
        elif case==2 or case==5:
            result.append(result1[size_res - 1])
            result.append(result1[size_res - 2])
            result.append(value)
        elif case==3 or case==6:
            result.append(result1[size_res - 3])
            result.append(result1[size_res - 2])
            result.append(result1[size_res - 1])
        elif case==7 or case==8:
            result.append(value1)
            result.append(result1[size_res - 2])
            result.append(value2)
        if case==1 or case==2:
            return(name_of_table, "select where ''")
        if case==3:
            return (name_of_table, "select where two col")
        if case==4 or case==5:
            return (name_of_table, "delete where ''")
        if case==6:
            return (name_of_table, "delete where two col")
        if case==7:
            return (name_of_table, "select where two val")
        if case==8:
            return (name_of_table, "delete where two val")
        #return name_of_table

def command_all(EmpInput):
    s1 = '\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s+\*\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s*;'
    s2 = '\s*(D|d)(e|E)(l|L)(e|E)(T|t)(E|e)\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s*;'
    case=0
    if re.match(s1, EmpInput) is not None:
        case = 1
    if re.match(s2, EmpInput) is not None:
        case = 2
    if case!=0:
        temp = EmpInput
        EmpInput1 = EmpInput.casefold()
        first_command = EmpInput1.split()[0]
        temp = re.sub(r'(f|F)(r|R)(o|O)(M|m)', '  from  ', temp)
        temp = temp.replace(first_command, "", 1)
        temp = temp.replace("from", "", 1)
        temp = temp.replace(" ", "", 1)
        temp = temp.replace(",", " ")
        temp = temp.replace(";", " ")
        result1 = str.split(temp)
        if case==1: #re.match(s1, EmpInput) is not None
            name_table = result1[1]
            return (name_table, "select")
        else:
            name_table = result1[0]
            return (name_table, "delete")

def exit(EmpInput):
    s1= '\s*(e|E)(x|X)(i|I)(t|T)\s*;'
    if re.match(s1, EmpInput) is not None:
        return 1
def nth_repl(s, sub, repl, n):
    find = s.find(sub)
    # If find is not -1 we have found at least one match for the substring
    i = find != -1
    # loop util we find the nth or we find no match
    while find != -1 and i != n:
        # find + 1 means we start searching from after the last match
        find = s.find(sub, find + 1)
        i += 1
    # If i is equal to n we found nth match so replace
    if i == n:
        return s[:find] + repl + s[find+len(sub):]
    return s

def full_join(EmpInput):
    s1='\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s+([a-zA-Z0-9]+\s*,\s*)*\s*[a-zA-Z0-9]+\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (F|f)(u|U)(L|l)(L|l)\s+(J|j)(O|o)(I|i)(N|n)\s+[a-zA-Z0-9]+\s+(O|o)(N|n)\s+[a-zA-Z0-9]+\s*=\s*[a-zA-Z0-9]+;'
    s2='\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s+([a-zA-Z0-9]+\s*,\s*)*\s*[a-zA-Z0-9]+\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (F|f)(u|U)(L|l)(L|l)\s+(J|j)(O|o)(I|i)(N|n)\s+[a-zA-Z0-9]+\s+(O|o)(N|n)\s+[a-zA-Z0-9]+\s*=\s*[a-zA-Z0-9]+\s+(w|W)(h|H)(e|E)(r|R)(e|E)\s+[a-zA-Z0-9]+\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*(\"[^\"]+\"\s*)\s*;'
    s3='\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s+([a-zA-Z0-9]+\s*,\s*)*\s*[a-zA-Z0-9]+\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (F|f)(u|U)(L|l)(L|l)\s+(J|j)(O|o)(I|i)(N|n)\s+[a-zA-Z0-9]+\s+(O|o)(N|n)\s+[a-zA-Z0-9]+\s*=\s*[a-zA-Z0-9]+\s+(w|W)(h|H)(e|E)(r|R)(e|E)\s+(\"[^\"]+\"\s*)((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*[a-zA-Z0-9]+\s*;'
    s4='\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s+([a-zA-Z0-9]+\s*,\s*)*\s*[a-zA-Z0-9]+\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (F|f)(u|U)(L|l)(L|l)\s+(J|j)(O|o)(I|i)(N|n)\s+[a-zA-Z0-9]+\s+(O|o)(N|n)\s+[a-zA-Z0-9]+\s*=\s*[a-zA-Z0-9]+\s+(w|W)(h|H)(e|E)(r|R)(e|E)\s+[a-zA-Z0-9]+\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*[a-zA-Z0-9]+\s*;'
    s5='\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s+\*\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (F|f)(u|U)(L|l)(L|l)\s+(J|j)(O|o)(I|i)(N|n)\s+[a-zA-Z0-9]+\s+(O|o)(N|n)\s+[a-zA-Z0-9]+\s*=\s*[a-zA-Z0-9]+;'
    s6='\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s+\*\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (F|f)(u|U)(L|l)(L|l)\s+(J|j)(O|o)(I|i)(N|n)\s+[a-zA-Z0-9]+\s+(O|o)(N|n)\s+[a-zA-Z0-9]+\s*=\s*[a-zA-Z0-9]+\s+(w|W)(h|H)(e|E)(r|R)(e|E)\s+[a-zA-Z0-9]+\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*(\"[^\"]+\"\s*)\s*;'
    s7='\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s+\*\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (F|f)(u|U)(L|l)(L|l)\s+(J|j)(O|o)(I|i)(N|n)\s+[a-zA-Z0-9]+\s+(O|o)(N|n)\s+[a-zA-Z0-9]+\s*=\s*[a-zA-Z0-9]+\s+(w|W)(h|H)(e|E)(r|R)(e|E)\s+(\"[^\"]+\"\s*)((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*[a-zA-Z0-9]+\s*;'
    s8='\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s+\*\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (F|f)(u|U)(L|l)(L|l)\s+(J|j)(O|o)(I|i)(N|n)\s+[a-zA-Z0-9]+\s+(O|o)(N|n)\s+[a-zA-Z0-9]+\s*=\s*[a-zA-Z0-9]+\s+(w|W)(h|H)(e|E)(r|R)(e|E)\s+[a-zA-Z0-9]+\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*[a-zA-Z0-9]+\s*;'
    s9='\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s+([a-zA-Z0-9]+\s*,\s*)*\s*[a-zA-Z0-9]+\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (F|f)(u|U)(L|l)(L|l)\s+(J|j)(O|o)(I|i)(N|n)\s+[a-zA-Z0-9]+\s+(O|o)(N|n)\s+[a-zA-Z0-9]+\s*=\s*[a-zA-Z0-9]+\s+(w|W)(h|H)(e|E)(r|R)(e|E)\s+(\"[^\"]+\"\s*)\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*(\"[^\"]+\"\s*)\s*;'
    s10='\s*(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)\s+\*\s+(f|F)(r|R)(o|O)(M|m)\s+[a-zA-Z0-9]+\s* (F|f)(u|U)(L|l)(L|l)\s+(J|j)(O|o)(I|i)(N|n)\s+[a-zA-Z0-9]+\s+(O|o)(N|n)\s+[a-zA-Z0-9]+\s*=\s*[a-zA-Z0-9]+\s+(w|W)(h|H)(e|E)(r|R)(e|E)\s+(\"[^\"]+\"\s*)\s*((=)||(<=)||(<)||(>)||(>=)||(=>)||(=<)||(!=))\s*(\"[^\"]+\"\s*)\s*;'
    case=0
    if re.match(s1, EmpInput) is not None:
            case=1
    elif re.match(s2, EmpInput) is not None:
        case=2
    elif re.match(s3, EmpInput) is not None:
        case =3
    elif re.match(s4, EmpInput) is not None:
        case = 4
    elif re.match(s5, EmpInput) is not None:
        case = 5
    elif re.match(s6, EmpInput) is not None:
        case = 6
    elif re.match(s7, EmpInput) is not None:
        case = 7
    elif re.match(s8, EmpInput) is not None:
        case = 8
    elif re.match(s9, EmpInput) is not None:
        case = 9
    elif re.match(s10, EmpInput) is not None:
        case = 10
    if case!=0:
        temp = EmpInput
        EmpInput1 = EmpInput.casefold()
        first_command = EmpInput1.split()[0]
        temp = replace_value(temp, 0)
        if case==9  or case==10:
            values = re.findall(r'\"[^\"]+\"', EmpInput)
            temp = temp.replace(values[0], "")
            temp = temp.replace(values[1], "")
            value1 = values[0].replace('"', "")
            value2 = values[1].replace('"', "")
            temp = re.sub(r';', '  ', temp)
            #temp = replace_value(temp,0)
            symbol = temp.split()[-1]
            #if symbol != '=':
            temp = temp.replace(symbol, '', 1)
            #else:
                #temp = nth_repl(temp, '=', '', 2)
        elif case==2 or case==3 or case== 6 or case==7:
            columns=re.findall(r'[a-zA-Z0-9]+', EmpInput)
            col_to_compare=columns[-1]
            values = re.findall(r'\"[^\"]+\"', EmpInput)
            temp = temp.replace(values[0], "")
            value = values[0].replace('"', "")
            temp = re.sub(r';', '  ', temp)
            #symbol = temp.split()[-2]

                #temp = temp.replace('=', '', 2)
        if case == 2 or case == 4 or case == 6 or case == 8 or case == 9 or case == 10:
            temp = replace_value(temp,1)
        elif case == 3 or case == 7:
            temp = replace_value_reversed(temp)
        temp = re.sub(r'(S|s)(e|E)(L|l)(E|e)(c|C)(T|t)', '  select  ', temp)
        temp = re.sub(r'(f|F)(r|R)(o|O)(M|m)', '  from  ', temp)
        temp = re.sub(r'(F|f)(u|U)(L|l)(L|l)', '  full  ', temp)
        temp = re.sub(r'(J|j)(O|o)(I|i)(N|n)', '  join  ', temp)
        temp = re.sub(r'(O|o)(N|n)', '  on  ', temp)
        #temp = re.sub(r'=', '  =  ', temp, 1)
        temp = re.sub(r';', '  ', temp)
        temp = temp.replace(first_command, "", 1)
        temp = temp.replace(" ", "", 1)
        temp = temp.replace(",", " ")
        result1 = str.split(temp)
        col_names=[]
        for a in range (len(result1)):
            if result1[a]=='from':
                break
        if case<5 or case==9:
            for t in range(a):
                col_names.append(result1[t])
        table1=result1[a+1]
        for b in range (len(result1)):
            if result1[b]=='join':
                break
        table2=result1[b+1]
        size=len(result1)
        #symbol='='

        if case==2 or case==3 or case==6 or case== 7 :
            value = re.findall(r'\"[^\"]+\"', EmpInput)
            value = value[0].replace('"', "")
            col2 = result1[size - 4]
            col1 = result1[size - 5]

            if case==2 or case ==6:
                col_to_compare = result1[size - 2]
                symbol = result1[size - 1]
            else:
                col_to_compare = result1[size - 1]
                symbol = result1[size - 2]
            if case== 2 or case==3:
                return (col_names, table1, table2, col1, col2, 'full join where "" ', col_to_compare, value, symbol)
            else:
                return (None, table1, table2, col1, col2, '* full join where "" ', col_to_compare, value, symbol)
        elif case==9 or case==10:
            col2 = result1[size - 2]
            col1 = result1[size - 3]
            #symbol = result1[size - 1]

            if case==9:
                return (col_names, table1, table2, col1, col2, 'full join where two val ', value1, value2, symbol)
            else:
                col2 = result1[size - 2]
                col1 = result1[size - 3]
                return (None, table1, table2, col1, col2, '* full join where two val ', value1, value2, symbol)
        elif case==4 or case== 8:
            col2 = result1[size - 5]
            col1 = result1[size - 6]
            col_to_compare2 = result1[size - 1]
            col_to_compare1 = result1[size - 3]
            symbol = result1[size - 2]
            if case== 4:
                return (col_names, table1, table2, col1, col2, "full join where two col", col_to_compare1, col_to_compare2, symbol)
            else:
                return (None, table1, table2, col1, col2, "* full join where two col", col_to_compare1, col_to_compare2, symbol)
        else:
            col1 = result1[size - 2]
            col2 = result1[size - 1]
            if case== 1:
                return(col_names, table1, table2,col1, col2, "full join" )
            else:
                return (None, table1, table2, col1, col2, "* full join")
    else:
        return None
