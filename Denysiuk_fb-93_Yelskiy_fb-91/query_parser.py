import re
import query_runer as qr

def parse_query(query):
    query = re.sub('[\r\n\t" ";]+', ' ', query)
    query=re.sub('[" "]*,[" "]*',',',query)
    query=re.sub('[(][" "]+', '(', query)# (    12   , 52   ) => (12,52)
    query = re.sub('[" "]+[)]', ')', query)
    query = re.sub('[)][" "]*,[(][" "]*', ') (', query)
    query=query.strip()
    command=query.split(' ')[0].lower()
    if command == '.end' and len(query[4:])==0:
        return True
    elif command == 'create':
        qr.create(query[7:])
    elif command == 'insert':
        qr.insert(query[7:])
    elif command == 'contains':
        qr.contains(query[9:])
    elif command == 'search':
        qr.search(query[7:])
    elif command == 'print_tree':
        qr.print_tree(query[11:])
    else:
        print('Incorrect query')
    return False


def run_query_from_console():
    while True:
        query_str = ''
        while True:
            string = input('>>')
            query_str += string + ' '
            if string.find(';') != -1 :
                break
        if parse_query(query_str) and re.search('[\r\n\t" "]?[".END"".end"][\r\n\t;" "]?', query_str):
            break
