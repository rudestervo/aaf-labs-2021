import KD_Tree
from re import match


def incorrect_name(set_name: str):
    if match(r"^[a-zA-Z][a-zA-Z0-9_]*$", set_name): return False
    return True


def incorrect_coordinates(coordinates: str):
    coordinates = " ".join(coordinates.split())
    if match(r"^[ ]*[(][ ]*[0-9]+[ ]*[,][ ]*[0-9]+[ ]*[)][ ]*$", coordinates): return False
    return True


def get_coordinates(coordinates: str):
    coordinates = "".join(coordinates.split())
    coordinates = "".join(coordinates.split("("))
    coordinates = "".join(coordinates.split(")"))
    coordinates = coordinates.split(",")
    if len(coordinates) == 2:
        return KD_Tree.Point(coordinates[0], coordinates[1])
    elif len(coordinates) == 4:
        return KD_Tree.Point(coordinates[0], coordinates[1]), KD_Tree.Point(coordinates[2], coordinates[3])
    else:
        return False


def create(set_name: str):
    if len(set_name.split()) > 1:
        print("expected one word in the set name (" + str(len(set_name.split())) + " words given)")
    else:
        if incorrect_name(set_name):
            print("incorrect set name")
        elif set_name in KD_Tree.KDTrees:
            print("tree with the same name already exists")
        else:
            KD_Tree.KDTrees[set_name] = KD_Tree.KDTree()
            print("set " + set_name + " has been created")


def insert(point: str):
    set_name = point.split()[0]
    coordinates = point[len(point.split()[0]) + 1:]
    if incorrect_name(set_name):
        print("incorrect set name")
    elif set_name not in KD_Tree.KDTrees:
        print("set name " + set_name + " does not exist")
    elif incorrect_coordinates(coordinates):
        print("incorrect point coordinates")
    else:
        if KD_Tree.KDTrees[set_name].contains(get_coordinates(coordinates)):
            print("point with the same coordinates already exist")
        else:
            KD_Tree.KDTrees[set_name].insert(get_coordinates(coordinates))
            print("point " + "".join(coordinates.split()) + " has been added to " + set_name)
    get_coordinates(coordinates)


def print_tree(tree_name: str):
    if incorrect_name(tree_name):
        print("incorrect tree name")
    elif tree_name not in KD_Tree.KDTrees:
        print("tree name " + tree_name.split()[0] + " does not exist")
    else:
        print("print_tree was called")
        KD_Tree.KDTrees[tree_name].print_tree()


def contains(point: str):
    set_name = point.split()[0]
    coordinates = point[len(point.split()[0]) + 1:]
    if incorrect_name(set_name):
        print("incorrect set name")
    elif set_name not in KD_Tree.KDTrees:
        print("set name " + set_name + " does not exist")
    elif incorrect_coordinates(coordinates):
        print("incorrect point coordinates")
    elif set_name in KD_Tree.KDTrees:
        print(KD_Tree.KDTrees[set_name].contains(get_coordinates(coordinates)))
        KD_Tree.KDTrees[set_name].contains(get_coordinates(coordinates))
    else:
        print(False)
        return False


def search(set_name: str):
    name = set_name.split()[0]
    if incorrect_name(name):
        print("incorrect set name")
    elif name not in KD_Tree.KDTrees:
        print("set name " + name + " does not exist")
    else:
        if (len(set_name.split()) == 2): print("incorrect command syntax")
        if (len(set_name.split()) > 2):
            if set_name.split()[1].lower() == "where":
                condition_params = set_name[
                                   len(set_name.split()[0]) + len(set_name.split()[1]) + len(set_name.split()[2]) + 3:]
                if set_name.split()[2].lower() == "inside":
                    where_inside(condition_params, name)
                elif set_name.split()[2].lower() == "above_to":
                    where_above_to(condition_params, name)
                elif set_name.split()[2].lower() == "nn":
                    where_nearest_neighbour(condition_params, name)
                else:
                    print("incorrect condition syntax")
            else:
                print("incorrect command syntax")
        else:
            KD_Tree.KDTrees[name].search()


def where_inside(coordinates: str, set_name: str):
    coordinates = " ".join(coordinates.split())
    if not match(r"^[ ]*[(][ ]*[0-9]+[ ]*[,][ ]*[0-9]+[ ]*[)][ ]*[,][ ]*[(][ ]*[0-9]+[ ]*[,][ ]*[0-9]+[ ]*[)][ ]*$",
                 coordinates):
        print("incorrect point coordinates")
    else:
        KD_Tree.KDTrees[set_name].search_where_inside(get_coordinates(coordinates))


def where_above_to(coordinate: str, set_name: str):
    if not coordinate.isdigit():
        print("incorrect coordinate")
    else:
        print(coordinate)
        KD_Tree.KDTrees[set_name].search_where_above_to(coordinate)


def where_nearest_neighbour(point: str, set_name: str):
    if incorrect_coordinates(point):
        print("incorrect point coordinates")
    else:
        KD_Tree.KDTrees[set_name].nn(get_coordinates(point))


def exit():
    print("exit was called")
