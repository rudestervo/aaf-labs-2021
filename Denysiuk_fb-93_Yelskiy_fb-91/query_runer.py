import re
import RTree
trees_dict={}

def not_match_name(name: str):
    if re.match("^[a-zA-Z][a-zA-Z0-9_]*$", name) is None:
        print("Invalid or empty name of the set")
        return True
    return False


def param_is_not_a_point(point: str):
    if re.match('^[(][0-9]+,[0-9]+[)]$', point) is None:
        print('The entered parameter is not a point')
        return True
    return False

def parse_point(point:str):
    point=point[1:-1]
    point=point.split(',')
    return RTree.Point(int(point[0]),int(point[1]))


def create(sub_query: str):
    if len(sub_query.split(' ')) > 1:
        print('Too many parameters')
        return
    if not_match_name(sub_query):
        return
    if sub_query in trees_dict.keys():
        print('Table with this name already exists')
        return
    trees_dict[sub_query]=RTree.RTree()


def insert(sub_query: str):
    param_lst = sub_query.split(' ')
    if len(param_lst) > 2:
        print('Too many parameters')
        return
    if not_match_name(param_lst[0]):
        return
    if param_is_not_a_point(param_lst[1]):
        return
    if param_lst[0] not in trees_dict.keys():
        print('Table with this name does not exist')
        return
    trees_dict[param_lst[0]].insert(parse_point(param_lst[1]))


def contains(sub_query: str):
    param_lst = sub_query.split(' ')
    if len(param_lst) > 2:
        print('Too many parameters')
        return
    if not_match_name(param_lst[0]):
        return
    if param_is_not_a_point(param_lst[1]):
        return
    if param_lst[0] not in trees_dict.keys():
        print('Table with this name does not exist')
        return
    print(trees_dict[param_lst[0]].search(parse_point(param_lst[1])).__str__().upper())


def search(sub_query: str):
    param_lst = sub_query.split(' ')
    if len(param_lst) > 5:
        print('Too many parameters')
        return
    if not_match_name(param_lst[0]):
        return
    if param_lst[0] not in trees_dict.keys():
        print('Table with this name does not exist')
        return
    if len(param_lst)==1:
        print([i.to_cortege() for i in trees_dict[param_lst[0]].search_by_condition()])
        return
    if param_lst[1].lower() =='where':
        if len(param_lst)==5 and param_lst[2].lower() =='inside':
            if param_is_not_a_point(param_lst[3]) or param_is_not_a_point(param_lst[4]):
                return
            rect=RTree.Rect(parse_point(param_lst[3]), parse_point(param_lst[4]))
            print([i.to_cortege() for i in trees_dict[param_lst[0]].search_by_condition(rect)])
            return
        elif len(param_lst)==4:
            if param_lst[2].lower() =='left_of':
                if re.match('^[0-9]+$',param_lst[3]) is None:
                    print(f'Expected an integer value instead of {param_lst[3]}')
                    return
                print([i.to_cortege() for i in trees_dict[param_lst[0]].search_by_condition(int(param_lst[3]))])
                return
            elif param_lst[2].lower() =='nn':
                if param_is_not_a_point(param_lst[3]):
                    return
                print([i.to_cortege() for i in trees_dict[param_lst[0]].search_by_condition(parse_point(param_lst[3]))])
                return
        else:
            print('Incorrect query')

    pass


def print_tree(sub_query: str):
    if len(sub_query.split(' ')) > 1:
        print('Too many parameters')
        return
    if not_match_name(sub_query):
        return
    trees_dict[sub_query].prt()