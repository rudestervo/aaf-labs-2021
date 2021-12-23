








def error(message):
    # do something maybe =/ ...
    print("\nERROR:", message, '\n')


    
def check_commands(cmd):
    return
    if cmd['cmd'] not in ['INSERT', 'SELECT', 'DELETE', 'CREATE']:
        error("Incorrect command")
        return 1
    if cmd['table_name'] == '' or cmd['table_name'] == 'WHERE':
        error("Incorrect table name")
        return 1
    if cmd['cmd'] == "SELECT":
        for key in cmd['condition']:
            if cmd['condition'][key] == '':
                error("Incorrect condition state")
                return 1
    if cmd['cmd'] == "DELETE" and cmd['condition'] :
        for key in cmd['condition']:
            if cmd['condition'][key] == '':
                error("Incorrect condition state")
                return 1
    return 0
        

def parse(cmd):
    arr = []
    try:
        for cmd_single in cmd.split(";"):
            arr.append(parses(cmd_single + ";"))
    except:
        print("[parsing fatal error]")

    return arr

def parses(cmd, print_parsed=False):
    if len(cmd) < 5:
        return None
    cmds = {}
    cmd = cmd + ";"
    # find end of command
    cmd = cmd[0:cmd.find(';')]
    
    # split by space
    lst = cmd.split()
    # first word always command
    cmds['cmd'] = lst[0].replace('\n', '').replace(' ', '').replace('\t', '').upper()
    
    # detect table name
    if 'INTO' in cmd:
        name = cmd[cmd.upper().find('INTO') + 4: cmd.find('(')].replace(',', ' ')
        cmds['table_name'] = name.split()[0]

    elif 'FROM' in cmd:
        cmds['table_name'] = cmd[cmd.upper().find('FROM') + 4::].split()[0].strip()
    else:
        cmds['table_name'] = lst[1].replace('\n', '').replace('\t', '')
        
    # work with arguments for INSERT
    if cmds['cmd'] == 'INSERT':
        parse_insert(cmd, cmds)
        
    # work with arguments for CREATE
    if cmds['cmd'] == 'CREATE':
        parse_create(cmd, cmds)

    # work with arguments for SELECT
    if cmds['cmd'] == 'SELECT':
        parse_select(cmd, cmds)

    # work with arguments for DELETE
    if cmds['cmd'] == 'DELETE':
        parse_delete(cmd, cmds)
        
    if print_parsed and not check_commands(cmds):
        for key in cmds:
            print(key, ' --> ', cmds[key])
    # check cmd        
    return cmds




def parse_create(cmd, dictionary):
    args = []
    indexed = []
    for arg in cmd[cmd.find("(")+1: cmd.find(')')].split(','):
        # fill bool array for indexing
        if "INDEXED" in arg:
            indexed.append(True)
        else:
            indexed.append(False)
        args.append(arg.replace("INDEXED", '').strip(' \n\t“”"') )

    dictionary['args'] = args
    dictionary['condition'] = indexed  
    
    
    
def parse_insert(cmd, dictionary):
    args = []
    if cmd.find('(') < 0 or cmd.find(')') < 0 or cmd.find('(') > cmd.find('('):
        error("incorrect input 'INSERT'")
    for arg in cmd[max(cmd.find("(")+1, 1+cmd.find(dictionary['table_name']) + len(dictionary['table_name'])): cmd.find(')')].replace(',', ' ').split('"'):
        arg = arg.replace('\n', ' ').replace('\t', ' ').replace(' ', '').replace('"', '').replace("'", '')
        if len(arg) >= 1 and arg!='\n':
            args.append(arg)

    dictionary['args'] = args

    
    
def parse_select(cmd, cmds):
    args = []
    conditions = []
    cmd = cmd.replace('\n', ' ').replace('\t', ' ')
    cmds['JOIN'] = False
    # find columns
    for arg in cmd[cmd.upper().find("SELECT")+6: cmd.upper().find('FROM')].replace(',', ' ').split(' '):
        if '*' in arg:
            break
        arg = arg.replace(' ', '')
        if len(arg) >= 1 and arg!='\n':
            args.append(arg)

    # if there is FULL_JOIN
    if ('FULL_JOIN') in cmd.upper():
        cmds['JOIN'] = True
        # second table name
        cmds['join_table'] = cmd[cmd.upper().find("FULL_JOIN")+9: cmd.find('ON')].strip(' \n\t“”"')

        # join condition
        cmds['join_args'] = []
        condition = cmd[cmd.find("ON")+2: cmd.find('WHERE')].split('=')
        for col in condition:
            cmds['join_args'].append(col.strip('\n\t“”" ').strip("'"))


    # if there is WHERE keyword:
    cmds['condition'] = None
    if ('WHERE') in cmd.upper():
        cols = {'value1':'', 'operator':'', 'value2':''}
        condition_str = cmd[cmd.find("WHERE")+5 : ].strip('"“”\n\t').strip("'")
        
        index = max(condition_str.find('>'), condition_str.find('='), condition_str.find('<'), condition_str.find('!')) 

        for c in condition_str[0:index]:
            if c not in " ><=!":
                cols['value1'] += c
            else:
                pass
        for c in condition_str[index-1:]:
            #print(c)
            if c in "><=!":
                cols['operator'] += c
            else:
                pass
                
        for c in condition_str[index+1:]:
            if c not in " ><=!":
                cols['value2'] += c
            else:
                pass
                
        cmds['condition'] = cols

    cmds['args'] = args
    

def parse_delete(cmd, cmds):
    cols = {'value1':'', 'operator':'', 'value2':''}
    if ('WHERE') in cmd.upper():
        condition_str = cmd[cmd.find("WHERE")+5 :].strip('"“”\n\t').strip("'")
        
        index = max(condition_str.find('>'), condition_str.find('='), condition_str.find('<'), condition_str.find('!')) 

        for c in condition_str[0:index]:
            if c.replace('"', '').replace("'", '') not in " ><=!":
                cols['value1'] += c.replace('"', '').replace("'", '')
            else:
                pass
        for c in condition_str[index-1:]:
            if c.replace('"', '').replace("'", '') in "><=!":
                cols['operator'] += c.replace('"', '').replace("'", '')
            else:
                pass
                
        for c in condition_str[index+1:]:
            if c.replace('"', '').replace("'", '') not in " ><=!":
                cols['value2'] += c.replace('"', '').replace("'", '')
            else:
                pass
                
        cmds['condition'] = cols


