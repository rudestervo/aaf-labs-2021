import re
import KDTree
pattern_create = 'CREATE \w{1,10}|a-z A-Z'
pattern_insert = 'INSERT \w{1,10} \[-?[0-9]*,*-?[0-9]*\]|a-z A-Z|$'
pattern_print_tree = 'PRINT_TREE \w{1,10}|a-z A-Z'
pattern_contains = '^CONTAINS \w{1,10} \[-?[0-9]*,*-?[0-9]*\]|a-z A-Z|$'
pattern_search = '^SEARCH \w{1,10} \[?WHERE (CONTAINED_BY \[-?[0-9],-?[0-9]\]|INTERSECTS \[-?[0-9],-?[0-9]\]|RIGHT_OF -?[0-9])\]?|a-z A-Z|$'

trees = {}


def delete_space_from_string(string):
    if (string[0] == ' '):
        string = string[1:]
    if (string[len(string)-1] == ''):
        print('EW')
    string = re.sub(' +', ' ', string)
    string = re.sub(' +;', ';', string)
    string = re.sub(' +]', ']', string)
    string = re.sub(' +,', ',', string)
    if(bool(re.search('RIGHT_OF', command, flags=re.IGNORECASE)) == False):
        string = re.sub(' +0', '0', string)
        string = re.sub(' +1', '1', string)
        string = re.sub(' +2', '2', string)
        string = re.sub(' +3', '3', string)
        string = re.sub(' +4', '4', string)
        string = re.sub(' +5', '5', string)
        string = re.sub(' +6', '6', string)
        string = re.sub(' +7', '7', string)
        string = re.sub(' +8', '8', string)
        string = re.sub(' +9', '9', string)

    return string


def is_command_correctly_written(command):

    if (len(command) == 0):
        print("Please, enter command!")
        return False
   # elif (re.search('-', command)):
        #print("Negative numbers are not allowed")
    elif (re.match(pattern_create, command, flags=re.IGNORECASE)):
        print("Command create is correct")
        return True
    elif (re.match(pattern_print_tree, command, flags=re.IGNORECASE)):
        print("Command print_tree is correct")
        return True
    elif (re.match(pattern_contains, command, flags=re.IGNORECASE)):
        print("Command contains is correct")
        return True
    elif (re.match(pattern_search, command, flags=re.IGNORECASE)):
        print("Command search is correct")
        return True
    elif (re.match(pattern_insert, command, flags=re.IGNORECASE)):
        print("Command insert is correct")
        return True
    else:
        print("Check the spelling of the command", command)
        return False


def parser(command):

    if (is_command_correctly_written(command) == True):
        words = command.replace(';', '').split(' ')
        parameters = re.findall(r'-?\d+', command)
        if (bool(re.search('CREATE', words[0], flags=re.IGNORECASE)) == True):
            #print('CREATE', ' ', words[1])
            # print ("call create_table func")   #<------------- вызов функции create_table
            if(words[1] in trees):
                print('A KD-Tree with this name is already exist')
            else:
                # add a new key-value pair to dictionary
                trees[words[1]] = KDTree.KD_Tree()
            #print('You have followed trees:')
            # print(trees)
        elif (bool(re.search('PRINT_TREE', words[0], flags=re.IGNORECASE)) == True):
            #print('PRINT_TREE', ' ', words[1])
            # print ('call print_tree func')     #<------------- вызов функции print_tree
            if(words[1] in trees):
                tempTree = trees[words[1]]
                tempTree.print()
            else:
                print("Such tree doesnt existcre")
        elif (bool(re.search('INSERT', words[0], flags=re.IGNORECASE)) == True):

            parameters[0] = int(parameters[0])
            parameters[1] = int(parameters[1])
            #print('INSERT', ' ', words[1], ' ', parameters)
           # print ('call insert_data func')    #<------------- вызов функции insert_data
            if(words[1] in trees):
                tempTree = trees[words[1]]
                tempTree.add_node(parameters)
            else:
                print("Such tree doesn`t exist")
        elif (bool(re.search('CONTAINS', words[0], flags=re.IGNORECASE)) == True):
            parameters[0] = int(parameters[0])
            parameters[1] = int(parameters[1])
           # print('CONTAINS', ' ', words[1], ' ', parameters)
            if (words[1] in trees):
                tempTree = trees[words[1]]
                tempTree.contains(parameters)
            else:
                print("Such tree doesnt exist")
            # <------------- вызов функции contains_data
            #print('call contains_data func')
        else:
            search_type = words[3]
           # print('SEARCH', ' ', words[1], ' ', search_type, ' ', parameters)
            if (words[1] in trees):
                tempTree = trees[words[1]]
                if(bool(re.search('RIGHT_OF', search_type, flags=re.IGNORECASE)) == True):
                    num = int(parameters[0])
                    tempTree.right_of(num)
                elif(bool(re.search('CONTAINED_BY', search_type, flags=re.IGNORECASE)) == True):
                    parameters[0] = int(parameters[0])
                    parameters[1] = int(parameters[1])

                    tempTree.search(parameters, 'contained_by')
                else:
                    parameters[0] = int(parameters[0])
                    parameters[1] = int(parameters[1])
                    tempTree.search(parameters, 'intersects')
            else:
                print("Such tree doesnt exist")
            # print('call search func')  # <------------- вызов функции search


print(
    "You can start with these commands: \n1) CREATE table; \n2) INSERT set_name [0,0]; \n3) PRINT_TREE set_name; \n4) CONTAINS set_name [0,0]; \n5) SEARCH set_name [WHERE ...];\n      a)RIGHT_OF 1\n      b)CONTAINED_BY [0,0]\n      c)INTERSECTS [0,0]\n")
while(1):
    #command = [input() for _ in range(4) ]
    lines = []
    while True:
        line = input('> ' if len(lines) == 0 else '... ')
        if line:
            lines.append(line)
            if ';' in line:
                break

    #print(lines)
    command = '\n'.join(lines)
    command = command.replace('\n', ' ')
    commands = command.split(';')
    commands.pop()
    i = 0
    sizeofcommands = len(commands)
    while i < sizeofcommands:
        #print (i,' ',commands[i])
        commands[i] = delete_space_from_string(commands[i])
        parser(commands[i])
        i += 1
